import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP: WIZARD MODE ---
st.set_page_config(page_title="Flood Solutions | ROI Wizard", layout="wide")

# --- CUSTOM "BEST-IN-CLASS" CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #1E293B, #0F172A, #020617);
        color: #F8FAFC;
    }
    
    /* Glass-Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Dynamic Metric Blades */
    .metric-blade {
        border-left: 4px solid #38BDF8;
        padding-left: 20px;
        margin: 15px 0;
    }
    .m-title { font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }
    .m-value { font-size: 2.2rem; font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #FFFFFF; }
    .m-sub { font-size: 0.85rem; color: #38BDF8; font-weight: 500; }
    
    /* Comparison Header */
    .vs-header {
        text-align: center;
        padding: 40px 0;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .status-pill {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL SIDEBAR ---
with st.sidebar:
    st.markdown("## 🛰️ Intelligence Layer")
    st.info("Define the operational baseline.")
    
    sub_cost = st.number_input("Annual Data Subscription ($)", value=150000)
    sar_latency = st.slider("Satellite Latency (Hours)", 6, 24, 12)
    events_per_year = st.slider("Flood Events / Year", 1, 10, 4)
    
    st.divider()
    st.markdown("### 🛠️ Response Logic")
    confidence_gain = st.slider("Targeting Efficiency Gain (%)", 0, 100, 85, help="How much 'blind scouting' is removed by ground-truth data?")

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["⚡ INFRASTRUCTURE / UTILITIES", "🏛️ GOVERNMENT ROI WIZARD"])

# ==========================================
# TAB 1: UTILITIES (REMAINS UNCHANGED)
# ==========================================
with tab1:
    st.markdown("<div class='status-pill'>SECTOR: ASSET PROTECTION</div>", unsafe_allow_html=True)
    st.title("Network Recovery & STPIS Benchmark")
    
    u_col1, u_col2 = st.columns([1, 2])
    with u_col1:
        u_assets = st.number_input("Total Region Assets", value=1200)
        u_impact = st.slider("Inundation Rate (%)", 5, 100, 20)
        u_crew = st.number_input("Crew Day Rate ($)", value=850)
        u_stpis = st.number_input("STPIS Penalty ($/min)", value=125)
    
    # Calculation
    exp_assets = int(u_assets * (u_impact/100))
    lat_gain = (48 - sar_latency)
    
    leg_u = 85000 + ((u_assets - exp_assets) * u_crew) + (exp_assets * 0.45 * u_crew) + (exp_assets * u_stpis * (lat_gain * 60))
    tar_u = (exp_assets * u_crew)
    u_roi = ((leg_u * events_per_year) - (tar_u * events_per_year) - sub_cost)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="metric-blade"><p class="m-title">Assets Verified</p><p class="m-value">{exp_assets}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-blade"><p class="m-title">Lead-Time Gain</p><p class="m-value">{lat_gain}h</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-blade"><p class="m-title">Annual Protection</p><p class="m-value">${u_roi:,.0f}</p></div>', unsafe_allow_html=True)
    
    st.bar_chart(pd.DataFrame({"Model": ["Legacy (Blind)", "Satellite (Targeted)"], "Cost": [leg_u, (tar_u + (sub_cost/events_per_year))]}).set_index("Model"))

# ==========================================
# TAB 2: GOVERNMENT ROI WIZARD
# ==========================================
with tab2:
    st.markdown("<div class='status-pill'>SECTOR: DISASTER MANAGEMENT</div>", unsafe_allow_html=True)
    st.title("The 'Deterministic Response' Wizard")
    st.markdown("### Yesterday's Search vs. Tomorrow's Action")

    # --- THE "MECHANICS" INPUTS ---
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        g_col1, g_col2, g_col3 = st.columns(3)
        
        with g_col1:
            st.markdown("#### 🚁 Aviation Recon")
            heli_rate = st.number_input("Heli Charter Rate ($/hr)", value=3500)
            heli_hrs = st.number_input("Recon Hrs / Day", value=10)
            weather_delay = st.slider("Weather/Cloud Delay (Hrs)", 24, 96, 72)
            
        with g_col2:
            st.markdown("#### 🚛 Field Mechanics")
            crew_cost_g = st.number_input("Personnel Burn Rate ($/day)", value=450)
            crew_count = st.number_input("Field Responders", value=100)
            waste_per_trip = st.number_input("Dry-Run Cost (Fuel/Labor)", value=2800)
            num_dry_runs = st.slider("Dry-Runs / Event", 0, 50, 15)
            
        with g_col3:
            st.markdown("#### 🛣️ Economic Friction")
            freight_rate = st.number_input("Freight Loss ($/hr)", value=15000)
            corridors = st.number_input("Impacted Corridors", value=2)
            manual_verify_days = st.slider("Manual Damage Verification (Days)", 7, 30, 14)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- THE MATH ENGINE: TIME VS MONEY ---
    # The "Yesterday" State
    blind_period_days = weather_delay / 24
    yesterday_aviation = (heli_rate * heli_hrs * blind_period_days)
    yesterday_burn = (crew_count * crew_cost_g * blind_period_days)
    yesterday_waste = (num_dry_runs * waste_per_trip)
    yesterday_freight = (corridors * freight_rate * (weather_delay + (sar_latency * 2))) # Extra buffer for scout time
    
    # The "Future" State (Satellite-Driven)
    future_aviation = 0 # Fully offset by all-weather data
    future_burn = yesterday_burn * (1 - (confidence_gain/100)) # Only active when they have "known" targets
    future_waste = yesterday_waste * 0.1 # 90% reduction in dry runs
    future_freight = (corridors * freight_rate * sar_latency) # Reopen as soon as data hits
    
    event_savings = (yesterday_aviation + yesterday_burn + yesterday_waste + yesterday_freight) - (future_aviation + future_burn + future_waste + future_freight)
    annual_gov_value = (event_savings * events_per_year) - sub_cost

    # --- TOP LEVEL WIZARD METRICS ---
    st.markdown("---")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f'<div class="metric-blade"><p class="m-title">Information Gap Closed</p><p class="m-value">{weather_delay - sar_latency}h</p><p class="m-sub">Deterministic Window</p></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-blade"><p class="m-title">Aviation Offset</p><p class="m-value">${(yesterday_aviation * events_per_year):,.0f}</p><p class="m-sub">Zero Weather Standby</p></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="metric-blade"><p class="m-title">Economic Yield</p><p class="m-value">${(yesterday_freight - future_freight) * events_per_year:,.0f}</p><p class="m-sub">Freight Resilience</p></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown(f'<div class="metric-blade" style="border-left-color: #10B981;"><p class="m-title">Total Annual ROI</p><p class="m-value" style="color: #10B981;">${annual_gov_value:,.0f}</p><p class="m-sub">Post-Subscription</p></div>', unsafe_allow_html=True)

    # --- THE MECHANICS COMPARISON: RADIAL-STYLE BAR ---
    st.markdown("### 📊 Operational Transformation: Today vs. Future State")
    comparison_df = pd.DataFrame({
        "Operational Layer": ["Aviation Recon", "Personnel Burn", "Waste (Dry Runs)", "Freight Downtime"],
        "Today (Probabilistic)": [yesterday_aviation, yesterday_burn, yesterday_waste, yesterday_freight],
        "Future (Deterministic)": [future_aviation, future_burn, future_waste, future_freight]
    })
    st.bar_chart(comparison_df.set_index("Operational Layer"), use_container_width=True)

    # --- STRATEGIC EXPLANATION ---
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col_msg1, col_msg2 = st.columns(2)
    with col_msg1:
        st.markdown("#### ❌ Today: Probabilistic Response")
        st.write("""
        - **Waiting for Sky:** Recon is grounded by the same storm causing the flood. 
        - **Blind Deployment:** Crews sent to regions based on 'Suspected' impact from low-fidelity models.
        - **The Dry Run Penalty:** Fuel and morale wasted checking areas that are actually dry.
        - **Economic Paralysis:** Logistics corridors remain closed 'just in case' because ground truth is missing.
        """)
    with col_msg2:
        st.markdown("#### ✅ Future: Deterministic Action")
        st.write(f"""
        - **All-Weather Truth:** Satellite data penetrates clouds 100% of the time. Action starts during the storm.
        - **Targeted Dispatch:** Crews deployed only to the **{confidence_gain}%** of confirmed flood zones.
        - **Velocity Boost:** Ground teams skip the scouting phase and go straight to restoration.
        - **Precision Reopening:** Corridors reopen the moment the data confirms water levels are safe.
        """)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.8rem;'>Proprietary Response ROI Framework | 2026 Emergency Management Standard</p>", unsafe_allow_html=True)
