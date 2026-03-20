import streamlit as st
import pandas as pd

st.set_page_config(page_title="Utility Aerial ROI", layout="wide")

st.title("🛰️ Satellite vs. Aerial Recon: Utility ROI Engine")
st.markdown("### *Optimizing the Discovery Phase of Flood Recovery*")
st.divider()

# --- SIDEBAR: GLOBAL UNIT COSTS ---
with st.sidebar:
    st.header("👥 1. Field Force & Fleet")
    total_people = st.number_input("Total Personnel Dispatched", value=100)
    person_hr = st.number_input("Labor Rate ($/hr/person)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr/vehicle)", value=60)
    
    st.divider()
    st.header("🏢 2. Subscription & Scale")
    annual_sub = st.number_input("Annual Satellite Sub ($)", value=150000)
    events_per_year = st.slider("Major Flood Events / Year", 1, 5, 2)
    
    st.header("🚁 3. Aerial Unit Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_team_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- SCENARIO INPUTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Current Recon Method")
    recon_method = st.selectbox("Primary Discovery Tool", ["Helicopter", "Drone Fleet", "Hybrid (Both)"])
    
    t_wait = st.number_input("Wait for Weather/Road Access (Hrs)", value=48)
    t_assets = st.number_input("Total Assets to Inspect", value=1500)
    
    # Dynamic inputs based on selection
    t_helo_hrs = 0
    t_drone_days = 0
    if recon_method in ["Helicopter", "Hybrid (Both)"]:
        t_helo_hrs = st.number_input("Manual Helicopter Hours", value=15)
    if recon_method in ["Drone Fleet", "Hybrid (Both)"]:
        t_drone_days = st.number_input("Manual Drone Team Days", value=12)

with col_right:
    st.subheader("🔵 Satellite-Led Strategy")
    st.write("**Method:** SAR Triage → Targeted Deployment")
    s_wait = st.number_input("Wait for Satellite Map (Hrs)", value=8)
    s_assets_verified = st.number_input("Verified Damage Sites", value=125)
    
    # Targeted aerial is significantly lower
    s_helo_hrs = st.number_input("Targeted Helo Hours (SAR Verified)", value=2)
    s_drone_days = st.number_input("Targeted Drone Days (SAR Verified)", value=2)

# --- CALCULATION LOGIC ---
def calc_event_costs(wait, assets, helo, drone):
    num_vehicles = total_people / 2.5
    standby = (total_people * person_hr + num_vehicles * vehicle_hr) * wait
    inspection = assets * 350 # Direct site visit cost
    aerial = (helo * helo_hr) + (drone * drone_team_day)
    return standby + inspection + aerial, standby, inspection, aerial

t_total, t_standby, t_inspect, t_aerial = calc_event_costs(t_wait, t_assets, t_helo_hrs, t_drone_days)
s_total, s_standby, s_inspect, s_aerial = calc_event_costs(s_wait, s_assets_verified, s_helo_hrs, s_drone_days)

# --- DASHBOARD ---
st.divider()
res1, res2, res3 = st.columns(3)
