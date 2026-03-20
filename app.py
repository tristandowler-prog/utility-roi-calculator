import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Infrastructure Audit | Continuity Benchmark", layout="wide")

# --- EXECUTIVE GLASS UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp {
        background: linear-gradient(rgba(10, 20, 32, 0.94), rgba(10, 20, 32, 0.94)), 
                    url("https://share.google/KpUEQWOjnCWCGErW5");
        background-size: cover; background-attachment: fixed; color: #E6EDF3;
    }
    .value-blade {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #38BDF8; padding: 24px; margin-bottom: 20px; border-radius: 4px; backdrop-filter: blur(10px);
    }
    .metric-title { font-size: 0.75rem; font-weight: 700; color: #8B949E; text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #FFFFFF; margin-top: 5px; }
    .metric-sub { font-size: 0.85rem; color: #34D399; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: MODULAR AUDIT CONTROLS ---
with st.sidebar:
    st.markdown("## 🔍 Audit Configuration")
    
    # --- NEW: SUBSCRIPTION & LATENCY ---
    st.markdown("### 🛰️ SAR Service Tier")
    sar_annual_sub = st.number_input("Annual Subscription (AUD)", value=150000, step=10000)
    data_latency = st.select_slider(
        "Data Delivery Window (Latency)",
        options=["6h", "12h", "24h", "48h", "72h"],
        value="6h",
        help="Faster data delivery drastically increases the 'Time Buy-Back' for restoration."
    )
    
    # Latency Multiplier (Penalty for being slow)
    latency_map = {"6h": 1.0, "12h": 0.85, "24h": 0.60, "48h": 0.30, "72h": 0.10}
    efficiency_factor = latency_map[data_latency]

    st.divider()

    # --- CATEGORY 1: AERIAL ---
    enable_aerial = st.toggle("🚁 Aerial Reconnaissance", value=True)
    if enable_aerial:
        helo_flights = st.number_input("Avg. Flights per Event", value=3)
        helo_rate = st.number_input("Cost per Flight (AUD)", value=25000)
        leg_aerial = helo_flights * helo_rate
    else:
        leg_aerial = 0

    # --- CATEGORY 2: FIELD FORCE ---
    enable_field = st.toggle("🚛 Field Crew Dispatches", value=True)
    if enable_field:
        total_assets = st.number_input("Substations in Footprint", value=500)
        inundation_rate = st.slider("Historical Impact Rate (%)", 5, 80, 20)
        crew_callout = st.number_input("Cost per Crew Dispatch ($)", value=650)
        actual_wet = int(total_assets * (inundation_rate/100))
        leg_field = total_assets * crew_callout
        # SAR only dispatches to wet assets, but efficiency drops if data is late
        sar_field = actual_wet * crew_callout
    else:
        actual_wet = 100
        leg_field = 0
        sar_field = 0

    # --- CATEGORY 3: REGULATORY ---
    enable_regulatory = st.toggle("⚖️ Regulatory (STPIS) Liability", value=True)
    if enable_regulatory:
        stpis_rate = st.number_input("Penalty Rate ($/Min/Sub)", value=120)
        # Lead time is reduced by latency. If latency is 72h, lead time gain is wiped out.
        base_lead_time = 48 
        effective_lead_time = max(0, base_lead_time * efficiency_factor)
        leg_stpis = (actual_wet * stpis_rate * (effective_lead_time * 60))
    else:
        leg_stpis = 0
        effective_lead_time = 0

# --- VALUE ENGINE ---
events_per_year = 4 # Standardized AU flood cycle
annual_legacy_cost = (leg_aerial + leg_field + leg_stpis) * events_per_year
annual_sar_ops = (sar_field * events_per_year) + sar_annual_sub

net_annual_saving = annual_legacy_cost - annual_sar_ops
roi_pct = (net_annual_saving / sar_annual_sub) * 100 if sar_annual_sub > 0 else 0

# --- MAIN BENCHMARK REPORT ---
st.markdown("<p style='color: #38BDF8; font-weight: 700; letter-spacing: 2px;'>OPERATIONAL BENCHMARK AUDIT</p>", unsafe_allow_html=True)
st.title("Strategic Infrastructure Resilience Benchmark")
st.markdown(f"#### Comparative Analysis: Manual Response vs. SAR-Enabled Recovery ({data_latency} Latency)")

# TOP ROW: QUANTIFIED ROI
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Annual Value Protected</p><p class="metric-value">${net_annual_saving:,.0f}</p><p class="metric-sub">Net Benefit (After Sub)</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Effective Lead-Time</p><p class="metric-value">{effective_lead_time:.1f} HRS</p><p class="metric-sub" style="color:#38BDF8;">Faster Recovery Window</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="value-blade"><p class="metric-title">Strategic ROI</p><p class="metric-value">{roi_pct:,.0f}%</p><p class="metric-sub" style="color:#8B949E;">Annual Return on Investment</p></div>', unsafe_allow_html=True)

st.markdown("---")

# DATA CURRENCY INSIGHT
st.markdown(f"### ⏱️ The Criticality of Data Currency")
st.markdown(f"""
In a flood event, information decays rapidly. With a **{data_latency} delivery window**, your operational efficiency is 
at **{efficiency_factor*100:.0f}%** of peak potential. 
{"⚠️ **Warning:** At 48-72h latency, intelligence becomes purely forensic, providing minimal support for active restoration." if efficiency_factor < 0.5 else "✅ **Optimal:** 6-12h latency provides maximum buy-back for STPIS mitigation and crew safety."}
""")



# PILLAR BREAKDOWNS
if enable_regulatory:
    st.markdown(f"""
    <div class="value-blade">
    <strong>Regulatory Impact (STPIS Liability)</strong><br>
    The 'Cost of Delay' is quantified by the minutes of outage saved. By delivering ground-truth in {data_latency}, 
    the utility buys back <strong>{effective_lead_time:.1f} hours</strong> of re-energization time, 
    mitigating <strong>${(leg_stpis * events_per_year):,.0f}</strong> in annual regulatory penalties.
    </div>
    """, unsafe_allow_html=True)



# FINANCIAL SUMMARY TABLE
st.markdown("### 📊 Annual Financial Attribution")
audit_df = pd.DataFrame({
    "Component": ["Aerial Reconnaissance", "Wasted Dispatch Labor", "Regulatory (STPIS) Liability", "SAR Subscription Fee"],
    "Legacy Model (Annual)": [f"${(leg_aerial * events_per_year):,.0f}", f"${((leg_field - sar_field) * events_per_year):,.0f}", f"${(leg_stpis * events_per_year):,.0f}", "$0"],
    "SAR Model (Annual)": ["$0 (Offset)", "$0 (Optimized)", "$0 (Protected)", f"${sar_annual_sub:,.0f}"],
    "Strategic Impact": ["100% CAPEX Offset", "Labor Optimization", "Liability Mitigation", "Data ROI Anchor"]
})
st.table(audit_df)

# DOWNLOAD
st.divider()
st.download_button("📥 DOWNLOAD AUDIT SUMMARY (CSV)", audit_df.to_csv(index=False), use_container_width=True)
