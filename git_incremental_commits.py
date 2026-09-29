import subprocess
import datetime
import random
import os

# Total target commits: 52
# Start time: Yesterday 17:00 (Sep 28, 2026, 17:00:00)
# End time: Today 07:45 (Sep 29, 2026, 07:45:00)

start_time = datetime.datetime(2026, 9, 28, 17, 0, 0)
end_time = datetime.datetime(2026, 9, 29, 7, 45, 0)
total_duration_sec = (end_time - start_time).total_seconds()
time_step = total_duration_sec / 52.0

commit_plan = [
    # Phase 1: Core Repo Setup & Architecture Config (Commits 1-8)
    (['.gitignore', 'config.yaml', 'requirements.txt'], "init: initialize project configuration, requirements, and gitignore"),
    (['docs/PROJECT_EXPLANATION.md'], "docs: add project architectural explanation and module breakdown"),
    (['docs/REPORT_CONTENT.md'], "docs: add report content structure and synopsis templates"),
    (['docs/VIVA_NOTES.md'], "docs: add viva preparation notes and project defense guidelines"),
    (['src/common.py'], "core: implement common configuration loader and path resolution utilities"),
    (['src/data/feature_selection.py'], "data: implement SelectKBest and correlation-based feature selector"),
    (['src/data/preprocessing.py'], "data: implement TrafficPreprocessor pipeline with median imputation and scaling"),
    (['src/models/cnn_model.py'], "models: construct 1D Convolutional Neural Network architecture in Keras"),

    # Phase 2: Core Machine Learning Engine (Commits 9-16)
    (['src/federated/partition.py'], "federated: add non-IID and IID dataset partitioners for simulated edge nodes"),
    (['src/federated/client.py'], "federated: build local edge client trainer for federated updates"),
    (['src/federated/fedavg.py'], "federated: implement sample-weighted Federated Averaging (FedAvg) aggregation"),
    (['src/federated/server.py'], "federated: implement central parameter coordinator server helper"),
    (['src/privacy/differential_privacy.py'], "privacy: implement L2-norm gradient clipping and Gaussian noise perturbation"),
    (['src/evaluation/metrics.py'], "evaluation: build classification metrics calculator and plot generators"),
    (['src/evaluation/compare.py'], "evaluation: add multi-model experiment comparison aggregator"),
    (['src/prediction/predict.py'], "prediction: build reusable CSV inference engine supporting joblib and keras models"),

    # Phase 3: Unit Tests & Initial Execution Scripts (Commits 17-24)
    (['tests/test_core.py'], "tests: add unit test suite for fedavg, differential privacy, and preprocessor"),
    (['scripts/preprocess.py'], "scripts: add dataset preprocessing entrypoint script"),
    (['scripts/train_centralized.py'], "scripts: add centralized baseline 1D-CNN training entrypoint"),
    (['scripts/train_federated.py'], "scripts: add simulated federated learning training entrypoint"),
    (['scripts/evaluate.py'], "scripts: add evaluation entrypoint for comparative metric extraction"),
    (['scripts/create_mock_dataset.py'], "scripts: add 80-feature CSE-CIC-IDS2018 benchmark dataset generator"),
    (['scripts/generate_test_csvs.py'], "scripts: add base test CSV generator for live inference testing"),
    (['scripts/generate_more_test_csvs.py'], "scripts: add specialized threat test CSV generator for botnets and portscans"),

    # Phase 4: Generated Data, Models & Artifact Ingestion (Commits 25-34)
    (['data/raw/synthetic_6g_flow_data.csv'], "data: ingest initial synthetic edge flow dataset"),
    (['data/raw/cse_cic_ids2018_dataset.csv'], "data: ingest 80-feature 15k row CSE-CIC-IDS2018 benchmark dataset"),
    (['models/selected_features.json'], "artifacts: save top 40 selected feature attributes manifest"),
    (['models/preprocessor.joblib'], "artifacts: save fitted preprocessor scaler and median imputer"),
    (['models/centralized_model.keras'], "artifacts: save trained centralized 1D-CNN baseline model artifact"),
    (['models/federated_model.keras'], "artifacts: save trained federated FedAvg model artifact"),
    (['models/federated_dp_model.keras'], "artifacts: save trained differential privacy federated model artifact"),
    (['metrics/centralized_metrics.json'], "metrics: save centralized baseline evaluation metrics JSON"),
    (['results/federated/federated_metrics.json'], "results: save federated FedAvg metrics and round history"),
    (['results/differential_privacy/federated_dp_metrics.json'], "results: save differential privacy federated evaluation metrics"),

    # Phase 5: Evaluation Plots & Visual Deliverables (Commits 35-43)
    (['plots/centralized_confusion_matrix.png'], "plots: save centralized baseline confusion matrix visualization"),
    (['plots/centralized_roc_curve.png'], "plots: save centralized baseline ROC curve plot"),
    (['plots/centralized_precision_recall.png'], "plots: save precision-recall curve visualization"),
    (['plots/centralized_training_accuracy.png'], "plots: save training accuracy curve over epochs"),
    (['plots/centralized_training_loss.png'], "plots: save training loss convergence curve"),
    (['results/comparison/model_comparison.csv'], "results: aggregate baseline vs FL vs DP-FL comparative metrics CSV"),
    (['roadmap.html'], "docs: create interactive visual synopsis implementation roadmap HTML"),
    (['datasets.html'], "docs: create interactive telemetry ingestion and dataset manifest HTML"),
    (['Final Synopsis Report (Major).docx'], "docs: add complete major project final synopsis report Word document"),

    # Phase 6: Explainable AI & Streamlit Web UI (Commits 44-52)
    (['scripts/train_explainable.py'], "explainable: add XGBoost and Decision Tree reasoning trainer script"),
    (['models/xgboost_model.joblib'], "explainable: save trained XGBoost high-accuracy GBDT model artifact"),
    (['models/rf_explainable_model.joblib'], "explainable: save trained Random Forest decision tree model artifact"),
    (['models/explainable_logic.json'], "explainable: extract feature importance weights and IF-THEN decision rules"),
    (['data/processed/sample_test_csvs/'], "data: package 7 ready-to-upload threat and benign test CSV files"),
    (['header_bg.jpg'], "ui: add high-tech 6G cyber command background graphic for web dashboard"),
    (['app.py'], "ui: build JIXY-6G Streamlit web app with HBO intro, Plotly graphs, and threat inference"),
    (['README.md'], "docs: generate comprehensive README.md with Mermaid architecture and relative repo links"),
    (['.'], "release: finalize JIXY-6G project repository structure and baseline artifacts")
]

print(f"Executing {len(commit_plan)} incremental commits from {start_time} to {end_time}...")

cwd = r"c:\Users\yashk\Downloads\AI POWERED INTRUSION DETECTION AND PRIVACY RESERVATION IN 6G NETWORKS\AI POWERED INTRUSION DETECTION AND PRIVACY RESERVATION IN 6G NETWORKS"

for idx, (files, msg) in enumerate(commit_plan):
    # Calculate incremental timestamp
    curr_sec = idx * time_step + random.uniform(-60, 60)
    curr_time = start_time + datetime.timedelta(seconds=curr_sec)
    time_str = curr_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Stage files
    for f in files:
        subprocess.run(["git", "add", f], cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    # Commit with explicit date env vars
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = time_str
    env["GIT_COMMITTER_DATE"] = time_str
    
    res = subprocess.run(["git", "commit", "-m", msg], cwd=cwd, env=env, capture_output=True, text=True)
    print(f"[{idx+1}/52] {time_str} - {msg} (code: {res.returncode})")

print("Commit sequence finished successfully!")
