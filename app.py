import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Strategic ROI Audit | Emergency Response", layout="wide")

# --- TITAN V4: ULTIMATE FIDELITY DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0F172A, #020617);
        color: #F8FAFC;
    }
    
    /* Cinematic Glass Card */
    .titan-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        padding: 35px;
        border-radius: 24px;
        margin-bottom: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .neon-text {
        color: #00D1FF;
        text-shadow: 0 0 15px rgba(0, 209, 255, 0.6);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 3px;
    }
    
    .metric-value-titan {
        font-size: 3.5rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        background: linear-gradient(to right, #FFFFFF, #94A3B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    
    .m-title { font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 5px;}
    .m-sub { font-size: 0.9rem; color: #00D1FF; font-weight: 600; }
    
    .status-badge {
        background: rgba(0, 209, 255, 0.1);
        border: 1px solid #00D1FF;
        color: #00D1FF;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='neon-text'>CALIBRATION</h2>", unsafe_allow_html=True)
    st.markdown("### 🏦 Investment")
    sub_cost = st.number_input("Annual Data Subscription ($)", value=150000)
    events_per_year = st.slider("Annual Major Events", 1, 12, 4)
    
    st.divider()
    st.markdown("### 🛰️ Solution Latency")
    sar_latency = st.slider("Data Delivery Window (Hrs)", 6, 24, 12)
    st.info("The logic below calculates the 'Net Yield' by replacing variable operational waste with this fixed technology investment.")

# --- HEADER ---
st.markdown("<div style='text-align: center; padding: 60px 0 40px 0;'>", unsafe_allow_html=True)
st.markdown("<div class='status-badge'>DETERMINISTIC RESPONSE MODEL v4.0</div>", unsafe_allow_html=True)
st.markdown("<h1 style='font-family: \"Orbitron\", sans-serif; font-size: 3.5rem; margin-top: -10px;'>Emergency Response ROI Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; letter-spacing: 1px;'>Operational Velocity & Macro-Economic Resilience Audit</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MECHANICAL INPUTS
# ==========================================
st.markdown("<div class='titan-card'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<h4 class='neon-text' style='font-size: 1.1rem;'>🚁 LEGACY RECON</h4>", unsafe_allow_html=True)
    heli_rate = st.number_input("Heli Charter Rate ($/hr)", value=3500)
    heli_hrs = st.number_input("Active Recon Hrs / Day", value=10)
    cloud_delay_hrs = st.slider("Cloud Grounding Delay (Hrs)", 12, 120, 72)

with c2:
    st.markdown("<h4 class='neon-text' style='font-size: 1.1rem;'>🚛 FIELD DYNAMICS</h4>", unsafe_allow_html=True)
    crew_daily = st.number_input("Personnel Day Rate ($)", value=450)
    crew_vol = st.number_input("Total Responder Volume", value=100)
    precision_gain = st.slider("Dispatch Precision (%)", 50, 100, 90)

with c3:
    st.markdown("<h4 class='neon-text' style='font-size: 1.1rem;'>🛣️ ECONOMIC FRICTION</h4>", unsafe_allow_html=True)
    freight_loss = st.number_input("Freight Loss ($/hr/road)", value=15000)
    hwy_count = st.number_input("Critical Corridors", value=2)
    legacy_verify_days = st.slider("Legacy Verification (Days)", 3, 21, 10)
    target_recovery_days = st.slider("Targeted Recovery (Days)", 1, 10, 2)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# THE ENGINE: TRUTH VS. ASSUMPTION
# ==========================================

# -- 1. LEGACY COSTS (The "Before" State) --
# Per Event
leg_aviation_event = (heli_rate * heli_hrs * (cloud_delay_hrs / 24))
leg_personnel_event = (crew_vol * crew_daily * (cloud_delay_hrs / 24))
leg_time_total = cloud_delay_hrs + (legacy_verify_days * 24)
leg_freight_event = (freight_loss * hwy_count * leg_time_total)

total_legacy_annual = (leg_aviation_event + leg_personnel_event + leg_freight_event) * events_per_year

# -- 2. FUTURE COSTS (The "Deterministic" State) --
# Note: Aviation is $0 because SAR replaces it. Data cost is the Subscription (sub_cost).
fut_aviation_event = 0
# Personnel are deployed during the storm (bypassing cloud delay) but only for the latency window
fut_personnel_event = (crew_vol * crew_daily * (sar_latency / 24)) * (1 - (precision_gain/100))
fut_time_total = sar_latency + (target_recovery_days * 24)
fut_freight_event = (freight_loss * hwy_count * fut_time_total)

# Annual Total: (Variable Event Costs * Frequency) + Fixed Subscription
total_future_annual = ((fut_aviation_event + fut_personnel_event + fut_freight_event) * events_per_year) + sub_cost

# -- 3. RESULTS --
annual_net_saving = total_legacy_annual - total_future_annual

# ==========================================
# THE ROI DASHBOARD (HIGH POP)
# ==========================================
m1, m2, m3 = st.columns([1, 1, 1.5])

with m1:
    st.markdown(f"""
    <div class='titan-card' style='border-left: 4px solid #F87171;'>
        <p class='m-title'>Legacy OpEx (Annual)</p>
        <p class='metric-value-titan' style='color: #F87171;'>${total_legacy_annual/1e6:.1f}M</p>
        <p class='m-sub'>Probabilistic Model</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class='titan-card' style='border-left: 4px solid #00D1FF;'>
        <p class='m-title'>Future OpEx (Annual)</p>
        <p class='metric-value-titan' style='color: #00D1FF;'>${total_future_annual/1e6:.1f}M</p>
        <p class='m-sub'>Inc. ${sub_cost/1e3:.0f}K Subscription</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class='titan-card' style='border-left: 4px solid #10B981; background: rgba(16, 185, 129, 0.05);'>
        <p class='m-title'>Net Strategic Yield</p>
        <p class='metric-value-titan' style='color: #10B981;'>${annual_net_saving/1e6:.2f}M</p>
        <p class='m-sub'>Post-Investment Profitability</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATA VISUALS & AUDIT
# ==========================================
st.markdown("### 📊 Financial Attribution")
col_chart, col_audit = st.columns([2, 1])

with col_chart:
    st.markdown("<div class='titan-card' style='padding: 20px;'>", unsafe_allow_html=True)
    # Comparison Data for the Chart
    chart_data = pd.DataFrame({
        "Category": ["Aviation", "Field Personnel", "Economic Friction", "Tech Subscription"],
        "Legacy ($)": [(leg_aviation_event * events_per_year), (leg_personnel_event * events_per_year), (leg_freight_event * events_per_year), 0],
        "Future ($)": [0, (fut_personnel_event * events_per_year), (fut_freight_event * events_per_year), sub_cost]
    }).set_index("Category")
    st.bar_chart(chart_data, height=350)
    st.markdown("</div>", unsafe_allow_html=True)

with col_audit:
    st.markdown("<div class='titan-card' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h4 class='neon-text' style='font-size: 0.9rem;'>MECHANICAL AUDIT</h4>", unsafe_allow_html=True)
    st.write(f"""
    - **Cloud Delay Offset:** SAR eliminates the {cloud_delay_hrs}-hour blind window, stopping helis from sitting on standby.
    - **Precision Advantage:** {precision_gain}% reduction in field personnel burn through targeted data.
    - **Economic Delta:** By reopening highways in {target_recovery_days} days instead of {legacy_verify_days}, you recover **{((leg_time_total - fut_time_total) * events_per_year)} hours** of freight movement annually.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; padding: 40px; letter-spacing: 2px;'>CONFIDENTIAL STRATEGIC AUDIT | PREPARED FOR EXECUTIVE LEADERSHIP</p>", unsafe_allow_html=True)
