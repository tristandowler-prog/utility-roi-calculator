import streamlit as st
import pandas as pd

st.set_page_config(page_title="Utility Flood ROI (Single Unit)", layout="wide")

st.title("🛰️ Satellite Flood Response: Single-Unit ROI Engine")
st.markdown("#### *Granular Operational Savings for Ergon Energy / QLD Networks*")

# --- SIDEBAR: UNIT COSTS ---
with st.sidebar:
    st.header("💳 1. The Investment")
    annual_sub = st.number_input("Annual Satellite Subscription (AUD)", value=150000)
    events_per_year = st.slider("Major Flood Events per Year", 1, 5, 2)
    
    st.divider()
    st.header("👤 2. Individual Labor Units")
    people_deployed = st.number_input("Total Personnel Deployed", value=50, help="Total headcount for the event.")
    person_hourly_rate = st.number_input("Labor Rate ($/hr/person)", value=175, help="Fully loaded rate including OT.")
    
    st.divider()
    st.header("🚜 3. Fleet Units")
    vehicles_deployed = st.number_input("Total Vehicles in Field", value=20)
    vehicle_hourly_rate = st.number_input("Fleet Rate ($/hr/vehicle)", value=55)

# --- INPUT TABS ---
t1, t2, t3 = st.tabs(["The Recon Gap", "Aerial & Drone Units", "Friction & Compliance"])

with t1:
    st.subheader("The 'Wait Time' Clock")
    col1, col2 = st.columns(2)
    with col1:
        manual_wait_hrs = st.number_input("Hours until Ground Access (Traditional)", value=48)
    with col2:
        sat_delivery_hrs = st.number_input("Hours to SAR Delivery", value=8)
    
    hrs_gained = manual_wait_hrs - sat_delivery_hrs
    st.info(f"🚀 **Headstart Gained:** {hrs_gained} hours of productive work restored.")

with t2:
    st.subheader("Aerial & Drone Replacement")
    col3, col4 = st.columns(2)
    with col3:
        helo_flight_hrs = st.number_input("Helicopter Flight Hours Saved", value=15)
        helo_unit_rate = st.number_input("Helicopter Rate ($/hr)", value=4500)
    with col4:
        drone_hrs_saved = st.number_input("Drone Pilot Hours Saved", value=40)
        drone_unit_rate = st.number_input("Drone Specialist Rate ($/hr)", value=150)

with t3:
    st.subheader("Operational Friction (Wasted Attempts)")
    col5, col6 = st.columns(2)
    with col5:
        total_visits_planned = st.number_input("Total Site Visits Planned", value=1200)
        blocked_road_pct = st.slider("% Visits Wasted (Flood/No Damage)", 0.0, 1.0, 0.70)
    with col6:
        cost_per_wasted_visit = st.number_input("Direct Cost per Wasted Visit", value=300, help="Fuel + 1hr labor for 2 people.")

# --- THE HARD MATH ---

# 1. Total Labor Standby (Single Unit)
labor_standby_saving = (people_deployed * person_hourly_rate) * hrs_gained
# 2. Total Fleet Standby
fleet_standby_saving = (vehicles_deployed * vehicle_hourly_rate) * hrs_gained
# 3. Aerial Replacement
aerial_total_saving = (helo_flight_hrs * helo_unit_rate) + (drone_hrs_saved * drone_unit_rate)
# 4.
