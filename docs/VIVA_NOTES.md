# Viva notes

## Core concepts

- **IDS:** an intrusion detection system observes events or network flows and classifies suspicious activity for defensive response.
- **6G:** the anticipated next generation of mobile networks. This project targets future 6G security needs conceptually; its benchmark is not 6G traffic.
- **AI for IDS:** models can learn traffic patterns from labeled flows and classify flows as BENIGN or ATTACK.
- **CNN:** a neural network using convolution filters. Here Conv1D operates on an ordered feature vector; tabular feature order does not guarantee spatial meaning.
- **Federated Learning:** clients train locally and share model parameters rather than raw records. This prototype simulates clients within one process.
- **FedAvg:** each client's weights are averaged in proportion to its number of local training examples.
- **Differential Privacy:** a mathematical privacy framework limiting the influence of an individual unit. Formal guarantees require specifying adjacency, mechanism, composition, and accounting.
- **Clipping:** scales an update whose L2 norm exceeds a configured bound.
- **Gaussian noise:** random normal perturbation added to clipped updates; more noise generally increases privacy protection and can reduce utility.
- **CSE-CIC-IDS2018:** a Canadian Institute for Cybersecurity network intrusion benchmark containing benign and attack traffic flow records.
- **Edge nodes:** simulated independent data holders that perform local model training.

## One training round

1. Coordinator distributes current CNN parameters.
2. Each simulated client trains on its own index partition.
3. For DP mode, client parameter deltas are L2-clipped and Gaussian noise is added.
4. Coordinator aggregates updated parameters with sample-count-weighted FedAvg.
5. The resulting global model is evaluated and distributed in the next round.

Raw client rows are not passed to the coordinator function. However, this implementation does not provide secure transport, secure aggregation, or a certified DP accountant. It is a local academic simulation.

## Advantages, limitations, future scope

Potential advantages include comparing centralized and distributed optimization, practicing privacy-aware system design, and retaining local partitions. Limitations include benchmark-to-deployment gap, binary labels, single-process simulation, computational cost, possible class/partition skew, and unaccounted update noise privacy. Future scope includes formal DP-SGD/accounting, secure aggregation, real distributed clients, multiclass detection, and measured edge deployment.
