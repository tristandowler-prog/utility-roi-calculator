import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="ICEYE ROI Precision Audit", layout="wide")

# --- HIGH-CONTRAST "REPORT" STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
    .roi-hero { 
        background-color: #000000; color: #FFFFFF !important; 
        padding: 25px; text-align: center; border-radius: 4px; margin-bottom: 20px;
    }
    .roi-hero h1, .roi-hero p { color: #FFFFFF !important; margin: 0; }
    label, p, h3, h4 { color: #111111 !important; font-weight: 700 !important; }
    .stNumberInput div div input { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

st.title("Emergency Response ROI: ICEYE vs. Legacy")

# --- 1. INVESTMENT & FREQUENCY ---
col_inv1, col_inv2, col_inv3 = st.columns(3)
with col_inv1:
    annual_sub = st.number_input("ICEYE Annual Subscription ($)", value=150000.00, step=1000.00, format="%.2f")
with col_inv2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_inv3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0, step=0.5)

# --- 2. OPERATIONAL INPUTS (MANUAL OVERRIDES) ---
st.markdown("### 🛠️ Step 1: Manual Overrides (Legacy Costs)")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### 🚁 Aviation & Recon")
    heli_rate = st.number_input("Heli Charter ($/hr)", value=3500.00, step=50.00, format="%.2f")
    heli_recon_hrs = st.number_input("Total Flight Hrs/Event", value=20.0, step=1.0)
    drone_daily = st.number_input("Drone Team Daily Rate ($)", value=2200.00, step=50.00, format="%.2f")
    cloud_window_days = st.number_input("Cloud/Wait Window (Days)", value=2.0, step=0.25)
    
with c2:
    st.markdown("#### 🚛 Field Personnel (Strike Teams)")
    team_count = st.number_input("Number of Strike Teams", value=6.0, step=1.0)
    team_daily_burn = st.number_input("Daily Team Burn ($)", value=12500.00, step=100.00, format="%.2f")
    dry_run_cost = st.number_input("Dry Run Penalty ($/trip)", value=2800.00, step=50.00, format="%.2f")
    dry_runs_event = st.number_input("Dry Runs Prevented/Event", value=10.0, step=1.0)

with c3:
    st.markdown("#### 🖥️ GIS & Information Analysis")
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, step=5.00, format="%.2f")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0, step=1.0)
    gis_processing_hrs = st.number_input("Manual Mapping Time (Hrs)", value=8.0, step=0.5)
    
    st.markdown("#### 🛣️ Logistics & Freight")
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000.00, step=500.00, format="%.2f")
    hwy_count = st.number_input("No. of Major Highways", value=2.0, step=1.0)

# --- 3. THE CALCULATION ENGINE ---

# TIME RECOVERED
leg_wait_total_hrs = (cloud_window_days * 24.0) + gis_processing_hrs
time_recovered_hrs = leg_wait_total_hrs - sar_latency

# LEGACY COSTS (Per Event)
# Aviation: Flight time + Drone standby for duration of blind window
leg_aviation_total = (heli_rate * heli_recon_hrs) + (drone_daily * cloud_window_days)
# GIS: Staff * Rate * Hours
leg_gis_total = (gis_staff_count * gis_hourly_rate * gis_processing_hrs)
# Personnel: Idle Burn + Dry Runs
leg_personnel_total = (team_count * team_daily_burn * cloud_window_days) + (dry_runs_event * dry_run_penalty)
# Freight: Loss * Highways * Total Wait Time
leg_logistics_total = (hwy_loss_hr * hwy_count * leg_wait_total_hrs)

# ICEYE COSTS (Per Event)
# Personnel: Only idle for SAR latency period
iceye_personnel_total = (team_count * team_daily_burn * (sar_latency / 24.0))
# Logistics: Only closed for SAR latency period
iceye_logistics_total = (hwy_loss_hr * hwy_count * sar_latency)

# ANNUAL AGGREGATES
annual_legacy = (leg_aviation_total + leg_gis_total + leg_personnel_total + leg_logistics_total) * events_pa
annual_iceye = ((iceye_personnel_total + iceye_logistics_total) * events_pa) + annual_sub

net_annual_profit = annual_legacy - annual_iceye

# --- 4. TOP-LEVEL RESULTS ---
st.markdown("---")
st.markdown(f"""
<div class='roi-hero'>
    <p>TOTAL NET ANNUAL RECOVERY (PROFIT)</p>
    <h1>${net_annual_profit:,.2f}</h1>
    <p>Acceleration of Actionable Intelligence by {time_recovered_hrs:.1f} hours per event</p>
</div>
""", unsafe_allow_html=True)

# --- 5. VISUAL CHART ---
chart_df = pd.DataFrame({
    "Category": ["Aviation & GIS", "Strike Teams", "Freight Logistics", "Solution Investment"],
    "Legacy Model ($)": [(leg_aviation_total + leg_gis_total) * events_pa, leg_personnel_total * events_pa, leg_logistics_total * events_pa, 0.0],
    "ICEYE Model ($)": [0.0, iceye_personnel_total * events_pa, iceye_logistics_total * events_pa, annual_sub]
}).set_index("Category")

st.bar_chart(chart_df, height=400)

st.write(f"""
### Defensible Logic Audit:
* **Aviation & GIS Offset:** Replaces **${leg_aviation_total*events_pa:,.2f}** in field recon and **${leg_gis_total*events_pa:,.2f}** in manual data labor annually.
* **Personnel Efficiency:** Saves **${(leg_personnel_total - iceye_personnel_total)*events_pa:,.2f}** by eliminating idle strike-team time and preventing **{dry_runs_event * events_pa:.0f}** failed deployments.
* **Economic Recovery:** Accelerating highway reopening by **{time_recovered_hrs:.1f} hours** recovers **${(leg_logistics_total - iceye_logistics_total)*events_pa:,.2f}** in regional freight productivity.
""")
