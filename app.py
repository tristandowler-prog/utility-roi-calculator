import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from fpdf import FPDF

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="ICEYE ROI Dashboard", layout="wide")

# Professional Color Palette
NAVY = "#1E3A8A"
SLATE = "#64748B"
SUCCESS = "#10B981"
DANGER = "#EF4444"
BG_LIGHT = "#F8FAFC"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_LIGHT}; color: #1E293B; }}
    .main-header {{ background: white; padding: 20px; border-bottom: 2px solid #E2E8F0; margin-bottom: 20px; }}
    .card {{ background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 25px; margin-bottom: 20px; }}
    .stat-label {{ color: {SLATE}; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }}
    .stat-value {{ font-size: 2rem; font-weight: 800; color: {NAVY}; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700; color: {SLATE}; }}
    .stTabs [aria-selected="true"] {{ color: {NAVY} !important; border-bottom-color: {NAVY} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. TOP NAVIGATION / GLOBAL INPUTS ---
with st.container():
    st.markdown("<div class='main-header'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=120)
        st.subheader("Strategic ROI Dashboard")
    with c2:
        currency = st.selectbox("Currency", ["AUD", "NZD", "USD", "EUR"])
        sym = {"AUD": "$", "NZD": "$", "USD": "$", "EUR": "€"}[currency]
    with c3:
        annual_events = st.number_input("Events / Year", value=2)
    with c4:
        iceye_sub = st.number_input("ICEYE Subscription", value=385000)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. DYNAMIC INPUT HANDLER ---
def get_vertical_inputs(key):
    st.markdown("#### ⚙️ Resource Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        teams = st.number_input(f"Field Teams", value=12, key=f"{key}_t")
        t_rate = st.number_input(f"Team Hourly Rate", value=225, key=f"{key}_tr")
        trucks = st.number_input(f"Total Truck Rolls", value=150, key=f"{key}_tk")
        tr_cost = st.number_input(f"Cost Per Truck Roll", value=650, key=f"{key}_tc")
    with col2:
        helis = st.number_input(f"Helicopters Deployed", value=2, key=f"{key}_h")
        h_rate = st.number_input(f"Heli Rate / Hr", value=6500, key=f"{key}_hr")
        planes = st.number_input(f"Planes Deployed", value=1, key=f"{key}_p")
        p_rate = st.number_input(f"Plane Rate / Hr", value=2800, key=f"{key}_pr")
    with col3:
        gis_h = st.number_input(f"Manual GIS Hours", value=140, key=f"{key}_gh")
        gis_r = st.number_input(f"GIS Analyst Rate", value=185, key=f"{key}_gr")
        latency = st.number_input(f"Manual Latency (Hrs)", value=72, key=f"{key}_lt")
    return locals()

# --- 4. TABS & LOGIC ---
t1, t2, t3 = st.tabs(["🏛️ COUNCIL", "🚨 EMERGENCY SERVICES", "⚡ UTILITIES"])

def calculate_and_plot(data, title):
    # Manual Logic
    m_labor = (data['teams'] * 40 * data['t_rate'])
    m_aviation = (data['helis'] * 30 * data['h_rate']) + (data['planes'] * 30 * data['p_rate'])
    m_logistics = (data['trucks'] * data['tr_cost'])
    m_intel = (data['gis_h'] * data['gis_r'])
    total_manual = m_labor + m_aviation + m_logistics + m_intel

    # ICEYE Logic (Efficiency Gains)
    i_labor = m_labor * 0.20 # 80% reduction via focused deployment
    i_aviation = (data['helis'] * 5 * data['h_rate']) # Tactical only
    i_logistics = m_logistics * 0.15 # 85% reduction in dry truck rolls
    i_intel = (8 * data['gis_r']) # Fast ingestion
    total_iceye = i_labor + i_aviation + i_logistics + i_intel

    # Viz
    fig = go.Figure(data=[
        go.Bar(name='Manual Process', x=['Labor', 'Aviation', 'Truck Rolls', 'GIS/Intel'], 
               y=[m_labor, m_aviation, m_logistics, m_intel], marker_color=SLATE),
        go.Bar(name='ICEYE Process', x=['Labor', 'Aviation', 'Truck Rolls', 'GIS/Intel'], 
               y=[i_labor, i_aviation, i_logistics, i_intel], marker_color=NAVY)
    ])
    fig.update_layout(barmode='group', height=350, margin=dict(t=20, b=20, l=0, r=0), 
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown(f"""<div class='card'>
            <p class='stat-label'>Event Savings</p>
            <p class='stat-value' style='color:{SUCCESS}'>{sym}{total_manual - total_iceye:,.0f}</p>
            <p class='stat-label'>Time to Insight</p>
            <p class='stat-value'>6h <span style='font-size:1rem; color:{SLATE};'>vs {data['latency']}h</span></p>
        </div>""", unsafe_allow_html=True)
    with col_r:
        st.plotly_chart(fig, use_container_width=True)
    
    return total_manual, total_iceye

with t1:
    d1 = get_vertical_inputs("c")
    m1, i1 = calculate_and_plot(d1, "Council")

with t2:
    d2 = get_vertical_inputs("e")
    m2, i2 = calculate_and_plot(d2, "Emergency")

with t3:
    d3 = get_vertical_inputs("u")
    m3, i3 = calculate_and_plot(d3, "Utility")

# --- 5. FINAL FINANCIAL SUMMARY ---
st.divider()
ann_manual = (m1 + m2 + m3) * annual_events
ann_iceye = ((i1 + i2 + i3) * annual_events) + iceye_sub
total_dividend = ann_manual - ann_iceye

st.markdown(f"""
    <div style='background:{NAVY}; padding: 40px; border-radius: 12px; text-align: center; color: white;'>
        <h2 style='margin:0; opacity:0.8; font-size: 1rem; letter-spacing: 2px;'>TOTAL ANNUAL STRATEGIC DIVIDEND</h2>
        <h1 style='font-size: 5rem; margin: 10px 0;'>{sym}{total_dividend:,.0f}</h1>
        <p style='margin:0;'>Net Savings across {annual_events} events including subscription cost.</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. PDF EXPORT ---
if st.button("📥 DOWNLOAD EXECUTIVE BRIEFING"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"ICEYE STRATEGIC ROI REPORT ({currency})", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Annual Manual Operational Burn: {sym}{ann_manual:,.0f}", ln=True)
    pdf.cell(200, 10, f"Annual ICEYE Integrated Cost: {sym}{ann_iceye:,.0f}", ln=True)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 15, f"NET BUDGET DIVIDEND: {sym}{total_dividend:,.0f}", ln=True)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="ICEYE_ROI_Summary.pdf">Click here to save PDF</a>', unsafe_allow_html=True)
