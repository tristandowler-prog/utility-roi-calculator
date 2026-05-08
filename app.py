import streamlit as st
import base64
from fpdf import FPDF

# --- 1. THE DESIGN SYSTEM (CSS) ---
st.set_page_config(page_title="ICEYE ROI Dashboard", layout="wide")

ICEYE_BLUE = "#39BBF0"
BACKGROUND = "#0B0C10"
CARD_BG = "rgba(255, 255, 255, 0.03)"
BORDER_COLOR = "rgba(255, 255, 255, 0.1)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp {{ background-color: {BACKGROUND}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }}
    .metric-label {{ color: #94A3B8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
    .metric-value {{ font-size: 2rem; font-weight: 800; color: #FFFFFF; margin: 5px 0; }}
    .metric-delta {{ font-size: 0.85rem; font-weight: 600; color: {ICEYE_BLUE}; }}

    .stTabs [data-baseweb="tab"] {{
        background-color: {CARD_BG};
        border-radius: 8px 8px 0 0;
        color: #94A3B8;
        padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{ background-color: {ICEYE_BLUE} !important; color: {BACKGROUND} !important; }}
    
    /* Input transparency */
    div[data-baseweb="input"], div[data-baseweb="select"] {{ background-color: rgba(255,255,255,0.05) !important; border-radius: 8px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=120)
st.markdown("<h1 style='font-weight:800; margin-bottom:0;'>Operational <span style='color:"+ICEYE_BLUE+";'>Alpha</span> Dashboard</h1>", unsafe_allow_html=True)
st.caption("Strategic ROI Assessment: 6-Hour Rapid Impact & 24-Hour Flood Insights")

# --- 3. GLOBAL CONFIG (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🗺️ Baseline Economics")
    annual_events = st.number_input("Major Events / Year", value=2)
    iceye_sub = st.number_input("Annual ICEYE Subscription ($)", value=385000)
    st.divider()
    st.markdown("### 🧑‍💻 Global Rates")
    gis_rate = st.number_input("GIS Analyst Rate ($/hr)", value=210)
    crew_rate = st.number_input("Field Crew/Inspector Rate ($/hr)", value=175)
    truck_fee = st.number_input("Truck Roll Admin Fee ($)", value=550)

# --- 4. CALCULATOR TABS ---
t1, t2, t3 = st.tabs(["🏛️ LOCAL COUNCIL", "🚨 PUBLIC SAFETY", "⚡ UTILITIES"])

# --- TAB 1: COUNCIL ---
with t1:
    st.markdown("### Damage Assessment & GIS Synthesis")
    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        c_props = st.number_input("Total Properties in Zone", value=2500)
        c_inspectors = st.number_input("Number of Field Inspectors", value=12)
        c_man_gis_hrs = st.number_input("Manual Mapping Hrs (Team Total)", value=120)
        c_verif_rate = st.slider("ICEYE Verification Requirement (%)", 1, 100, 15)
        
    m_c_cost = (c_props * 1.5 * crew_rate) + (c_props * truck_fee) + (c_man_gis_hrs * gis_rate)
    i_c_cost = (c_props * (c_verif_rate/100) * 1.5 * crew_rate) + (c_props * (c_verif_rate/100) * truck_fee) + (8 * gis_rate)
    
    with col_out:
        v1, v2 = st.columns(2)
        v1.markdown(f"<div class='metric-card'><p class='metric-label'>Manual RDA Burn</p><p class='metric-value'>${m_c_cost:,.0f}</p></div>", unsafe_allow_html=True)
        v2.markdown(f"<div class='metric-card'><p class='metric-label'>ICEYE Integrated Cost</p><p class='metric-value'>${i_c_cost:,.0f}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card' style='border: 1px solid {ICEYE_BLUE};'><p class='metric-label'>Council Event Saving</p><p class='metric-value' style='color:{ICEYE_BLUE};'>${(m_c_cost - i_c_cost):,.0f}</p></div>", unsafe_allow_html=True)

# --- TAB 2: PUBLIC SAFETY ---
with t2:
    st.markdown("### Search & Reconnaissance Fleet")
    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        p_heli_qty = st.number_input("Helicopters Deployed", value=2)
        p_heli_hr = st.number_input("Heli Rate ($/hr)", value=6500)
        p_plane_qty = st.number_input("Airplanes Deployed", value=1)
        p_plane_hr = st.number_input("Plane Rate ($/hr)", value=2800)
        p_flight_hrs = st.number_input("Total Flight Hrs per Asset", value=30)
        
    m_p_cost = (p_heli_qty * p_flight_hrs * p_heli_hr) + (p_plane_qty * p_flight_hrs * p_plane_hr)
    i_p_cost = (5 * p_heli_hr) + (8 * gis_rate) # Tactical rescue flights only + integration
    
    with col_out:
        v1, v2 = st.columns(2)
        v1.markdown(f"<div class='metric-card'><p class='metric-label'>Manual Air Search</p><p class='metric-value'>${m_p_cost:,.0f}</p></div>", unsafe_allow_html=True)
        v2.markdown(f"<div class='metric-card'><p class='metric-label'>ICEYE SAR Intelligence</p><p class='metric-value'>${i_p_cost:,.0f}</p></div>", unsafe_allow_html=True)

# --- TAB 3: UTILITIES ---
with t3:
    st.markdown("### Infrastructure Grid Clearance")
    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        u_assets = st.number_input("Critical Assets (Substations/Pylons)", value=120)
        u_crews = st.number_input("Number of Field Crews", value=15)
        u_clearance = st.slider("Remote SAR Clearance Rate (%)", 1, 100, 85)
        
    m_u_cost = (u_assets * 4 * crew_rate) + (u_assets * truck_fee)
    i_u_cost = (u_assets * (1-u_clearance/100) * 4 * crew_rate) + (u_assets * (1-u_clearance/100) * truck_fee)
    
    with col_out:
        v1, v2 = st.columns(2)
        v1.markdown(f"<div class='metric-card'><p class='metric-label'>Blind Patrol Burn</p><p class='metric-value'>${m_u_cost:,.0f}</p></div>", unsafe_allow_html=True)
        v2.markdown(f"<div class='metric-card'><p class='metric-label'>ICEYE Targeted Clearance</p><p class='metric-value'>${i_u_cost:,.0f}</p></div>", unsafe_allow_html=True)

# --- 5. THE BOTTOM BAR (GRAND ROI) ---
st.divider()
event_savings = (m_c_cost + m_p_cost + m_u_cost) - (i_c_cost + i_p_cost + i_u_cost)
annual_net = (event_savings * annual_events) - iceye_sub

st.markdown(f"""
    <div style='background: linear-gradient(90deg, {ICEYE_BLUE} 0%, #1e40af 100%); padding: 40px; border-radius: 24px; text-align: center; margin-top:20px;'>
        <p style='color: white; font-weight: 800; letter-spacing: 3px; margin:0;'>NET ANNUAL OPERATIONAL DIVIDEND</p>
        <h1 style='color: white; font-size: 5rem; margin: 0;'>${annual_net:,.0f}</h1>
        <p style='color: rgba(255,255,255,0.8);'>Calculated based on {annual_events} events per year and user-defined unit rates.</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. PDF EXPORT ---
if st.button("📥 Export Strategic Briefing (PDF)"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ICEYE ROI Executive Summary", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Annual Manual Operational Burn: ${((m_c_cost + m_p_cost + m_u_cost) * annual_events):,.0f}", ln=True)
    pdf.cell(200, 10, f"Annual ICEYE-Augmented Cost (inc. Subscription): ${(((i_c_cost + i_p_cost + i_u_cost) * annual_events) + iceye_sub):,.0f}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"TOTAL ANNUAL DIVIDEND: ${annual_net:,.0f}", ln=True)
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="ICEYE_ROI_Summary.pdf">Download PDF Briefing</a>', unsafe_allow_html=True)
