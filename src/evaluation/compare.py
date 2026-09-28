import csv
from pathlib import Path
from src.common import ROOT

def write_comparison():
    candidates=[ROOT/'metrics'/'centralized_metrics.json',ROOT/'results'/'federated'/'federated_metrics.json',ROOT/'results'/'differential_privacy'/'federated_dp_metrics.json']
    import json
    rows=[]
    for p in candidates:
        if p.exists():
            d=json.loads(p.read_text(encoding='utf-8')); rows.append({k:d.get(k) for k in ('experiment','accuracy','precision','recall','f1','roc_auc','training_time_seconds','dp_enabled','num_clients','rounds')})
    out=ROOT/'results'/'comparison'; out.mkdir(parents=True,exist_ok=True)
    if rows:
        with open(out/'model_comparison.csv','w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return rows
