import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE Utility ROI", layout="wide")

st.title("🛰️ ICEYE SAR: The 'Universal Truth' ROI Engine")
st.markdown("### *Compare Manual 'Search & Rescue' vs. Satellite-Directed Recovery*")
st.divider()

# --- SIDEBAR: UNIT COSTS ---
with st.sidebar:
    st.header("💰 1. Annual SAR Investment")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events / Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Field Force Costs")
    total_people = st.number_input("Total Personnel", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    st.header("🚁 3. Legacy Recon Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_team_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- SYSTEM LOGIC ---
num_vehicles = total_people / 2.5
hourly_burn = (total_people * person_hr) + (num_vehicles * vehicle_hr)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy 'Search' Method")
    t_wait = st.number_input("Wait Time for Air/Roads (Hrs)", value=48, help="Waiting for clouds to clear or roads to open.")
    t_assets = st.number_input("Assets to Inspect Manually", value=2000, help="Total poles/transformers in the flood zone.")
    t_helo_hrs = st.number_input("Helicopter Search Hours", value=15)
    t_drone_days = st.number_input("Drone Search Days", value=12)

with col_right:
    st.subheader("🔵 ICEYE 'Directed' Method")
    s_wait = st.number_input("Time to SAR Flood Map (Hrs)", value=8, help="ICEYE delivery window.")
    # We assume only ~7% of assets actually require a truck roll based on depth data
    s_hit_rate = st.slider("% of Assets Impacted (via SAR)", 1, 20, 7)
    s_assets = (t_assets * s_hit_rate) / 100
    st.info(f"💡 **SAR Logic:** ICEYE depth data identifies only **{int(s_assets)}** assets as flooded. The other **{int(t_assets - s_assets)}** are cleared remotely.")

# --- THE MATH ---
# Legacy (The expensive way)
t_standby = hourly_burn * t_wait
t_aerial = (t_helo_hrs * helo_hr) + (t_drone_days * drone_team_day)
t_inspect = t_assets * 350 # Standard cost for a manual physical check
t_total_event = t_standby + t_aerial + t_inspect

# SAR (The directed way)
s_standby = hourly_burn * s_wait
s_aerial = 0 # REPLACED BY SAR
s_inspect = s_assets * 350 # Only visiting the 'Hit List' from ICEYE
s_total_event = s_standby + s_inspect

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

# 1. Cost per event (Operational only)
m1.metric("Legacy Ops / Event", f"${t_total_event:,.0f}")
m2.metric("SAR Ops / Event", f"${s_total_event:,.0f}", delta=f"-${t_total_event - s_total_event:,.0f}", delta_color="inverse")

# 2. Total Annual Position (Savings * Events - Sub)
annual_savings = (t_total_event - s_total_event) * events_per_year
net_roi = annual_savings - annual_sub
m3.metric("Net Annual Position", f"${net_roi:,.0f}", help="Total savings across all events minus the sub cost.")

# --- COMPARISON TABLE ---
st.subheader("Operational Impact (Per Event)")
data = {
    "Expense": ["Field Standby (Wait Time)", "Aerial Recon (Helo/Drone)", "Truck Rolls (Site Visits)"],
    "Legacy Method": [f"${t_standby:,.0f}", f"${t_aerial:,.0f}", f"${t_inspect:,.0f}"],
    "ICEYE Method": [f"${s_standby:,.0f}", "$0 (Replaced)", f"${s_inspect:,.0f}"]
}
st.table(pd.DataFrame(data))

st.success(f"**Strategy:** By using ICEYE to clear **{int(t_assets - s_assets)}** assets without sending a truck, you save **${t_inspect - s_inspect:,.0f}** in field labor alone per event.")
