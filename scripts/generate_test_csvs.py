import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(101)
out_dir = Path('data/processed/sample_test_csvs')
out_dir.mkdir(parents=True, exist_ok=True)

# Shared feature list matching CSE-CIC-IDS2018 benchmark schema
features = [
    'Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts',
    'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Fwd Pkt Len Max', 'Fwd Pkt Len Min',
    'Fwd Pkt Len Mean', 'Fwd Pkt Len Std', 'Bwd Pkt Len Max', 'Bwd Pkt Len Min',
    'Bwd Pkt Len Mean', 'Bwd Pkt Len Std', 'Flow Byts/s', 'Flow Pkts/s',
    'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
    'Fwd IAT Tot', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
    'Bwd IAT Tot', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
    'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags',
    'Fwd Header Len', 'Bwd Header Len', 'Fwd Pkts/s', 'Bwd Pkts/s',
    'Pkt Len Min', 'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Std', 'Pkt Len Var',
    'FIN Flag Cnt', 'SYN Flag Cnt', 'RST Flag Cnt', 'PSH Flag Cnt', 'ACK Flag Cnt',
    'URG Flag Cnt', 'CWE Flag Count', 'ECE Flag Cnt', 'Down/Up Ratio',
    'Pkt Size Avg', 'Fwd Seg Size Avg', 'Bwd Seg Size Avg', 'Fwd Byts/b Avg',
    'Fwd Pkts/b Avg', 'Fwd Blk Rate Avg', 'Bwd Byts/b Avg', 'Bwd Pkts/b Avg',
    'Bwd Blk Rate Avg', 'Subflow Fwd Pkts', 'Subflow Fwd Byts', 'Subflow Bwd Pkts',
    'Subflow Bwd Byts', 'Init Fwd Win Byts', 'Init Bwd Win Byts', 'Fwd Act Data Pkts',
    'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min',
    'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min'
]

# 1. Normal Traffic Sample CSV (mostly BENIGN traffic)
n_normal = 200
normal_data = {f: np.random.uniform(5, 100, size=n_normal) for f in features}
normal_data['Dst Port'] = np.random.choice([80, 443, 53], size=n_normal)
normal_data['Protocol'] = np.random.choice([6, 17], size=n_normal)
normal_data['Flow Pkts/s'] = np.random.uniform(10, 200, size=n_normal)
normal_data['Tot Fwd Pkts'] = np.random.randint(1, 20, size=n_normal)

df_normal = pd.DataFrame(normal_data)
df_normal.to_csv(out_dir / 'normal_web_traffic_sample.csv', index=False)

# 2. DDoS Threat Sample CSV (high packet bursts, high flow rate)
n_ddos = 250
ddos_data = {f: np.random.uniform(10, 500, size=n_ddos) for f in features}
ddos_data['Dst Port'] = [80] * n_ddos
ddos_data['Protocol'] = [6] * n_ddos
ddos_data['Flow Pkts/s'] = np.random.uniform(15000, 30000, size=n_ddos)
ddos_data['Tot Fwd Pkts'] = np.random.randint(800, 2000, size=n_ddos)
ddos_data['Flow Duration'] = np.random.uniform(200000, 500000, size=n_ddos)
ddos_data['SYN Flag Cnt'] = [1] * n_ddos

df_ddos = pd.DataFrame(ddos_data)
df_ddos.to_csv(out_dir / 'ddos_attack_threat_sample.csv', index=False)

# 3. Mixed Traffic Sample CSV (50% Normal, 50% Attack)
n_mixed = 300
mixed_data = {f: np.random.uniform(10, 200, size=n_mixed) for f in features}
attack_rows = np.random.choice(n_mixed, size=150, replace=False)

mixed_data['Dst Port'] = np.random.choice([80, 443, 22, 8080], size=n_mixed)
mixed_data['Protocol'] = np.random.choice([6, 17], size=n_mixed)
mixed_data['Flow Pkts/s'] = np.random.uniform(10, 300, size=n_mixed)
mixed_data['Tot Fwd Pkts'] = np.random.randint(1, 30, size=n_mixed)

# Inject attack signals into attack rows
mixed_data['Flow Pkts/s'][attack_rows] += 18000
mixed_data['Tot Fwd Pkts'][attack_rows] += 1000
mixed_data['Flow Duration'][attack_rows] += 300000

df_mixed = pd.DataFrame(mixed_data)
df_mixed.to_csv(out_dir / 'mixed_network_telemetry_sample.csv', index=False)

print("Generated 3 test CSV sample files in data/processed/sample_test_csvs/")
