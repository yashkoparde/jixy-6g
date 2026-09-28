import numpy as np

def partition_data(X,y,num_clients=3,method='non_iid',seed=42):
    """Return index arrays. non_iid uses label-sorted shards; this is a simulation only."""
    if num_clients<2: raise ValueError('At least two clients are required.')
    rng=np.random.default_rng(seed); y=np.asarray(y); n=len(y)
    if n<num_clients: raise ValueError('Fewer rows than clients.')
    if method.lower()=='iid':
        ids=rng.permutation(n); return [a for a in np.array_split(ids,num_clients)]
    if method.lower()!='non_iid': raise ValueError('partition method must be iid or non_iid')
    # Sort by binary label and split into 2*num_clients chunks; adjacent chunks create label skew.
    ids=np.argsort(y,kind='stable'); shards=[s for s in np.array_split(ids,2*num_clients) if len(s)]
    rng.shuffle(shards); clients=[[] for _ in range(num_clients)]
    for i,shard in enumerate(shards): clients[i%num_clients].extend(shard.tolist())
    return [np.asarray(c,dtype=int) for c in clients]
