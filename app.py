import streamlit as st
import pandas as pd
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Infrastructure Audit | Continuity Benchmark", layout="wide")

# --- HIGH-AUTHORITY ENTERPRISE UI (GLASS-MORPHISM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(10, 18, 30, 0.94), rgba(10, 18, 30, 0.94)), 
                    url("https://share.google/KpUEQWOjnCWCGErW5");
        background-size: cover;
        background-attachment: fixed;
        color: #E6EDF3;
    }

    .value-blade {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #38BDF8;
        padding: 24px;
        margin-bottom: 20px;
        border-radius: 4px;
        backdrop-filter: blur(10px);
    }

    .metric-title { font-size: 0.75rem; font-weight: 700; color: #8B949E; text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #FFFFFF; margin-top: 5px; }
    .metric-sub { font-size: 0.85rem; color: #34D399; font-weight: 600; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: OPERATIONAL AUDIT LEVERS ---
with st.sidebar:
    st.markdown("### 🔍 Audit Parameters")
    
    st.markdown("#### Operational Modules")
    enable_aerial = st.toggle("Aerial Reconnaissance", value=True)
    enable_field = st.toggle("Field Force Efficiency", value=True)
    enable_regulatory = st.toggle("Regulatory (STPIS) Liability", value=True)
    
    st.divider()
    
    with st.expander("🛠️ NETWORK BASELINES", expanded=True):
        total_assets = st.number_input("Substations in Zone", value=500)
        hit_rate = st.slider("Historical Impact Rate (%)", 5, 80, 20)
        crew_rate = st.number_input("Crew Dispatch Cost ($)", value=650)
    
    with st.expander("⚖️ REGULATORY (STPIS)"):
        stpis_rate = st.number_input("STPIS Penalty ($/Min/Asset)", value=120, help="Calculated based on VCR (Value of Customer Reliability) standards.")
        lead_time_hrs = st.slider("SAR Intelligence Lead (Hrs)", 12, 72, 44)

# --- THE VALUE ENGINE ---
actual_wet = int(total_assets * (hit_rate/100))
wasted_dispatches = total_assets - actual_wet

# 1. Aerial Recon Logic
leg_aerial = 85000 if enable_aerial else 0

# 2. Field Force Logic (The Search Phase)
leg_field = (total_assets * crew_rate) if enable_field else 0
sar_field = (actual_wet * crew_rate) if enable_field else 0

# 3. Regulatory Liability Logic
# STPIS logic: (Impacted Assets * Penalty Rate * Duration Saved in Minutes)
stpis_liability_mitigated = (actual_wet * stpis_rate * (lead_time_hrs * 60)) if enable_regulatory else 0

# Totals
legacy_total = leg_aerial + leg_field + stpis_liability_mitigated
sar_event_cost = 25000 # Standard per-event allocation
sar_total = sar_event_cost + sar_field

total_value_at_risk_mitigated = legacy_total - sar_total
roi_multiplier = total_value_at_risk_mitigated / sar_event_cost

# --- MAIN BENCHMARK REPORT ---
st.markdown("<p style='color: #38BDF8; font-weight: 700; letter-spacing: 2px;'>GRID RESILIENCE BENCHMARK</p>", unsafe_allow_html=True)
st.title("Quantifying the Satellite Intelligence Advantage")
st.markdown("#### Moving from Reactive Hindsight to Predictive Operational Foresight")

# TOP ROW:
