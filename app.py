import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="ICEYE Strategic ROI", layout="wide")

# --- HIGH-CONTRAST "REPORT" STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1A1A1A; font-family: 'Inter', sans-serif; }
    .main-metric-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .roi-card { background-color: #F0FDF4; border: 2px solid #16A34A; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .section-header { color: #0F172A; font-weight: 700; font-size: 1.1rem; margin-bottom: 15px; border-bottom: 2px solid #E2E8F0; padding-bottom: 5px; text-transform: uppercase;}
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #0F172A; margin: 5px 0;}
    .roi-value { font-size: 2.8rem; font-weight: 900; color: #16A34A; margin: 5px 0;}
    .label { font-size: 0.85rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Global Controls) ---
with st.sidebar:
    st.markdown("### 🏦 FIXED INVESTMENTS")
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000)
    events_per_year = st.slider("Major Flood Events / Year", 1, 10, 3)
    
    st.markdown("### 🛰️ ICEYE PERFORMANCE")
    sar_latency = st.slider("SAR Data Delivery (Hrs)", 4, 12, 6, help="Time from acquisition to analysis-ready data delivery.")

# --- TOP SECTION: FINANCIAL IMPACT (NO SCROLL) ---
st.markdown("<h1 style='font-size: 2.5rem; color: #0F172A; margin-bottom: 0;'>Strategic Response Economic Audit</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1.1rem; margin-bottom: 30px;'>Validating Deterministic Intelligence vs. Legacy Operations</p>", unsafe_allow_html=True)

# Main Levers (Moved up for immediate visibility)
c1, c2, c3, c4 = st.columns(4)
with c1:
    cloud_blind_hrs = st.number_input("Cloud Blindness (Hrs)", value=48)
with c2:
    gis_process_hrs = st.number_input("GIS Manual Processing (Hrs)", value=8)
with c3:
    team_count = st.number_input("Active Strike Teams", value=6)
with c4:
    hwy_count = st.number_input("Impacted Highways", value=2)

# --- THE CALCULATOR ENGINE ---
# TIME GAPS
leg_wait_total = cloud_blind_hrs + gis_process_hrs 
fut_wait_total = sar_latency # ICEYE delivers Analysis-Ready Data (ARD), eliminating manual GIS time

# 1. AVIATION & INTELLIGENCE COSTS
leg_aviation = (3500 * 10 * (cloud_blind_hrs/24)) + (2200 * (cloud_blind_hrs/24))
leg_gis_labor = (gis_process_hrs * 120 * 2) # Assumes 2 GIS officers at $120/hr
fut_aviation_gis = 0 # Replaced by ICEYE Subscription

# 2. STRIKE TEAM WASTE (Idle Burn + Dry Runs)
team_burn_rate = 12500
dry_run_penalty = 2800
leg_personnel = (team_count * team_burn_rate * (cloud_blind_hrs/24)) + (8 * dry_run_penalty)
fut_personnel = (team_count * team_burn_rate * (sar_latency/24)) + (1 * dry_run_penalty) # 90% reduction in dry runs

# 3. ECONOMIC FRICTION (Freight Delay)
freight_loss_hr = 15000
leg_freight = (freight_loss_hr * hwy_count * leg_wait_total)
fut_freight = (freight_loss_hr * hwy_count * fut_wait_total)

# AGGREGATES
leg_total_event = leg_aviation + leg_gis_labor + leg_personnel + leg_freight
fut_total_event = fut_aviation_gis + fut_personnel + fut_freight

event_saving = leg_total_event - fut_total_event
total_annual_roi = (event_saving * events_per_year) - annual_sub

# --- IMPACT DASHBOARD ---
m1, m2, m3 = st.columns([1, 1, 1.5])
with m1:
    ops_saving = (leg_aviation + leg_gis_labor + leg_personnel) - (fut_aviation_gis + fut_personnel)
    st.markdown(f"<div class='main-metric-card'><p class='label'>Ops & Personnel Recovery</p><p class='metric-value'>${(ops_saving * events_per_year)/1e3:.0f}K</p></div>", unsafe_allow_html=True)
with m2:
    freight_saving = leg_freight - fut_freight
    st.markdown(f"<div class='main-metric-card'><p class='label'>Economic / Freight Recovery</p><p class='metric-value'>${(freight_saving * events_per_year)/1e6:.1f}M</p></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='roi-card'><p class='label' style='color: #16A34A;'>Net Annual ROI (Post-Investment)</p><p class='roi-value'>${total_annual_roi/1e6:.2f}M</p></div>", unsafe_allow_html=True)

# --- SECONDARY AUDIT DATA ---
st.markdown("<p class='section-header'>Data Bottleneck Breakdown</p>", unsafe_allow_html=True)
col_chart, col_text = st.columns([2, 1])

with col_chart:
    chart_data = pd.DataFrame({
        "Cost Center": ["Aviation & GIS Labor", "Strike Team Waste", "Freight Downtime"],
        "Legacy Workflow ($)": [leg_aviation + leg_gis_labor, leg_personnel, leg_freight],
        "ICEYE ARD Workflow ($)": [fut_aviation_gis, fut_personnel, fut_freight]
    }).set_index("Cost Center")
    st.bar_chart(chart_data, height=350)

with col_text:
    st.markdown("### The Intelligence Gap")
    st.write(f"""
    Currently, logistics and field crews are frozen by a **{leg_wait_total}-hour intelligence gap** ({cloud_blind_hrs}hrs waiting for visibility + {gis_process_hrs}hrs manual map processing).
    
    By delivering Analysis-Ready Data (ARD) directly to the Common Operating Picture within **{fut_wait_total} hours**, 
    ICEYE completely bypasses both the weather and processing bottlenecks.
    """)
