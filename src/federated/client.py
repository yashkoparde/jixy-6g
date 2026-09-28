import numpy as np
from src.models.cnn_model import build_cnn

def train_client(global_weights,X,y,input_dim,config,local_epochs=1):
    model=build_cnn(input_dim,config['training']['learning_rate']); model.set_weights(global_weights)
    h=model.fit(X,y,epochs=local_epochs,batch_size=config['training']['batch_size'],verbose=0,shuffle=True)
    return model.get_weights(),len(y),{'loss':float(h.history['loss'][-1]),'accuracy':float(h.history['accuracy'][-1])}
