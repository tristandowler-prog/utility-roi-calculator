import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="Flood Solutions | Continuity Audit", layout="wide")

# --- EXECUTIVE "GLASS" UI ---
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

# --- SIDEBAR: STRATEGIC INPUT LAYER ---
with st.sidebar:
    st.markdown("## 🛡️ Strategic Input Layer")
    st.info("Calibrated to 2026 Regulatory VCR/STPIS and Labor baselines.")
    
    with st.expander("📡 SATELLITE DATA SERVICE", expanded=True):
        sar_sub = st.number_input("Annual Data Subscription ($)", value=150000)
        data_latency = st.select_slider("Data Delivery Window (Latency)", options=["6h", "12h", "24h", "48h"], value="6h")

    with st.expander("📐 NETWORK & EXPOSURE", expanded=True):
        total_assets = st.number_input("Total Assets in Network", value=1200)
        inundation_rate = st.slider("Historical Impact Rate (%)", 5, 100, 20)
        annual_events = st.slider("Significant Flood Events / Year", 1, 10, 4)

    st.divider()

    st.markdown("### 🚛 Operational Modules")
    enable_aerial = st.toggle("Aerial Reconnaissance", value=True)
    enable_field = st.toggle("Field Force Optimization", value=True)
    enable_double_trip = st.toggle("Eliminate 'Double-Trip' Penalty", value=True)
    enable_regulatory = st.toggle("Regulatory (STPIS) Liability", value=True)

    if enable_field or enable_double_trip:
        with st.expander("🛠️ Labor & Gear Assumptions"):
            crew_cost = st.number_input("Fully Burdened Crew Rate ($)", value=850)
            double_trip_risk = st.slider("Mismatched Gear Risk (%)", 0, 100, 45)
            recovery_boost = st.slider("Targeted Recovery Gain (Hrs/Asset)", 1, 12, 4)
    
    if enable_regulatory:
        with st.expander("⚖️ STPIS Assumptions"):
            stpis_penalty = st.number_input("Penalty Rate ($/Min/Asset)", value=125)

# --- THE VALUE ENGINE ---
exposed_assets = int(total_assets * (inundation_rate / 100))
dry_assets = total_assets - exposed_assets

# Latency Factor (Decay of value)
latency_eff = {"6h": 1.0, "12h": 0.82, "24h": 0.55, "48h": 0.20}[data_latency]
base_search_time = 44 
effective_time_saved = base_search_time * latency_eff

# Calculations
leg_aerial = 85000 if enable_aerial else 0
leg_search_waste = (dry_assets * crew_cost) if enable_field else 0
leg_double_trip = (exposed_assets * (double_trip_risk/100) * crew_cost) if enable_double_trip else 0
leg_stpis = (exposed_assets * stpis_penalty * ((effective_time_saved + recovery_boost) * 60)) if enable_regulatory else 0

legacy_event_total = leg_aerial + leg_search_waste + leg_double_trip + leg_stpis
sar_event_total = (exposed_assets * crew_cost) 

annual_net_benefit = (legacy_event_total * annual_events) - (sar_event_total * annual_events) - sar_sub
roi_ratio = (annual_net_benefit / sar_sub) * 100 if sar_sub > 0 else 0

# --- MAIN INTERFACE ---
st.markdown("<p style='color: #00D1FF; font-weight: 700; letter-spacing: 2px;'>FLOOD SOLUTIONS: AUDIT REPORT</p>", unsafe_allow_html=True)
st.title("Strategic Infrastructure Recovery Benchmark")
st.markdown(f"#### Annualized Strategic Impact over {annual_events} Flood Events")

# KPI STRIP
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Assets Exposed</p><p class="metric-value">{exposed_assets:,}</p><p class="metric-sub">Targeted Recovery</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Lead-Time Gain</p><p class="metric-value">{effective_time_saved:.1f}h</p><p class="metric-sub">Search Phase Offset</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Annual ROI</p><p class="metric-value">{roi_ratio:,.0f}%</p><p class="metric-sub">Post-Subscription</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Value Protected</p><p class="metric-value">${annual_net_benefit:,.0f}</p><p class="metric-sub">Annual Risk Avoidance</p></div>', unsafe_allow_html=True)

# THE GAP ANALYSIS
st.markdown("### 📊 Restoration Efficiency: Legacy vs. Targeted Response")
chart_data = pd.DataFrame({
    "Strategy": ["Legacy (Blind Search)", "Targeted Flood Solution"],
    "Annual Operational Cost ($)": [(legacy_event_total * annual_events), (sar_event_total * annual_events + sar_sub)]
})
st.bar_chart(chart_data, x="Strategy", y="Annual Operational Cost ($)", color="#00D1FF")

# STRATEGIC PILLARS
st.markdown("---")
st.markdown("### 🧩 Strategic Value Defensibility")

col_a, col_b = st.columns(2)

with col_a:
    if enable_double_trip:
        st.markdown(f"""
        <div class="value-blade">
        <strong>The 'Double-Trip' Gear Mismatch</strong><br>
        Without depth-intelligence, <b>{double_trip_risk}%</b> of dispatches currently arrive with incorrect equipment. 
        High-fidelity satellite data ensures 'Right Gear, First Trip,' eliminating redundant dispatch cycles and labor waste.
        <br><br><i>Annual Leakage Avoided: ${(leg_double_trip * annual_events):,.0f}</i>
        </div>
        """, unsafe_allow_html=True)

with col_b:
    if enable_regulatory:
        st.markdown(f"""
        <div class="value-blade">
        <strong>Regulatory Compliance (STPIS)</strong><br>
        Outage duration is the primary driver of regulatory penalties. Accelerating ground-truth delivery by <b>{effective_time_saved:.1f} hours</b> 
        lowers restoration latency and protects the regulated rate of return.
        <br><br><i>Annual Penalty Mitigation: ${(leg_stpis * annual_events):,.0f}</i>
        </div>
        """, unsafe_allow_html=True)



# THE FINANCIAL TABLE
st.markdown("### 📊 Financial Attribution Matrix (Annualized)")
audit_df = pd.DataFrame({
    "Cost Category": ["Aerial Recon", "Wasted Search Dispatches", "Double-Trip Friction", "Regulatory Liability", "Direct Repair Dispatch"],
    "Legacy Model": [f"${(leg_aerial*annual_events):,.0f}", f"${(leg_search_waste*annual_events):,.0f}", f"${(leg_double_trip*annual_events):,.0f}", f"${(leg_stpis*annual_events):,.0f}", f"${(sar_event_total*annual_events):,.0f}"],
    "Flood Solution Enabled": ["$0 (Offset)", "$0 (Eliminated)", "$0 (Verified)", "$0 (Accelerated)", f"${(sar_event_total*annual_events):,.0f}"],
    "Logic": ["Total Data Coverage", "Intelligence Filter", "First-Trip Fix", "Time-Lead Gain", "Core Operations"]
})
st.table(audit_df)

st.divider()
st.button("📄 GENERATE EXECUTIVE PROPOSAL (PDF)", use_container_width=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.75rem;'>Benchmarked against 2026 National Energy Market (NEM) standards.</p>", unsafe_allow_html=True)
