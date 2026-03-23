import streamlit as st
import pandas as pd

# 1. SETUP - Standard configuration for total visibility and reliability.
st.set_page_config(page_title="ICEYE ROI Final Audit", layout="wide")

# 2. HEADER
st.title("ICEYE Flood Solutions: Operational ROI Audit")
st.write("A deterministic financial model comparing SAR persistence against legacy visual reconnaissance.")

# 3. GLOBAL CONTROLS (Top Row)
st.subheader("1. System Parameters")
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, step=1000.00, format="%.2f")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0, step=0.5)

st.divider()

# 4. DETAILED INPUTS (Per Event Manual Overrides)
st.subheader("2. Per-Event Operational Inputs (Manual Overrides)")
st.info("Structure your legacy costs for a SINGLE event below. The tool will scale these by the 'Events Per Year' selected above.")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 🚁 Aviation & Drone Recon")
    heli_rate = st.number_input("Heli Charter ($/hr)", value=3500.00, step=50.00, format="%.2f")
    heli_hrs = st.number_input("Heli Flight Hrs / Event", value=20.0, step=1.0)
    
    st.write("---")
    drone_rate = st.number_input("Drone Team Hourly Rate ($/hr)", value=250.00, step=10.00, format="%.2f")
    drone_hrs = st.number_input("Drone Flight Hrs / Event", value=15.0, step=1.0)
    drone_standby = st.number_input("Drone Team Daily Standby ($)", value=1200.00, step=50.00, format="%.2f")
    cloud_window_days = st.number_input("Cloud/Visual Wait Window (Days)", value=2.0, step=0.25)

with c2:
    st.write("### 🚛 Field Personnel (Strike Teams)")
    team_count = st.number_input("Active Strike Teams", value=6.0, step=1.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, step=100.00, format="%.2f")
    dry_run_penalty = st.number_input("Dry Run Penalty ($ per trip)", value=2800.00, step=50.00, format="%.2f")
    dry_runs_prevented = st.number_input("Dry Runs Prevented per Event", value=10.0, step=1.0)

with c3:
    st.write("### 🖥️ GIS & Infrastructure")
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, step=5.00, format="%.2f")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0, step=1.0)
    gis_processing_hrs = st.number_input("Manual Mapping Time (Hrs)", value=8.0, step=0.5)
    
    st.write("---")
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000.00, step=500.00, format="%.2f")
    hwy_count = st.number_input("Impacted Major Highways", value=2.0, step=1.0)

# 5. MATH ENGINE (SCALING LOGIC)
# Time Gap Analysis
leg_wait_hrs = (cloud_window_days * 24.0) + gis_processing_hrs
time_recovered_hrs = leg_wait_hrs - sar_latency

# --- LEGACY CALCULATIONS (PER EVENT) ---
# Aviation = (Heli Flight) + (Drone Flight) + (Drone Standby during Cloud Window)
leg_aviation_event = (heli_rate * heli_hrs) + (drone_rate * drone_hrs) + (drone_standby * cloud_window_days)
leg_gis_event = (gis_staff_count * gis_hourly_rate * gis_processing_hrs)
# Personnel = (Team Burn * Days of Blindness) + (Cost of Dry Runs)
leg_personnel_event = (team_count * team_daily_burn * cloud_window_days) + (dry_runs_prevented * dry_run_penalty)
# Logistics = Economic loss for total wait time
leg_logistics_event = (hwy_loss_hr * hwy_count * leg_wait_hrs)

# --- ICEYE CALCULATIONS (PER EVENT) ---
# ICEYE eliminates Aviation and GIS labor. 
# Personnel only idle for the SAR delivery period.
iceye_personnel_event = (team_count * team_daily_burn * (sar_latency / 24.0))
iceye_logistics_event = (hwy_loss_hr * hwy_count * sar_latency)

# --- ANNUAL AGGREGATES ---
annual_legacy_total = (leg_aviation_event + leg_gis_event + leg_personnel_event + leg_logistics_event) * events_pa
annual_iceye_total = ((iceye_personnel_event + iceye_logistics_event) * events_pa) + annual_sub

net_annual_profit = annual_legacy_total - annual_iceye_total

# 6. RESULTS - Standard Metrics
st.divider()
st.subheader("3. Annualized Strategic Financial Impact")
r1, r2, r3 = st.columns(3)
r1.metric("Net Annual Recovery (ROI)", f"${net_annual_profit:,.2f}")
r2.metric("Total Annual Hours Gained", f"{time_recovered_hrs * events_pa:.1f} hrs")
r3.metric("Annual Legacy Waste Offset", f"${annual_legacy_total:,.2f}")

# 7. VISUAL COMPARISON
chart_data = {
    "Expense Category": ["Aviation & Recon", "GIS Analysis", "Field Personnel", "Logistics & Freight", "Solution Investment"],
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
df_chart = pd.DataFrame(chart_data).set_index("Expense Category")
st.bar_chart(df_chart, height=450)

# 8. BUSINESS CASE FINDINGS
st.divider()
st.subheader("4. Technical Audit Notes")

st.write(f"**Aviation Efficiency:** Traditional methods require **${leg_aviation_event:,.2f}** per event in flights and standby crews. ICEYE SAR replaces this with a fixed subscription, providing data regardless of cloud ceiling or drone battery limitations.")

st.write(f"**The 'Visual Information Gap':** By reducing the time-to-intel by **{time_recovered_hrs:.1f} hours** per event, you recover **${(leg_logistics_event - iceye_logistics_event) * events_pa:,.2f}** in annual freight productivity for the region.")

st.write(f"**Operational Scalability:** With an annual investment of **${annual_sub:,.2f}**, the cost per event is effectively fixed. As disaster frequency increases to **{events_pa:.0f} events**, your cost avoidance scales to **${net_annual_profit:,.2f}**.")
