import streamlit as st
import pandas as pd
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Infrastructure Audit | Continuity Benchmark", layout="wide")

# --- HIGH-AUTHORITY ENTERPRISE UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp {
        background: linear-gradient(rgba(10, 20, 32, 0.94), rgba(10, 20, 32, 0.94)), 
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
    .metric-sub { font-size: 0.85rem; color: #34D399; font-weight: 600; }
    
    /* Input Styling */
    .stNumberInput, .stSlider { background: rgba(255,255,255,0.02); border-radius: 8px; padding: 5px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: MODULAR AUDIT CONTROLS ---
with st.sidebar:
    st.markdown("## 🔍 Audit Configuration")
    st.info("Toggle operational modules to build your custom business case.")

    # --- CATEGORY 1: AERIAL ---
    st.markdown("---")
    enable_aerial = st.toggle("🛰️ Aerial Reconnaissance", value=True)
    if enable_aerial:
        helo_flights = st.number_input("Avg. Flights per Event", value=3)
        helo_rate = st.number_input("Cost per Flight (AUD)", value=25000)
        leg_aerial = helo_flights * helo_rate
    else:
        leg_aerial = 0

    # --- CATEGORY 2: FIELD FORCE ---
    st.markdown("---")
    enable_field = st.toggle("🚛 Field Crew Dispatches", value=True)
    if enable_field:
        total_assets = st.number_input("Substations in Footprint", value=500)
        inundation_rate = st.slider("Historical Impact Rate (%)", 5, 80, 20)
        crew_callout = st.number_input("Cost per Crew Dispatch ($)", value=650)
        
        actual_wet = int(total_assets * (inundation_rate/100))
        wasted_dispatches = total_assets - actual_wet
        
        leg_field = total_assets * crew_callout
        sar_field = actual_wet * crew_callout
    else:
        actual_wet = 100 # Default for other calcs
        leg_field = 0
        sar_field = 0

    # --- CATEGORY 3: REGULATORY ---
    st.markdown("---")
    enable_regulatory = st.toggle("⚖️ Regulatory (STPIS) Liability", value=True)
    if enable_regulatory:
        stpis_rate = st.number_input("Penalty Rate ($/Min/Sub)", value=120)
        lead_time_hrs = st.slider("SAR Intelligence Lead (Hrs)", 6, 72, 44)
        leg_stpis = (actual_wet * stpis_rate * (lead_time_hrs * 60))
    else:
        leg_stpis = 0

# --- VALUE ENGINE ---
sar_event_cost = 25000 # Standard per-event data allocation
legacy_total = leg_aerial + leg_field + leg_stpis
sar_total = sar_event_cost + sar_field

total_mitigated = legacy_total - sar_total
roi_multiplier = total_mitigated / sar_event_cost if sar_event_cost > 0 else 0

# --- MAIN BENCHMARK REPORT ---
st.markdown("<p style='color: #38BDF8; font-weight: 700; letter-spacing: 2px;'>OPERATIONAL BENCHMARK AUDIT</p>", unsafe_allow_html=True)
st.title("Satellite Intelligence vs. Legacy Flood Response")
st.markdown("#### Quantifying Operational Friction & Regulatory Exposure")

# TOP ROW: QUANTIFIED ROI
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Value at Risk Mitigated</p><p class="metric-value">${total_mitigated:,.0f}</p><p class="metric-sub">Per Event Outcome</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Lead-Time Advantage</p><p class="metric-value">{lead_time_hrs if enable_regulatory else "--"} HRS</p><p class="metric-sub" style="color:#38BDF8;">Faster Restoration Window</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Intelligence Multiplier</p><p class="metric-value">{roi_multiplier:,.1f}x</p><p class="metric-sub" style="color:#8B949E;">Return on Data Investment</p></div>', unsafe_allow_html=True)

st.markdown("---")

# PILLAR BREAKDOWNS
st.markdown("### 🧩 Critical Value Drivers")

if enable_aerial:
    st.markdown(f"""
    <div class="value-blade">
    <strong>Module: Aerial Reconnaissance Optimization</strong><br>
    SAR eliminates the requirement for visual scouting flights. Unlike helicopters, 
    SAR penetrates 100% cloud cover and functions during 2:00 AM storm surges. 
    <strong>Offset Value: ${leg_aerial:,.0f}</strong>
    </div>
    """, unsafe_allow_html=True)
    

if enable_field:
    st.markdown(f"""
    <div class="value-blade">
    <strong>Module: Frictionless Field Force Dispatch</strong><br>
    By identifying 'Ground Truth' inundation lines digitally, the utility prevents 
    <strong>{wasted_dispatches} zero-value dispatches</strong>. Resources are deployed directly 
    to high-probability repair sites on Trip 1.
    </div>
    """, unsafe_allow_html=True)
    

if enable_regulatory:
    st.markdown(f"""
    <div class="value-blade">
    <strong>Module: Regulatory (STPIS) Liability Protection</strong><br>
    Under AER standards, the outage clock is penalized for every minute of delay. 
    Accelerating restoration by <strong>{lead_time_hrs} hours</strong> mitigates 
    <strong>${leg_stpis:,.0f}</strong> in potential service target penalties.
    </div>
    """, unsafe_allow_html=True)
    

# AUDIT TABLE
st.markdown("### 📊 Operational Cost Variance")
audit_df = pd.DataFrame({
    "Operational Phase": ["Aerial Reconnaissance", "Wasted Search Phase", "Regulatory Liability", "Repair Dispatch"],
    "Legacy Model (AUD)": [f"${leg_aerial:,.0f}", f"${(leg_field - sar_field):,.0f}", f"${leg_stpis:,.0f}", f"${sar_field:,.0f}"],
    "SAR-Enabled Model": ["$0", "$0", "$0 (Accelerated)", f"${sar_field:,.0f}"],
    "Efficiency Gain": ["-100%", "-100%", "Risk Mitigation", "Direct Precision"]
})
st.table(audit_df)

# DOWNLOAD
st.divider()
st.download_button("📥 DOWNLOAD AUDIT SUMMARY (CSV)", audit_df.to_csv(index=False), use_container_width=True)
st.markdown("<p style='text-align: center; color: #8B949E; font-size: 0.75rem;'>Benchmarked against Australian Utility Operational Standards © 2026</p>", unsafe_allow_html=True)
