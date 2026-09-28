"""Coordinator helper: aggregates parameters only; raw client rows stay local."""
from src.federated.fedavg import fedavg

def aggregate(client_results):
    weights=[r['weights'] for r in client_results]; counts=[r['num_samples'] for r in client_results]
    return fedavg(weights,counts)
