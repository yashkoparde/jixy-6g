import numpy as np

def fedavg(client_weights,sample_counts):
    if not client_weights or len(client_weights)!=len(sample_counts): raise ValueError('weights and sample_counts must be non-empty and aligned')
    counts=np.asarray(sample_counts,dtype=float)
    if np.any(counts<=0): raise ValueError('sample counts must be positive')
    total=counts.sum(); reference=client_weights[0]
    if any(len(w)!=len(reference) for w in client_weights): raise ValueError('model weight lists differ in length')
    result=[]
    for layer_i,base in enumerate(reference):
        shape=np.asarray(base).shape
        if any(np.asarray(w[layer_i]).shape!=shape for w in client_weights): raise ValueError('model weight shapes differ')
        result.append(sum(np.asarray(w[layer_i],dtype=np.float64)*(counts[i]/total) for i,w in enumerate(client_weights)).astype(np.asarray(base).dtype))
    return result
