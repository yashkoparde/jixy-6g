import json
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from pathlib import Path
from sklearn.tree import export_text
from sklearn.ensemble import RandomForestClassifier
from src.common import ROOT, load_config
from src.data.preprocessing import TrafficPreprocessor

def train_explainable_models():
    print("Training Explainable GBDT & Decision Tree Models...")
    cfg = load_config()
    
    # Load dataset
    data_path = ROOT / 'data' / 'processed' / 'dataset.npz'
    if not data_path.exists():
        p = TrafficPreprocessor(cfg)
        p.fit_transform_split()
    
    data = np.load(data_path, allow_pickle=True)
    Xtr, ytr = data['X_train'], data['y_train']
    Xte, yte = data['X_test'], data['y_test']
    
    # Load selected feature names
    feat_json = ROOT / 'models' / 'selected_features.json'
    if feat_json.exists():
        feature_names = json.loads(feat_json.read_text())
    else:
        feature_names = [f"Feature_{i}" for i in range(Xtr.shape[1])]

    # 1. Train XGBoost Gradient Boosted Trees Model
    xgb_clf = xgb.XGBClassifier(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        random_state=42
    )
    xgb_clf.fit(Xtr, ytr)
    acc_xgb = xgb_clf.score(Xte, yte)
    print(f"XGBoost Test Accuracy: {acc_xgb*100:.2f}%")
    
    # 2. Train Random Forest (for Decision Tree logic visualization)
    rf_clf = RandomForestClassifier(
        n_estimators=30,
        max_depth=3,
        random_state=42
    )
    rf_clf.fit(Xtr, ytr)
    acc_rf = rf_clf.score(Xte, yte)
    print(f"Random Forest Test Accuracy: {acc_rf*100:.2f}%")
    
    # Extract decision tree logic text rules
    tree_rules = export_text(rf_clf.estimators_[0], feature_names=feature_names[:Xtr.shape[1]])
    
    # Save models and feature importances
    models_dir = ROOT / 'models'
    joblib.dump(xgb_clf, models_dir / 'xgboost_model.joblib')
    joblib.dump(rf_clf, models_dir / 'rf_explainable_model.joblib')
    
    importances = xgb_clf.feature_importances_
    feat_imp = sorted(zip(feature_names[:Xtr.shape[1]], importances.tolist()), key=lambda x: x[1], reverse=True)
    
    (models_dir / 'explainable_logic.json').write_text(json.dumps({
        'feature_importances': feat_imp,
        'tree_reasoning_rules': tree_rules
    }, indent=2), encoding='utf-8')
    
    print("Saved Explainable AI models & decision reasoning rules to models/explainable_logic.json")

if __name__ == '__main__':
    train_explainable_models()
