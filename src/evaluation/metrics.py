import json
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report,roc_auc_score
from src.common import ROOT

def calculate_metrics(y_true, probabilities, threshold=.5):
    probs=np.asarray(probabilities).reshape(-1); pred=(probs>=threshold).astype(int); truth=np.asarray(y_true).astype(int)
    result={'accuracy':float(accuracy_score(truth,pred)),'precision':float(precision_score(truth,pred,zero_division=0)),
      'recall':float(recall_score(truth,pred,zero_division=0)),'f1':float(f1_score(truth,pred,zero_division=0)),
      'confusion_matrix':confusion_matrix(truth,pred,labels=[0,1]).tolist(),
      'classification_report':classification_report(truth,pred,labels=[0,1],target_names=['BENIGN','ATTACK'],output_dict=True,zero_division=0)}
    result['roc_auc']=float(roc_auc_score(truth,probs)) if len(np.unique(truth))==2 else None
    return result

def save_json(data,path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,default=lambda x: float(x)),encoding='utf-8')
