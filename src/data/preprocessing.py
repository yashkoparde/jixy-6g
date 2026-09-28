"""Leakage-safe CSE-CIC-IDS2018 CSV preprocessing and reusable prediction pipeline."""
from pathlib import Path
import json, re
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from src.common import ROOT, load_config, resolve, get_logger, seed_everything
from src.data.feature_selection import FeatureSelector

DROP_NAMES={'flow id','source ip','destination ip','src ip','dst ip','timestamp'}
def normalize_name(s): return re.sub(r'\s+',' ',str(s).replace('\ufeff','').strip()).lower()

class TrafficPreprocessor:
    def __init__(self, config=None):
        self.config=config or load_config(); self.label_column=normalize_name(self.config['dataset'].get('label_column','Label'))
        self.imputer=SimpleImputer(strategy='median'); self.scaler=StandardScaler(); self.category_maps={}; self.feature_columns=[]
        fs=self.config['features']; self.selector=FeatureSelector(fs['selection_method'],fs['num_features'],fs.get('user_features'))
    def _read_csvs(self, paths):
        frames=[]
        for p in paths:
            try:
                df=pd.read_csv(p,low_memory=False,encoding_errors='replace'); df.columns=[normalize_name(c) for c in df.columns]
            except Exception as e: raise ValueError(f'Could not read {p}: {e}') from e
            frames.append(df)
        if not frames: raise FileNotFoundError('Dataset not found. Please place the CSE-CIC-IDS2018 CSV files inside data/raw/.')
        data=pd.concat(frames,ignore_index=True,sort=False); data=data.loc[:,~data.columns.duplicated()]
        if self.label_column not in data: raise ValueError(f"Missing required label column '{self.label_column}'. Available columns: {list(data.columns)}")
        return data
    def _clean(self, df):
        df=df.copy(); df.columns=[normalize_name(c) for c in df.columns]
        df=df.drop_duplicates(); df.replace([np.inf,-np.inf],np.nan,inplace=True)
        labels=df[self.label_column].astype('string').str.strip()
        valid=labels.notna() & (labels!='')
        df=df.loc[valid].copy(); labels=labels.loc[valid]
        df['original_label']=labels
        df['target']=(labels.str.upper()!='BENIGN').astype('int8')
        drop=[c for c in df.columns if c in DROP_NAMES or c in {self.label_column,'original_label','target'}]
        X=df.drop(columns=drop,errors='ignore')
        return X,df['target'].to_numpy(),df['original_label'].to_numpy()
    def fit_transform_split(self, paths=None):
        raw=resolve(self.config['dataset']['path']); paths=list(paths or raw.glob('*.csv'))
        df=self._read_csvs(paths); X,y,labels=self._clean(df)
        if len(np.unique(y))<2: raise ValueError('Dataset must contain both BENIGN and attack rows.')
        max_rows=self.config['training'].get('max_samples')
        if max_rows and len(y)>max_rows:
            # Stratified cap is deterministic and happens before fitting preprocessing.
            _,keep=train_test_split(np.arange(len(y)),train_size=max_rows,random_state=self.config['seed'],stratify=y)
            X=X.iloc[keep].reset_index(drop=True); y=y[keep]; labels=labels[keep]
        test_size=self.config['dataset'].get('test_size',.2)
        idx_train,idx_test=train_test_split(np.arange(len(y)),test_size=test_size,random_state=self.config['seed'],stratify=y)
        Xtr=X.iloc[idx_train].copy(); Xte=X.iloc[idx_test].copy(); ytr=y[idx_train]; yte=y[idx_test]
        # Numeric columns are coerced; categorical columns are train-fitted integer mappings.
        self.category_maps={}; train_parts={}; test_parts={}
        for c in X.columns:
            numeric=pd.to_numeric(Xtr[c],errors='coerce')
            if numeric.notna().mean()>=.95:
                train_parts[c]=numeric; test_parts[c]=pd.to_numeric(Xte[c],errors='coerce')
            else:
                vals=Xtr[c].astype('string').fillna('__MISSING__'); cats=sorted(vals.unique().tolist())
                mapping={v:i for i,v in enumerate(cats)}; self.category_maps[c]=mapping
                train_parts[c]=vals.map(mapping).astype(float)
                test_parts[c]=Xte[c].astype('string').fillna('__MISSING__').map(mapping).fillna(-1).astype(float)
        A=pd.DataFrame(train_parts).replace([np.inf,-np.inf],np.nan); B=pd.DataFrame(test_parts).replace([np.inf,-np.inf],np.nan)
        self.feature_columns=list(A.columns)
        A=pd.DataFrame(self.imputer.fit_transform(A),columns=self.feature_columns)
        B=pd.DataFrame(self.imputer.transform(B),columns=self.feature_columns)
        A=pd.DataFrame(self.scaler.fit_transform(A),columns=self.feature_columns)
        B=pd.DataFrame(self.scaler.transform(B),columns=self.feature_columns)
        self.selector.fit(A,ytr); A=self.selector.transform(A); B=self.selector.transform(B)
        self.save()
        return A.to_numpy(dtype='float32'),ytr.astype('float32'),B.to_numpy(dtype='float32'),yte.astype('float32'),labels[idx_test]
    def transform_frame(self, df):
        df=df.copy(); df.columns=[normalize_name(c) for c in df.columns]
        if self.label_column in df: df=df.drop(columns=[self.label_column])
        df=df.drop(columns=[c for c in df.columns if c in DROP_NAMES],errors='ignore')
        out={}
        for c in self.feature_columns:
            if c not in df: out[c]=np.nan; continue
            if c in self.category_maps:
                out[c]=df[c].astype('string').fillna('__MISSING__').map(self.category_maps[c]).fillna(-1)
            else: out[c]=pd.to_numeric(df[c],errors='coerce')
        X=pd.DataFrame(out).replace([np.inf,-np.inf],np.nan)
        X=pd.DataFrame(self.imputer.transform(X),columns=self.feature_columns)
        X=pd.DataFrame(self.scaler.transform(X),columns=self.feature_columns)
        return self.selector.transform(X).to_numpy(dtype='float32')
    def save(self):
        d=ROOT/'models'; d.mkdir(exist_ok=True)
        joblib.dump(self,d/'preprocessor.joblib')
        (d/'selected_features.json').write_text(json.dumps(self.selector.selected_features_,indent=2),encoding='utf-8')
    @staticmethod
    def load(path=None): return joblib.load(path or ROOT/'models'/'preprocessor.joblib')

def prepare_dataset():
    logger=get_logger('preprocess'); cfg=load_config(); seed_everything(cfg['seed']); p=TrafficPreprocessor(cfg)
    Xtr,ytr,Xte,yte,orig=p.fit_transform_split()
    d=resolve('data/processed'); d.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(d/'dataset.npz',X_train=Xtr,y_train=ytr,X_test=Xte,y_test=yte,test_original_labels=orig)
    logger.info('Saved train=%s test=%s selected_features=%d',Xtr.shape,Xte.shape,Xtr.shape[1])
    return Xtr,ytr,Xte,yte
