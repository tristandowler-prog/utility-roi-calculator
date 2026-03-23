import streamlit as st
import pandas as pd

# 1. SETUP - Standard Streamlit components for 100% visibility & reliability.
st.set_page_config(page_title="ICEYE ROI: Operational Audit", layout="wide")

st.title("ICEYE Flood Solutions: Operational Efficiency Audit")
st.write("Quantitative analysis of Resource Recovery: Moving from 'Data Cleaning' to 'Active Response'.")

# 2. GLOBAL PARAMETERS (Annual Constants)
st.subheader("1. System Parameters")
col_sys1, col_sys2, col_sys3 = st.columns(3)
with col_sys1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, format="%.2f")
with col_sys2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_sys3:
    sar_latency = st.number_input("ICEYE Data Delivery Latency (Hrs)", value=6.0, step=0.5)

st.divider()

# 3. PER-EVENT OPERATIONAL LEDGER (Variable Costs)
st.subheader("2. Per-Event Operational Ledger (Manual Overrides)")
st.info("Define costs for a SINGLE event. The model scales these by the 'Events Per Year' selected above.")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 🚁 Aviation & Recon (Per Event)")
    heli_rate = st.number_input("Heli Flight Rate ($/hr)", value=3500.00, format="%.2f")
    heli_hrs = st.number_input("Heli Recon Flight Hrs", value=20.0)
    heli_standby = st.number_input("Heli Daily Standby Fee ($)", value=1500.00, format="%.2f")
    
    st.write("---")
    drone_rate = st.number_input("Drone Team Rate ($/hr)", value=250.00, format="%.2f")
    drone_hrs = st.number_input("Drone Recon Flight Hrs", value=15.0)
    drone_standby = st.number_input("Drone Daily Standby Fee ($)", value=1200.00, format="%.2f")

with c2:
    st.write("### 🚛 Field Strike Teams (Per Event)")
    team_count = st.number_input("Number of Active Teams", value=6.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, format="%.2f")
    # THE BLIND WINDOW: Days spent without a clear flood map due to clouds/night
    cloud_wait_days = st.number_input("Blind Window (Cloud/Night Days)", value=2.0)
    
    st.write("---")
    dry_run_penalty = st.number_input("Dry Run Penalty (Wasted Shift/Fuel) ($)", value=2800.00, format="%.2f")
    dry_runs_per_event = st.number_input("Wasted Deployments (Dry Runs) / Event", value=10.0)

with c3:
    st.write("### 🖥️ GIS Staff Utility (Per Event)")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0)
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, format="%.2f")
    
    st.write("---")
    st.write("**Legacy Mapping Workflow (Manual):**")
    leg_processing_hrs = st.number_input("Manual Mapping/Data Cleaning (Hrs)", value=12.0)
    
    st.write("**ICEYE Mapping Workflow (Automated):**")
    iceye_processing_hrs = st.number_input("SAR Layer Prep/QC (Hrs)", value=2.0)

# 4. THE MATH ENGINE (AUDITED LINE-BY-LINE)

# --- LEGACY CALCULATIONS (PER EVENT) ---
# Total Aviation = (Active Flight) + (Standby Fees * Blind Days)
leg_air_event = (heli_rate * heli_hrs) + (heli_standby * cloud_wait_days) + \
                (drone_rate * drone_hrs) + (drone_standby * cloud_wait_days)

# Total GIS Labor = Staff * Rate * Time spent cleaning/rectifying data
leg_gis_event = (gis_staff_count * gis_hourly_rate * leg_processing_hrs)

# Field Waste = (Total Team Burn * Days Blind) + (Cost of Dry Runs/Incorrect Deployments)
leg_field_waste_event = (team_count * team_daily_burn * cloud_wait_days) + (dry_runs_per_event * dry_run_penalty)

# --- ICEYE CALCULATIONS (PER EVENT) ---
# ICEYE eliminates Aviation/Drone recon (SAR replaces the photo-flight)
# GIS Labor is reduced to minimal prep time
iceye_gis_event = (gis_staff_count * gis_hourly_rate * iceye_processing_hrs)

# Field Waste is minimized because teams only wait for SAR delivery latency (e.g. 6 hrs)
# rather than the multi-day cloud window.
iceye_field_waste_event = (team_count * team_daily_burn * (sar_latency / 24.0))

# --- ANNUAL SCALING ---
annual_legacy_total = (leg_air_event + leg_gis_event + leg_field_waste_event) * events_pa
annual_iceye_total = ((iceye_gis_event + iceye_field_waste_event) * events_pa) + annual_sub

net_annual_recovery = annual_legacy_total - annual_iceye_total

# 5. RESULTS DISPLAY
st.divider()
st.subheader("3. Strategic Annual Impact")
r1, r2, r3 = st.columns(3)
r1.metric("Net Operational Recovery", f"${net_annual_recovery:,.2f}")
r2.metric("Annual GIS Time Recovered", f"{(leg_processing_hrs - iceye_processing_hrs) * events_pa:.1f} Hours")
r3.metric("Annual Aviation Offset", f"${leg_air_event * events_pa:,.2f}")

# 6. VISUAL CHART
st.markdown("### 📊 Annual Resource Cost Distribution")
chart_data = {
    "Category": ["Aviation Recon", "GIS Manual Labor", "Field Readiness Waste", "ICEYE Subscription"],
    "Legacy Model ($)": [leg_air_event*events_pa, leg_gis_event*events_pa, leg_field_waste_event*events_pa, 0],
    "ICEYE Model ($)": [0, iceye_gis_event*events_pa, iceye_field_waste_event*events_pa, annual_sub]
}
df_chart = pd.DataFrame(chart_data).set_index("Category")
st.bar_chart(df_chart, height=450)

# 7. AUDIT FINDINGS FOR THE EM
st.divider()
st.subheader("4. Operational Audit Findings")
st.write(f"**GIS Productivity:** Your GIS team currently spends **{leg_processing_hrs * events_pa:.1f} hours** per year on manual digitizing and cloud-clearing. ICEYE recovers **{(leg_processing_hrs - iceye_processing_hrs) * events_pa:.1f} hours** for high-value analysis.")
st.write(f"**Field Force Effectiveness:** By collapsing the **{cloud_wait_days} day** blind window to **{sar_latency} hours**, you avoid **${(leg_field_waste_event - iceye_field_waste_event) * events_pa:,.2f}** in annual labor waste caused by information delay.")
st.write(f"**Budget Certainty:** This model replaces weather-dependent variable costs with a deterministic SAR feed, providing flood truth through clouds and night.")
