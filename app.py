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
    
    .stApp {{
        background-color: {BACKGROUND};
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Dribbble-style Metric Card */
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 16px;
        padding: 24px;
        text-align: left;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }}
    
    .metric-label {{
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
    }}
    
    .metric-delta {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {ICEYE_BLUE};
    }}

    /* Customizing Streamlit Tabs to look like a Sidebar/Menu */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 45px;
        white-space: pre-wrap;
        background-color: {CARD_BG};
        border-radius: 8px;
        color: #94A3B8;
        border: 1px solid {BORDER_COLOR};
        padding: 10px 20px;
        font-weight: 600;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {ICEYE_BLUE} !important;
        color: {BACKGROUND} !important;
        border: none !important;
    }}

    /* Input Field Styling */
    div[data-baseweb="input"] {{
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER SECTION ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=120)
with col_title:
    st.markdown("<h1 style='margin-top:0; font-weight:800;'>Operational Impact <span style='color:"+ICEYE_BLUE+";'>Analysis</span></h1>", unsafe_allow_html=True)

# --- 3. THE GLOBAL SETTINGS ---
with st.container():
    st.markdown("### ⚙️ Global Assumptions")
    c1, c2, c3 = st.columns(3)
    with c1:
        annual_events = st.number_input("Annual Major Events", value=2)
    with c2:
        iceye_sub = st.number_input("Annual ICEYE Access Fee", value=385000)
    with c3:
        currency = st.selectbox("Currency", ["USD", "GBP", "EUR", "AUD"])

# --- 4. THE CALCULATOR CORE ---
t1, t2, t3 = st.tabs(["🏛️ Local Council", "🚨 Public Safety", "⚡ Utilities"])

# Standardized Layout for Tabs
def render_tab_ui(title, manual_logic, iceye_logic, settings_callback):
    st.markdown(f"## {title}")
    col_settings, col_visuals = st.columns([1, 2], gap="large")
    
    with col_settings:
        st.markdown("<p style='color:"+ICEYE_BLUE+"; font-weight:700;'>CONFIGURATIONS</p>", unsafe_allow_html=True)
        inputs = settings_callback()
    
    with col_visuals:
        m_cost = manual_logic(inputs)
        i_cost = iceye_logic(inputs)
        savings = m_cost - i_cost
        
        # Dashboard Cards
        v1, v2 = st.columns(2)
        with v1:
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>Manual Operational Burn</div><div class='metric-value'>${m_cost:,.0f}</div><div class='metric-delta' style='color:#FF4B4B;'>Baseline Expense</div></div>""", unsafe_allow_html=True)
        with v2:
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>ICEYE Augmented Cost</div><div class='metric-value'>${i_cost:,.0f}</div><div class='metric-delta'>Capability Optimized</div></div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='metric-card' style='border: 1px solid {ICEYE_BLUE};'><div class='metric-label'>Per Event Savings</div><div class='metric-value' style='color:{ICEYE_BLUE};'>${savings:,.0f}</div></div>""", unsafe_allow_html=True)
        
        return m_cost, i_cost

# --- TAB LOGIC ---
def council_settings():
    props = st.number_input("Impacted Properties", value=2500)
    inspectors = st.number_input("No. of Inspectors", value=12)
    hr_rate = st.number_input("Inspector Hourly Rate", value=175)
    truck = st.number_input("Truck Roll Admin Fee", value=550)
    gis_hrs = st.number_input("Manual Mapping Hrs", value=80)
    gis_rate = st.number_input("GIS Analyst Rate", value=210)
    verif_rate = st.slider("Field Verification Required %", 1, 100, 15)
    return (props, inspectors, hr_rate, truck, gis_hrs, gis_rate, verif_rate)

def council_manual(inputs):
    return (inputs[0] * 1.5 * inputs[2]) + (inputs[0] * inputs[3]) + (inputs[4] * inputs[5])

def council_iceye(inputs):
    # (Props * Verification% * 1.5h * Rate) + (Trucks * Verification%) + 4h Ingest
    return (inputs[0] * (inputs[6]/100) * 1.5 * inputs[2]) + (inputs[0] * (inputs[6]/100) * inputs[3]) + (4 * inputs[5])

with t1:
    m_c, i_c = render_tab_ui("Council Damage Assessment", council_manual, council_iceye, council_settings)

with t2:
    # Public Safety Logic (Condensed for space)
    st.markdown("### Public Safety Recon")
    p_heli = st.number_input("Helis Deployed", value=2)
    p_h_rate = st.number_input("Heli $/hr", value=6500)
    p_h_hrs = st.number_input("Manual Search Hrs", value=60)
    
    m_p = (p_heli * p_h_hrs * p_h_rate)
    i_p = (10 * p_h_rate) # Tactical only
    
    v1, v2 = st.columns(2)
    with v1: st.markdown(f"<div class='metric-card'><div class='metric-label'>Manual Air Search</div><div class='metric-value'>${m_p:,.0f}</div></div>", unsafe_allow_html=True)
    with v2: st.markdown(f"<div class='metric-card'><div class='metric-label'>ICEYE Air Recon</div><div class='metric-value'>${i_p:,.0f}</div></div>", unsafe_allow_html=True)

with t3:
    st.markdown("### Utility Grid Clearance")
    u_assets = st.number_input("Assets to Check", value=80)
    u_rate = st.number_input("Crew $/hr", value=225)
    u_truck = st.number_input("Heavy Vehicle Fee", value=850)
    u_clear = st.slider("SAR Remote Clearance %", 1, 100, 85)
    
    m_u = (u_assets * 4 * u_rate) + (u_assets * u_truck)
    i_u = (u_assets * (1-u_clear/100) * 4 * u_rate) + (u_assets * (1-u_clear/100) * u_truck)
    
    v1, v2 = st.columns(2)
    with v1: st.markdown(f"<div class='metric-card'><div class='metric-label'>Blind Patrols</div><div class='metric-value'>${m_u:,.0f}</div></div>", unsafe_allow_html=True)
    with v2: st.markdown(f"<div class='metric-card'><div class='metric-label'>SAR-Led Patrols</div><div class='metric-value'>${i_u:,.0f}</div></div>", unsafe_allow_html=True)

# --- 5. THE BOTTOM BAR (STICKY ROI) ---
st.divider()
total_savings = ((m_c + m_p + m_u) * annual_events) - (((i_c + i_p + i_u) * annual_events) + iceye_sub)

st.markdown(f"""
    <div style='background: linear-gradient(90deg, {ICEYE_BLUE} 0%, #1e40af 100%); padding: 40px; border-radius: 20px; text-align: center;'>
        <p style='color: white; font-weight: 800; letter-spacing: 3px; margin:0;'>TOTAL ANNUAL STRATEGIC DIVIDEND</p>
        <h1 style='color: white; font-size: 5rem; margin: 0;'>${total_savings:,.0f}</h1>
        <p style='color: rgba(255,255,255,0.7);'>Net of ICEYE Subscription & Manual Operational Reductions</p>
    </div>
""", unsafe_allow_html=True)
