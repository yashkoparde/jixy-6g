from pathlib import Path
import json
import base64
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.common import ROOT, load_config
from src.prediction.predict import predict_csv

st.set_page_config(
    page_title='JIXY 6G | Zero-Trust Threat Intelligence',
    page_icon='🛡️',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Minimalist HBO-style Intro Animation State for JIXY 6G
if 'hbo_intro_shown' not in st.session_state:
    intro_placeholder = st.empty()
    intro_placeholder.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #030508; z-index: 99999; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Helvetica Neue', sans-serif;">
        <div style="font-size: 5.5rem; font-weight: 800; letter-spacing: 20px; color: #ffffff; text-transform: uppercase; font-family: 'Cinzel', 'Times New Roman', serif; text-shadow: 0 0 40px rgba(0, 242, 254, 0.6);">
            J I X Y — 6 G
        </div>
        <div style="width: 140px; height: 2px; background: linear-gradient(90deg, transparent, #00f2fe, transparent); margin-top: 30px;"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2.2)
    intro_placeholder.empty()
    st.session_state['hbo_intro_shown'] = True

# Custom CSS for dark minimalist aesthetic
header_img_path = ROOT / 'header_bg.jpg'
bg_css = ""
if header_img_path.exists():
    encoded_img = base64.b64encode(header_img_path.read_bytes()).decode()
    bg_css = f"""
    .hero-banner {{
        background: linear-gradient(180deg, rgba(8, 12, 22, 0.82) 0%, rgba(11, 15, 25, 0.96) 100%), url("data:image/jpeg;base64,{encoded_img}");
        background-size: cover;
        background-position: center;
        border-radius: 12px;
        padding: 35px;
        border: 1px solid rgba(0, 242, 254, 0.25);
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.6);
        margin-bottom: 25px;
    }}
    """

st.markdown(f"""
<style>
    {bg_css}
    .main {{ background-color: #07090e; }}
    .stApp {{ background-color: #07090e; color: #e6edf3; }}
    .metric-card {{
        background: rgba(18, 24, 38, 0.85);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }}
    h1, h2, h3 {{ color: #ffffff !important; font-family: 'Inter', sans-serif; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #121826;
        border-radius: 6px;
        color: #c9d1d9;
        padding: 10px 20px;
        font-weight: 500;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #00f2fe !important;
        color: #07090e !important;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# JIXY 6G Minimalist Project Header
st.markdown("""
<div class="hero-banner">
    <div style="font-size: 0.8rem; letter-spacing: 4px; color: #00f2fe; text-transform: uppercase; font-weight: 600; margin-bottom: 6px;">
        NEXT-GEN SECURITY FRAMEWORK
    </div>
    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; letter-spacing: 2px; background: linear-gradient(90deg, #ffffff 0%, #00f2fe 50%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        J I X Y — 6 G
    </h1>
    <p style="color: #8b949e; font-size: 1.05rem; margin-top: 8px; font-weight: 400; max-width: 800px;">
        AI-Powered Intrusion Detection & Differential Privacy Preservation for Heterogeneous 6G Edge Architecture
    </p>
    <div style="display: flex; gap: 12px; margin-top: 18px;">
        <span style="background: rgba(0, 242, 254, 0.12); border: 1px solid rgba(0, 242, 254, 0.4); color: #00f2fe; padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
            XGBoost & 1D-CNN Models
        </span>
        <span style="background: rgba(79, 172, 254, 0.12); border: 1px solid rgba(79, 172, 254, 0.4); color: #4facfe; padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
            Non-IID Sample FedAvg
        </span>
        <span style="background: rgba(0, 255, 136, 0.12); border: 1px solid rgba(0, 255, 136, 0.4); color: #00ff88; padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
            Differential Privacy Perturbation
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

cfg = load_config()

# Interactive Tabs (Threat Inference Engine Promoted to First Position)
tabs = st.tabs([
    '🛡️ Threat Inference Engine',
    '🌐 System Architecture',
    '📊 Benchmark Metrics',
    '🧠 Explainable AI Reasoning',
    '🔬 Telemetry Features'
])

with tabs[0]:
    st.subheader("🛡️ Threat Inference Engine & Visual Analytics")
    st.write("Upload a network flow CSV file to perform real-time intrusion classification and visualize threat telemetry.")
    
    col_up, col_mod = st.columns([2, 1])
    with col_up:
        upload = st.file_uploader("Upload flow records CSV", type=['csv'])
    with col_mod:
        model_map = {
            'XGBoost High-Accuracy Model (.joblib)': 'xgboost_model.joblib',
            'Federated Model (.keras)': 'federated_model.keras',
            'Federated DP Model (.keras)': 'federated_dp_model.keras',
            'Centralized Baseline Model (.keras)': 'centralized_model.keras'
        }
        model_choice_label = st.selectbox(
            "Select Inference Model Engine",
            list(model_map.keys())
        )
        selected_file_name = model_map[model_choice_label]
        
    if upload and st.button("🔍 Run Threat Inference Engine", type="primary"):
        temp_csv = ROOT / 'data' / 'processed' / 'dashboard_upload.csv'
        temp_csv.parent.mkdir(parents=True, exist_ok=True)
        temp_csv.write_bytes(upload.getvalue())
        
        with st.spinner("Analyzing network flow records..."):
            try:
                res = predict_csv(temp_csv, ROOT / 'models' / selected_file_name)
                
                total_rows = len(res)
                attack_count = (res['prediction'] == 'ATTACK').sum()
                benign_count = total_rows - attack_count
                risk_pct = attack_count / total_rows * 100
                
                # Summary Metric Cards
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Analyzed Flows", total_rows)
                m2.metric("BENIGN Normal Flows", benign_count)
                m3.metric("ATTACK Threat Flows", attack_count, delta=f"{risk_pct:.1f}% Threat Risk", delta_color="inverse")
                
                # Comprehensive Analytics Visual Graphs
                st.subheader("📊 Visual Threat Analytics & Distribution Graphs")
                g1, g2 = st.columns(2)
                
                with g1:
                    # Donut Chart for Attack vs Benign Ratio
                    df_pie = pd.DataFrame({'Classification': ['BENIGN', 'ATTACK'], 'Count': [benign_count, attack_count]})
                    fig_pie = px.pie(
                        df_pie, names='Classification', values='Count', hole=0.4,
                        title="Network Flow Classification Ratio",
                        color='Classification',
                        color_discrete_map={'BENIGN': '#00f2fe', 'ATTACK': '#ff4b4b'},
                        template='plotly_dark'
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                    
                with g2:
                    # Histogram / Density plot of Attack Probabilities
                    fig_hist = px.histogram(
                        res, x='attack_probability', nbins=20,
                        title="Threat Probability Distribution Density",
                        labels={'attack_probability': 'Attack Probability'},
                        color_discrete_sequence=['#00f2fe'], template='plotly_dark'
                    )
                    fig_hist.update_layout(yaxis_title="Flow Count")
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
                # Feature Distribution Graphs if key features exist
                if 'Flow Pkts/s' in res.columns:
                    st.subheader("📈 Telemetry Anomaly Scatter: Packet Rate vs Attack Probability")
                    fig_scatter = px.scatter(
                        res, x='Flow Pkts/s', y='attack_probability', color='prediction',
                        title="Flow Packet Rate vs Model Attack Confidence",
                        color_discrete_map={'BENIGN': '#00f2fe', 'ATTACK': '#ff4b4b'},
                        hover_data=['Dst Port'] if 'Dst Port' in res.columns else None,
                        template='plotly_dark'
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                
                st.subheader("Detailed Prediction Data Table")
                st.dataframe(res, use_container_width=True)
                
                st.download_button(
                    label="📥 Download Classified CSV Report",
                    data=res.to_csv(index=False),
                    file_name="jixy6g_threat_report.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Inference failed: {e}")

with tabs[1]:
    col1, col2 = st.columns([1.8, 1])
    with col1:
        st.subheader("6G Zero-Trust Architecture")
        st.markdown("""
        ```text
        [CSE-CIC-IDS2018 Telemetry] ──► [Header Normalization & Cleaning]
                                                        │
                                                        ▼
                                    [80-Feature Stratified Train/Test Split]
                                                        │
                      ┌─────────────────────────────────┴─────────────────────────────────┐
                      ▼                                                                   ▼
        [Centralized Deep Baseline]                                         [Simulated Edge Clients]
         (Pooled Data Training)                                              (Local Process Isolation)
                      │                                                                   │
                      │                                                     [Local 1D-CNN & GBDT Models]
                      │                                                                   │
                      │                                                     [DP Noise & L2 Norm Clipping]
                      │                                                                   │
                      │                                                     [Sample-Weighted FedAvg]
                      │                                                                   │
                      └─────────────────────────────────┬─────────────────────────────────┘
                                                        ▼
                                       [Global Evaluation & Inference]
        ```
        """)
        st.info("💡 **Security Principle:** Edge clients maintain absolute data isolation. Only noise-perturbed weight deltas and sample counts enter the central aggregation channel.")

    with col2:
        st.subheader("Federated & Privacy Parameters")
        st.json({
            'Simulated Edge Nodes': cfg['federated']['num_clients'],
            'FL Rounds': cfg['federated']['rounds'],
            'Data Partition': cfg['federated']['partition'],
            'Privacy Engine': {
                'DP Status': cfg['privacy']['enabled'],
                'L2 Norm Bound (C)': cfg['privacy']['clip_norm'],
                'Noise Multiplier (σ)': cfg['privacy']['noise_multiplier'],
                'Delta Target (δ)': cfg['privacy']['delta']
            }
        })

with tabs[2]:
    st.subheader("Model Benchmark Matrix")
    
    paths = [
        ROOT / 'metrics' / 'centralized_metrics.json',
        ROOT / 'results' / 'federated' / 'federated_metrics.json',
        ROOT / 'results' / 'differential_privacy' / 'federated_dp_metrics.json'
    ]
    
    rows = []
    for p in paths:
        if p.exists():
            d = json.loads(p.read_text(encoding='utf-8'))
            rows.append({
                'Experiment': d.get('experiment', '').upper(),
                'Accuracy': f"{d.get('accuracy', 0)*100:.2f}%",
                'Precision': f"{d.get('precision', 0)*100:.2f}%",
                'Recall': f"{d.get('recall', 0)*100:.2f}%",
                'F1-Score': f"{d.get('f1', 0)*100:.2f}%",
                'ROC-AUC': f"{d.get('roc_auc', 0):.4f}",
                'Training Time (s)': f"{d.get('training_time_seconds', 0):.2f}s",
                'DP Perturbation': "ENABLED" if d.get('dp_enabled') else "DISABLED"
            })
            
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        
        st.subheader("Comparative Benchmark Charts")
        metrics_data = []
        for p in paths:
            if p.exists():
                d = json.loads(p.read_text(encoding='utf-8'))
                exp = d.get('experiment', '').replace('_', ' ').title()
                metrics_data.extend([
                    {'Experiment': exp, 'Metric': 'Accuracy', 'Value': d.get('accuracy', 0)},
                    {'Experiment': exp, 'Metric': 'Precision', 'Value': d.get('precision', 0)},
                    {'Experiment': exp, 'Metric': 'Recall', 'Value': d.get('recall', 0)},
                    {'Experiment': exp, 'Metric': 'F1-Score', 'Value': d.get('f1', 0)},
                    {'Experiment': exp, 'Metric': 'ROC-AUC', 'Value': d.get('roc_auc', 0)}
                ])
        if metrics_data:
            fig = px.bar(pd.DataFrame(metrics_data), x='Metric', y='Value', color='Experiment', barmode='group',
                         title="Baseline vs Federated vs DP-Federated Performance",
                         color_discrete_sequence=['#00f2fe', '#4facfe', '#7f56d9'], template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        cm_path = ROOT / 'plots' / 'centralized_confusion_matrix.png'
        if cm_path.exists():
            st.image(str(cm_path), caption="Centralized Baseline Confusion Matrix", use_container_width=True)
    with c2:
        roc_path = ROOT / 'plots' / 'centralized_roc_curve.png'
        if roc_path.exists():
            st.image(str(roc_path), caption="Centralized ROC Curve", use_container_width=True)

with tabs[3]:
    st.subheader("🧠 Explainable AI: Model Thinking & Decision Tree Rules")
    st.write("Examine how the Gradient Boosted Trees (XGBoost) model weighs network telemetry to make predictions.")
    
    exp_path = ROOT / 'models' / 'explainable_logic.json'
    if exp_path.exists():
        logic_data = json.loads(exp_path.read_text(encoding='utf-8'))
        
        c_exp1, c_exp2 = st.columns([1.2, 1])
        with c_exp1:
            st.subheader("Feature Importance Weights (AI Decision Drivers)")
            imp_df = pd.DataFrame(logic_data['feature_importances'], columns=['Feature', 'Importance Weight'])
            top_imp = imp_df[imp_df['Importance Weight'] > 0].head(10)
            
            fig_imp = px.bar(
                top_imp, x='Importance Weight', y='Feature', orientation='h',
                title="XGBoost Feature Importance Weights",
                color='Importance Weight', color_continuous_scale='tealgrn', template='plotly_dark'
            )
            fig_imp.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_imp, use_container_width=True)
            
        with c_exp2:
            st.subheader("Explicit Decision Tree Rules")
            st.write("IF-THEN decision rules extracted from the model (Class 0.0 = BENIGN, Class 1.0 = ATTACK):")
            st.code(logic_data['tree_reasoning_rules'], language='text')

with tabs[4]:
    st.subheader("Selected Telemetry Features")
    feat_path = ROOT / 'models' / 'selected_features.json'
    if feat_path.exists():
        feats = json.loads(feat_path.read_text(encoding='utf-8'))
        st.write(f"**Total Extracted Features ({len(feats)}):**")
        badge_html = " ".join([f'<span style="background:#121826; color:#00f2fe; border:1px solid #30363d; padding:6px 12px; border-radius:6px; margin:4px; display:inline-block; font-family:monospace;">{f}</span>' for f in feats])
        st.markdown(badge_html, unsafe_allow_html=True)
