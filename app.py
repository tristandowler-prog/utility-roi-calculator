import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI: Source of Truth", layout="wide")

st.title("ICEYE Flood Solutions: Operational ROI Audit")
st.write("Comparing 'Blind Response' (Legacy) vs. 'Data-Driven Response' (ICEYE).")

# 1. SYSTEM PARAMS
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, format="%.2f")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0)
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0)

st.divider()

# 2. INPUTS
c1, c2, c3 = st.columns(3)
with c1:
    st.write("### 🚁 Aviation (Variable)")
    heli_rate = st.number_input("Heli Rate ($/hr)", value=3500.00)
    heli_hrs_recon = st.number_input("Flight Hrs for Recon only", value=20.0)
    cloud_wait_days = st.number_input("Days Blind (Cloud Window)", value=2.0)
with c2:
    st.write("### 🚛 Strike Teams (Variable)")
    team_count = st.number_input("Number of Teams", value=6.0)
    team_day_rate = st.number_input("Team Daily Rate ($)", value=12500.00)
    dry_run_cost = st.number_input("Cost of one Wasted Trip ($)", value=2800.00)
    dry_runs_saved = st.number_input("Wasted Trips Saved per Event", value=10.0)
with c3:
    st.write("### 🛣️ Logistics (Variable)")
    hwy_loss_hr = st.number_input("Hwy Economic Loss ($/hr)", value=15000.00)
    hwy_count = st.number_input("Number of Hwy's", value=2.0)

# 3. THE MATH
# Time Gap
total_blind_hrs = (cloud_wait_days * 24.0)
time_saved_per_event = total_blind_hrs - sar_latency

# LEGACY (Per Event)
leg_air = (heli_rate * heli_hrs_recon)
leg_labor_idle = (team_count * team_day_rate * cloud_wait_days)
leg_wasted_trips = (dry_runs_saved * dry_run_cost)
leg_econ_loss = (hwy_loss_hr * hwy_count * total_blind_hrs)
total_legacy_event = leg_air + leg_labor_idle + leg_wasted_trips + leg_econ_loss

# ICEYE (Per Event)
# We still pay for labor, but only for the 6-hour data latency, not 2 days.
iceye_labor_idle = (team_count * team_day_rate * (sar_latency / 24.0))
iceye_econ_loss = (hwy_loss_hr * hwy_count * sar_latency)
total_iceye_event = iceye_labor_idle + iceye_econ_loss

# ANNUAL TOTALS
annual_legacy = total_legacy_event * events_pa
annual_iceye = (total_iceye_event * events_pa) + annual_sub
net_roi = annual_legacy - annual_iceye

# 4. OUTPUTS
st.divider()
st.subheader("Results")
m1, m2, m3 = st.columns(3)
m1.metric("Net Annual Recovery", f"${net_roi:,.2f}")
m2.metric("Hours of Blindness Removed", f"{time_saved_per_event * events_pa:.0f} hrs")
m3.metric("Annual Legacy Waste", f"${annual_legacy:,.2f}")

# 5. CHART
chart_data = {
    "Category": ["Aviation", "Wasted Labor", "Wasted Trips", "Economic Loss", "ICEYE Sub"],
    "Legacy ($)": [leg_air*events_pa, leg_labor_idle*events_pa, leg_wasted_trips*events_pa, leg_econ_loss*events_pa, 0],
    "ICEYE ($)": [0, iceye_labor_idle*events_pa, 0, iceye_econ_loss*events_pa, annual_sub]
}
st.bar_chart(pd.DataFrame(chart_data).set_index("Category"))
