import json, time
from datetime import datetime,timezone
import numpy as np
from src.common import ROOT,load_config,seed_everything,get_logger
from src.data.preprocessing import prepare_dataset
from src.models.cnn_model import build_cnn
from src.evaluation.metrics import calculate_metrics,save_json
from src.evaluation.plots import save_evaluation_plots

def train_centralized():
    cfg=load_config(); seed_everything(cfg['seed']); log=get_logger('centralized','training.log')
    X,y,Xt,yt=prepare_dataset(); tc=cfg['training']; model=build_cnn(X.shape[1],tc['learning_rate'])
    cb=[__import__('tensorflow').keras.callbacks.EarlyStopping(monitor='val_loss',patience=tc['patience'],restore_best_weights=True)]
    start=time.time(); h=model.fit(X,y,epochs=tc['epochs'],batch_size=tc['batch_size'],validation_split=tc['validation_split'],callbacks=cb,verbose=2); elapsed=time.time()-start
    prob=model.predict(Xt,batch_size=tc['batch_size'],verbose=0).ravel(); result=calculate_metrics(yt,prob); result.update(training_time_seconds=elapsed,timestamp=datetime.now(timezone.utc).isoformat(),experiment='centralized',config=cfg,selected_features=int(X.shape[1]))
    model.save(ROOT/'models'/'centralized_model.keras'); save_json(result,ROOT/'metrics'/'centralized_metrics.json')
    save_evaluation_plots(yt,prob,result,ROOT/'plots',h.history,'centralized'); log.info('Complete metrics=%s', {k:result[k] for k in ('accuracy','f1','training_time_seconds')}); return result
