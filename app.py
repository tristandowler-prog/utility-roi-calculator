import streamlit as st
import pandas as pd
import base64
from fpdf import FPDF

# --- 1. UI SETUP & BRANDING ---
st.set_page_config(page_title="ICEYE | Strategic ROI", layout="wide")
ICEYE_BLUE, ICEYE_DARK = "#39BBF0", "#0B0C10"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {ICEYE_DARK}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    .stTabs [data-baseweb="tab"] {{ height: 50px; background-color: #111827; color: #9CA3AF; font-weight: 700; }}
    .stTabs [aria-selected="true"] {{ background-color: {ICEYE_BLUE} !important; color: #000 !important; }}
    .formula-card {{ background: #111827; border: 1px solid {ICEYE_BLUE}44; padding: 15px; border-radius: 4px; margin: 10px 0; }}
    .math-text {{ font-family: 'Courier New', monospace; color: {ICEYE_BLUE}; font-size: 0.85rem; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL UNIT RATES (SIDEBAR) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=150)
    st.markdown("### 📊 UNIT COST CONTROL")
    
    with st.expander("🚁 AVIATION & ASSETS", expanded=True):
        heli_hr = st.number_input("Heli (Twin) $/hr", value=6500)
        plane_hr = st.number_input("Fixed-Wing $/hr", value=2800)
        truck_roll_cost = st.number_input("Truck Roll Admin Fee $", value=550)
        
    with st.expander("👷 GROUND & ANALYST", expanded=True):
        inspector_hr = st.number_input("Field Inspector $/hr", value=175)
        gis_hr = st.number_input("GIS Analyst $/hr", value=210)
    
    st.divider()
    annual_events = st.slider("Major Events / Year", 1, 5, 2)
    iceye_sub = st.number_input("ICEYE Annual Access Fee ($)", value=385000)

# --- 3. OPERATIONAL CALCULATOR ---
st.title("Strategic Capability & ROI Tool")
st.caption("Quantifying the 6-Hour 'Rapid Impact' and 24-Hour 'Flood Insights' Advantage")

t1, t2, t3 = st.tabs(["🏛️ LOCAL COUNCIL", "🚨 PUBLIC SAFETY", "⚡ UTILITIES"])

# --- TAB 1: COUNCIL (RDA & INSPECTIONS) ---
with t1:
    st.header("Council: Damage Assessment & GIS Latency")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.subheader("🔴 Manual RDA Lifecycle")
        c_props = st.number_input("Properties in Impact Zone", value=2500)
        c_inspectors = st.number_input("No. of Field Inspectors", value=12)
        c_hrs_per_prop = st.slider("Manual Hours / Prop (Drive + Log)", 0.5, 4.0, 1.5)
        c_gis_days = st.slider("Days to produce Manual Flood Map", 1, 10, 5)
        
        manual_c_labor = (c_props * c_hrs_per_prop * inspector_hr)
        manual_c_trucks = (c_props * truck_roll_cost)
        manual_c_gis = (c_gis_days * 8 * 2 * gis_hr) # 2 analysts
        manual_c_total = manual_c_labor + manual_c_trucks + manual_c_gis
        
        st.markdown(f"""<div class='formula-card'><p class='math-text'>(Props[{c_props}]*Hrs[{c_hrs_per_prop}]*${inspector_hr}) + (Props*${truck_roll_cost}) + (GIS Team Days)</p>
        <h2 style='color:#FF4B4B'>${manual_c_total:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with c_col2:
        st.subheader("🟢 ICEYE-Enabled Verification")
        st.info("⚡ ICEYE 24h Insights: Ready-to-use depth/extent GeoJSON.")
        c_verif_rate = st.slider("Field Verification Rate (%)", 5, 50, 15)
        iceye_c_total = (c_props * (c_verif_rate/100) * c_hrs_per_prop * inspector_hr) + \
                        (c_props * (c_verif_rate/100) * truck_roll_cost) + (4 * gis_hr) # 4 hrs integration
        
        st.markdown(f"""<div class='formula-card'><p class='math-text'>(Target-Props[{int(c_props*(c_verif_rate/100))}]*Labor+Trucks) + (4h GIS Integration)</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_c_total:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- TAB 2: PUBLIC SAFETY (RECON) ---
with t2:
    st.header("Public Safety: Mission Realignment")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.subheader("🔴 Manual Discovery")
        p_helis = st.number_input("Helis Deployed", 1, 10, 2)
        p_planes = st.number_input("Planes Deployed", 1, 5, 1)
        p_flight_hrs = st.number_input("Avg Flight Hrs per Asset", value=30)
        
        manual_ps = (p_helis * p_flight_hrs * heli_hr) + (p_planes * p_flight_hrs * plane_hr)
        st.markdown(f"<div class='formula-card'><h2 style='color:#FF4B4B'>${manual_ps:,.0f}</h2></div>", unsafe_allow_html=True)
    
    with p_col2:
        st.subheader("🟢 ICEYE Rapid Impact")
        st.info("⚡ ICEYE 6h Rapid Impact: 6-hourly heartbeat of observed extent.")
        p_tactical_heli = st.number_input("Tactical Heli Hrs (Rescue Only)", value=5)
        iceye_ps = (p_tactical_heli * heli_hr) + (8 * gis_hr)
        st.markdown(f"<div class='formula-card'><h2 style='color:{ICEYE_BLUE}'>${iceye_ps:,.0f}</h2></div>", unsafe_allow_html=True)

# --- TAB 3: UTILITIES (RESTORED TRUCK ROLLS) ---
with t3:
    st.header("Utility: Field Force Burn")
    u_col1, u_col2 = st.columns(2)
    with u_col1:
        u_assets = st.number_input("Substations/Assets", value=80)
        manual_u = (u_assets * 4 * inspector_hr) + (u_assets * truck_roll_cost)
        st.subheader("🔴 Blind Patrols")
        st.markdown(f"<div class='formula-card'><h2 style='color:#FF4B4B'>${manual_u:,.0f}</h2></div>", unsafe_allow_html=True)
    with u_col2:
        u_clearance = st.slider("SAR Remote Clearance %", 50, 95, 85)
        iceye_u = (u_assets * (1-u_clearance/100) * 4 * inspector_hr) + \
                  (u_assets * (1-u_clearance/100) * truck_roll_cost)
        st.subheader("🟢 SAR-Led Clearance")
        st.markdown(f"<div class='formula-card'><h2 style='color:{ICEYE_BLUE}'>${iceye_u:,.0f}</h2></div>", unsafe_allow_html=True)

# --- 4. SUMMARY & PDF ---
st.divider()
total_manual_pa = (manual_c_total + manual_ps + manual_u) * annual_events
total_iceye_pa = ((iceye_c_total + iceye_ps + iceye_u) * annual_events) + iceye_sub
net_dividend = total_manual_pa - total_iceye_pa

st.markdown(f"<div style='text-align:center; padding:30px; border:2px solid {ICEYE_BLUE};'><h3>NET ANNUAL STRATEGIC DIVIDEND</h3><h1 style='font-size:5rem;'>${net_dividend:,.0f}</h1></div>", unsafe_allow_html=True)

# PDF EXPORT LOGIC
def create_pdf(m, i, d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(40, 10, "ICEYE ROI Executive Briefing")
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.cell(40, 10, f"Annual Manual Operational Burn: ${m:,.0f}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Annual ICEYE-Augmented Cost: ${i:,.0f}")
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(40, 10, f"NET BUDGET DIVIDEND: ${d:,.0f}")
    return pdf.output(dest='S').encode('latin-1')

if st.button("Export Executive Briefing (PDF)"):
    pdf_bytes = create_pdf(total_manual_pa, total_iceye_pa, net_dividend)
    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="ICEYE_ROI_Briefing.pdf">Download PDF Briefing</a>', unsafe_allow_html=True)
