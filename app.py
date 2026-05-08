import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="ICEYE Strategic ROI", layout="wide", page_icon="🛰️")

# Professional Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .executive-card { 
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-left: 5px solid #38BDF8; border-radius: 10px; padding: 25px; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] { font-size: 1.2rem; font-weight: bold; }
    .burn-label { color: #94A3B8; font-size: 0.9rem; text-transform: uppercase; }
    .burn-value { color: #F43F5E; font-size: 1.5rem; font-weight: bold; }
    .save-value { color: #10B981; font-size: 1.5rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL SIDEBAR: THE HOURLY BURN RATES ---
with st.sidebar:
    st.title("💰 Unit Cost Baseline")
    st.markdown("Enter your actual contract rates to drive the ROI.")
    
    with st.expander("🚁 Aviation & Drones", expanded=True):
        heli_rate = st.number_input("Heli (Inc. Fuel/Pilot) $/hr", value=5500)
        plane_rate = st.number_input("Fixed-Wing Recon $/hr", value=2200)
        drone_team_day = st.number_input("Drone Team (Daily Rate)", value=4500)
        
    with st.expander("🚛 Field Crews & Trucks", expanded=True):
        field_crew_hr = st.number_input("Field Crew (2p+4WD) $/hr", value=320)
        truck_roll_admin = st.number_input("Truck Roll Admin Fee $", value=450)
        
    with st.expander("💻 GIS & Intelligence", expanded=True):
        gis_analyst_hr = st.number_input("GIS Analyst Surge Rate $/hr", value=195)
        it_ops_daily = st.number_input("Command Center Ops $/day", value=12500)

    st.divider()
    annual_events = st.slider("Events per Year", 1, 8, 3)
    iceye_subscription = st.number_input("ICEYE Annual Subscription", value=350000)

# --- 3. MAIN INTERFACE ---
st.title("🛰️ ICEYE Strategic ROI: Current vs. Achievable State")
tab1, tab2, tab3 = st.tabs(["🚨 EMERGENCY SERVICES", "🏛️ LOCAL COUNCIL", "⚡ UTILITIES"])

# --- TAB 1: EMERGENCY SERVICES (Focus: Information Gap) ---
with tab1:
    st.header("Emergency Response & Situational Awareness")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Current State: Manual Recon")
        recon_flight_hrs = st.number_input("Recon Flight Hrs / Event", value=30)
        drone_days = st.number_input("Drone Deployment Days", value=5)
        gis_manual_mapping = st.number_input("Manual Mapping Hrs (GIS Team)", value=80)
        
        # Math
        current_resp_cost = (recon_flight_hrs * heli_rate) + (drone_days * drone_team_day) + (gis_manual_mapping * gis_analyst_hr)
        st.markdown(f'<p class="burn-label">Event Burn</p><p class="burn-value">${current_resp_cost:,.0f}</p>', unsafe_allow_html=True)
        st.caption("Covers: Aviation recon, BVLOS drone teams, and manual digitizing.")

    with col2:
        st.markdown("### 🟢 Achievable: ICEYE Intelligence")
        # ICEYE replaces recon flights. Drones/Helis move to high-value rescue.
        iceye_gis_verification = 8 # Automated; analyst just verifies
        iceye_resp_cost = (iceye_gis_verification * gis_analyst_hr)
        
        st.markdown(f'<p class="burn-label">Event Burn</p><p class="save-value">${iceye_resp_cost:,.0f}</p>', unsafe_allow_html=True)
        st.caption("Covers: Instant situational awareness and automated GIS updates.")

# --- TAB 2: LOCAL COUNCIL (Focus: RDA & Funding Velocity) ---
with tab2:
    st.header("Council Recovery & Infrastructure Claims")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Current State: Manual RDA")
        properties_to_inspect = st.number_input("Building-Level Inspections", value=2500)
        inspections_per_crew_day = st.slider("Inspections / Crew / Day", 5, 50, 15)
        num_crews = st.number_input("Inspection Crews Deployed", value=10)
        
        # Math
        days_to_complete = properties_to_inspect / (inspections_per_crew_day * num_crews)
        labor_cost = (days_to_complete * 8 * num_crews * field_crew_hr)
        truck_cost = (num_crews * truck_roll_admin * days_to_complete)
        council_current_total = labor_cost + truck_cost
        
        st.markdown(f'<p class="burn-label">Event Burn</p><p class="burn-value">${council_current_total:,.0f}</p>', unsafe_allow_html=True)
        st.caption(f"Takes approx {days_to_complete:.1f} days to complete.")

    with col2:
        st.markdown("### 🟢 Achievable: SAR-Verified RDA")
        # ICEYE verifies 80% of properties remotely. Crews target the remaining 20%.
        targeted_inspections = properties_to_inspect * 0.2
        iceye_days = targeted_inspections / (inspections_per_crew_day * num_crews)
        iceye_labor = (iceye_days * 8 * num_crews * field_crew_hr)
        iceye_truck = (num_crews * truck_roll_admin * iceye_days)
        council_iceye_total = iceye_labor + iceye_truck
        
        st.markdown(f'<p class="burn-label">Event Burn</p><p class="save-value">${council_iceye_total:,.0f}</p>', unsafe_allow_html=True)
        st.caption("Crews deployed only to high-probability damage zones.")

# --- TAB 3: UTILITIES (Focus: Restoration & Patrols) ---
with tab3:
    st.header("Network Restoration & Asset Clearance")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Current State: Blind Patrols")
        substations_verify = st.number_input("Substations/Assets to Verify", value=50)
        patrol_hrs_site = st.slider("Recon Hrs per Asset (Travel+Check)", 1, 8, 4)
        
        utility_manual_cost = (substations_verify * patrol_hrs_site * field_crew_hr)
        st.markdown(f'<p class="burn-label">Event Burn</p><p class="burn-value">${utility_manual_cost:,.0f}</p>', unsafe_allow_html=True)
        st.caption("Includes: Sending trucks through floodwaters just to see if a site is dry.")

    with col2:
        st.markdown("### 🟢 Achievable: Digital Asset Clearance")
        # ICEYE clears assets through clouds.
        clearance_reduction = 0.85 # 85% cleared remotely
        utility_iceye_cost = (substations_verify * (1 - clearance_reduction) * patrol_hrs_site * field_crew_hr)
        
        st.markdown(f'<p class="burn-label">Event Burn</p><p class="save-value">${utility_iceye_cost:,.0f}</p>', unsafe_allow_html=True)
        st.caption("Assets cleared via SAR; re-energization starts hours earlier.")

# --- 4. THE EXECUTIVE SUMMARY ---
st.divider()
total_manual_pa = (current_resp_cost + council_current_total + utility_manual_cost) * annual_events
total_iceye_pa = (iceye_resp_cost + council_iceye_total + utility_iceye_cost) * annual_events
net_roi = total_manual_pa - total_iceye_pa - iceye_subscription

st.subheader("📊 Executive Business Case (Annual)")
summary_cols = st.columns(3)
summary_cols[0].metric("Current Operational Burn", f"${total_manual_pa:,.0f}")
summary_cols[1].metric("ICEYE Optimized Burn", f"${total_iceye_pa:,.0f}")
summary_cols[2].metric("Net Annual Savings", f"${net_roi:,.0f}", delta="ROI Positive")

st.info("The logic above is driven by Hard Savings: reduced aviation hours, targeted field deployment, and minimized manual GIS labor.")
