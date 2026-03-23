import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="ROI Audit", layout="wide")

# --- NO-BULLSHIT AUDIT STYLING (BLACK, WHITE, GREY) ---
st.markdown("""
<style>
    /* Force high contrast for all text */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    /* Ensure all input labels are solid black */
    label, p, span, div {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    /* Simple grey boxes for sectioning */
    .audit-section {
        background-color: #F2F2F2;
        border: 1px solid #000000;
        padding: 20px;
        margin-bottom: 20px;
    }
    .roi-box {
        background-color: #000000;
        color: #FFFFFF !important;
        padding: 20px;
        text-align: center;
    }
    .roi-box p, .roi-box h1, .roi-box span {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER (REVERTED) ---
st.title("Emergency Response ROI Analysis")
st.markdown("---")

# --- TOP ROW: THE MONEY (NO SCROLL) ---
# We calculate first so the numbers appear at the top
with st.sidebar:
    st.header("FIXED COSTS")
    sub_cost = st.number_input("Annual ICEYE Subscription ($)", value=150000)
    events_year = st.slider("Events Per Year", 1, 10, 3)
    sar_latency = st.slider("SAR Latency (Hrs)", 4, 12, 6)

# INPUTS (Black text on White/Grey)
c1, c2, c3, c4 = st.columns(4)
with c1:
    cloud_blind_hrs = st.number_input("Cloud Blindness (Hrs)", value=48)
with c2:
    gis_process_hrs = st.number_input("GIS Manual Processing (Hrs)", value=8)
with c3:
    team_count = st.number_input("Active Strike Teams", value=6)
with c4:
    hwy_count = st.number_input("Impacted Highways", value=2)

# --- MATH ENGINE ---
# Legacy: Cloud Window + GIS Bottleneck
leg_wait = cloud_blind_hrs + gis_process_hrs
fut_wait = sar_latency

# 1. Aviation & GIS Labor
leg_aviation = (3500 * 10 * (cloud_blind_hrs/24)) + (2200 * (cloud_blind_hrs/24))
leg_gis_labor = (gis_process_hrs * 120 * 2) 

# 2. Strike Teams (Idle Burn + Dry Runs)
leg_personnel = (team_count * 12500 * (cloud_blind_hrs/24)) + (8 * 2800)
fut_personnel = (team_count * 12500 * (sar_latency/24)) + (1 * 2800)

# 3. Freight
leg_freight = (15000 * hwy_count * leg_wait)
fut_freight = (15000 * hwy_count * fut_wait)

# ROIs
event_saving = (leg_aviation + leg_gis_labor + leg_personnel + leg_freight) - (fut_personnel + fut_freight)
total_annual_roi = (event_saving * events_year) - sub_cost

# --- RESULTS DASHBOARD (TOP OF PAGE) ---
r1, r2 = st.columns([1, 1.5])
with r1:
    st.markdown(f"""
    <div style='border: 2px solid black; padding: 20px;'>
        <p style='margin:0;'>ANNUAL OPS SAVING</p>
        <h2 style='margin:0;'>${((leg_aviation + leg_gis_labor + leg_personnel - fut_personnel)*events_year)/1e3:.0f}K</h2>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class='roi-box'>
        <p style='margin:0; letter-spacing: 2px;'>NET ANNUAL ROI</p>
        <h1 style='margin:0; font-size: 3.5rem;'>${total_annual_roi/1e6:.2f}M</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Operational Audit Breakdown")

# --- CHART ---
chart_df = pd.DataFrame({
    "Category": ["Aviation/GIS", "Strike Teams", "Freight"],
    "Legacy Model ($)": [leg_aviation + leg_gis_labor, leg_personnel, leg_freight],
    "ICEYE Model ($)": [0, fut_personnel, fut_freight]
}).set_index("Category")
st.bar_chart(chart_df)

st.markdown(f"""
**Key Strategic Outcome:**
Bypassing the cloud window and GIS bottleneck saves **{leg_wait - fut_wait} hours** per event. 
This is not 'magic'—it is the deterministic removal of idle time for Strike Teams and the acceleration of highway reopening.
""")
