import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE SAR ROI", layout="wide")

st.title("🛰️ ICEYE SAR: Infrastructure Impact ROI")
st.markdown("### *GIS Overlay Logic: Replacing 'Manual Search' with 'Observed Truth'*")
st.divider()

# --- SIDEBAR: OPERATIONAL COSTS ---
with st.sidebar:
    st.header("💰 1. ICEYE Investment")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events / Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Field Force Burn Rate")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    st.header("🚁 3. Legacy Recon (Avoided Cost)")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_team_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- SYSTEM MATH ---
num_vehicles = total_people / 2.5
hourly_burn = (total_people * person_hr) + (num_vehicles * vehicle_hr)

# --- SCENARIO INPUTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy: Manual Verification")
    t_wait = st.number_input("Access Delay (Hrs)", value=48, help="Waiting for water to recede to allow safe aerial or ground recon.")
    t_assets = st.number_input("Total Assets in Storm Area", value=2000, help="Total infrastructure that must be 'cleared' manually.")
    t_helo_hrs = st.number_input("Helo Flight Hours (Patrol)", value=15)
    t_drone_days = st.number_input("Drone Team Days", value=12)

with col_right:
    st.subheader("🔵 ICEYE: GIS-Directed Response")
    s_wait = st.number_input("Time to ICEYE Layer (Hrs)", value=8, help="Typical delivery time for SAR flood extent/depth layers.")
    # The outcome of the GIS Overlay
    s_assets_wet = st.number_input("Assets Impacted by Flood Layer", value=140, help="Specific assets where ICEYE depth data > 0.")
    st.info(f"💡 **The GIS Filter:** The overlay instantly 'clears' **{int(t_assets - s_assets_wet)}** assets. No truck roll or flight required.")

# --- THE MATH ---
# Legacy: Costs of finding and clearing 2000 assets
t_standby = hourly_burn * t_wait
t_aerial = (t_helo_hrs * helo_hr) + (t_drone_days * drone_team_day)
t_inspect = t_assets * 350  # Average cost of a 'search-and-clear' site visit
t_total_event = t_standby + t_aerial + t_inspect

# ICEYE: Costs of a targeted response
s_standby = hourly_burn * s_wait
s_inspect = s_assets_wet * 350 # Targeted visits ONLY to confirmed wet assets
s_total_event = s_standby + s_inspect # NO HELO/DRONE COST

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

# 1. Operational cost per event (Direct spend)
m1.metric("Legacy Spend / Event", f"${t_total_event:,.0f}")
m2.metric("ICEYE Spend / Event", f"${s_total_event:,.0f}", 
          delta=f"-${t_total_event - s_total_event:,.0f}", delta_color="inverse")

# 2. Total Annual Position
savings_per_event = t_total_event - s_total_event
annual_net = (savings_per_event * events_per_year) - annual_sub
m3.metric("Net Annual Position", f"${annual_net:,.0f}", help="Sum of event savings minus the subscription fee.")

# --- COMPARISON TABLE ---
st.subheader("Workforce Efficiency (Per Event)")
data = {
    "Category": ["Standby (Information Gap)", "Aerial Search (Helo/Drone)", "Physical Site Verification"],
    "Legacy Method ($)": [f"${t_standby:,.0f}", f"${t_aerial:,.0f}", f"${t_inspect:,.0f}"],
    "ICEYE GIS Method ($)": [f"${s_standby:,.0f}", "$0 (Replaced by Data)", f"${s_inspect:,.0f}"]
}
st.table(pd.DataFrame(data))

st.success(f"**Hard Saving:** The ICEYE layer prevents **{int(t_assets - s_assets_wet)}** unnecessary site visits and eliminates **${t_aerial:,.0f}** in search flights.")
