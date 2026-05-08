import streamlit as st
import base64
from fpdf import FPDF

# --- 1. ENTERPRISE DESIGN SYSTEM (Clean, Professional, ROI-Focused) ---
st.set_page_config(page_title="ICEYE ROI Calculator", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Roboto', sans-serif;
    }
    
    /* ROI Card Styling */
    .roi-section {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .header-box {
        background: #1E3A8A;
        padding: 20px;
        border-radius: 8px;
        color: white;
        margin-bottom: 30px;
    }
    
    .comparison-header {
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
        padding-bottom: 10px;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 15px;
    }

    .manual-red { color: #B91C1C; font-weight: 700; }
    .iceye-blue { color: #1E3A8A; font-weight: 700; }
    
    /* Input field optimization */
    .stNumberInput label { font-weight: 600 !important; color: #475569 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. EXECUTIVE CONTROLS & CURRENCY ---
with st.container():
    st.markdown("""<div class='header-box'>
        <h1 style='margin:0;'>ICEYE | Strategic ROI Dashboard</h1>
        <p style='margin:0; opacity:0.8;'>Operational Impact Analysis & Resource Optimization</p>
    </div>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=140)
    st.markdown("### 🗺️ GLOBAL PARAMETERS")
    currency = st.selectbox("Currency Selection", ["AUD", "NZD", "USD", "EUR"])
    annual_events = st.number_input("Major Events / Year", value=2)
    iceye_sub = st.number_input("Annual ICEYE Service Fee", value=385000)
    st.divider()
    st.info("Input actual agency/utility costs below to generate a transparent comparison.")

symbol = {"AUD": "$", "NZD": "$", "USD": "$", "EUR": "€"}[currency]

# --- 3. VERTICAL CALCULATIONS ---
t1, t2, t3 = st.tabs(["🏛️ LOCAL COUNCIL", "🚨 EMERGENCY SERVICES", "⚡ UTILITIES"])

def render_inputs(key_prefix):
    col_a, col_b = st.columns(2)
    with col_a:
        teams = st.number_input("Number of Field Teams", value=10, key=f"{key_prefix}_teams")
        team_rate = st.number_input("Field Team Rate (per hr)", value=225, key=f"{key_prefix}_t_rate")
        trucks = st.number_input("Truck Rolls (per event)", value=120, key=f"{key_prefix}_trucks")
        truck_cost = st.number_input("Cost per Truck Roll", value=650, key=f"{key_prefix}_tr_cost")
    with col_b:
        helis = st.number_input("Number of Helicopters", value=2, key=f"{key_prefix}_helis")
        heli_rate = st.number_input("Heli Rate (per hr)", value=6500, key=f"{key_prefix}_h_rate")
        planes = st.number_input("Number of Airplanes", value=1, key=f"{key_prefix}_planes")
        plane_rate = st.number_input("Plane Rate (per hr)", value=2800, key=f"{key_prefix}_p_rate")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        gis_hours = st.number_input("Manual GIS Digitizing (Total Man-Hours)", value=140, key=f"{key_prefix}_gis_h")
        gis_rate = st.number_input("GIS Analyst Rate (per hr)", value=185, key=f"{key_prefix}_gis_r")
    with c2:
        latency = st.number_input("Data-to-Insight Latency (Total Hours)", value=72, key=f"{key_prefix}_latency", help="Time burden to produce actionable intel.")
    
    return {
        "teams": teams, "team_rate": team_rate, "trucks": trucks, "truck_cost": truck_cost,
        "helis": helis, "h_rate": heli_rate, "planes": planes, "p_rate": plane_rate,
        "gis_h": gis_hours, "gis_r": gis_rate, "latency": latency
    }

# --- TAB 1: COUNCIL ---
with t1:
    st.markdown("<div class='roi-section'>", unsafe_allow_html=True)
    st.subheader("Council Damage Assessment & RDA")
    data = render_inputs("council")
    
    # Manual Logic: 40 hours per team + Trucks + Aviation + GIS
    manual_council = (data['teams'] * 40 * data['team_rate']) + (data['trucks'] * data['truck_cost']) + \
                     (data['helis'] * 20 * data['h_rate']) + (data['gis_h'] * data['gis_r'])
    
    # ICEYE Logic: 80% Reduction in field/truck, 0 Aviation (Search), 4hr GIS
    iceye_council = (data['teams'] * 8 * data['team_rate']) + (data['trucks'] * 0.2 * data['truck_cost']) + \
                    (4 * data['gis_r'])
    
    c1, c2 = st.columns(2)
    c1.metric("Current Operational Burn", f"{symbol}{manual_council:,.0f}", delta="Manual Process", delta_color="inverse")
    c2.metric("ICEYE Augmented Cost", f"{symbol}{iceye_council:,.0f}", delta=f"{data['latency'] - 6}h Faster Insight")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: EMERGENCY SERVICES ---
with t2:
    st.markdown("<div class='roi-section'>", unsafe_allow_html=True)
    st.subheader("Emergency Services: Search & Rescue Recon")
    data_es = render_inputs("es")
    
    manual_es = (data_es['helis'] * data_es['latency'] * data_es['h_rate']) + \
                (data_es['planes'] * data_es['latency'] * data_es['p_rate']) + (data_es['gis_h'] * data_es['gis_r'])
    
    # ICEYE Logic: No search flights, 5h tactical rescue flights only
    iceye_es = (data_es['helis'] * 5 * data_es['h_rate']) + (8 * data_es['gis_r'])
    
    c1, c2 = st.columns(2)
    c1.metric("Blind Search Expense", f"{symbol}{manual_es:,.0f}", delta="Risk Exposure High", delta_color="inverse")
    c2.metric("Informed Ops Cost", f"{symbol}{iceye_es:,.0f}", delta="SAR Clearance Provided")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: UTILITIES ---
with t3:
    st.markdown("<div class='roi-section'>", unsafe_allow_html=True)
    st.subheader("Utility Infrastructure Grid Clearance")
    data_u = render_inputs("util")
    
    # Manual: Full patrol of all assets
    manual_u = (data_u['teams'] * 60 * data_u['team_rate']) + (data_u['trucks'] * data_u['truck_cost'])
    
    # ICEYE: 85% Remote Clearance via SAR
    iceye_u = (manual_u * 0.15) + (8 * data_u['gis_r'])
    
    c1, c2 = st.columns(2)
    c1.metric("Grid Inspection Burn", f"{symbol}{manual_u:,.0f}", delta="Slow Recovery", delta_color="inverse")
    c2.metric("SAR-Led Recovery", f"{symbol}{iceye_u:,.0f}", delta="85% Efficiency Gain")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. THE BOOMER ROI SUMMARY ---
st.divider()
total_man = (manual_council + manual_es + manual_u) * annual_events
total_ice = ((iceye_council + iceye_es + iceye_u) * annual_events) + iceye_sub
savings = total_man - total_ice

st.markdown(f"""
    <div style='background: #FFFFFF; border: 4px solid #1E3A8A; padding: 40px; border-radius: 8px; text-align: center;'>
        <h2 style='color: #1E3A8A; margin:0;'>TOTAL ANNUAL STRATEGIC DIVIDEND</h2>
        <h1 style='font-size: 5rem; color: #1E3A8A; margin: 10px 0;'>{symbol}{savings:,.0f}</h1>
        <p style='font-weight: bold; color: #475569;'>Net Savings based on {annual_events} events and ${iceye_sub:,.0f} Annual Investment</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. PDF EXPORT ---
if st.button("Generate Executive ROI Report (PDF)"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"ICEYE STRATEGIC ROI ANALYSIS ({currency})", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Current Manual Process Burn: {symbol}{total_man:,.0f}", ln=True)
    pdf.cell(200, 10, f"ICEYE-Augmented Process Cost: {symbol}{total_ice:,.0f}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"NET ANNUAL SAVINGS: {symbol}{savings:,.0f}", ln=True)
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="ICEYE_ROI_Analysis.pdf">Click here to download PDF</a>', unsafe_allow_html=True)
