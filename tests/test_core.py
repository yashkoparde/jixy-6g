import numpy as np
import pandas as pd
import pytest
from src.federated.fedavg import fedavg
from src.privacy.differential_privacy import privatize_update
from src.data.feature_selection import FeatureSelector
from src.data.preprocessing import TrafficPreprocessor
from src.models.cnn_model import build_cnn

def test_fedavg_equal_weights():
    got=fedavg([[np.array([1.])],[np.array([3.])]], [2,2]); assert np.allclose(got[0],[2.])
def test_fedavg_sample_weighted():
    got=fedavg([[np.array([1.])],[np.array([3.])]], [1,3]); assert np.allclose(got[0],[2.5])
def test_dp_clips_and_preserves_shapes():
    out,info=privatize_update([np.array([3.,4.])],clip_norm=1,noise_multiplier=0)
    assert out[0].shape==(2,) and info['clip_scale']==pytest.approx(.2) and np.linalg.norm(out[0])==pytest.approx(1)
def test_feature_selector_user_list():
    X=pd.DataFrame({'a':[0,1,2],'b':[2,1,0]}); selector=FeatureSelector('user',user_features=['b']).fit(X,[0,0,1]); assert selector.transform(X).columns.tolist()==['b']
def test_cnn_output_shape():
    model=build_cnn(5); assert model.output_shape==(None,1)
def test_clean_labels_and_invalid_rows():
    p=TrafficPreprocessor({'dataset':{'label_column':'Label'},'features':{'selection_method':'selectkbest','num_features':2}})
    X,y,labels=p._clean(pd.DataFrame({' A ':['1','2','3'],'Label':['BENIGN','DDoS',None]})); assert y.tolist()==[0,1] and labels.tolist()==['BENIGN','DDoS']
