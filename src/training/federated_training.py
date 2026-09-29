import time
from datetime import datetime,timezone
import numpy as np
from src.common import ROOT,load_config,seed_everything,get_logger
from src.data.preprocessing import prepare_dataset
from src.models.cnn_model import build_cnn
from src.federated.partition import partition_data
from src.federated.client import train_client
from src.federated.fedavg import fedavg
from src.privacy.differential_privacy import privatize_update
from src.evaluation.metrics import calculate_metrics,save_json
from src.evaluation.plots import save_evaluation_plots,save_round_plot

def train_federated(dp=False,clients=None,rounds=None):
    cfg=load_config(); seed_everything(cfg['seed']); log=get_logger('federated','federated.log')
    X,y,Xt,yt=prepare_dataset(); fc=cfg['federated']; nclients=clients or fc['num_clients']; nr=rounds or fc['rounds']
    partitions=partition_data(X,y,nclients,fc['partition'],cfg['seed']); model=build_cnn(X.shape[1],cfg['training']['learning_rate']); global_weights=model.get_weights()
    privacy=cfg['privacy']; rng=np.random.default_rng(cfg['seed']); round_metrics=[]; start=time.time()
    for rnd in range(1,nr+1):
        updates=[]; counts=[]; losses=[]; accs=[]
        for cid,idx in enumerate(partitions):
            local_weights,count,metrics=train_client(global_weights,X[idx],y[idx],X.shape[1],cfg,fc['local_epochs'])
            delta=[lw-gw for lw,gw in zip(local_weights,global_weights)]
            if dp: delta,dp_stats=privatize_update(delta,privacy['clip_norm'],privacy['noise_multiplier'],rng)
            else: dp_stats={}
            updates.append([gw+d for gw,d in zip(global_weights,delta)]); counts.append(count); losses.append(metrics['loss']); accs.append(metrics['accuracy'])
            log.info('round=%d client=%d samples=%d loss=%.5f',rnd,cid+1,count,metrics['loss'])
        global_weights=fedavg(updates,counts); model.set_weights(global_weights)
        prob=model.predict(Xt,batch_size=cfg['training']['batch_size'],verbose=0).ravel(); metrics=calculate_metrics(yt,prob)
        row={'round':rnd,'client_mean_loss':float(np.mean(losses)),'client_mean_accuracy':float(np.mean(accs)),**{k:metrics[k] for k in ('accuracy','precision','recall','f1','roc_auc')}}
        round_metrics.append(row); log.info('round=%d fedavg accuracy=%.5f f1=%.5f',rnd,row['accuracy'],row['f1'])
    elapsed=time.time()-start; prob=model.predict(Xt,batch_size=cfg['training']['batch_size'],verbose=0).ravel(); result=calculate_metrics(yt,prob)
    experiment='federated_dp' if dp else 'federated'; result.update(experiment=experiment,training_time_seconds=elapsed,timestamp=datetime.now(timezone.utc).isoformat(),config=cfg,num_clients=nclients,rounds=nr,dp_enabled=dp,noise_multiplier=privacy['noise_multiplier'] if dp else 0,clip_norm=privacy['clip_norm'] if dp else None,selected_features=int(X.shape[1]),round_metrics=round_metrics,raw_data_transmitted=False)
    out=ROOT/'results'/('differential_privacy' if dp else 'federated'); out.mkdir(parents=True,exist_ok=True)
    model.save(ROOT/'models'/(experiment+'_model.keras')); save_json(result,out/(experiment+'_metrics.json'))
    save_evaluation_plots(yt,prob,result,out,None,experiment)
    save_round_plot(round_metrics,out/'federated_round_accuracy.png','accuracy'); save_round_plot(round_metrics,out/'federated_round_loss.png','client_mean_loss')
    log.info('finished experiment=%s elapsed=%.2f',experiment,elapsed); return result
