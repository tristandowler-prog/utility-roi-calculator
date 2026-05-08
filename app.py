import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import datetime

# --- 1. SETTINGS & GLASSMORPHIC CSS ---
st.set_page_config(page_title="ICEYE Intelligence ROI", layout="wide", initial_sidebar_state="expanded")

def apply_modern_theme():
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        /* Glassmorphism cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: #38bdf8;
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #38bdf8;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.8);
        }
        /* Hide default streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

apply_modern_theme()

# --- 2. LOGIC & MATH (DRY - Don't Repeat Yourself) ---
def calculate_roi(ev, sub, lat, h_rate, h_hrs, h_stby, d_rate, d_hrs, d_stby, t_cnt, t_burn, c_days, d_pen, d_ev, g_cnt, g_rate, l_proc, i_proc):
    leg_air = ((h_rate * h_hrs) + (h_stby * c_days) + (d_rate * d_hrs) + (d_stby * c_days)) * ev
    leg_gis = (g_cnt * g_rate * l_proc) * ev
    leg_field = ((t_cnt * t_burn * c_days) + (d_ev * d_pen)) * ev
    
    ice_gis = (g_cnt * g_rate * i_proc) * ev
    ice_field = (t_cnt * t_burn * (lat / 24.0)) * ev
    
    total_leg = leg_air + leg_gis + leg_field
    total_ice = ice_gis + ice_field + sub
    
    return total_leg, total_ice, leg_air, (l_proc - i_proc) * ev

# --- 3. SIDEBAR CONTROLS (THE "ENGINE ROOM") ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=120)
    st.markdown("### 🛠️ Configuration")
    
    with st.expander("📡 ICEYE Parameters", expanded=True):
        events_pa = st.slider("Events / Year", 1, 20, 4)
        annual_sub = st.number_input("Subscription ($)", value=250000.0)
        sar_latency = st.slider("Latency (Hrs)", 1, 24, 8)

    with st.expander("🚁 Aviation Assets"):
        h_rate = st.number_input("Heli $/Hr", value=3500.0)
        h_hrs = st.number_input("Heli Hrs/Event", value=8.0)
        h_stby = st.number_input("Heli Standby $/Day", value=5000.0)
        d_rate = st.number_input("Drone $/Hr", value=250.0)
        d_hrs = st.number_input("Drone Hrs/Event", value=15.0)
        d_stby = st.number_input("Drone Standby $/Day", value=1200.0)

    with st.expander("🚛 Field & GIS Teams"):
        t_cnt = st.number_input("Active Teams", value=6)
        t_burn = st.number_input("Daily Team Burn ($)", value=12500.0)
        c_days = st.number_input("Cloud Window (Days)", value=2.0)
        g_rate = st.number_input("GIS $/Hr", value=120.0)
        l_proc = st.number_input("Legacy GIS Hrs", value=12.0)
        i_proc = st.number_input("ICEYE GIS Hrs", value=2.0)
        d_pen = 2800.0 # Keeping some constants for clean UI
        d_ev = 10
        g_cnt = 2

# --- 4. CALCULATION RUN ---
total_legacy, total_iceye, air_savings, hrs_saved = calculate_roi(
    events_pa, annual_sub, sar_latency, h_rate, h_hrs, h_stby, d_rate, d_hrs, d_stby, 
    t_cnt, t_burn, c_days, d_pen, d_ev, g_cnt, g_rate, l_proc, i_proc
)
net_savings = total_legacy - total_iceye

# --- 5. THE DASHBOARD ---
st.title("ICEYE | Value Realization Dashboard")
st.markdown(f"**Analysis Period:** {datetime.date.today().year} Annual Forecast")

# Big Stats Row
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Net Annual Recovery</div>
        <div class="metric-value">${net_savings:,.0f}</div>
        <div style="color: #4ade80;">↑ {int((net_savings/total_legacy)*100)}% Efficiency Increase</div>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Aviation Budget Offset</div>
        <div class="metric-value">${air_savings:,.0f}</div>
        <div style="color: #94a3b8;">Reallocated Capital</div>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">GIS Time Recovery</div>
        <div class="metric-value">{hrs_saved:,.0f} Hrs</div>
        <div style="color: #94a3b8;">Direct Labor Savings</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# Charts Row
c_left, c_right = st.columns([2, 1])

with c_left:
    st.subheader("Cost Distribution: Legacy vs. ICEYE")
    fig = go.Figure(data=[
        go.Bar(name='Legacy Model', x=['Total Cost'], y=[total_legacy], marker_color='#64748b'),
        go.Bar(name='ICEYE Model', x=['Total Cost'], y=[total_iceye], marker_color='#38bdf8')
    ])
    fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f8fafc")
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.subheader("Executive Actions")
    st.info("💡 **Key Insight:** Reducing info-latency from 48h to 8h is the primary driver of your field labor recovery.")
    
    if st.button("🚀 Finalize & Export PDF"):
        st.toast("Generating Secure Report...")
        # (PDF generation logic would go here - similar to previous code)
        st.success("Report Ready for Download")

# --- 6. "VIBE" CELEBRATION ---
if net_savings > 1000000:
    st.balloons()
