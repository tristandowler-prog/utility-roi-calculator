import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# --- 1. ICEYE CORPORATE BRANDING (V3 - 2026) ---
ICEYE_BLUE = "#39BBF0"      # Electric Cyan
ICEYE_DARK = "#0B0C10"      # Space Black
ICEYE_GREY = "#1F2833"      # Radar Grey
ICEYE_WHITE = "#F0F2F5"     # Signal White

st.set_page_config(page_title="ICEYE | Persistent Monitoring ROI", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    .stApp {{ background-color: {ICEYE_DARK}; color: {ICEYE_WHITE}; font-family: 'Inter', sans-serif; }}
    
    /* Global Header Style */
    h1 {{ font-weight: 900; letter-spacing: -1.5px; color: {ICEYE_WHITE}; text-transform: uppercase; }}
    h2, h3 {{ color: {ICEYE_BLUE}; font-weight: 700; letter-spacing: -0.5px; }}
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {{ background-color: #000000; border-right: 1px solid {ICEYE_BLUE}44; }}
    
    /* Metrics & Cards */
    .metric-card {{
        background: {ICEYE_GREY};
        border: 1px solid {ICEYE_BLUE}33;
        padding: 24px; border-radius: 4px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }}
    .metric-title {{ color: {ICEYE_BLUE}; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; }}
    .metric-val {{ font-size: 2.2rem; font-weight: 900; color: #FFFFFF; }}
    
    /* Radar Effect Button */
    .stButton>button {{
        background: transparent; color: {ICEYE_BLUE};
        border: 2px solid {ICEYE_BLUE}; border-radius: 0px;
        font-weight: 900; text-transform: uppercase; letter-spacing: 2px;
        transition: all 0.3s ease; width: 100%;
    }}
    .stButton>button:hover {{ background: {ICEYE_BLUE}; color: #000; box-shadow: 0 0 20px {ICEYE_BLUE}66; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE "HARD BURN" INPUTS (OPERATIONAL PRECISION) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=160)
    st.markdown("### OPERATIONAL PARAMETERS")
    
    with st.expander("🚁 AERIAL RECONNAISSANCE", expanded=True):
        # 2026 AU Market Rates
        heli_rate = st.number_input("Heli $/hr (Twin Engine)", value=6200)
        plane_rate = st.number_input("Fixed-Wing Recon $/hr", value=2800)
        drone_day_rate = st.number_input("Drone Team (2p) $/day", value=4800)
        drone_teams_qty = st.slider("Active Drone Teams", 1, 20, 5)

    with st.expander("🚛 GROUND FORCE & DATA", expanded=False):
        truck_roll_cost = st.number_input("Truck Roll Admin (Per unit)", value=550)
        field_crew_hr = st.number_input("Field Crew (2p) $/hr", value=345)
        gis_analyst_hr = st.number_input("Senior GIS Analyst $/hr", value=210)

    st.divider()
    annual_events = st.slider("Major Flood Events p.a.", 1, 5, 3)
    iceye_access_fee = st.number_input("ICEYE Annual Access ($)", value=425000)

# --- 3. ROI ENGINE: THE THREE VERTICALS ---
st.title("Strategic ROI Analysis")
st.caption("Quantifying the Persistent Monitoring Advantage vs. Point-in-Time Reconnaissance")

tab1, tab2, tab3 = st.tabs(["🏛️ GOVERNMENT/COUNCIL", "⚡ CRITICAL UTILITIES", "🚨 PUBLIC SAFETY"])

# COUNCIL LOGIC
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-card'><p class='metric-title'>Current State: Blind Recon</p>", unsafe_allow_html=True)
        c_props = st.number_input("LGA Buildings in Hazard Zone", 1000, 10000, 3500)
        c_scout_days = st.slider("Days spent 'finding' damage", 3, 14, 7)
        # Total cost of finding the damage (Drones + Trucks)
        c_manual_cost = (c_scout_days * drone_teams_qty * drone_day_rate) + (c_props * 0.5 * truck_roll_cost)
        st.markdown(f"<p class='metric-val'>${c_manual_cost:,.0f}</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'><p class='metric-title'>ICEYE: Precision Verification</p>", unsafe_allow_html=True)
        # ICEYE eliminates the 'finding' phase. Field work becomes 'verification' of SAR data.
        c_iceye_cost = (c_manual_cost * 0.15) + (gis_analyst_hr * 40)
        st.markdown(f"<p class='metric-val'>${c_iceye_cost:,.0f}</p></div>", unsafe_allow_html=True)

# UTILITIES LOGIC
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-card'><p class='metric-title'>Current: Reactive Patrols</p>", unsafe_allow_html=True)
        u_sites = st.number_input("Critical Substations/Assets", 20, 200, 80)
        u_recon_hrs = st.number_input("Heli Patrol Hours (Post-Event)", 5, 50, 20)
        u_manual_cost = (u_recon_hrs * heli_rate) + (u_sites * truck_roll_cost)
        st.markdown(f"<p class='metric-val'>${u_manual_cost:,.0f}</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'><p class='metric-title'>ICEYE: Digital Clearance</p>", unsafe_allow_html=True)
        u_iceye_cost = (u_manual_cost * 0.05) + (gis_analyst_hr * 16) # Remote SAR clearance
        st.markdown(f"<p class='metric-val'>${u_iceye_cost:,.0f}</p></div>", unsafe_allow_html=True)

# PUBLIC SAFETY LOGIC
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-card'><p class='metric-title'>Current: Information Gap</p>", unsafe_allow_html=True)
        s_recon_hrs = st.number_input("Aerial Recon Flight Hours", 10, 100, 40)
        s_manual_cost = (s_recon_hrs * plane_rate) + (s_recon_hrs * 0.5 * heli_rate)
        st.markdown(f"<p class='metric-val'>${s_manual_cost:,.0f}</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'><p class='metric-title'>ICEYE: Targeted Rescue</p>", unsafe_allow_html=True)
        s_iceye_cost = (gis_analyst_hr * 24) # Data feed into command center
        st.markdown(f"<p class='metric-val'>${s_iceye_cost:,.0f}</p></div>", unsafe_allow_html=True)

# --- 4. EXECUTIVE RECON: AGGREGATED ROI ---
st.divider()
annual_manual = (c_manual_cost + u_manual_cost + s_manual_cost) * annual_events
annual_iceye_ops = (c_iceye_cost + u_iceye_cost + s_iceye_cost) * annual_events
net_return = annual_manual - annual_iceye_ops - iceye_access_fee

st.markdown(f"""
<div style="text-align: center; margin: 40px 0;">
    <p style="color: {ICEYE_BLUE}; letter-spacing: 5px; font-weight: 900; margin-bottom: 0;">ANNUAL OPERATIONAL ALPHA</p>
    <h1 style="font-size: 6rem; margin-top: -10px;">${net_return:,.0f}</h1>
    <p style="color: #94A3B8; font-size: 1.2rem;">Net Financial Benefit after ICEYE Implementation</p>
</div>
""", unsafe_allow_html=True)

# --- 5. PDF EXPORT (CRISP & CLEAN) ---
def generate_iceye_pdf(m_burn, i_burn, net, sub):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(11, 12, 16) # ICEYE Dark
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_font("Arial", 'B', 30)
    pdf.set_text_color(57, 187, 240) # ICEYE Blue
    pdf.cell(0, 40, "ICEYE ROI REPORT", 0, 1, 'L')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(240, 242, 245)
    pdf.cell(0, 10, f"Annual Manual Operational Burn: ${m_burn:,.0f}", 0, 1)
    pdf.cell(0, 10, f"Annual ICEYE-Augmented Burn: ${i_burn:,.0f}", 0, 1)
    pdf.cell(0, 10, f"ICEYE Platform Access: ${sub:,.0f}", 0, 1)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, f"NET ANNUAL GAIN: ${net:,.0f}", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

if st.button("Generate Executive Briefing (PDF)"):
    pdf_bytes = generate_iceye_pdf(annual_manual, annual_iceye_ops, net_return, iceye_access_fee)
    b64 = base64.b64encode(pdf_bytes).decode('latin-1')
    st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="ICEYE_ROI_Briefing.pdf">DOWNLOAD PDF</a>', unsafe_allow_html=True)
