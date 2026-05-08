import streamlit as st
import pandas as pd

# --- EXECUTIVE OPERATIONAL SETTINGS ---
st.set_page_config(page_title="Hard Savings: Current vs ICEYE", layout="wide")

st.sidebar.title("🛠️ The 'Current State' Burn")
# Field Services
crew_hourly = st.sidebar.number_input("Field Crew Rate (2p + Vehicle $/hr)", value=320)
num_trucks = st.sidebar.slider("Number of Trucks Deployed", 1, 50, 15)
hours_per_day = st.sidebar.slider("Operational Hours / Day", 8, 16, 12)

# GIS & Data
gis_surge_rate = st.sidebar.number_input("GIS Analyst Surge Rate ($/hr)", value=195)
manual_mapping_days = st.sidebar.number_input("Days to complete manual flood map", value=5)

# --- ANALYTIC ENGINE ---
st.title("🛰️ ICEYE Hard-Savings ROI: Total Disaster Burn")

c1, c2 = st.columns(2)

with c1:
    st.subheader("🔴 CURRENT STATE: Manual Response")
    daily_truck_burn = num_trucks * crew_hourly * hours_per_day
    total_field_cost = daily_truck_burn * manual_mapping_days
    gis_burn = (manual_mapping_days * 8 * gis_surge_rate * 3) # Assuming 3 analysts
    
    st.error(f"Daily Truck Roll Burn: ${daily_truck_burn:,.0f}")
    st.error(f"Total Mapping Labor: ${total_field_cost + gis_burn:,.0f}")
    st.caption("Includes: Blind recon flights, failed dispatches, and manual GIS digitizing.")

with c2:
    st.subheader("🟢 ACHIEVABLE STATE: ICEYE Intelligence")
    # ICEYE eliminates the need for 'searching' trucks. Crews are only sent to 'Action' sites.
    iceye_truck_burn = (num_trucks * 0.3) * crew_hourly * hours_per_day # 70% reduction in 'blind' patrols
    iceye_field_cost = iceye_truck_burn * 2 # Usually restoration starts Day 1 or 2
    iceye_gis_burn = (8 * gis_surge_rate) # Single analyst to verify automated output
    
    st.success(f"Optimized Daily Burn: ${iceye_truck_burn:,.0f}")
    st.success(f"Total Response Labor: ${iceye_field_cost + iceye_gis_burn:,.0f}")
    st.caption("Includes: Targeted restoration, 0 'blind' patrols, and automated GIS integration.")

# --- THE ROI SUMMARY ---
st.divider()
total_savings_per_event = (total_field_cost + gis_burn) - (iceye_field_cost + iceye_gis_burn)
st.subheader(f"💰 Hard Savings per Event: ${total_savings_per_event:,.0f}")

st.info("""
**Note for Executives:** This doesn't include 'soft' benefits like public safety or community morale. 
This is purely the **cash saved** by not paying crews to drive through floodwaters looking for things that a satellite can see in 10 minutes.
""")
