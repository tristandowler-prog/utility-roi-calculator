import streamlit as st
import pandas as pd

# 1. SETUP - Standard configuration for 100% reliability.
st.set_page_config(page_title="ICEYE ROI: Source of Truth", layout="wide")

# 2. HEADER
st.title("ICEYE Flood Solutions: Operational ROI Audit")
st.write("The definitive model comparing Variable Legacy Costs (Aviation, Labor, Downtime) vs. Deterministic SAR Intelligence.")

# 3. GLOBAL CONTROLS
st.subheader("1. System Parameters")
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, step=1000.00, format="%.2f")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0, step=0.5)

st.divider()

# 4. PER-EVENT INPUTS (The Manual Overrides)
st.subheader("2. Per-Event Operational Inputs (The 'Manual' Truth)")
st.info("Input the costs for a SINGLE event. These scale automatically by the frequency of events.")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 🚁 Aviation & Drone Recon")
    heli_flight_rate = st.number_input("Heli Flight Rate ($/hr)", value=3500.00, step=50.00, format="%.2f")
    heli_flight_hrs = st.number_input("Heli Flight Hrs / Event", value=20.0, step=1.0)
    heli_standby_daily = st.number_input("Heli Daily Standby Fee ($)", value=1500.00, step=50.00, format="%.2f")
    
    st.write("---")
    drone_flight_rate = st.number_input("Drone Team Flight Rate ($/hr)", value=250.00, step=10.00, format="%.2f")
    drone_flight_hrs = st.number_input("Drone Flight Hrs / Event", value=15.0, step=1.0)
    drone_standby_daily = st.number_input("Drone Team Daily Standby ($)", value=1200.00, step=50.00, format="%.2f")
    
    st.write("---")
    cloud_window_days = st.number_input("Cloud / Visual Blind Window (Days)", value=2.0, step=0.25)

with c2:
    st.write("### 🚛 Field Personnel (Strike Teams)")
    team_count = st.number_input("Active Strike Teams", value=6.0, step=1.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, step=100.00, format="%.2f")
    dry_run_penalty = st.number_input("Dry Run Penalty ($ per trip)", value=2800.00, step=50.00, format="%.2f")
    dry_runs_prevented = st.number_input("Dry Runs Prevented / Event", value=10.0, step=1.0)

with c3:
    st.write("### 🖥️ GIS & Infrastructure")
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, step=5.00, format="%.2f")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0, step=1.0)
    gis_processing_hrs = st.number_input("Manual Mapping Time (Hrs)", value=8.0, step=0.5)
    
    st.write("---")
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000.00, step=500.00, format="%.2f")
    hwy_count = st.number_input("Impacted Major Highways", value=2.0, step=1.0)

# 5. THE CALCULATION ENGINE (QC CHECKED)

# Time Gap
leg_wait_hrs = (cloud_window_days * 24.0) + gis_processing_hrs
time_recovered_per_event = leg_wait_hrs - sar_latency

# --- LEGACY CALCULATIONS (PER EVENT) ---
# Aviation = Active Flight + Passive Standby during the cloud window
leg_aviation_event = (heli_flight_rate * heli_flight_hrs) + (heli_standby_daily * cloud_window_days) + \
                     (drone_flight_rate * drone_flight_hrs) + (drone_standby_daily * cloud_window_days)

leg_gis_event = (gis_staff_count * gis_hourly_rate * gis_processing_hrs)

# Personnel = (Team Burn * Days spent blind) + (Cost of failed deployments)
leg_personnel_event = (team_count * team_daily_burn * cloud_window_days) + (dry_runs_prevented * dry_run_penalty)

# Logistics = Total hours highways are closed while waiting for visual truth
leg_logistics_event = (hwy_loss_hr * hwy_count * leg_wait_hrs)

# --- ICEYE CALCULATIONS (PER EVENT) ---
# ICEYE eliminates aviation and manual mapping. 
# Personnel only wait for the SAR latency period.
iceye_personnel_event = (team_count * team_daily_burn * (sar_latency / 24.0))
iceye_logistics_event = (hwy_loss_hr * hwy_count * sar_latency)

# --- ANNUAL SCALING ---
annual_legacy_total = (leg_aviation_event + leg_gis_event + leg_personnel_event + leg_logistics_event) * events_pa
annual_iceye_total = ((iceye_personnel_event + iceye_logistics_event) * events_pa) + annual_sub

net_annual_profit = annual_legacy_total - annual_iceye_total

# 6. RESULTS - Standard Metrics
st.divider()
st.subheader("3. Annualized Strategic Financial Impact")
r1, r2, r3 = st.columns(3)
r1.metric("Net Annual Recovery (ROI)", f"${net_annual_profit:,.2f}")
r2.metric("Total Annual Hours Gained", f"{time_recovered_per_event * events_pa:.1f} hrs")
r3.metric("Annual Legacy Waste Offset", f"${annual_legacy_total:,.2f}")

# 7. VISUAL CHART
st.markdown("### 📊 Annual Cost Distribution")
chart_data = {
    "Category": ["Aviation & Recon", "GIS Analysis", "Field Personnel", "Logistics & Freight", "Solution Investment"],
    "Legacy Model ($)": [
        leg_aviation_event * events_pa,
        leg_gis_event * events_pa,
        leg_personnel_event * events_pa,
        leg_logistics_event * events_pa,
        0.0
    ],
    "ICEYE Model ($)": [
        0.0, 
        0.0, 
        iceye_personnel_event * events_pa,
        iceye_logistics_event * events_pa,
        annual_sub
    ]
}
df_chart = pd.DataFrame(chart_data).set_index("Category")
st.bar_chart(df_chart, height=450)

# 8. THE TAKEAWAYS
st.divider()
st.subheader("4. Final Business Case Findings")

st.write(f"**Aviation Standby Waste:** By relying on visual assets (Heli/Drone), you are paying **${(heli_standby_daily + drone_standby_daily) * cloud_window_days * events_pa:,.2f}** annually just to have crews wait for weather to clear. ICEYE provides a deterministic feed that removes this standby cost entirely.")

st.write(f"**Actionable Lead Time:** SAR bypasses the **{cloud_window_days} day** cloud window and **{gis_processing_hrs} hour** mapping delay, delivering truth in **{sar_latency} hours**. This recovers **{time_recovered_per_event * events_pa:.1f} hours** of operational time annually across **{events_pa:.0f} events**.")

st.write(f"**Economic Recovery:** The ability to verify highway status through clouds recovers **${(leg_logistics_event - iceye_logistics_event) * events_pa:,.2f}** in annual freight productivity that would otherwise be lost to precautionary closures.")
