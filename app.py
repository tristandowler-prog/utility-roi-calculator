import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="Infrastructure Audit | ICEYE Strategic", layout="wide")

# --- EXECUTIVE "AUDIT" UI (KEEPING THE STYLE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp {
        background: linear-gradient(rgba(10, 22, 35, 0.96), rgba(10, 22, 35, 0.96)), 
                    url("https://share.google/KpUEQWOjnCWCGErW5");
        background-size: cover; background-attachment: fixed; color: #F1F5F9;
    }
    .value-blade {
        background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #00D1FF; padding: 22px; margin-bottom: 20px; border-radius: 4px; backdrop-filter: blur(15px);
    }
    .metric-title { font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; }
    .metric-value { font-size: 2.4rem; font-weight: 800; color: #FFFFFF; line-height: 1.1; }
    .metric-sub { font-size: 0.85rem; color: #00D1FF; font-weight: 600; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: DEFENDABLE INPUTS ---
with st.sidebar:
    st.markdown("## 🛡️ Strategic Input Layer")
    st.info("Calibrated to 2026 AER VCR/STPIS and AU Labor baselines.")
    
    # MODULE: SUBSCRIPTION & LATENCY
    st.markdown("### 🛰️ ICEYE Service Tier")
    sar_sub = st.number_input("Annual Subscription (AUD)", value=150000)
    data_latency = st.select_slider("Latency SLA", options=["6h", "12h", "24h", "48h"], value="6h")

    st.divider()

    # MODULE: NETWORK SCALE
    st.markdown("### 📐 Network Exposure")
    total_assets = st.number_input("Total Assets in Network", value=1200)
    inundation_rate = st.slider("Historical Impact Rate (%)", 5, 100, 20)
    annual_events = st.slider("Significant Flood Events / Year", 1, 10, 4)

    st.divider()

    # MODULE: OPERATIONAL FRICTION (TOGGLES)
    st.markdown("### 🚛 Operational Modules")
    enable_aerial = st.toggle("Aerial Reconnaissance", value=True)
    enable_field = st.toggle("Field Force Optimization", value=True)
    enable_regulatory = st.toggle("Regulatory (STPIS) Liability", value=True)
    enable_double_trip = st.toggle("Eliminate 'Double-Trip' Penalty", value=True)

    if enable_field or enable_double_trip:
        with st.expander("🛠️ Labor & Gear Assumptions"):
            crew_cost = st.number_input("Fully Burdened Crew Rate ($)", value=850)
            double_trip_risk = st.slider("Mismatched Gear Risk (%)", 0, 100, 45)
    
    if enable_regulatory:
        with st.expander("⚖️ STPIS Assumptions"):
            stpis_penalty = st.number_input("Penalty Rate ($/Min/Asset)", value=125)

# --- THE VALUE ENGINE ---
exposed_assets = int(total_assets * (inundation_rate / 100))
dry_assets = total_assets - exposed_assets

# Latency Factor
latency_eff = {"6h": 1.0, "12h": 0.82, "24h": 0.55, "48h": 0.20}[data_latency]
time_saved_hrs = 48 * latency_eff 

# Calculations
