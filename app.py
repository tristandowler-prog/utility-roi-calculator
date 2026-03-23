import streamlit as st
import pandas as pd

# 1. SETUP - Standard configuration for guaranteed visibility.
st.set_page_config(page_title="ICEYE Multi-Event ROI", layout="wide")

# 2. HEADER
st.title("ICEYE Flood Solutions: Multi-Event ROI Audit")
st.write("This tool models the scaling cost of flood response. Legacy costs are calculated **per event**, while ICEYE provides a fixed-cost efficiency anchor.")

# 3. GLOBAL CONTROLS (Top Row)
st.subheader("1. System Parameters")
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, step=1000.00, format="%.2f", help="Fixed annual cost regardless of event count.")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0, help="This scales all variable legacy and operational costs.")
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6.0, step=0.5, help="Deterministic delivery time per event.")

st.divider()

# 4. DETAILED INPUTS (Per Event Manual Overrides)
st.subheader("2. Per-Event Operational Inputs (Manual Overrides)")
st.info("Note: The values below represent the cost for a SINGLE event. They will be multiplied by the 'Events Per Year' in the final analysis.")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 🚁 Aviation & Recon (Per Event)")
    heli_rate = st.number_input("Heli Charter ($/hr)", value=3500.00, step=50.00, format="%.2f")
    heli_recon_hrs = st.number_input("Flight Hrs per Event", value=20.0, step=1.0)
    drone_daily = st.number_input("Drone Team Daily Rate ($)", value=2200.00, step=50.00, format="%.2f")
    cloud_window_days = st.number_input("Cloud/Visual Wait Window (Days)", value=2.0, step=0.25)

with c2:
    st.write("### 🚛 Field Personnel (Per Event)")
    team_count = st.number_input("Active Strike Teams", value=6.0, step=1.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, step=100.00, format="%.2f")
    dry_run_penalty_cost = st.number_input("Dry Run Penalty ($ per trip)", value=2800.00, step=50.00, format="%.2f")
    dry_runs_prevented = st.number_input("Dry Runs Prevented per Event", value=10.0, step=1.0)

with c3:
    st.write("### 🖥️ GIS & Infrastructure (Per Event)")
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($)", value=120.00, step=5.00, format="%.2f")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0, step=1.0)
    gis_processing_hrs = st.number_input("Manual Mapping Time (Hrs)", value=8.0, step=0.5)
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000.00, step=500.00, format="%.2f")
    hwy_count = st.number_input("Impacted Major Highways", value=2.0, step=1.0)

# 5. MATH ENGINE (SCALING LOGIC)
# Time Analysis
leg_wait_hrs = (cloud_window_days * 24.0) + gis_processing_hrs
time_recovered_hrs = leg_wait_hrs - sar_latency

# --- LEGACY CALCULATIONS (PER EVENT) ---
leg_aviation_event = (heli_rate * heli_recon_hrs) + (drone_daily * cloud_window_days)
leg_gis_event = (gis_staff_count * gis_hourly_rate * gis_processing_hrs)
leg_personnel_event = (team_count * team_daily_burn * cloud_window_days) + (dry_runs_prevented * dry_run_penalty_cost)
leg_logistics_event = (hwy_loss_hr * hwy_count * leg_wait_hrs)

# --- ICEYE CALCULATIONS (PER EVENT) ---
iceye_personnel_event = (team_count * team_daily_burn * (sar_latency / 24.0))
iceye_logistics_event = (hwy_loss_hr * hwy_count * sar_latency)

# --- ANNUAL AGGREGATES (SCALING) ---
annual_legacy_cost = (leg_aviation_event + leg_gis_event + leg_personnel_event + leg_logistics_event) * events_pa
# ICEYE variable ops scale with events, but the subscription is FIXED
annual_iceye_variable_ops = (iceye_personnel_event + iceye_logistics_event) * events_pa
annual_iceye_total_cost = annual_iceye_variable_ops + annual_sub

net_annual_profit = annual_legacy_cost - annual_iceye_total_cost

# 6. RESULTS - Standard Metrics
st.divider()
st.subheader("3. Annualized Strategic Impact")
r1, r2, r3 = st.columns(3)
r1.metric("Net Annual Recovery", f"${net_annual_profit:,.2f}")
r2.metric("Total Annual Hours Saved", f"{time_recovered_hrs * events_pa:.1f} hrs")
r3.metric("Total Annual Legacy Waste", f"${annual_legacy_cost:,.2f}")

# 7. VISUAL COMPARISON
chart_data = {
    "Expense Category": ["Aviation & GIS", "Field Personnel", "Logistics & Freight", "Solution Investment"],
    "Legacy Model ($)": [
        (leg_aviation_event + leg_gis_event) * events_pa,
        leg_personnel_event * events_pa,
        leg_logistics_event * events_pa,
        0.0
    ],
    "ICEYE Model ($)": [
        0.0, # ICEYE eliminates recon and manual GIS labor
        iceye_personnel_event * events_pa,
        iceye_logistics_event * events_pa,
        annual_sub # Fixed subscription
    ]
}
df_chart = pd.DataFrame(chart_data).set_index("Expense Category")
st.bar_chart(df_chart, height=450)

# 8. BUSINESS CASE FINDINGS
st.divider()
st.subheader("4. Scalability Insights")

st.write(f"**The Power of Fixed Costs:** At **{events_pa:.0f} events per year**, your total legacy spend is **${annual_legacy_cost:,.2f}**. Because the ICEYE subscription is a fixed anchor, every additional flood event increases your ROI by **${(leg_aviation_event + leg_gis_event + (leg_personnel_event - iceye_personnel_event) + (leg_logistics_event - iceye_logistics_event)):,.2f}**.")

st.write(f"**Operational Efficiency:** By replacing variable reconnaissance costs with a persistent SAR feed, you are removing **${(leg_aviation_event + leg_gis_event) * events_pa:,.2f}** in direct annual OpEx waste.")
