import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif

class FeatureSelector:
    """Train-fitted feature selector; supports selectkbest, correlation, and user list."""
    def __init__(self, method='selectkbest', k=40, user_features=None):
        self.method=method.lower(); self.k=k; self.user_features=user_features or []
        self.columns_=None; self.selector_=None; self.selected_features_=[]
    def fit(self, X, y):
        self.columns_=list(X.columns)
        if self.method == 'user':
            missing=set(self.user_features)-set(self.columns_)
            if missing: raise ValueError(f'User selected features not found: {sorted(missing)}')
            self.selected_features_=list(self.user_features)
        elif self.method == 'correlation':
            scores=X.corrwith(pd.Series(y,index=X.index)).abs().replace([np.inf,-np.inf],np.nan).fillna(0)
            self.selected_features_=scores.sort_values(ascending=False).head(min(self.k,len(X.columns))).index.tolist()
        elif self.method == 'selectkbest':
            self.selector_=SelectKBest(f_classif,k=min(self.k,len(self.columns_))).fit(X,y)
            self.selected_features_=[c for c,s in zip(self.columns_,self.selector_.get_support()) if s]
        else: raise ValueError('selection method must be selectkbest, correlation, or user')
        return self
    def transform(self, X):
        absent=set(self.selected_features_)-set(X.columns)
        if absent: raise ValueError(f'Missing selected features: {sorted(absent)}')
        return X.loc[:,self.selected_features_]
