import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE Strategic ROI", layout="wide")

# 1. HEADER
st.title("Emergency Response ROI: ICEYE Flood Solutions")
st.write("This tool calculates the economic recovery gained by bypassing the 'Visual Information Gap' using SAR persistence.")

# 2. THE INPUT ARSENAL (Manual Overrides)
st.header("1. Operational Cost Inputs")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚁 Aviation & Recon")
    heli_rate = st.number_input("Heli Charter ($/hr)", value=3500)
    heli_hrs_event = st.number_input("Total Recon Hours/Event", value=40)
    drone_daily = st.number_input("Drone Team Daily ($)", value=2200)
    drone_days = st.number_input("Drone Deployment (Days)", value=5)

with col2:
    st.subheader("🚛 Field Personnel (SES/RFS)")
    team_count = st.number_input("Number of Strike Teams", value=6)
    team_daily_burn = st.number_input("Daily Team Burn ($)", value=12500)
    dry_run_penalty = st.number_input("Dry Run Penalty ($/failed trip)", value=2800)
    dry_runs_event = st.number_input("Dry Runs Prevented/Event", value=10)

with col3:
    st.subheader("🖥️ GIS & Analysis")
    gis_staff_rate = st.number_input("GIS Staff Hourly Rate ($)", value=120)
    gis_staff_count = st.number_input("GIS Staff Count", value=2)
    gis_process_hrs = st.number_input("Manual Processing Gap (Hrs)", value=8)

st.header("2. Economic & Timeline Inputs")
col4, col5 = st.columns(2)
with col4:
    cloud_window_hrs = st.number_input("Cloud/Visual Blindness Window (Hrs)", value=48)
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000)
    hwy_count = st.number_input("Number of Major Highways", value=2)

with col5:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000)
    events_pa = st.number_input("Major Events Per Year", value=3)
    sar_latency = st.number_input("ICEYE Data Latency (Hrs)", value=6)

# 3. CALCULATIONS
# Legacy Wait = Total time crews are 'blind' + Time spent processing data
legacy_wait = cloud_window_hrs + gis_process_hrs
time_recovered = legacy_wait - sar_latency

# Financials
# Legacy Recon/GIS
leg_recon = (heli_rate * heli_hrs_event) + (drone_daily * drone_days)
leg_gis = (gis_process_hrs * gis_staff_rate * gis_staff_count)
# Personnel (Idle time during blind window + Dry runs)
leg_personnel = (team_count * team_daily_burn * (cloud_window_hrs/24)) + (dry_runs_event * dry_run_penalty)
# Freight
leg_freight = (hwy_loss_hr * hwy_count * legacy_wait)

# ICEYE Performance
fut_personnel = (team_count * team_daily_burn * (sar_latency/24))
fut_freight = (hwy_loss_hr * hwy_count * sar_latency)

# TOTALS
event_saving = (leg_recon + leg_gis + leg_personnel + leg_freight) - (fut_personnel + fut_freight)
annual_roi = (event_saving * events_pa) - annual_sub

# 4. OUTPUTS (High Visibility)
st.markdown("---")
st.header("3. Strategic ROI Results")
m1, m2, m3 = st.columns(3)
m1.metric("Time Gained (Hrs/Event)", f"{time_recovered} hrs")
m2.metric("Per Event Recovery", f"${event_saving/1e6:.2f}M")
m3.metric("NET ANNUAL ROI", f"${annual_roi/1e6:.2f}M")

# Visual Chart
chart_df = pd.DataFrame({
    "Category": ["Aviation/GIS", "Strike Teams", "Logistics/Freight"],
    "Legacy Workflow ($)": [leg_recon + leg_gis, leg_personnel, leg_freight],
    "ICEYE Workflow ($)": [0, fut_personnel, fut_freight]
}).set_index("Category")
st.bar_chart(chart_df)
