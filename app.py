import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="ICEYE Flood ROI Tool", layout="wide")

# --- ICEYE BRANDING & HIGH-CONTRAST UI ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #121212; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    /* Top Header */
    .header-box { background-color: #000000; color: #FFFFFF; padding: 25px; border-radius: 5px; margin-bottom: 30px; }
    .header-box h1 { color: #FFFFFF !important; margin: 0; font-weight: 800; }
    /* Input Sections */
    .input-card { background-color: #F8F9FA; border-left: 5px solid #000000; padding: 20px; border-radius: 4px; margin-bottom: 20px; }
    .input-header { font-weight: 800; text-transform: uppercase; font-size: 0.9rem; color: #444; margin-bottom: 15px; }
    /* Final ROI UI */
    .roi-panel { background-color: #E6F4EA; border: 2px solid #1E7E34; padding: 30px; border-radius: 8px; text-align: center; }
    .roi-label { font-weight: 700; color: #1E7E34; text-transform: uppercase; letter-spacing: 1px; }
    .roi-value { font-size: 3.5rem; font-weight: 900; color: #1E7E34; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='header-box'><h1>ICEYE Flood Solutions: Economic Impact Audit</h1><p>Strategic Value Demonstration for Australian Government & Infrastructure</p></div>", unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM PARAMETERS ---
with st.sidebar:
    st.markdown("### 🛰️ ICEYE SUBSCRIPTION")
    annual_sub = st.number_input("Annual Solution Cost ($)", value=150000)
    events_pa = st.slider("Major Events Per Year", 1, 10, 3)
    
    st.markdown("---")
    st.markdown("### ⚡ SAR PERFORMANCE")
    sar_latency = st.slider("Data Latency (Hrs)", 4, 12, 6, help="ICEYE SAR bypasses cloud/darkness vs Optical/Visual.")

# --- MAIN INPUT INTERFACE ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("<p class='input-header'>1. Aviation & Reconnaissance (Legacy)</p>", unsafe_allow_html=True)
    heli_rate = st.number_input("Heli Charter Rate ($/hr)", value=3500)
    heli_hrs_event = st.number_input("Heli Total Recon Hours/Event", value=40, help="Wait time for clear sky + flight time.")
    drone_daily = st.number_input("Drone Team Daily Rate ($)", value=2200)
    drone_days = st.number_input("Drone Mobilization Days", value=5)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("<p class='input-header'>2. Field Strike Teams (SES/RFS/ADF)</p>", unsafe_allow_html=True)
    team_count = st.number_input("Active Strike Teams", value=6)
    team_daily_burn = st.number_input("Team Daily Operating Cost ($)", value=12500, help="Includes wages, allowances, fuel, backfill.")
    blind_window_days = st.number_input("Cloud/Visual 'Blind' Window (Days)", value=2.0, help="Days where ground truth is uncertain.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_in2:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("<p class='input-header'>3. Infrastructure & Logistics (Economic)</p>", unsafe_allow_html=True)
    hwy_loss_hr = st.number_input("Hwy Closure Freight Loss ($/hr)", value=15000)
    hwy_count = st.number_input("Major Corridors Impacted", value=2)
    gis_process_hrs = st.number_input("Manual GIS Analysis Gap (Hrs)", value=8, help="Time to manually map extent from photos.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("<p class='input-header'>4. DRFA Category B/C Recovery</p>", unsafe_allow_html=True)
    dry_run_penalty = st.number_input("Dry Run / Bad Tasking Penalty ($)", value=2800)
    dry_runs_saved = st.number_input("Failed Taskings Prevented / Event", value=10)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CALCULATION ENGINE (ICEYE LOGIC)
# ==========================================

# 1. Total Information Gap (Legacy vs ICEYE)
legacy_gap_hrs = (blind_window_days * 24) + gis_process_hrs
iceye_gap_hrs = sar_latency
time_recovered_hrs = legacy_gap_hrs - iceye_gap_hrs

# 2. Hard Cost Offsets (OpEx)
# Legacy costs for Recon
total_leg_recon = (heli_rate * heli_hrs_event) + (drone_daily * drone_days)
# Personnel Waste (Teams idle during blind window)
total_leg_personnel = (team_count * team_daily_burn * blind_window_days) + (dry_runs_saved * dry_run_penalty)
# Freight Impact
total_leg_freight = (hwy_loss_hr * hwy_count * legacy_gap_hrs)

# ICEYE Cost of Operations (Reduced personnel idle time)
total_iceye_personnel = (team_count * team_daily_burn * (sar_latency/24))
total_iceye_freight = (hwy_loss_hr * hwy_count * sar_latency)

# TOTALS
annual_ops_saving = ((total_leg_recon + total_leg_personnel) - total_iceye_personnel) * events_pa
annual_logistics_saving = (total_leg_freight - total_iceye_freight) * events_pa
net_annual_roi = (annual_ops_saving + annual_logistics_saving) - annual_sub

# ==========================================
# DEFENSEABLE OUTPUTS
# ==========================================
st.markdown("---")
res_c1, res_c2 = st.columns([1.5, 1])

with res_c1:
    st.markdown("<div class='roi-panel'>", unsafe_allow_html=True)
    st.markdown("<p class='roi-label'>Projected Net Annual ROI</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='roi-value'>${net_annual_roi/1e6:.2f}M</p>", unsafe_allow_html=True)
    st.markdown(f"**Strategic Gain:** {time_recovered_hrs:.0f} Hours of Actionable Intelligence recovered per event.")
    st.markdown("</div>", unsafe_allow_html=True)

with res_c2:
    st.markdown("### Cost Recovery Split")
    st.write(f"- **Ops & Aviation Offset:** ${annual_ops_saving/1e3:.0f}k")
    st.write(f"- **Logistics/Freight Recovery:** ${annual_logistics_saving/1e6:.1f}M")
    st.info(f"Analysis assumes ICEYE provides 'Truth' data {time_recovered_hrs/24:.1f} days faster than optical/ground methods.")

# VISUAL COMPARISON
chart_data = pd.DataFrame({
    "Sector": ["Aviation & Recon", "Field Personnel", "Freight Logistics"],
    "Legacy Model ($)": [total_leg_recon, total_leg_personnel, total_leg_freight],
    "ICEYE SAR Model ($)": [0, total_iceye_personnel, total_iceye_freight]
}).set_index("Sector")
st.bar_chart(chart_data)
