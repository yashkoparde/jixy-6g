"""Client update clipping and Gaussian perturbation.

This is a client-level update perturbation simulation. It is not DP-SGD and does
not provide a certified epsilon without a complete subsampling/accounting model.
"""
import numpy as np

def privatize_update(update,clip_norm=1.0,noise_multiplier=1.0,rng=None):
    if clip_norm<=0 or noise_multiplier<0: raise ValueError('clip_norm must be positive and noise_multiplier nonnegative')
    rng=rng or np.random.default_rng(); arrays=[np.asarray(a,dtype=np.float32) for a in update]
    norm=float(np.sqrt(sum(np.sum(a.astype(np.float64)**2) for a in arrays)))
    scale=min(1.0,clip_norm/(norm+1e-12))
    clipped=[a*scale for a in arrays]
    noisy=[a+rng.normal(0,clip_norm*noise_multiplier,size=a.shape).astype(np.float32) for a in clipped]
    return noisy,{'update_l2_norm':norm,'clip_scale':float(scale),'noise_std':float(clip_norm*noise_multiplier)}
