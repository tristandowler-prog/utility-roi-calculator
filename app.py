import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# --- 1. CORPORATE BRANDING & UI ---
st.set_page_config(page_title="ICEYE | Strategic ROI Intelligence", layout="wide", page_icon="🛰️")

# ICEYE Official Hex Codes
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
    .stButton>button {{ background-color: {ICEYE_BLUE}; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL UNIT COSTS (The Hard Burn) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=180)
    st.markdown("### 🛠️ Operational Baseline")
    
    with st.expander("🚁 Aviation & Drones", expanded=True):
        heli_hr = st.number_input("Heli Rate ($/hr)", value=5500)
        plane_hr = st.number_input("Plane Recon Rate ($/hr)", value=2200)
        drone_day = st.number_input("Drone Team (Daily)", value=4500)
        
    with st.expander("🚛 Field & GIS Teams", expanded=True):
        crew_hr = st.number_input("Field Crew (2p) $/hr", value=320)
        gis_hr = st.number_input("GIS Analyst Surge $/hr", value=195)
        truck_fee = st.number_input("Truck Roll Admin Fee $", value=450)
    
    events_pa = st.slider("Significant Events / Year", 1, 8, 3)
    iceye_sub = st.number_input("ICEYE Annual Subscription", value=350000)

# --- 3. ROI LOGIC & TABS ---
st.title("🛰️ ICEYE Flood Insights: Strategic ROI")
st.markdown("#### Quantifying the Information Gap in Disaster Response")

tab1, tab2, tab3 = st.tabs(["🏛️ LOCAL COUNCIL", "⚡ UTILITIES", "🚨 EMERGENCY SERVICES"])

# --- TAB 1: COUNCIL ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Current: Manual RDA")
        props = st.number_input("Properties to Inspect", value=2000, key="c1")
        insp_rate = st.slider("Inspections / Crew / Day", 5, 50, 15, key="c2")
        crews = st.number_input("Manual Crews", value=10, key="c3")
        
        days_c = props / (insp_rate * crews)
        manual_burn_c = (days_c * 8 * crews * crew_hr) + (crews * truck_fee * days_c)
        st.error(f"Manual Event Cost: ${manual_burn_c:,.0f}")
    
    with col2:
        st.subheader("🟢 Achievable: Focused Deployment")
        focus_factor = st.slider("Focused Efficiency (%)", 50, 95, 80, key="c4")
        iceye_burn_c = manual_burn_c * (1 - (focus_factor/100))
        st.success(f"ICEYE Event Cost: ${iceye_burn_c:,.0f}")

# --- TAB 2: UTILITIES ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Current: Waiting for Clearance")
        assets = st.number_input("Assets to Verify", value=50, key="u1")
        patrol_t = st.slider("Patrol Time (Hrs/Site)", 1, 8, 4, key="u2")
        manual_u_burn = (assets * patrol_t * crew_hr) + (assets * truck_fee)
        st.error(f"Manual Event Cost: ${manual_u_burn:,.0f}")
    
    with col2:
        st.subheader("🟢 Achievable: Remote Clearance")
        clearance_r = st.slider("SAR Remote Clearance Rate (%)", 50, 95, 85, key="u4")
        iceye_u_burn = manual_u_burn * (1 - (clearance_r/100))
        st.success(f"ICEYE Event Cost: ${iceye_u_burn:,.0f}")

# --- TAB 3: EMERGENCY SERVICES ---
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Current: Search & Recon")
        recon_h = st.number_input("Recon Flight Hrs", value=30, key="e1")
        gis_m = st.number_input("Manual Mapping Hrs", value=80, key="e2")
        manual_e_burn = (recon_h * heli_rate) + (gis_m * gis_hr)
        st.error(f"Manual Event Cost: ${manual_e_burn:,.0f}")
        
    with col2:
        st.subheader("🟢 Achievable: Tactical Allocation")
        iceye_e_burn = (gis_hr * 8) # Automation saves 90% of recon and GIS labor
        st.success(f"ICEYE Event Cost: ${iceye_e_burn:,.0f}")

# --- 4. THE PDF EXPORT ---
def create_pdf(manual, iceye, savings, sub):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(35, 31, 32) # ICEYE Black
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(57, 187, 240) # ICEYE Blue
    pdf.cell(0, 20, "ICEYE STRATEGIC BUSINESS CASE", 0, 1, 'C')
    
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.ln(10)
    pdf.cell(0, 10, f"Annual Manual Burn: ${manual:,.0f}", 0, 1)
    pdf.cell(0, 10, f"Annual ICEYE Burn: ${iceye:,.0f}", 0, 1)
    pdf.cell(0, 10, f"Annual Subscription: ${sub:,.0f}", 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, f"NET ANNUAL SAVINGS: ${savings:,.0f}", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

st.divider()
total_manual = (manual_burn_c + manual_u_burn + manual_e_burn) * events_pa
total_iceye_op = (iceye_burn_c + iceye_u_burn + iceye_e_burn) * events_pa
net_gain = total_manual - total_iceye_op - iceye_sub

st.markdown(f"""
<div class="executive-card">
    <div style="color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px;">Annual Strategic Capability Dividend</div>
    <div class="metric-value">${net_gain:,.0f}</div>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Export Executive Business Case (PDF)"):
    pdf_data = create_pdf(total_manual, total_iceye_op, net_gain, iceye_sub)
    b64 = base64.b64encode(pdf_data).decode('latin-1')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="ICEYE_Business_Case.pdf">Click here to download</a>'
    st.markdown(href, unsafe_allow_html=True)
