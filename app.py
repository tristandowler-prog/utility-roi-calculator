import streamlit as st
import pandas as pd
import base64

# --- 1. THE COMMAND CENTER UI ---
st.set_page_config(page_title="ICEYE | Precision ROI", layout="wide")

ICEYE_BLUE = "#39BBF0"
ICEYE_DARK = "#0B0C10"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {ICEYE_DARK}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    .stTabs [data-baseweb="tab"] {{ 
        height: 50px; background-color: #111827; border-radius: 4px 4px 0 0;
        padding: 10px 40px; color: #9CA3AF; border: 1px solid #374151; font-weight: 700;
    }}
    .stTabs [aria-selected="true"] {{ background-color: {ICEYE_BLUE} !important; color: #000 !important; }}
    .formula-card {{
        background: #111827; border: 1px solid {ICEYE_BLUE}44;
        padding: 20px; border-radius: 8px; margin: 10px 0;
    }}
    .math-text {{ font-family: 'Courier New', monospace; color: {ICEYE_BLUE}; font-size: 0.85rem; }}
    .burn-header {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #9CA3AF; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE HARD COST SIDEBAR (UNIT RATES) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=150)
    st.markdown("### 📊 GLOBAL BURN RATES")
    
    with st.expander("🚁 AVIATION RATES", expanded=True):
        heli_hr = st.number_input("Heli (Twin) $/hr", value=6500)
        plane_hr = st.number_input("Fixed-Wing $/hr", value=2800)
        drone_hr = st.number_input("Drone Team $/hr", value=600) # Broken down from day rate
        
    with st.expander("🚛 GROUND & LABOR", expanded=True):
        crew_hr = st.number_input("Field Crew (2p) $/hr", value=345)
        truck_admin = st.number_input("Truck Roll Admin $", value=550)
        gis_hr = st.number_input("GIS Analyst $/hr", value=210)
    
    st.divider()
    annual_events = st.slider("Events Per Year", 1, 6, 2)
    iceye_sub = st.number_input("ICEYE Annual Subscription ($)", value=385000)

# --- 3. THE CALCULATOR ---
st.title("Strategic Capability & ROI Engine")
st.caption("Granular Time-Based Analysis: Manual vs. ICEYE-Augmented Response")

t1, t2, t3 = st.tabs(["🏛️ LOCAL COUNCIL", "⚡ UTILITIES", "🚨 PUBLIC SAFETY"])

# --- TAB 1: COUNCIL ---
with t1:
    st.header("Council: RDA Efficiency")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Manual RDA")
        c_props = st.number_input("Buildings to Inspect", value=2500, key="c1")
        c_hrs_per_prop = st.slider("Manual Hours per Prop", 0.5, 4.0, 1.5, step=0.1)
        manual_c = (c_props * c_hrs_per_prop * crew_hr) + (c_props * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Props [{c_props}] * Hours [{c_hrs_per_prop}] * ${crew_hr}) + (Props * ${truck_admin})</p>
        <h2 style='color:#FF4B4B'>${manual_c:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 ICEYE Targeted RDA")
        c_verif_rate = st.slider("Properties requiring field verify (%)", 5, 50, 15)
        c_iceye_hrs = st.slider("Targeted Hours per Prop", 0.5, 4.0, 0.8, step=0.1)
        # Reduced props + faster speed because they know exactly where to go
        iceye_c = (c_props * (c_verif_rate/100) * c_iceye_hrs * crew_hr) + (c_props * (c_verif_rate/100) * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Verify-Props [{int(c_props*(c_verif_rate/100))}] * Hours [{c_iceye_hrs}] * ${crew_hr}) + (Trucks * ${truck_admin})</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_c:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- TAB 2: UTILITIES ---
with t2:
    st.header("Utility: Asset Clearance")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Blind Patrols")
        u_assets = st.number_input("Critical Assets", value=80, key="u1")
        u_patrol_hrs = st.number_input("Patrol Hours per Asset", value=6)
        manual_u = (u_assets * u_patrol_hrs * crew_hr) + (u_assets * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Assets [{u_assets}] * Hours [{u_patrol_hrs}] * ${crew_hr}) + (Assets * ${truck_admin})</p>
        <h2 style='color:#FF4B4B'>${manual_u:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 Remote SAR Clearance")
        u_sar_clear = st.slider("Remote Clearance Success (%)", 50, 95, 85)
        # Remaining assets still need hours, but fewer assets overall
        iceye_u = (u_assets * (1-u_sar_clear/100) * u_patrol_hrs * crew_hr) + (u_assets * (1-u_sar_clear/100) * truck_admin)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Remaining Assets [{u_assets*(1-u_sar_clear/100):,.1f}] * Hours * ${crew_hr}) + (Trucks * ${truck_admin})</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_u:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- TAB 3: PUBLIC SAFETY ---
with t3:
    st.header("Public Safety: Recon vs Rescue")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Search-Heavy Response")
        p_plane_hrs = st.number_input("Total Plane Flight Hours", value=40)
        p_heli_hrs = st.number_input("Total Heli Flight Hours", value=20)
        p_drone_hrs = st.number_input("Total Drone Ops Hours", value=120)
        
        manual_ps = (p_plane_hrs * plane_hr) + (p_heli_hrs * heli_hr) + (p_drone_hrs * drone_hr)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Plane Hrs * ${plane_hr}) + (Heli Hrs * ${heli_hr}) + (Drone Hrs * ${drone_hr})</p>
        <h2 style='color:#FF4B4B'>${manual_ps:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 Data-Led Response")
        p_iceye_heli = st.number_input("Tactical Heli Hours (Rescue Only)", value=5)
        p_gis_hrs = st.number_input("GIS Analysis Hours", value=48)
        
        iceye_ps = (p_iceye_heli * heli_hr) + (p_gis_hrs * gis_hr)
        
        st.markdown(f"""<div class='formula-card'><p class='burn-header'>Formula</p>
        <p class='math-text'>(Rescue Heli Hrs [{p_iceye_heli}] * ${heli_hr}) + (GIS Mapping Hrs [{p_gis_hrs}] * ${gis_hr})</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_ps:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- 4. THE CAPABILITY DIVIDEND ---
st.divider()
total_manual = (manual_c + manual_u + manual_ps) * annual_events
total_iceye_ops = (iceye_c + iceye_u + iceye_ps) * annual_events
net_gain = total_manual - total_iceye_ops - iceye_sub

s1, s2, s3 = st.columns(3)
with s1:
    st.caption("Total Annual Manual Burn")
    st.subheader(f":red[${total_manual:,.0f}]")
with s2:
    st.caption("Total Annual ICEYE (Ops + Sub)")
    st.subheader(f"${(total_iceye_ops + iceye_sub):,.0f}")
with s3:
    st.caption("Net Annual Strategic Dividend")
    st.subheader(f":green[${net_gain:,.0f}]")

st.markdown(f"""
<div style="text-align: center; border: 1px solid {ICEYE_BLUE}; padding: 30px; margin-top: 20px;">
    <h1 style="margin:0; font-size: 4rem;">ROI: {((net_gain/iceye_sub)*100) if iceye_sub > 0 else 0:,.0f}%</h1>
    <p style="color: {ICEYE_BLUE}; font-weight: 700;">CAPACITY RELEASED BACK TO BUDGET</p>
</div>
""", unsafe_allow_html=True)
