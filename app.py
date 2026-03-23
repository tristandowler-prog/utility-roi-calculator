import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="ICEYE ROI Audit", layout="wide")

# --- ZERO-DESIGN STYLING (TOTAL READABILITY) ---
st.markdown("""
<style>
    /* Force standard high-contrast text */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, label { color: #000000 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

st.title("Emergency Response ROI: ICEYE vs. Legacy")

# --- 1. THE BIG PICTURE (TOP ROW) ---
st.markdown("### 🏛️ Step 1: ICEYE Investment & Performance")
col_inv1, col_inv2, col_inv3 = st.columns(3)
with col_inv1:
    annual_sub = st.number_input("Annual ICEYE Subscription ($)", value=150000.00, step=1000.00, format="%.2f")
with col_inv2:
    events_pa = st.number_input("Major Flood Events Per Year", value=3.0, step=1.0)
with col_inv3:
    sar_latency = st.number_input("ICEYE Data Latency (Hrs)", value=6.0, step=0.5)

# --- 2. OPERATIONAL INPUTS ---
st.markdown("---")
st.markdown("### 🛠️ Step 2: Legacy Operational Costs (Manual Overrides)")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### 🚁 Aviation & Recon")
    heli_rate = st.number_input("Heli Charter ($/hr)", value=3500.00, step=50.00, format="%.2f")
    heli_recon_hrs = st.number_input("Total Flight Hrs/Event", value=20.0, step=1.0)
    drone_daily = st.number_input("Drone Team Daily Rate ($)", value=2200.00, step=50.00, format="%.2f")
    cloud_window_days = st.number_input("Cloud/Visual Blind Window (Days)", value=2.0, step=0.25)
    
with c2:
    st.markdown("#### 🚛 Field Personnel (Strike Teams)")
    team_count = st.number_input("Number of Strike Teams", value=6.0, step=1.0)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.00, step=100.00, format="%.2f")
    dry_run_penalty_cost = st.number_input("Dry Run Penalty ($/trip)", value=2800.00, step=50.00, format="%.2f")
    dry_runs_prevented = st.number_input("Dry Runs Prevented w/ SAR", value=10.0, step=1.0)

with c3:
    st.markdown("#### 🖥️ GIS & Infrastructure")
    gis_hourly_rate = st.number_input("GIS Staff Hourly Rate ($/hr)", value=120.00, step=5.00, format="%.2f")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2.0, step=1.0)
    gis_processing_hrs = st.number_input("Manual Mapping Time (Hrs)", value=8.0, step=0.5)
    hwy_loss_hr = st.number_input("Freight Loss per Hwy ($/hr)", value=15000.00, step=500.00, format="%.2f")
    hwy_count = st.number_input("No. of Major Highways", value=2.0, step=1.0)

# ==========================================
# 3. THE MATH (VERIFIED)
# ==========================================

# Time Gaps
leg_wait_hrs = (cloud_window_days * 24.0) + gis_processing_hrs
time_recovered_hrs = leg_wait_hrs - sar_latency

# LEGACY COSTS (Per Event)
leg_aviation = (heli_rate * heli_recon_hrs) + (drone_daily * cloud_window_days)
leg_gis = (gis_staff_count * gis_hourly_rate * gis_processing_hrs)
leg_personnel = (team_count * team_daily_burn * cloud_window_days) + (dry_runs_prevented * dry_run_penalty_cost)
leg_logistics = (hwy_loss_hr * hwy_count * leg_wait_hrs)

# ICEYE COSTS (Per Event)
iceye_personnel = (team_count * team_daily_burn * (sar_latency / 24.0))
iceye_logistics = (hwy_loss_hr * hwy_count * sar_latency)

# ANNUAL AGGREGATES
total_legacy_annual = (leg_aviation + leg_gis + leg_personnel + leg_logistics) * events_pa
total_iceye_annual = ((iceye_personnel + iceye_logistics) * events_pa) + annual_sub

net_annual_roi = total_legacy_annual - total_iceye_annual

# ==========================================
# 4. RESULTS (Standard Metrics - Safe Visibility)
# ==========================================
st.markdown("---")
st.markdown("### 📈 Strategic Financial Results")
res1, res2, res3 = st.columns(3)

res1.metric("Annual Net Profit (ROI)", f"${net_annual_roi:,.2f}")
res2.metric("Time Recovered per Event", f"{time_recovered_hrs:.1f} Hours")
res3.metric("Annual Ops Recovery", f"${(total_legacy_annual - total_iceye_annual - annual_sub):,.2f}")

# ==========================================
# 5. VISUAL CHART
# ==========================================
st.markdown("### 📊 Annual Cost Breakdown")

chart_data = {
    "Category": ["Aviation & GIS", "Field Personnel", "Logistics/Freight", "ICEYE Subscription"],
    "Legacy Model ($)": [
        (leg_aviation + leg_gis) * events_pa, 
        leg_personnel * events_pa, 
        leg_logistics * events_pa, 
        0.0
    ],
    "ICEYE Model ($)": [
        0.0, 
        iceye_personnel * events_pa, 
        iceye_logistics * events_pa, 
        annual_sub
    ]
}

df_chart = pd.DataFrame(chart_data).set_index("Category")
st.bar_chart(df_chart, height=400)

st.markdown(f"""
**Key Strategic Takeaways:**
* **Information Advantage:** ICEYE recovers **{time_recovered_hrs:.1f} hours** of actionable intel by removing the 2-day cloud wait and the 8-hour GIS manual mapping bottleneck.
* **Operational Savings:** By removing redundant recon and GIS labor, you offset **${(leg_aviation + leg_gis)*events_pa:,.2f}** in annual OpEx.
* **Economic Recovery:** Accelerating the reopening of **{hwy_count:.0f} highways** recovers **${(leg_logistics - iceye_logistics)*events_pa:,.2f}** in freight productivity annually.
""")
