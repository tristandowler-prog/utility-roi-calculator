import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE SAR ROI", layout="wide")

st.title("🛰️ ICEYE SAR: Strategic ROI Engine")
st.markdown("### *Observed Flood Data vs. Manual Infrastructure Verification*")
st.divider()

# --- SIDEBAR: COSTS ---
with st.sidebar:
    st.header("💰 1. ICEYE Investment")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events / Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Workforce Burn Rate")
    total_people = st.number_input("Total Personnel", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    st.header("🚁 3. Legacy Search Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- SYSTEM MATH ---
num_vehicles = total_people / 2.5
hourly_burn = (total_people * person_hr) + (num_vehicles * vehicle_hr)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy: Search & Rescue")
    t_wait = st.number_input("Wait for Visual Access (Hrs)", value=48)
    t_assets = st.number_input("Total Assets in Zone", value=2000)
    t_helo = st.number_input("Helicopter Patrol Hours", value=15)
    t_drone = st.number_input("Drone Team Days", value=12)

with col_right:
    st.subheader("🔵 ICEYE: Observed Truth")
    s_wait = st.number_input("Time to Data Layer (Hrs)", value=8)
    # The result of the GIS Overlay
    s_assets_wet = st.number_input("GIS-Confirmed Wet Assets", value=140)
    st.info("💡 **SAR Logic:** ICEYE data replaces all search flights. You only visit confirmed wet assets.")

# --- THE CORRECT MATH ---
# 1. Legacy Costs (Everything is expensive because you don't know where the water is)
t_standby = hourly_burn * t_wait
t_recon = (t_helo * helo_hr) + (t_drone * drone_day)
t_inspect = t_assets * 350 # Visiting every asset to check status
t_total_event = t_standby + t_recon + t_inspect

# 2. SAR Costs (The Data Layer is the recon)
s_standby = hourly_burn * s_wait
s_recon = 0 # THIS IS THE KEY: ICEYE IS THE RECON
s_inspect = s_assets_wet * 350 # ONLY visiting what the GIS overlay shows as wet
s_total_event = s_standby + s_inspect

# --- RESULTS DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

# The "Cost per Event" now refers ONLY to the operational spend (Labor/Fleet/Flights)
m1.metric("Legacy Spend / Event", f"${t_total_event:,.0f}")
m2.metric("SAR Spend / Event", f"${s_total_event:,.0f}", 
          delta=f"-${t_total_event - s_total_event:,.0f}", delta_color="inverse")

# Total ROI including the subscription
annual_savings = (t_total_event - s_total_event) * events_per_year
final_position = annual_savings - annual_sub
m3.metric("Net Annual Position", f"${final_position:,.0f}", help="Total savings minus the 150k sub.")

# --- THE BREAKDOWN TABLE ---
st.subheader("Direct Cost Comparison (Per Event)")
data = {
    "Expense Category": ["Field Force Standby", "Reconnaissance (Helo/Drone)", "Physical Site Inspections"],
    "Legacy (No SAR)": [f"${t_standby:,.0f}", f"${t_recon:,.0f}", f"${t_inspect:,.0f}"],
    "ICEYE (With SAR)": [f"${s_standby:,.0f}", "$0 (Replaced by Data)", f"${s_inspect:,.0f}"]
}
st.table(pd.DataFrame(data))

st.success(f"**The Value:** The ICEYE overlay clears **{int(t_assets - s_assets_wet)}** assets remotely. You save **${t_total_event - s_total_event:,.0f}** in operational waste per event.")
