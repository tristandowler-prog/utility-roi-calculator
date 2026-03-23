import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP: THE TITAN UI ---
st.set_page_config(page_title="ROI Analysis | Emergency Response", layout="wide")

# --- CSS: THE "1000% POP" DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0F172A, #020617);
        color: #F8FAFC;
    }
    
    /* Cinematic Glass Cards */
    .titan-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    
    /* Neon Accents */
    .neon-text {
        color: #00D1FF;
        text-shadow: 0 0 10px rgba(0, 209, 255, 0.5);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
    }
    
    .neon-border {
        border-left: 5px solid #00D1FF;
        padding-left: 20px;
    }

    /* Metric Styling */
    .metric-value-titan {
        font-size: 3rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        background: linear-gradient(to right, #FFFFFF, #94A3B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-box {
        text-align: center;
        padding: 60px 0 40px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='neon-text'>MISSION CONTROL</h2>", unsafe_allow_html=True)
    st.info("Calibrate the Deterministic Response Layer.")
    
    sub_cost = st.number_input("Annual Data Subscription ($)", value=150000)
    sar_latency = st.slider("Target Data Latency (Hrs)", 6, 24, 12)
    events_per_year = st.slider("Annual Major Events", 1, 12, 4)
    st.divider()
    efficiency_gain = st.slider("Dispatch Precision (%)", 50, 100, 90)

# --- HEADER SECTION ---
st.markdown("""
<div class='header-box'>
    <p style='letter-spacing: 5px; color: #00D1FF; font-weight: 700;'>STRATEGIC CONTINUITY AUDIT</p>
    <h1 style='font-family: "Orbitron", sans-serif; font-size: 3.5rem; margin-top: -10px;'>Emergency Response ROI Analysis</h1>
</div>
""", unsafe_allow_html=True)

# --- TAB NAVIGATION ---
tab1, tab2 = st.tabs(["⚡ INFRASTRUCTURE RECOVERY", "🏛️ GOVERNMENT & DISASTER OPS"])

# ==========================================
# TAB 1: UTILITIES
# ==========================================
with tab1:
    st.markdown("<div class='titan-card neon-border'>", unsafe_allow_html=True)
    u1, u2 = st.columns([1, 2])
    with u1:
        st.markdown("### 🛠️ Network Variables")
        u_assets = st.number_input("Network Assets in Region", value=1200)
        u_impact = st.slider("Verified Impact Rate (%)", 5, 100, 20)
        u_crew = st.number_input("Field Crew Day Rate ($)", value=850)
        u_stpis = st.number_input("Regulatory Penalty ($/min)", value=125)
    
    with u2:
        # Logic Calculation
        exp_assets = int(u_assets * (u_impact/100))
        lat_gain = (48 - sar_latency)
        # Math remains defensible/unchanged
        leg_u = 85000 + ((u_assets - exp_assets) * u_crew) + (exp_assets * 0.45 * u_crew) + (exp_assets * u_stpis * (lat_gain * 60))
        tar_u = (exp_assets * u_crew)
        u_roi_total = ((leg_u * events_per_year) - (tar_u * events_per_year) - sub_cost)
        
        st.markdown("### 💎 Value Attribution")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Annual Protection**\n<div class='metric-value-titan'>${u_roi_total/1e6:.1f}M</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**Efficiency Gain**\n<div class='metric-value-titan'>{lat_gain}h</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: GOVERNMENT ROI WIZARD
# ==========================================
with tab2:
    # --- INPUT LAYER ---
    st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    
    with g1:
        st.markdown("<h4 class='neon-text'>🚁 AVIATION</h4>", unsafe_allow_html=True)
        heli_rate = st.number_input("Heli Charter ($/hr)", value=3500)
        heli_recon_hrs = st.number_input("Daily Recon Window", value=10)
        weather_grounding = st.slider("Cloud/Night Delay (Hrs)", 24, 96, 72)
        
    with g2:
        st.markdown("<h4 class='neon-text'>🚛 FIELD OPS</h4>", unsafe_allow_html=True)
        crew_daily = st.number_input("Personnel Burn ($/day)", value=450)
        crew_vol = st.number_input("Active Responders", value=100)
        waste_trip = st.number_input("Dry-Run Penalty ($/unit)", value=2800)
        waste_count = st.slider("Dry-Runs Per Event", 0, 50, 15)
        
    with g3:
        st.markdown("<h4 class='neon-text'>🛣️ LOGISTICS</h4>", unsafe_allow_html=True)
        freight_loss = st.number_input("Economic Loss ($/hr)", value=15000)
        num_corridors = st.number_input("Impacted HWYs", value=2)
        recovery_speed = st.slider("Targeted Reopening (Days)", 1, 14, 3)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- THE ENGINE ---
    gap_days = weather_grounding / 24
    
    # Yesterday: Probabilistic
    y_heli = (heli_rate * heli_recon_hrs * gap_days)
    y_burn = (crew_vol * crew_daily * gap_days)
    y_waste = (waste_count * waste_trip)
    y_freight = (num_corridors * freight_loss * (weather_grounding + sar_latency))
    
    # Tomorrow: Deterministic
    t_heli = 0 
    t_burn = y_burn * (1 - (efficiency_gain/100))
    t_waste = y_waste * 0.1
    t_freight = (num_corridors * freight_loss * sar_latency)
    
    total_savings = (y_heli + y_burn + y_waste + y_freight) - (t_heli + t_burn + t_waste + t_freight)
    annual_gov_roi = (total_savings * events_per_year) - sub_cost

    # --- VISUAL ACTION BOARD ---
    
    st.markdown("### ⚡ Operational Mechanics Breakdown")
    
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "Mechanical Layer": ["Aviation Standby", "Personnel Idling", "Dispatch Waste", "Economic Downtime"],
            "Legacy Model ($)": [y_heli, y_burn, y_waste, y_freight],
            "Deterministic Model ($)": [t_heli, t_burn, t_waste, t_freight]
        })
        st.bar_chart(chart_data.set_index("Mechanical Layer"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_v2:
        st.markdown(f"""
        <div class='titan-card neon-border'>
            <p class='m-title'>Net Annual Savings</p>
            <p class='metric-value-titan' style='color: #10B981;'>${annual_gov_roi/1e6:.2f}M</p>
            <p class='m-sub'>Based on {events_per_year} Optimized Events</p>
            <hr style='border: 0.5px solid rgba(255,255,255,0.1)'>
            <p style='font-size: 0.85rem; color: #94A3B8;'>
                By closing the <b>{weather_grounding - sar_latency} hour</b> information gap, 
                this framework reallocates capital from <i>Search & Scouting</i> to <i>Targeted Restoration</i>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- STRATEGIC PILLARS ---
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='titan-card'><b>Deterministic Dispatch</b><br><small>Redirecting crews from dry-zones to confirmed impact hotspots.</small></div>", unsafe_allow_html=True)
    p2.markdown("<div class='titan-card'><b>Cloud-Bypass Protocol</b><br><small>Eliminating the 72-hour 'blind-window' caused by severe weather.</small></div>", unsafe_allow_html=True)
    p3.markdown("<div class='titan-card'><b>Corridor Resilience</b><br><small>Reopening critical freight links hours before visual confirmation is possible.</small></div>", unsafe_allow_html=True)

# --- THE FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding-bottom: 40px;'>
    <p style='color: #64748B; font-size: 0.85rem; letter-spacing: 2px;'>
        PROPRIETARY RESILIENCE AUDIT | © 2026 STRATEGIC RESPONSE GROUP | CONFIDENTIAL
    </p>
</div>
""", unsafe_allow_html=True)
