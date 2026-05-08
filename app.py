import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from fpdf import FPDF

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="ICEYE ROI Dashboard", layout="wide")

NAVY = "#1E3A8A"
SLATE = "#64748B"
SUCCESS = "#10B981"
BG_LIGHT = "#F8FAFC"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_LIGHT}; color: #1E293B; }}
    .main-header {{ background: white; padding: 20px; border-bottom: 2px solid #E2E8F0; margin-bottom: 20px; }}
    .card {{ background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 25px; margin-bottom: 20px; }}
    .stat-label {{ color: {SLATE}; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }}
    .stat-value {{ font-size: 2rem; font-weight: 800; color: {NAVY}; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL INPUTS ---
with st.container():
    st.markdown("<div class='main-header'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=120)
        st.subheader("Boomer ROI Dashboard")
    with c2:
        currency = st.selectbox("Currency", ["AUD", "NZD", "USD", "EUR"])
        sym = {"AUD": "$", "NZD": "$", "USD": "$", "EUR": "€"}[currency]
    with c3:
        annual_events = st.number_input("Events / Year", value=2)
    with c4:
        iceye_sub = st.number_input("ICEYE Subscription", value=385000)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. INPUT HANDLER ---
def get_vertical_inputs(key):
    st.markdown("#### ⚙️ Resource Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        teams = st.number_input(f"Field Teams", value=12, key=f"{key}_teams_in")
        t_rate = st.number_input(f"Team Hourly Rate", value=225, key=f"{key}_rate_in")
        trucks = st.number_input(f"Total Truck Rolls", value=150, key=f"{key}_trucks_in")
        tr_cost = st.number_input(f"Cost Per Truck Roll", value=650, key=f"{key}_tcost_in")
    with col2:
        helis = st.number_input(f"Helicopters", value=2, key=f"{key}_helis_in")
        h_rate = st.number_input(f"Heli Rate / Hr", value=6500, key=f"{key}_hrate_in")
        planes = st.number_input(f"Planes", value=1, key=f"{key}_planes_in")
        p_rate = st.number_input(f"Plane Rate / Hr", value=2800, key=f"{key}_prate_in")
    with col3:
        gis_h = st.number_input(f"Manual GIS Hours", value=140, key=f"{key}_gish_in")
        gis_r = st.number_input(f"GIS Analyst Rate", value=185, key=f"{key}_gisr_in")
        latency = st.number_input(f"Manual Latency (Hrs)", value=72, key=f"{key}_lat_in")
    return locals()

# --- 4. CALCULATION & PLOTTING (FIXED) ---
def calculate_and_plot(data, key_suffix):
    # Manual Logic
    m_labor = (data['teams'] * 40 * data['t_rate'])
    m_aviation = (data['helis'] * 30 * data['h_rate']) + (data['planes'] * 30 * data['p_rate'])
    m_logistics = (data['trucks'] * data['tr_cost'])
    m_intel = (data['gis_h'] * data['gis_r'])
    total_manual = m_labor + m_aviation + m_logistics + m_intel

    # ICEYE Logic
    i_labor = m_labor * 0.20 
    i_aviation = (data['helis'] * 5 * data['h_rate']) 
    i_logistics = m_logistics * 0.15 
    i_intel = (8 * data['gis_r']) 
    total_iceye = i_labor + i_aviation + i_logistics + i_intel

    # VIZ
    fig = go.Figure(data=[
        go.Bar(name='Manual Process', x=['Labor', 'Aviation', 'Trucks', 'GIS'], 
               y=[m_labor, m_aviation, m_logistics, m_intel], marker_color=SLATE),
        go.Bar(name='ICEYE Process', x=['Labor', 'Aviation', 'Trucks', 'GIS'], 
               y=[i_labor, i_aviation, i_logistics, i_intel], marker_color=NAVY)
    ])
    fig.update_layout(barmode='group', height=350, margin=dict(t=20, b=20, l=0, r=0), 
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown(f"""<div class='card'>
            <p class='stat-label'>Event Savings</p>
            <p class='stat-value' style='color:{SUCCESS}'>{sym}{total_manual - total_iceye:,.0f}</p>
            <p class='stat-label'>Insights Latency</p>
            <p class='stat-value'>6h <span style='font-size:1rem; color:{SLATE};'>vs {data['latency']}h</span></p>
        </div>""", unsafe_allow_html=True)
    with col_r:
        # ADDING UNIQUE KEY HERE PREVENTS DUPLICATE ID ERROR
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{key_suffix}")
    
    return total_manual, total_iceye

# --- 5. TABS ---
t1, t2, t3 = st.tabs(["🏛️ COUNCIL", "🚨 EMERGENCY SERVICES", "⚡ UTILITIES"])

with t1:
    d1 = get_vertical_inputs("council")
    m1, i1 = calculate_and_plot(d1, "council")

with t2:
    d2 = get_vertical_inputs("es")
    m2, i2 = calculate_and_plot(d2, "es")

with t3:
    d3 = get_vertical_inputs("util")
    m3, i3 = calculate_and_plot(d3, "util")

# --- 6. FINAL ROI ---
st.divider()
ann_manual = (m1 + m2 + m3) * annual_events
ann_iceye = ((i1 + i2 + i3) * annual_events) + iceye_sub
total_dividend = ann_manual - ann_iceye

st.markdown(f"""
    <div style='background:{NAVY}; padding: 40px; border-radius: 12px; text-align: center; color: white;'>
        <p style='margin:0; opacity:0.8; font-size: 1rem; letter-spacing: 2px; font-weight:bold;'>NET ANNUAL STRATEGIC DIVIDEND</p>
        <h1 style='font-size: 5rem; margin: 10px 0;'>{sym}{total_dividend:,.0f}</h1>
        <p style='margin:0;'>Consolidated across {annual_events} events per annum.</p>
    </div>
""", unsafe_allow_html=True)
