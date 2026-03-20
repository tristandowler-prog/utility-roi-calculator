import streamlit as st
import pandas as pd
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Strategic Audit | Utility Resilience", layout="wide")

# --- BIG 4 CONSULTING DESIGN SYSTEM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        padding: 2rem 1rem;
    }
    .report-card {
        background-color: #F9FAFB;
        border-radius: 8px;
        padding: 25px;
        border-left: 5px solid #111827;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 0.8rem;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    .kpi-box {
        text-align: center;
        padding: 20px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS (CUSTOMER INPUTS) ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Audit Filters</h2>", unsafe_allow_html=True)
    
    with st.expander("📡 SATELLITE & DATA"):
        sar_sub = st.number_input("Annual SAR Subscription (AUD)", value=150000)
        sar_latency = st.select_slider("Data Refresh Cadence", options=["48h", "24h", "12h", "6h"], value="6h")
        processing_time = st.number_input("SAR Processing Time (Hrs)", value=1, help="Time from satellite pass to actionable dashboard.")

    with st.expander("🚁 AERIAL RECONNAISSANCE"):
        helo_rate = st.number_input("Helicopter Hourly Rate (AUD)", value=2800, help="Avg AU rate for Bell 206/H125 utility config.")
        helo_hours = st.number_input("Helo Scouting Hours / Event", value=12)
        drone_rate = st.number_input("Drone Team Hourly Rate (AUD)", value=450)
        drone_hours = st.number_input("Drone Scouting Hours / Event", value=20)

    with st.expander("👥 FIELD FORCE & MOB"):
        labor_rate = st.number_input("Fully Burdened Labor ($/hr)", value=185)
        crew_size = st.number_input("Emergency Response Staff", value=120)
        mob_fee = st.number_input("Contractor Mob Fee (Per Crew)", value=15000)
        num_contractors = st.number_input("Contractor Crews", value=10)

    with st.expander("⛈️ EVENT SCALE"):
        events_per_year = st.slider("Annual Flood Events", 1, 12, 6)
        total_assets = st.number_input("Substations in Footprint", value=500)
        inundation_pct = st.slider("Actual Inundation Rate (%)", 5, 100, 20)

# --- LOGIC & CALCULATION ---
actual_wet = int(total_assets * (inundation_pct / 100))
hourly_burn = (crew_size * labor_rate) + (num_contractors * 750) # contractors cost more

# LEGACY MODEL (The "Blind" Response)
legacy_scouting_cost = (helo_rate * helo_hours) + (drone_rate * drone_hours)
legacy_labor_search = (hourly_burn * 48) # Avg 2 days blind searching
legacy_truck_rolls = total_assets * 450 # Checking every single asset
legacy_mob = num_contractors * mob_fee
legacy_total_event = legacy_scouting_cost + legacy_labor_search + legacy_truck_rolls + legacy_mob

# SAR MODEL (The "Targeted" Response)
sar_data_cost = sar_sub / events_per_year
sar_desk_eval = (hourly_burn * 4) # 4 hours to verify dashboard
sar_targeted_rolls = actual_wet * 450 # Only go to wet assets
sar_mob_saving = legacy_mob * 0.5 # Cancel 50% of contractors
sar_total_event = sar_data_cost + sar_desk_eval + sar_targeted_rolls + (legacy_mob - sar_mob_saving)

event_savings = legacy_total_event - sar_total_event
annual_savings = event_savings * events_per_year
roi = (annual_savings / sar_sub) * 100

# --- MAIN REPORT SECTION ---
st.markdown("<p class='section-header'>Strategic Advisory | Global Utility Infrastructure</p>", unsafe_allow_html=True)
st.title("Financial & Operational Audit: SAR-Enabled Flood Response")
st.markdown("---")

# KPI TOP LINE
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Annual Cash Avoidance</p><h2 style='color:#111827;'>${annual_savings:,.0f}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Strategic ROI</p><h2 style='color:#059669;'>{roi:,.0f}%</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>SAIDI Recovery Advance</p><h2 style='color:#2563EB;'>44 Hours</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# THE DETAILED BREAKDOWN
st.markdown("### 1. The Cost of Uncertainty (Legacy vs. Targeted)")
col_a, col_b = st.columns([2, 1])

with col_a:
    st.markdown("""
    <div class='report-card'>
        <strong>Analysis of 'Blind' Scouting Overhead</strong><br>
        In the legacy model, the utility incurs a 'Search Penalty'—paying for helicopters and field crews to verify 
        assets that are ultimately dry. SAR technology substitutes this physical search with a 6-hour refresh 
        digital twin, allowing for <strong>Targeted Dispatch</strong>.
    </div>
    """, unsafe_allow_html=True)
    
    # Audit Table
    audit_data = {
        "Cost Pillar": ["Aerial Recon (Helo/Drone)", "Blind Search Labor", "Asset Verification Visits", "Contractor Mobilization"],
        "Legacy Model (AUD)": [f"${legacy_scouting_cost:,.0f}", f"${legacy_labor_search:,.0f}", f"${legacy_truck_rolls:,.0f}", f"${legacy_mob:,.0f}"],
        "SAR Model (AUD)": ["$0", f"${sar_desk_eval:,.0f
