from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay,roc_curve,precision_recall_curve

def save_evaluation_plots(y_true,probabilities,metrics,out_dir,history=None,prefix='model'):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); pred=(np.asarray(probabilities).reshape(-1)>=.5).astype(int)
    fig,ax=plt.subplots(); ConfusionMatrixDisplay(np.asarray(metrics['confusion_matrix']),display_labels=['BENIGN','ATTACK']).plot(ax=ax,colorbar=False); fig.tight_layout(); fig.savefig(out/f'{prefix}_confusion_matrix.png',dpi=140); plt.close(fig)
    if len(np.unique(y_true))==2:
        fpr,tpr,_=roc_curve(y_true,probabilities); fig,ax=plt.subplots(); ax.plot(fpr,tpr,label=f"AUC={metrics.get('roc_auc'):.3f}"); ax.plot([0,1],[0,1],'--'); ax.set(xlabel='False positive rate',ylabel='True positive rate',title='ROC curve'); ax.legend(); fig.tight_layout(); fig.savefig(out/f'{prefix}_roc_curve.png',dpi=140); plt.close(fig)
        pr,rc,_=precision_recall_curve(y_true,probabilities); fig,ax=plt.subplots(); ax.plot(rc,pr); ax.set(xlabel='Recall',ylabel='Precision',title='Precision-recall curve'); fig.tight_layout(); fig.savefig(out/f'{prefix}_precision_recall.png',dpi=140); plt.close(fig)
    if history:
        for metric in ('loss','accuracy'):
            vals=history.get(metric,[])
            if vals:
                fig,ax=plt.subplots(); ax.plot(vals,label='train'); val=history.get('val_'+metric,[])
                if val: ax.plot(val,label='validation')
                ax.set(xlabel='Epoch',ylabel=metric,title=f'Training {metric}'); ax.legend(); fig.tight_layout(); fig.savefig(out/f'{prefix}_training_{metric}.png',dpi=140); plt.close(fig)

def save_round_plot(rounds,path,key='accuracy',title=None):
    if not rounds:return
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); fig,ax=plt.subplots(); ax.plot([r['round'] for r in rounds],[r.get(key,0) for r in rounds],marker='o'); ax.set(xlabel='Federated round',ylabel=key,title=title or f'Federated round {key}'); fig.tight_layout(); fig.savefig(p,dpi=140); plt.close(fig)
