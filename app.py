import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# --- 1. CORPORATE BRANDING & UI ---
st.set_page_config(page_title="ICEYE | Strategic ROI Intelligence", layout="wide", page_icon="🛰️")

# ICEYE Official Palette
ICEYE_BLUE = "#39BBF0"
ICEYE_BLACK = "#231F20"
ICEYE_DARK_GREY = "#0B0E14"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {ICEYE_DARK_GREY}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    .executive-card {{ 
        background: linear-gradient(135deg, #1E293B 0%, {ICEYE_BLACK} 100%);
        border-left: 5px solid {ICEYE_BLUE}; border-radius: 12px; padding: 25px; margin-bottom: 20px;
    }}
    .metric-value {{ font-size: 2.4rem; font-weight: 800; color: {ICEYE_BLUE}; }}
    .stButton>button {{ background-color: {ICEYE_BLUE}; color: white; border-radius: 8px; border: none; padding: 12px 30px; font-weight: bold; width: 100%; }}
    .stTabs [data-baseweb="tab"] {{ color: #94A3B8; font-size: 1.1rem; }}
    .stTabs [aria-selected="true"] {{ color: {ICEYE_BLUE} !important; border-bottom-color: {ICEYE_BLUE} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL UNIT COSTS (SIDEBAR) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=180)
    st.markdown("### 💰 Operational Burn Rates")
    
    with st.expander("🚁 Aviation & Drones", expanded=True):
        heli_hr = st.number_input("Heli Rate ($/hr)", value=5500)
        plane_hr = st.number_input("Plane Recon Rate ($/hr)", value=2200)
        drone_day = st.number_input("Drone Team (Daily)", value=4500)
        
    with st.expander("🚛 Field & GIS Teams", expanded=True):
        crew_hr = st.number_input("Field Crew (2p) $/hr", value=320)
        gis_hr = st.number_input("GIS Analyst Surge $/hr", value=195)
        truck_fee = st.number_input("Truck Roll Admin Fee $", value=450)
    
    st.divider()
    events_pa = st.slider("Events per Year", 1, 8, 3)
    iceye_sub = st.number_input("ICEYE Annual Subscription ($)", value=350000)

# --- 3. ROI ENGINE ---
st.title("🛰️ ICEYE Strategic Business Case")
st.markdown("#### Quantifying Hard-Cost Savings in Disaster Response")

tab1, tab2, tab3 = st.tabs(["🏛️ LOCAL COUNCIL", "⚡ UTILITIES", "🚨 EMERGENCY SERVICES"])

# --- TAB 1: COUNCIL ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔴 Current: Manual RDA")
        props = st.number_input("Properties to Inspect", value=2000, key="c1")
        insp_rate = st.slider("Inspections / Crew / Day", 5, 50, 15, key="c2")
        crews = st.number_input("Manual Crews Deployed", value=10, key="c3")
        
        days_c = props / (insp_rate * crews)
        manual_burn_c = (days_c * 8 * crews * crew_hr) + (crews * truck_fee * days_c)
        st.error(f"Manual Event Cost: ${manual_burn_c:,.0f}")
    
    with col2:
        st.markdown("### 🟢 Achievable: Focused Deployment")
        focus_factor = st.slider("Deployment Focus (%)", 50, 95, 80, key="c4", help="Percentage of dry properties skipped via SAR clearance.")
        iceye_burn_c = manual_burn_c * (1 - (focus_factor/100))
        st.success(f"ICEYE Event Cost: ${iceye_burn_c:,.0f}")

# --- TAB 2: UTILITIES ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔴 Current: Blind Patrols")
        assets = st.number_input("Assets to Verify", value=50, key="u1")
        patrol_t = st.slider("Patrol Time (Hrs/Site)", 1, 8, 4, key="u2")
        manual_u_burn = (assets * patrol_t * crew_hr) + (assets * truck_fee)
        st.error(f"Manual Event Cost: ${manual_u_burn:,.0f}")
    
    with col2:
        st.markdown("### 🟢 Achievable: Remote Clearance")
        clearance_r = st.slider("SAR Remote Clearance Rate (%)", 50, 95, 85, key="u4")
        iceye_u_burn = manual_u_burn * (1 - (clearance_r/100))
        st.success(f"ICEYE Event Cost: ${iceye_u_burn:,.0f}")

# --- TAB 3: EMERGENCY SERVICES ---
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔴 Current: Search & Recon")
        recon_h = st.number_input("Recon Flight Hours", value=30, key="e1")
        gis_m = st.number_input("Manual GIS Mapping Hrs", value=80, key="e2")
        # FIXED: Variable heli_rate changed to heli_hr to match sidebar
        manual_e_burn = (recon_h * heli_hr) + (gis_m * gis_hr)
        st.error(f"Manual Event Cost: ${manual_e_burn:,.0f}")
        
    with col2:
        st.markdown("### 🟢 Achievable: Targeted Action")
        # Assuming ICEYE eliminates the need for 'searching' and automates GIS
        iceye_e_burn = (gis_hr * 8) 
        st.success(f"ICEYE Event Cost: ${iceye_e_burn:,.0f}")

# --- 4. SUMMARY & PDF ---
st.divider()
total_manual_pa = (manual_burn_c + manual_u_burn + manual_e_burn) * events_pa
total_iceye_op_pa = (iceye_burn_c + iceye_u_burn + iceye_e_burn) * events_pa
net_savings = total_manual_pa - total_iceye_op_pa - iceye_sub

st.markdown(f"""
<div class="executive-card">
    <div style="color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.8rem;">Net Annual Strategic Dividend</div>
    <div class="metric-value">${net_savings:,.0f}</div>
    <div style="color: #94A3B8; font-size: 0.9rem; margin-top: 10px;">
        ROI: {((net_savings / iceye_sub) * 100) if iceye_sub > 0 else 0:.0f}% based on hard-cost reallocation.
    </div>
</div>
""", unsafe_allow_html=True)

def generate_pdf(m_burn, i_burn, s_val, sub_val):
    pdf = FPDF()
    pdf.add_page()
    # Dark Header
    pdf.set_fill_color(35, 31, 32)
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(57, 187, 240)
    pdf.cell(0, 20, "ICEYE STRATEGIC BUSINESS CASE", 0, 1, 'C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.ln(20)
    pdf.cell(0, 10, "ANNUAL OPERATIONAL SUMMARY", 0, 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, "Current Manual Response Burn:")
    pdf.cell(0, 10, f"${m_burn:,.0f}", 0, 1)
    pdf.cell(100, 10, "ICEYE-Optimized Response Burn:")
    pdf.cell(0, 10, f"${i_burn:,.0f}", 0, 1)
    pdf.cell(100, 10, "ICEYE Annual Subscription:")
    pdf.cell(0, 10, f"${sub_val:,.0f}", 0, 1)
    
    pdf.ln(10)
    pdf.set_fill_color(57, 187, 240)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, f" NET ANNUAL CAPABILITY DIVIDEND: ${s_val:,.0f} ", 0, 1, 'C', True)
    
    return pdf.output(dest='S').encode('latin-1')

if st.button("📊 GENERATE EXECUTIVE PDF REPORT"):
    pdf_out = generate_pdf(total_manual_pa, total_iceye_op_pa, net_savings, iceye_sub)
    b64_pdf = base64.b64encode(pdf_out).decode('latin-1')
    pdf_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="ICEYE_Business_Case.pdf">📥 Click here to download your report</a>'
    st.markdown(pdf_link, unsafe_allow_html=True)
