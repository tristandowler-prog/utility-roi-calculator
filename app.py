import streamlit as st
import pandas as pd

# --- 1. THE "OPEN BOOK" BRANDING ---
st.set_page_config(page_title="ICEYE | Financial Transparency Tool", layout="wide")

# ICEYE Corporate Palette
ICEYE_BLUE = "#39BBF0"
ICEYE_DARK = "#0B0C10"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {ICEYE_DARK}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    .formula-box {{ 
        background: #161B22; border-left: 4px solid {ICEYE_BLUE}; 
        padding: 15px; margin: 10px 0; font-family: 'Courier New', monospace; font-size: 0.9rem;
    }}
    .heavy-metric {{ font-size: 2.5rem; font-weight: 800; color: {ICEYE_BLUE}; }}
    .sidebar-header {{ color: {ICEYE_BLUE}; font-weight: 700; text-transform: uppercase; font-size: 0.8rem; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE TRANSPARENT SIDEBAR (HARD COSTS) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=150)
    st.markdown("<p class='sidebar-header'>Unit Cost Assumptions</p>", unsafe_allow_html=True)
    
    # Aviation & Drones
    heli_hr = st.number_input("Heli (Twin Engine) $/hr", value=6500)
    plane_hr = st.number_input("Fixed-Wing Recon $/hr", value=2800)
    drone_team_day = st.number_input("Drone Strike Team $/day", value=4800)
    
    # Ground & Admin
    crew_hr = st.number_input("Field Crew (2p) $/hr", value=345)
    truck_admin = st.number_input("Truck Roll Admin Fee $", value=550, help="Fuel, wear, dispatch, and safety overhead.")
    gis_hr = st.number_input("Senior GIS Analyst $/hr", value=210)
    
    st.divider()
    annual_events = st.slider("Significant Events / Year", 1, 5, 2)
    iceye_sub = st.number_input("ICEYE Platform Fee ($)", value=380000)

# --- 3. THE MAIN CALCULATOR ---
st.title("Financial Vulnerability Analysis")
st.markdown("### Comparing Manual Reconnaissance vs. ICEYE SAR Monitoring")

# --- VERTICAL 1: PUBLIC SAFETY ---
st.header("🚨 Public Safety & Aviation Efficiency")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Manual Recon Baseline")
    recon_hrs = st.number_input("Recon Flight Hours (Per Event)", 10, 100, 40)
    manual_ps_cost = (recon_hrs * plane_hr) + (recon_hrs * 0.5 * heli_hr)
    
    st.markdown(f"""
    <div class="formula-box">
    (Recon Hrs [{recon_hrs}] * Plane ${plane_hr}) + <br>
    (Spotlight Hrs [{recon_hrs*0.5}] * Heli ${heli_hr}) = 
    <b>${manual_ps_cost:,.0f}</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("ICEYE Optimized")
    # ICEYE replaces 90% of recon hours because you already have the polygons.
    iceye_ps_cost = (recon_hrs * 0.1 * heli_hr) + (gis_hr * 16)
    st.markdown(f"""
    <div class="formula-box">
    (Rescue-Only Heli [{recon_hrs*0.1}] * Heli ${heli_hr}) + <br>
    (Data Integration [{16}] * GIS ${gis_hr}) = 
    <b>${iceye_ps_cost:,.0f}</b>
    </div>
    """, unsafe_allow_html=True)

# --- VERTICAL 2: LOCAL COUNCIL (DRFA COMPLIANCE) ---
st.divider()
st.header("🏛️ Council: DRFA Audit-Proofing")
c_col1, c_col2 = st.columns(2)

with c_col1:
    st.subheader("The 'Search' Phase (Manual)")
    total_props = st.number_input("Buildings in Impact Zone", 500, 10000, 2500)
    # Average 20 mins per house for manual RDA photo/log
    labor_manual = (total_props * 0.33 * crew_hr) + (total_props * truck_admin)
    
    st.markdown(f"""
    <div class="formula-box">
    (Props [{total_props}] * 20m Labor ${crew_hr}) + <br>
    (Truck Rolls [{total_props}] * Admin ${truck_admin}) = 
    <b>${labor_manual:,.0f}</b>
    </div>
    """, unsafe_allow_html=True)

with c_col2:
    st.subheader("The 'Verify' Phase (ICEYE)")
    # Research shows ICEYE depth/extent removes 70% of 'dry hole' truck rolls.
    verification_rate = st.slider("Targeted Verification Rate (%)", 10, 50, 25)
    iceye_c_cost = (total_props * (verification_rate/100) * crew_hr) + (total_props * (verification_rate/100) * truck_admin)
    
    st.markdown(f"""
    <div class="formula-box">
    (Verified Props [{total_props * (verification_rate/100):,.0f}] * Labor ${crew_hr}) + <br>
    (Targeted Truck Rolls * Admin ${truck_admin}) = 
    <b>${iceye_c_cost:,.0f}</b>
    </div>
    """, unsafe_allow_html=True)

# --- 4. SUMMARY DASHBOARD ---
st.divider()
total_manual_pa = (manual_ps_cost + labor_manual) * annual_events
total_iceye_pa = (iceye_ps_cost + iceye_c_cost) * annual_events
net_savings = total_manual_pa - total_iceye_pa - iceye_sub

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("<p class='sidebar-header'>Annual Manual Burn</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='heavy-metric' style='color: #FF4B4B;'>${total_manual_pa:,.0f}</p>", unsafe_allow_html=True)
with s2:
    st.markdown("<p class='sidebar-header'>Annual ICEYE Total Cost</p>", unsafe_allow_html=True)
    # Cost = (Optimized Ops * Events) + Subscription
    st.markdown(f"<p class='heavy-metric'>${(total_iceye_pa + iceye_sub):,.0f}</p>", unsafe_allow_html=True)
with s3:
    st.markdown("<p class='sidebar-header'>Net Operational Dividend</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='heavy-metric' style='color: #00FF00;'>${net_savings:,.0f}</p>", unsafe_allow_html=True)
