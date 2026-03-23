import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="ICEYE ROI Audit", layout="wide")

# --- HIGH-CONTRAST "AUDIT" STYLING (BLACK & WHITE) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
    .stMetric { border: 2px solid #000000; padding: 15px; background-color: #F8F9FA; }
    .roi-hero { 
        background-color: #000000; 
        color: #FFFFFF !important; 
        padding: 30px; 
        text-align: center; 
        border-radius: 8px;
        margin-bottom: 25px;
    }
    .roi-hero h1, .roi-hero p { color: #FFFFFF !important; margin: 0; }
    label, p, h3 { color: #000000 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. GLOBAL INVESTMENT (TOP OF APP) ---
st.title("Emergency Response ROI Analysis")

# Define these first so we can use them in the Hero section
col_inv1, col_inv2, col_inv3 = st.columns(3)
with col_inv1:
    annual_sub = st.number_input("ICEYE Annual Subscription ($)", value=150000, step=10000)
with col_inv2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3)
with col_inv3:
    sar_latency = st.number_input("ICEYE Data Delivery (Hrs)", value=6)

# --- 2. OPERATIONAL INPUTS (MANUAL OVERRIDES) ---
st.markdown("### 🛠️ Step 1: Define Current Legacy Costs (Manual Overrides)")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Aviation & Recon")
    heli_rate = st.number_input("Heli Rate ($/hr)", value=3500)
    heli_hrs = st.number_input("Recon Hrs/Event", value=40)
    drone_daily = st.number_input("Drone Daily ($)", value=2200)
    drone_days = st.number_input("Drone Days", value=5)

with c2:
    st.markdown("#### Field Personnel")
    team_count = st.number_input("Strike Teams", value=6)
    team_burn = st.number_input("Daily Team Burn ($)", value=12500)
    dry_run_penalty = st.number_input("Dry Run Penalty ($)", value=2800)
    dry_runs_saved = st.number_input("Dry Runs Prevented", value=10)

with c3:
    st.markdown("#### Infrastructure & GIS")
    cloud_window = st.number_input("Cloud Blindness (Hrs)", value=48)
    hwy_loss_hr = st.number_input("Hwy Loss ($/hr)", value=15000)
    hwy_count = st.number_input("No. of Highways", value=2)
    gis_process_hrs = st.number_input("GIS Processing (Hrs)", value=8)
    gis_staff_cost = st.number_input("GIS Staff/Hr Total ($)", value=240) # 2 staff x $120

# --- 3. THE CALCULATION ENGINE ---
# Legacy Time Gap
leg_wait = cloud_window + gis_process_hrs
time_recovered = leg_wait - sar_latency

# Legacy Costs (Per Event)
leg_recon = (heli_rate * heli_hrs) + (drone_daily * drone_days)
leg_gis = (gis_process_hrs * gis_staff_cost)
leg_personnel = (team_count * team_burn * (cloud_window/24)) + (dry_runs_saved * dry_run_penalty)
leg_logistics = (hwy_loss_hr * hwy_count * leg_wait)

# ICEYE Costs (Per Event)
iceye_personnel = (team_count * team_burn * (sar_latency/24))
iceye_logistics = (hwy_loss_hr * hwy_count * sar_latency)

# ANNUAL AGGREGATES
total_legacy_annual = (leg_recon + leg_gis + leg_personnel + leg_logistics) * events_pa
total_iceye_annual = ((iceye_personnel + iceye_logistics) * events_pa) + annual_sub

net_annual_roi = total_legacy_annual - total_iceye_annual

# --- 4. THE BOTTOM LINE (NOW AT THE TOP) ---
st.markdown("---")
st.markdown(f"""
<div class='roi-hero'>
    <p>TOTAL NET ANNUAL SAVING / PROFIT</p>
    <h1>${net_annual_roi/1e6:.2f} Million</h1>
    <p>Bypassing {time_recovered} hours of visual blindness per event</p>
</div>
""", unsafe_allow_html=True)

# --- 5. VISUAL PROOF (UPDATED CHART) ---
st.markdown("### 📊 Annualized Cost Comparison")

# Splitting the subscription cost across the categories for the chart 
# or showing it as a standalone "Investment" bar
chart_df = pd.DataFrame({
    "Cost Category": ["Aviation & GIS", "Field Personnel", "Freight Logistics", "Solution Investment"],
    "Legacy Model ($)": [(leg_recon + leg_gis) * events_pa, leg_personnel * events_pa, leg_logistics * events_pa, 0],
    "ICEYE Model ($)": [0, iceye_personnel * events_pa, iceye_logistics * events_pa, annual_sub]
}).set_index("Cost Category")

st.bar_chart(chart_df, height=400)

st.write(f"""
**Technical Summary:**
By investing **${annual_sub/1e3:.0f}k** annually, the organization eliminates **${(leg_recon + leg_gis)*events_pa/1e3:.0f}k** in redundant reconnaissance 
and recovers **${(leg_logistics - iceye_logistics)*events_pa/1e6:.1f}M** in economic productivity by shortening the highway verification window by **{time_recovered} hours**.
""")
