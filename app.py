import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE Utility ROI", layout="wide")

st.title("🛰️ ICEYE SAR: Infrastructure Impact ROI")
st.markdown("### *Replicating Manual Spreadsheet Logic: Fixed Subscription vs. Variable Operational Spend*")
st.divider()

# --- SIDEBAR: SPREADSHEET INPUTS ---
with st.sidebar:
    st.header("💰 1. Fixed Subscription")
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Workforce Rates")
    total_people = st.number_input("Total Field Personnel", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    # Pre-calculating the hourly burn of the entire fleet
    num_vehicles = total_people / 2.5
    hourly_burn = (total_people * person_hr) + (num_vehicles * vehicle_hr)
    
    st.header("🚁 3. Avoided Search Costs")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_day_rate = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE SPREADSHEET MATH ---
# Data share: 150k / 2 = 75k. 150k / 5 = 30k.
data_share_per_event = annual_sub / events_per_year

# --- SCENARIO COMPARISON ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy: Manual Search & Verify")
    t_wait = st.number_input("Wait for Visual/Aerial Access (Hrs)", value=48)
    t_assets = st.number_input("Total Assets in Storm Zone", value=2000)
    t_helo_hrs = st.number_input("Helo Patrol Hours", value=15)
    t_drone_days = st.number_input("Drone Search Days", value=12)

with col_right:
    st.subheader("🔵 ICEYE: GIS-Directed Response")
    s_wait = st.number_input("Time to ICEYE GIS Layer (Hrs)", value=8)
    # The 'Filter' result
    s_assets_wet = st.number_input("GIS-Confirmed Submerged Assets", value=140)
    st.info(f"💡 **Data Cost:** At {events_per_year} events, data is **${data_share_per_event:,.0f}** per event.")

# --- CALCULATION BLOCK (MANUAL TRACE) ---

# Legacy Event Costs
t_standby = hourly_burn * t_wait
t_aerial_recon = (t_helo_hrs * helo_hr) + (t_drone_days * drone_day_rate)
t_physical_inspections = t_assets * 350 # Cost of checking every asset manually
t_total_event = t_standby + t_aerial_recon + t_physical_inspections

# SAR Event Costs
s_standby = hourly_burn * s_wait
s_aerial_recon = 0 # REPLACED BY SAR DATA
s_physical_inspections = s_assets_wet * 350 # ONLY visiting wet assets
s_total_event = s_standby + s_physical_inspections + data_share_per_event

# --- DASHBOARD METRICS ---
st.divider()
m1, m2, m3 = st.columns(3)

# Formatting for metrics
leg_str = f"${t_total_event:,.0f}"
sar_str = f"${s_total_event:,.0f}"
diff_str = f"-${t_total_event - s_total_event:,.0f}"
annual_benefit = (t_total_event - s_total_event) * events_per_year
annual_str = f"${annual_benefit:,.0f}"

m1.metric("Legacy Cost / Event", leg_str)
m2.metric("True SAR Cost / Event", sar_str, delta=diff_str, delta_color="inverse")
m3.metric("Net Annual Position", annual_str, help="Total annual savings minus the sub.")

# --- THE BREAKDOWN TABLE ---
st.subheader("Detailed Cost Comparison (Per Event)")

comparison_df = pd.DataFrame({
    "Category": ["Field Standby (Wait Time Labor)", "Aerial Recon (Helo/Drones)", "Manual Site Inspections", "Satellite Data (Sub Share)"],
    "Legacy Method ($)": [
        f"${t_standby:,.0f}", 
        f"${t_aerial_recon:,.0f}", 
        f"${t_physical_inspections:,.0f}", 
        "$0"
    ],
    "ICEYE GIS Method ($)": [
        f"${s_standby:,.0f}", 
        "$0 (Replaced)", 
        f"${s_physical_inspections:,.0f}", 
        f"${data_share_per_event:,.0f}"
    ]
})
st.table(comparison_df)

# --- THE CHART ---
st.subheader("Operational Spend Analysis")
chart_data = pd.DataFrame({
    "Category": ["Standby", "Recon", "Inspections", "Data Cost"],
    "Legacy": [t_standby, t_aerial_recon, t_physical_inspections, 0],
    "ICEYE": [s_standby, 0, s_physical_inspections, data_share_per_event]
})
st.bar_chart(chart_data.set_index("Category"))

# --- STRATEGIC OUTPUTS ---
st.divider()
st.subheader("🎯 Value Realization")
c1, c2 = st.columns(2)

assets_cleared = int(t_assets - s_assets_wet)
labor_waste_saved = f"${(t_assets - s_assets_wet) * 350:,.0f}"

c1.write(f"✅ **Remote Clearance:** {assets_cleared} assets cleared via GIS overlay without a truck roll.")
c2.write(f"🛑 **Waste Eliminated:** {labor_waste_saved} in unnecessary field inspections per event.")

st.success(f"**Total Restoration Head-Start:** Repairs can begin **{int(t_wait - s_wait)} hours** earlier compared to legacy methods.")
