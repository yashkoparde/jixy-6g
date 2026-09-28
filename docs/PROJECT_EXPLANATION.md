# Module explanation

## Data layer

`src/data/preprocessing.py` discovers CSVs, normalizes headers, detects the configured label, removes duplicate and invalid-label rows, maps BENIGN to 0 and all other attack labels to 1, then performs a stratified train/test split. Numeric coercion and train-fitted categorical mappings, median imputation, standardization, and feature selection are applied without fitting on test rows. The preprocessor is persisted with Joblib for inference. Direct identifiers and timestamps are excluded.

`src/data/feature_selection.py` provides train-fitted SelectKBest, correlation ranking, and an explicit user feature allow-list. It records selected feature names.

## Model and training

`src/models/cnn_model.py` creates a configurable 1D CNN with convolution, batch normalization, pooling, global average pooling, dense/dropout, and sigmoid output. `src/training/centralized_training.py` fits one model and saves metrics and plots. `src/federated/partition.py` creates IID random or label-skewed simulated partitions. `client.py` trains a fresh local copy from global parameters. `fedavg.py` validates layer shapes and computes weighted averages. `server.py` is a thin parameter-only aggregation helper. `federated_training.py` runs repeated rounds, distributes global parameters, and evaluates after aggregation.

## Privacy and evaluation

`src/privacy/differential_privacy.py` clips a complete client delta by global L2 norm and adds Gaussian noise with standard deviation `clip_norm * noise_multiplier`. This is illustrative client-update perturbation. Without a defined privacy unit, neighboring relation, sampling model, and composition accountant, the configured delta/noise must not be presented as a certified epsilon guarantee.

`src/evaluation/metrics.py` computes accuracy, precision, recall, F1, confusion matrix, report, and ROC-AUC when both classes are present. Plot helpers save confusion, ROC, precision-recall, training, and federated-round graphs. `compare.py` gathers artifacts only; it never inserts hypothetical results.

## Prediction and dashboard

`src/prediction/predict.py` loads the saved preprocessing object and a selected Keras model, transforms user-supplied flow rows consistently, and appends attack probability and binary prediction. `app.py` displays available experiments and plots and lets a user upload a flow CSV. It shows the local-simulation and privacy limitations explicitly.

## Artifacts and logging

Models are stored in `models/`, centralized metrics in `metrics/`, federated outputs in `results/`, processed arrays in `data/processed/`, and logs in `logs/`. Configuration is embedded in experiment JSON for reproducibility.
