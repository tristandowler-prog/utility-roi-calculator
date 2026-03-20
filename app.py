import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE SAR ROI", layout="wide")

st.title("🛰️ ICEYE SAR: Operational ROI Engine")
st.markdown("### *Logic: Data as a Workforce Multiplier*")
st.divider()

# --- SIDEBAR: FIXED COSTS ---
with st.sidebar:
    st.header("💰 1. Annual Investment")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events / Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Workforce Burn Rate")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    st.header("🚁 3. Legacy Search Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE "FIXED" ACCOUNTING LOGIC ---
# The subscription is a fixed cost shared by the number of events
data_cost_per_event = annual_sub / events_per_year

num_vehicles = total_people / 2.5
hourly_burn = (total_people * person_hr) + (num_vehicles * vehicle_hr)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy: Search & Rescue")
    t_wait = st.number_input("Wait for Visual/Aerial Access (Hrs)", value=48)
    t_assets = st.number_input("Total Assets to Clear Manually", value=2000)
    t_helo = st.number_input("Helo Patrol Hours", value=15)
    t_drone = st.number_input("Drone Team Days", value=12)

with col_right:
    st.subheader("🔵 ICEYE: Observed Truth")
    s_wait = st.number_input("Time to ICEYE Layer (Hrs)", value=8)
    # This is the result of the GIS overlay
    s_assets_wet = st.number_input("GIS-Confirmed Wet Assets", value=140)
    st.info(f"💡 **Utilization Effect:** At {events_per_year} events/year, the SAR data cost is **${data_cost_per_event:,.0f}** per event.")

# --- THE CALCULATIONS ---

# 1. LEGACY (The high-uncertainty way)
t_standby = hourly_burn * t_wait
t_recon = (t_helo * helo_hr) + (t_drone * drone_day)
t_inspect = t_assets * 350 # Cost to visit EVERY asset to verify status
t_total_event = t_standby + t_recon + t_inspect

# 2. SAR (The directed way)
s_standby = hourly_burn * s_wait
s_recon = 0 # REPLACED BY SAR DATA
s_inspect = s_assets_wet * 350 # ONLY visiting the CONFIRMED wet assets
# SAR Total = Ops + the slice of the subscription
s_total_event = s_standby + s_inspect + data_cost_per_event

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

# Legacy Spend
m1.metric("Legacy Cost / Event", f"${t_total_event:,.0f}")

# SAR Spend (This will now properly decrease as events increase)
m2.metric("True SAR Cost / Event", f"${s_total_event:,.0f}", 
          delta=f"-${t_total_event - s_total_event:,.0f}", delta_color="inverse")

# Net Annual Position (Savings * Events - Sub)
# Which is mathematically the same as (Legacy_Event - SAR_Event) * Events
annual_net = (t_total_event - s_total_event) * events_per_year
m3.metric("Net Annual Position", f"${annual_net:,.0f}", help="Total yearly savings minus the flat 150k sub.")

# --- THE BREAKDOWN TABLE ---
st.subheader("Cost Breakdown (Per Event)")
data = {
    "Category": ["Personnel Standby (Wait Time)", "Aerial Recon (Helo/Drone)", "Physical Site Inspections", "Satellite Data (Subscription Share)"],
    "Legacy Method ($)": [f"${t_standby:,.0f}", f"${t_recon:,.0f}", f"${t_inspect:,.0f}", "$0"],
    "ICEYE Method ($)": [f"${s_standby:,.0f}", "$0 (Replaced)", f"${s_inspect:,.0f}", f"${data_cost_per_event:,.0f}"]
}
st.table(pd.DataFrame(data))

# --- COMPARISON CHART ---

st.subheader("Operational Spend Analysis")
chart_df = pd.DataFrame({
    "Category": ["Standby", "Recon", "Inspections", "Data Cost"],
    "Legacy": [t_standby, t_recon, t_inspect, 0],
    "ICEYE": [s_standby, 0, s_inspect, data_cost_per_event]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**Strategy:** By overlaying the ICEYE flood layer, you remotely clear **{int(t_assets - s_assets_wet)}** assets. This eliminates the need for **${t_recon:,.0f}** in search flights and **${t_inspect - s_inspect:,.0f}** in manual site verification.")
