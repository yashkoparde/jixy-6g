import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(2026)
out_dir = Path('data/processed/sample_test_csvs')
out_dir.mkdir(parents=True, exist_ok=True)

# 80-feature schema matching CSE-CIC-IDS2018 benchmark
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

# 1. Botnet Infection Cyber Threat Sample
n_bot = 220
bot_data = {f: np.random.uniform(5, 200, size=n_bot) for f in features}
bot_data['Dst Port'] = np.random.choice([6667, 8080, 1080], size=n_bot)
bot_data['Protocol'] = [6] * n_bot
bot_data['Flow Pkts/s'] = np.random.uniform(12000, 25000, size=n_bot)
bot_data['Tot Fwd Pkts'] = np.random.randint(500, 1500, size=n_bot)
bot_data['Flow Duration'] = np.random.uniform(150000, 450000, size=n_bot)

df_bot = pd.DataFrame(bot_data)
df_bot.to_csv(out_dir / 'botnet_infected_node_sample.csv', index=False)

# 2. Port Scan Reconnaissance Attack Sample
n_scan = 180
scan_data = {f: np.random.uniform(1, 50, size=n_scan) for f in features}
scan_data['Dst Port'] = np.random.randint(1, 1024, size=n_scan)
scan_data['Protocol'] = [6] * n_scan
scan_data['Flow Pkts/s'] = np.random.uniform(16000, 28000, size=n_scan)
scan_data['Tot Fwd Pkts'] = np.random.randint(600, 1200, size=n_scan)
scan_data['SYN Flag Cnt'] = [1] * n_scan

df_scan = pd.DataFrame(scan_data)
df_scan.to_csv(out_dir / 'portscan_reconnaissance_sample.csv', index=False)

# 3. High Density 6G Video Streaming (Benign Heavy Traffic)
n_vid = 300
vid_data = {f: np.random.uniform(10, 80, size=n_vid) for f in features}
vid_data['Dst Port'] = [443] * n_vid
vid_data['Protocol'] = [17] * n_vid # UDP streaming
vid_data['Flow Pkts/s'] = np.random.uniform(50, 250, size=n_vid)
vid_data['Tot Fwd Pkts'] = np.random.randint(5, 30, size=n_vid)

df_vid = pd.DataFrame(vid_data)
df_vid.to_csv(out_dir / '6g_hd_video_stream_benign.csv', index=False)

# 4. Multi-Vector Attack Burst (DDoS + Infiltration Mix)
n_multi = 250
multi_data = {f: np.random.uniform(10, 150, size=n_multi) for f in features}
multi_data['Dst Port'] = np.random.choice([80, 22, 443, 8080], size=n_multi)
multi_data['Protocol'] = [6] * n_multi
multi_data['Flow Pkts/s'] = np.random.uniform(18000, 35000, size=n_multi)
multi_data['Tot Fwd Pkts'] = np.random.randint(900, 2500, size=n_multi)
multi_data['Flow Duration'] = np.random.uniform(300000, 600000, size=n_multi)

df_multi = pd.DataFrame(multi_data)
df_multi.to_csv(out_dir / 'multivector_intrusion_burst_sample.csv', index=False)

print("Generated 4 additional specialized test CSV sample files in data/processed/sample_test_csvs/")
