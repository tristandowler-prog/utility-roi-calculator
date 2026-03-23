import streamlit as st
import pandas as pd

# 1. SETUP - No custom CSS. No HTML. Standard Streamlit only for 100% visibility.
st.set_page_config(page_title="ICEYE ROI Master Audit", layout="wide")

st.title("ICEYE Flood Solutions: Operational ROI Ledger")
st.write("A verified financial model scaling per-event operational costs against a fixed ICEYE subscription.")

# 2. SYSTEM PARAMETERS
st.subheader("1. Global Constants")
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, format="%.2f")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0, step=0.5)

st.divider()

# 3. PER-EVENT INPUTS (The Manual Overrides)
st.subheader("2. Per-Event Operational Costs")
c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 🚁 Aviation & Drone")
    # Heli
    heli_rate = st.number_input("Heli Flight Rate ($/hr)", value=3500.00, format="%.2f")
    heli_hrs = st.number_input("Heli Flight Hrs / Event", value=20.0)
    heli_standby = st.number_input("Heli Daily Standby ($)", value=1500.00, format="%.2f")
    # Drone
    drone_rate = st.number_input("Drone Flight Rate ($/hr)", value=250.00, format="%.2f")
    drone_hrs = st.number_input("Drone Flight Hrs / Event", value=15.0)
    drone_standby = st.number_input("Drone Daily Standby ($)", value=1200.00, format="%.2f")
    # Weather Gap
    cloud_wait_days = st.number_input("Cloud / Visual Blind Window (Days)", value=2.0)

with c2:
    st.write("### 🚛 Field Personnel")
    team_count = st.number_input("Active Strike Teams", value=6.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, format="%.2f")
    dry_run_penalty = st.number_input("Dry Run Penalty ($/trip)", value=2800.00, format="%.2f")
    dry_runs_per_event = st.number_input("Wasted Trips (Dry Runs) / Event", value=10.0)

with c3:
    st.write("### 🖥️ GIS & Infrastructure")
    # GIS STAFFING - RESTORED AND VERIFIED
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0)
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, format="%.2f")
    gis_hrs_per_event = st.number_input("Manual Mapping Time (Hrs) / Event", value=8.0)
    # LOGISTICS
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000.00, format="%.2f")
    hwy_count = st.number_input("Impacted Major Highways", value=2.0)

# 4. MATH ENGINE (SCALING LINEARLY)

# --- LEGACY CALCULATIONS (PER EVENT) ---
# Aviation = Flight time + Standby while waiting for clouds
leg_aviation_event = (heli_rate * heli_hrs) + (heli_standby * cloud_wait_days) + \
                     (drone_rate * drone_hrs) + (drone_standby * cloud_wait_days)

# GIS = Staff x Rate x Hours
leg_gis_event = (gis_staff_count * gis_hourly_rate * gis_hrs_per_event)

# Personnel = (Team Burn * Days spent blind) + (Cost of Dry Runs)
leg_personnel_event = (team_count * team_daily_burn * cloud_wait_days) + (dry_runs_per_event * dry_run_penalty)

# Logistics = Highway Loss * Count * (Cloud Days + Mapping Time)
leg_wait_total_hrs = (cloud_wait_days * 24.0) + gis_hrs_per_event
leg_logistics_event = (hwy_loss_hr * hwy_count * leg_wait_total_hrs)

# --- ICEYE CALCULATIONS (PER EVENT) ---
# ICEYE replaces aviation recon and manual mapping.
# Personnel and Logistics only wait for the SAR latency (e.g. 6 hrs).
iceye_personnel_event = (team_count * team_daily_burn * (sar_latency / 24.0))
iceye_logistics_event = (hwy_loss_hr * hwy_count * sar_latency)

# --- ANNUAL TOTALS ---
total_annual_legacy = (leg_aviation_event + leg_gis_event + leg_personnel_event + leg_logistics_event) * events_pa
total_annual_iceye = ((iceye_personnel_event + iceye_logistics_event) * events_pa) + annual_sub
net_annual_roi = total_annual_legacy - total_annual_iceye

# 5. RESULTS DISPLAY
st.divider()
st.subheader("3. Strategic Impact (Annualized)")
r1, r2, r3 = st.columns(3)
r1.metric("Net Annual Recovery (ROI)", f"${net_annual_roi:,.2f}")
r2.metric("Annual GIS Costs Removed", f"${leg_gis_event * events_pa:,.2f}")
r3.metric("Annual Legacy Spend", f"${total_annual_legacy:,.2f}")

# 6. VISUAL CHART
st.markdown("### 📊 Annual Cost Distribution")
chart_data = {
    "Category": ["Aviation Recon", "GIS Analysis", "Field Personnel", "Logistics & Freight", "ICEYE Sub"],
    "Legacy Model ($)": [
        leg_aviation_event * events_pa,
        leg_gis_event * events_pa,
        leg_personnel_event * events_pa,
        leg_logistics_event * events_pa,
        0.0
    ],
    "ICEYE Model ($)": [
        0.0, 0.0, 
        iceye_personnel_event * events_pa,
        iceye_logistics_event * events_pa,
        annual_sub
    ]
}
df_chart = pd.DataFrame(chart_data).set_index("Category")
st.bar_chart(df_chart, height=450)

# 7. BUSINESS CASE FINDINGS
st.divider()
st.subheader("4. Key Takeaways")
st.write(f"**GIS Efficiency:** Manual processing by **{gis_staff_count:.0f} staff** currently consumes **{gis_hrs_per_event * events_pa:.1f} hours** of labor annually. ICEYE provides analysis-ready data, bypassing this manual bottleneck.")
st.write(f"**Aviation Waste:** You are paying **${(heli_standby + drone_standby) * cloud_wait_days * events_pa:,.2f}** per year in 'Weather Standby' fees for visual assets that cannot see through clouds.")
st.write(f"**Time Advantage:** SAR intelligence recovers **{leg_wait_total_hrs - sar_latency:.1f} hours** of operational lead time per flood event.")
