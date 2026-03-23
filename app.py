import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Executive ROI Analysis | Flood Response", layout="wide")

# --- INSTITUTIONAL DESIGN SYSTEM (WHITE/GREY/NAVY) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }
    
    /* Executive Card Style */
    .exec-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .section-header {
        color: #0F172A;
        font-weight: 700;
        font-size: 1.1rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-label {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .metric-value-large {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E293B;
        line-height: 1;
        margin: 10px 0;
    }
    
    .roi-positive { color: #059669; }
    .roi-negative { color: #DC2626; }
    
    /* Clean Sidebar */
    .css-1d391kg { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM PARAMETERS ---
with st.sidebar:
    st.markdown("### 🏦 CAPITAL ALLOCATION")
    annual_sub = st.number_input("Annual Solution Investment ($)", value=150000)
    event_freq = st.slider("Annual Major Events", 1, 8, 3)
    st.divider()
    st.markdown("### ⚡ EFFICIENCY TARGETS")
    sar_latency = st.slider("Data Latency (Hrs)", 4, 12, 6)
    precision_rate = st.slider("Dispatch Precision (%)", 60, 100, 95)

# --- HEADER ---
st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #64748B; font-weight: 400; margin-bottom: 0;'>STRATEGIC AUDIT</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 2.8rem; margin-top: 0; color: #0F172A;'>Flood Response Economic Impact</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# OPERATIONAL INPUTS (EXECUTIVE GRID)
# ==========================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='exec-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-header'>🚁 Aviation & Recon</p>", unsafe_allow_html=True)
    heli_rate = st.number_input("Heli Charter ($/hr)", value=3500)
    cloud_window = st.slider("Visual Blindness (Hrs)", 12, 96, 48, help="Cloud grounding period")
    drone_rate = st.number_input("Drone Team Standby ($/day)", value=2200)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='exec-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-header'>🚛 Strike Team Ops</p>", unsafe_allow_html=True)
    team_burn = st.number_input("Team Daily Burn ($)", value=12500)
    team_count = st.number_input("Active Strike Teams", value=6)
    dry_run_cost = st.number_input("Dry Run Penalty ($/unit)", value=2800)
    dry_run_freq = st.slider("Dry Runs Per Event", 0, 20, 8)
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='exec-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-header'>🛣️ Logistics & GIS</p>", unsafe_allow_html=True)
    freight_loss = st.number_input("Freight Loss ($/hr/road)", value=15000)
    hwy_count = st.number_input("Critical Corridors", value=2)
    gis_processing = st.slider("GIS Manual Labor (Hrs)", 2, 24, 8)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CALCULATION LOGIC
# ==========================================

# 1. Aviation Costs
leg_aviation = (heli_rate * 10 * (cloud_window/24)) + (drone_rate * (cloud_window/24))
fut_aviation = 0 

# 2. Strike Team Costs
leg_teams = (team_count * team_burn * (cloud_window/24)) + (dry_run_freq * dry_run_cost)
# SAR allows deterministic tasking; dry runs drop by 90%
fut_teams = (team_count * team_burn * (sar_latency/24)) + (dry_run_freq * 0.1 * dry_run_cost)

# 3. Logistics Costs (The Verification Gap)
leg_gap = cloud_window + gis_processing
fut_gap = sar_latency
leg_logistics = (freight_loss * hwy_count * leg_gap)
fut_logistics = (freight_loss * hwy_count * fut_gap)

# 4. Net Position
per_event_saving = (leg_aviation + leg_teams + leg_logistics) - (fut_aviation + fut_teams + fut_logistics)
annual_net_saving = (per_event_saving * event_freq) - annual_sub

# ==========================================
# RESULTS DASHBOARD
# ==========================================
st.markdown("<p class='section-header'>Annual Financial Performance</p>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"<div class='exec-card'><p class='metric-label'>Aviation Offset</p><p class='metric-value-large'>${(leg_aviation * event_freq)/1e3:.0f}K</p></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='exec-card'><p class='metric-label'>Ops Efficiency</p><p class='metric-value-large'>${((leg_teams - fut_teams) * event_freq)/1e3:.0f}K</p></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='exec-card'><p class='metric-label'>Logistics Recovery</p><p class='metric-value-large'>${((leg_logistics - fut_logistics) * event_freq)/1e6:.1f}M</p></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='exec-card'><p class='metric-label'>Net Annual ROI</p><p class='metric-value-large roi-positive'>${annual_net_saving/1e6:.2f}M</p></div>", unsafe_allow_html=True)

# --- STRATEGIC VISUALS ---
st.markdown("### Decision Latency Impact")
v1, v2 = st.columns([2, 1])

with v1:
    st.markdown("<div class='exec-card'>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Category": ["Aviation Ops", "Strike Team Waste", "Freight Downtime"],
        "Legacy (Visual Dependent)": [leg_aviation, leg_teams, leg_logistics],
        "Deterministic (ICEYE)": [fut_aviation, fut_teams, fut_logistics]
    }).set_index("Category")
    st.bar_chart(chart_data, height=350)
    st.markdown("</div>", unsafe_allow_html=True)

with v2:
    st.markdown("<div class='exec-card' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<p class='section-header'>Summary</p>", unsafe_allow_html=True)
    st.write(f"""
    By bypassing the **{cloud_window}-hour visual blind spot**, the response moves from reactive searching to deterministic execution.
    
    **Key Lever:** The "Verification Gap" for major corridors is reduced from **{leg_gap} hours** to **{fut_gap} hours**, 
    recovering **${(leg_logistics - fut_logistics)/1e6:.1f}M** in economic productivity per event.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8rem; padding: 40px;'>CONFIDENTIAL STRATEGIC ANALYSIS | PREPARED FOR EXECUTIVE LEADERSHIP</p>", unsafe_allow_html=True)
