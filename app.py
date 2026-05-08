import streamlit as st
import pandas as pd
import base64

# --- 1. THE COMMAND CENTER UI ---
st.set_page_config(page_title="ICEYE | Strategic ROI", layout="wide")

# Official ICEYE Palette (2026 Brand Update)
ICEYE_BLUE = "#39BBF0"
ICEYE_DARK = "#0B0C10"
ICEYE_GRID = "#1F2937"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {ICEYE_DARK}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; background-color: transparent; }}
    .stTabs [data-baseweb="tab"] {{ 
        height: 50px; background-color: #111827; border-radius: 4px 4px 0 0;
        padding: 10px 40px; color: #9CA3AF; border: 1px solid #374151; font-weight: 700;
    }}
    .stTabs [aria-selected="true"] {{ background-color: {ICEYE_BLUE} !important; color: #000 !important; }}
    
    .formula-card {{
        background: #111827; border: 1px solid {ICEYE_BLUE}44;
        padding: 20px; border-radius: 8px; margin: 10px 0;
    }}
    .math-text {{ font-family: 'Courier New', monospace; color: {ICEYE_BLUE}; font-size: 0.95rem; }}
    .burn-header {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #9CA3AF; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE HARD COST SIDEBAR ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=150)
    st.markdown("### 📊 UNIT COST BASELINE")
    
    with st.expander("🚁 AERIAL RECON", expanded=True):
        heli_hr = st.number_input("Heli $/hr", value=6500)
        plane_hr = st.number_input("Plane $/hr", value=2800)
        drone_team_day = st.number_input("Drone Team $/day", value=4800)
        drone_qty = st.slider("Active Drone Teams", 1, 15, 4)

    with st.expander("🚛 GROUND & AUDIT", expanded=True):
        crew_hr = st.number_input("Field Crew (2p) $/hr", value=345)
        truck_admin = st.number_input("Truck Roll Admin Fee $", value=550)
        gis_hr = st.number_input("GIS Analyst $/hr", value=210)
    
    st.divider()
    annual_events = st.slider("Events Per Year", 1, 6, 2)
    iceye_sub = st.number_input("ICEYE Annual Access Fee ($)", value=385000)

# --- 3. THE TRANSPARENT ROI TABS ---
st.title("Strategic ROI Assessment")
st.caption("A data-driven comparison of Information-Gap vs. Persistent Monitoring")

t1, t2, t3 = st.tabs(["🏛️ LOCAL COUNCIL", "⚡ UTILITIES", "🚨 PUBLIC SAFETY"])

# --- TAB 1: COUNCIL ---
with t1:
    st.header("Council: DRFA Funding Evidence")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Manual RDA (Search Mode)")
        props = st.number_input("Properties to Inspect", 500, 10000, 2500)
        manual_c = (props * 0.4 * crew_hr) + (props * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Props [{props}] * 24min Labor ${crew_hr}) + (Props * Admin ${truck_admin})</p>
        <h2 style='color:#FF4B4B'>${manual_c:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 ICEYE (Verify Mode)")
        target_rate = st.slider("Targeted Verification %", 10, 50, 20)
        iceye_c = (props * (target_rate/100) * crew_hr) + (props * (target_rate/100) * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Target Props [{props*(target_rate/100):,.0f}] * Labor ${crew_hr}) + (Trucks * Admin ${truck_admin})</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_c:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- TAB 2: UTILITIES ---
with t2:
    st.header("Utility: Infrastructure Clearance")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Blind Patrols")
        u_assets = st.number_input("Critical Sub-Stations", 10, 200, 60)
        manual_u = (u_assets * 4 * crew_hr) + (u_assets * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Assets [{u_assets}] * 4hr Patrol ${crew_hr}) + (Assets * Admin ${truck_admin})</p>
        <h2 style='color:#FF4B4B'>${manual_u:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 Remote Clearance")
        clear_r = st.slider("SAR Remote Clearance %", 50, 95, 80)
        iceye_u = (u_assets * (1 - (clear_r/100)) * 4 * crew_hr) + (u_assets * (1 - (clear_r/100)) * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Field Verification [{u_assets*(1-clear_r/100):,.1f}] * Patrol ${crew_hr}) + (Trucks * Admin ${truck_admin})</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_u:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- TAB 3: PUBLIC SAFETY ---
with t3:
    st.header("Public Safety: Aviation Realignment")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Information Gap")
        flight_hrs = st.number_input("Recon Flight Hours", 10, 100, 30)
        manual_ps = (flight_hrs * plane_hr) + (flight_hrs * 0.5 * heli_hr) + (drone_qty * drone_team_day * 5)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Plane ${plane_hr} * hrs) + (Heli ${heli_hr} * 0.5 hrs) + ({drone_qty} Drone Teams * 5 days)</p>
        <h2 style='color:#FF4B4B'>${manual_ps:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 Data-Led Response")
        # ICEYE removes the "search" flight hours. We keep a buffer for validation.
        iceye_ps = (flight_hrs * 0.1 * heli_hr) + (gis_hr * 40)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Tactical-Only Heli ${heli_hr} * 10%) + (GIS Analyst Integration ${gis_hr} * 40hr)</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_ps:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- 4. THE CAPABILITY DIVIDEND ---
st.divider()
total_manual = (manual_c + manual_u + manual_ps) * annual_events
total_iceye_ops = (iceye_c + iceye_u + iceye_ps) * annual_events
dividend = total_manual - total_iceye_ops - iceye_sub

st.markdown(f"""
<div style="text-align: center; border: 2px solid {ICEYE_BLUE}; padding: 40px; border-radius: 8px; background: #0F172A;">
    <p style="letter-spacing: 5px; font-weight: 900; color: {ICEYE_BLUE};">NET ANNUAL CAPABILITY DIVIDEND</p>
    <h1 style="font-size: 5rem; margin: 0;">${dividend:,.0f}</h1>
    <p style="color: #94A3B8;">Calculated across {annual_events} events per year including subscription costs.</p>
</div>
""", unsafe_allow_html=True)
