import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="ICEYE Strategic ROI", layout="wide", page_icon="🛰️")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .executive-card { 
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-left: 5px solid #38BDF8; border-radius: 10px; padding: 20px; margin-bottom: 20px;
    }
    .burn-value { color: #F43F5E; font-size: 1.5rem; font-weight: bold; }
    .save-value { color: #10B981; font-size: 1.5rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL SIDEBAR: THE UNIT COSTS (NOTHING REMOVED) ---
with st.sidebar:
    st.title("💰 Unit Cost Baseline")
    
    with st.expander("🚁 Aviation & Drones", expanded=True):
        heli_rate = st.number_input("Heli $/hr", value=5500)
        plane_rate = st.number_input("Plane $/hr", value=2200)
        drone_team_day = st.number_input("Drone Team (Daily)", value=4500)
        
    with st.expander("🚛 Field Crews & Trucks", expanded=True):
        field_crew_hr = st.number_input("Field Crew $/hr", value=320)
        truck_roll_admin = st.number_input("Truck Roll Admin Fee $", value=450)
        
    with st.expander("💻 GIS & Intelligence", expanded=True):
        gis_analyst_hr = st.number_input("GIS Analyst Surge $/hr", value=195)
        it_ops_daily = st.number_input("Command Center Ops $/day", value=12500)

    st.divider()
    annual_events = st.slider("Events per Year", 1, 8, 3)
    iceye_subscription = st.number_input("ICEYE Annual Subscription", value=350000)

# --- 3. MAIN INTERFACE ---
st.title("🛰️ ICEYE Strategic ROI: Focused Deployment Model")
st.info("ICEYE doesn't replace the field crew; it replaces the 'Blind Recon' phase, ensuring every truck roll is high-value.")

tab1, tab2, tab3 = st.tabs(["🚨 EMERGENCY SERVICES", "🏛️ LOCAL COUNCIL", "⚡ UTILITIES"])

# --- TAB 1: EMERGENCY SERVICES (Reallocating the Aviation Budget) ---
with tab1:
    st.header("Search vs. Rescue Allocation")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔴 CURRENT: Blind Recon")
        recon_flight_hrs = st.number_input("Recon/Mapping Flight Hrs", value=30)
        drone_days = st.number_input("Drone Scouting Days", value=5)
        gis_manual_hrs = st.number_input("Manual Mapping Hrs", value=80)
        
        current_cost = (recon_flight_hrs * heli_rate) + (drone_days * drone_team_day) + (gis_manual_hrs * gis_analyst_hr)
        st.markdown(f'<p class="burn-value">${current_cost:,.0f}</p>', unsafe_allow_html=True)
    
    with c2:
        st.markdown("### 🟢 ACHIEVABLE: Precision Deployment")
        # Shift: Helis are now 90% for RESCUE, 10% for spot-check
        iceye_recon_offset = recon_flight_hrs * 0.1
        iceye_gis_verify = 8
        iceye_cost = (iceye_recon_offset * heli_rate) + (iceye_gis_verify * gis_analyst_hr)
        
        st.markdown(f'<p class="save-value">${iceye_cost:,.0f}</p>', unsafe_allow_html=True)
        st.caption("Aviation assets reallocated from 'Looking' to 'Saving'.")

# --- TAB 2: LOCAL COUNCIL (The Inspection Squeeze) ---
with tab2:
    st.header("Rapid Damage Assessment: Focused Deployment")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔴 CURRENT: Area-Wide Patrols")
        properties = st.number_input("Total Properties in LGA", value=3000)
        insp_per_day = st.slider("Inspections / Crew / Day", 5, 50, 20)
        crews = st.number_input("Manual Teams Deployed", value=10)
        
        days = properties / (insp_per_day * crews)
        manual_burn = (days * 8 * crews * field_crew_hr) + (crews * truck_roll_admin * days)
        st.markdown(f'<p class="burn-value">${manual_burn:,.0f}</p>', unsafe_allow_html=True)
        st.caption(f"Crews spend {days:.1f} days doing blind 'street-by-street' checks.")

    with c2:
        st.markdown("### 🟢 ACHIEVABLE: Data-Led Verification")
        # Field crew is still needed for the 'Last Mile' or complex claims, but 75% less 'searching'
        efficiency_gain = st.slider("Deployment Focus (% reduction in blind patrolling)", 50, 90, 75)
        focused_days = days * (1 - (efficiency_gain/100))
        iceye_council_burn = (focused_days * 8 * crews * field_crew_hr) + (crews * truck_roll_admin * focused_days)
        
        st.markdown(f'<p class="save-value">${iceye_council_burn:,.0f}</p>', unsafe_allow_html=True)
        st.caption(f"Crews spend {focused_days:.1f} days only visiting SAR-flagged properties.")

# --- TAB 3: UTILITIES (Substation Clearance) ---
with tab3:
    st.header("Restoration Efficiency")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🔴 CURRENT: Blind Patrols")
        assets = st.number_input("Assets/Substations to Verify", value=60)
        patrol_hr = st.slider("Travel/Verify Time (Hrs/Site)", 1, 8, 4)
        
        utility_burn = (assets * patrol_hr * field_crew_hr) + (assets * truck_roll_admin)
        st.markdown(f'<p class="burn-value">${utility_burn:,.0f}</p>', unsafe_allow_html=True)
    
    with c2:
        st.markdown("### 🟢 ACHIEVABLE: Remote Clearance")
        # SAR clears the majority; humans only go to 'unclear' or 'confirmed damaged' sites
        sar_clearance_rate = st.slider("Remote Clearance Rate (%)", 50, 95, 80)
        remaining_patrols = assets * (1 - (sar_clearance_rate/100))
        iceye_utility_burn = (remaining_patrols * patrol_hr * field_crew_hr) + (remaining_patrols * truck_roll_admin)
        
        st.markdown(f'<p class="save-value">${iceye_utility_burn:,.0f}</p>', unsafe_allow_html=True)
        st.caption("80% of assets cleared via SAR, eliminating redundant truck rolls.")

# --- 4. SUMMARY (ALL DATA KEPT) ---
st.divider()
total_current = (current_cost + manual_burn + utility_burn) * annual_events
total_iceye = (iceye_cost + iceye_council_burn + iceye_utility_burn) * annual_events
net_roi = total_current - total_iceye - iceye_subscription

cols = st.columns(3)
cols[0].metric("Manual Multi-Agency Burn", f"${total_current:,.0f}")
cols[1].metric("ICEYE Focused Burn", f"${total_iceye:,.0f}")
cols[2].metric("Net Annual Benefit", f"${net_roi:,.0f}", delta="ROI Positive")
