import argparse
from src.training.federated_training import train_federated
from src.evaluation.compare import write_comparison
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--clients',type=int); p.add_argument('--rounds',type=int); g=p.add_mutually_exclusive_group(); g.add_argument('--dp',action='store_true'); g.add_argument('--no-dp',action='store_true'); a=p.parse_args()
    print(train_federated(dp=a.dp,clients=a.clients,rounds=a.rounds)); write_comparison()
