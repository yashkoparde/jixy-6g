from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from src.common import ROOT
from src.data.preprocessing import TrafficPreprocessor

def predict_csv(csv_path, model_path=None):
    if model_path is None:
        target_path = ROOT / 'models' / 'xgboost_model.joblib'
    else:
        target_path = Path(model_path)
        
    path_str = str(target_path).lower()
    prep = TrafficPreprocessor.load()
    df = pd.read_csv(csv_path, low_memory=False)
    X = prep.transform_frame(df)
    
    # Strictly isolate joblib vs Keras 3 model loading
    if target_path.suffix == '.joblib' or 'joblib' in path_str or 'xgboost' in path_str or 'rf_' in path_str:
        clf = joblib.load(target_path)
        probabilities = clf.predict_proba(X)[:, 1]
    else:
        import tensorflow as tf
        model = tf.keras.models.load_model(target_path)
        probabilities = model.predict(X, verbose=0).ravel()
        
    result = df.copy()
    result['attack_probability'] = np.round(probabilities, 4)
    result['prediction'] = np.where(probabilities >= 0.5, 'ATTACK', 'BENIGN')
    return result
