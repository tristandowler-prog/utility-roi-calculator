import streamlit as st
import pandas as pd

# 1. SETUP - Absolute standard Streamlit for 100% text visibility.
st.set_page_config(page_title="ICEYE ROI: Emergency Management", layout="wide")

st.title("ICEYE Flood Solutions: Operational Efficiency Audit")
st.write("Focused on Resource Recovery: Transitioning GIS and Field Teams from 'Data Processing' to 'Actionable Response'.")

# 2. GLOBAL PARAMETERS
st.subheader("1. System Parameters")
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, format="%.2f")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0, step=0.5)

st.divider()

# 3. PER-EVENT OPERATIONAL LEDGER
st.subheader("2. Per-Event Operational Ledger (Manual Overrides)")
c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 🚁 Aviation & Recon (Per Event)")
    heli_rate = st.number_input("Heli Flight Rate ($/hr)", value=3500.00, format="%.2f")
    heli_hrs = st.number_input("Heli Flight Hrs (Recon Only)", value=20.0)
    heli_standby = st.number_input("Heli Daily Standby Fee ($)", value=1500.00, format="%.2f")
    
    st.write("---")
    drone_rate = st.number_input("Drone Team Flight Rate ($/hr)", value=250.00, format="%.2f")
    drone_hrs = st.number_input("Drone Flight Hrs / Event", value=15.0)
    drone_standby = st.number_input("Drone Daily Standby Fee ($)", value=1200.00, format="%.2f")

with c2:
    st.write("### 🚛 Field Strike Teams (Per Event)")
    team_count = st.number_input("Number of Active Teams", value=6.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, format="%.2f")
    cloud_wait_days = st.number_input("Blind Window (Cloud/Night Days)", value=2.0)
    
    st.write("---")
    dry_run_penalty = st.number_input("Dry Run Penalty (Wasted Shift/Fuel) ($)", value=2800.00, format="%.2f")
    dry_runs_per_event = st.number_input("Wasted Deployments / Event", value=10.0)

with c3:
    st.write("### 🖥️ GIS Staff Utility (Per Event)")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0)
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, format="%.2f")
    
    st.write("---")
    st.write("**Legacy Mapping Workflow:**")
    leg_processing_hrs = st.number_input("Manual Mapping/Cleaning (Hrs)", value=12.0)
    
    st.write("**ICEYE Mapping Workflow:**")
    iceye_processing_hrs = st.number_input("Actionable Prep Time (Hrs)", value=2.0)

# 4. THE MATH ENGINE

# LEGACY (Per Event)
leg_air = (heli_rate * heli_hrs) + (heli_standby * cloud_wait_days) + \
          (drone_rate * drone_hrs) + (drone_standby * cloud_wait_days)

leg_gis = (gis_staff_count * gis_hourly_rate * leg_processing_hrs)

# Field Personnel: Burn during blind window + Wasted dry runs
leg_field_waste = (team_count * team_daily_burn * cloud_wait_days) + (dry_runs_per_event * dry_run_penalty)

# ICEYE (Per Event)
# ICEYE eliminates aviation recon. 
# GIS staff still work, but only for the prep time (2 hrs vs 12 hrs).
iceye_gis = (gis_staff_count * gis_hourly_rate * iceye_processing_hrs)

# Personnel: Only "wait" for data latency (6 hrs) instead of 2 days.
iceye_field_waste = (team_count * team_daily_burn * (sar_latency / 24.0))

# ANNUAL TOTALS
total_annual_legacy = (leg_air + leg_gis + leg_field_waste) * events_pa
total_annual_iceye = ((iceye_gis + iceye_field_waste) * events_pa) + annual_sub
net_annual_recovery = total_annual_legacy - total_annual_iceye

# 5. RESULTS
st.divider()
st.subheader("3. Resource Recovery Impact (Annualized)")
r1, r2, r3 = st.columns(3)
r1.metric("Net Operational Recovery", f"${net_annual_recovery:,.2f}")
r2.metric("Annual GIS Time Recovered", f"{(leg_processing_hrs - iceye_processing_hrs) * events_pa:.1f} Hours")
r3.metric("Annual Aviation Offset", f"${leg_air * events_pa:,.2f}")

# 6. CHART
st.markdown("### 📊 Annual Resource Cost Distribution")
chart_data = {
    "Category": ["Aviation Recon", "GIS Manual Labor", "Field Readiness Waste", "ICEYE Subscription"],
    "Legacy Model ($)": [leg_air*events_pa, leg_gis*events_pa, leg_field_waste*events_pa, 0],
    "ICEYE Model ($)": [0, iceye_gis*events_pa, iceye_field_waste*events_pa, annual_sub]
}
df_chart = pd.DataFrame(chart_data).set_index("Category")
st.bar_chart(df_chart, height=450)

# 7. BUSINESS CASE FOR THE EM
st.divider()
st.subheader("4. Operational Audit Findings")
st.write(f"**GIS Value Transition:** Your GIS team currently spends **{leg_processing_hrs * events_pa:.0f} hours** per year manually cleaning data. ICEYE reduces this to **{iceye_processing_hrs * events_pa:.0f} hours**, allowing staff to focus on critical situational analysis.")
st.write(f"**Removing the 'Blind Window':** By eliminating the **{cloud_wait_days} day** wait for visual recon, you recover **${(leg_field_waste - iceye_field_waste) * events_pa:,.2f}** in annual team productivity that is currently lost to idleness and dry runs.")
st.write(f"**Deterministic Intelligence:** ICEYE replaces variable, weather-dependent costs (Aviation) with a fixed **${annual_sub:,.2f}** line item, providing flood extent data through clouds and night every **{sar_latency} hours**.")
