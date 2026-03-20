import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI Auditor", layout="wide")

st.title("🛰️ ICEYE SAR: Operational ROI Auditor")
st.markdown("### *Manual Search & Rescue vs. Satellite Observed Truth*")
st.divider()

# --- SIDEBAR: THE SPREADSHEET INPUTS ---
with st.sidebar:
    st.header("💰 1. The ICEYE Subscription")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Field Force Rates")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    st.divider()
    st.header("🚁 3. Aerial Recon Rates")
    helo_rate = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_rate = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE FIXED MATH ---
# Sub divided by events (The Core Request)
data_share = annual_sub / events_per_year
# Hourly Burn = (People * Rate) + (Cars * Rate)
hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 The Manual Way (Search)")
    t_search_hrs = st.number_input("Hours spent searching/scouting", value=48)
    t_helo_hrs = st.number_input("Helicopter Hours", value=15)
    t_drone_days = st.number_input("Drone Team Days", value=12)
    t_assets = st.number_input("Total Assets to Verify", value=2000)
    
    # Manual Costs
    manual_labor = hourly_burn * t_search_hrs
    manual_aerial = (t_helo_hrs * helo_rate) + (t_drone_days * drone_rate)
    manual_inspections = t_assets * 350
    manual_total = manual_labor + manual_aerial + manual_inspections

with col_right:
    st.subheader("🔵 The ICEYE Way (Know)")
    s_desk_hrs = st.number_input("Hours at desk to confirm truth", value=4)
    s_assets_wet = st.number_input("Confirmed 'Wet' Assets", value=140)
    
    # SAR Costs
    sar_labor = hourly_burn * s_desk_hrs
    sar_inspections = s_assets_wet * 350
    # Total = Data + Desk Labor + Targeted Inspections
    sar_total = data_share + sar_labor + sar_inspections
    
    st.info(f"💡 **Data Cost:** ${data_share:,.0f} per event")

# --- THE DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Manual Cost / Event", f"${manual_total:,.0f}")
m2.metric("True SAR Cost / Event", f"${sar_total:,.0f}", 
          delta=f"-${manual_total - sar_total:,.0f}", delta_color="inverse")

annual_net = (manual_total - sar_total) * events_per_year
m3.metric("Net Annual Position", f"${annual_net:,.0f}")

# --- THE BREAKDOWN TABLE ---
st.subheader("Cost Breakdown per Event")
df = pd.DataFrame({
    "Category": ["Field Labor (Search/Desk)", "Aerial Recon (Helo/Drone)", "Physical Inspections", "Satellite Data Share"],
    "Manual ($)": [f"${manual_labor:,.0f}", f"${manual_aerial:,.0f}", f"${manual_inspections:,.0f}", "$0"],
    "ICEYE ($)": [f"${sar_labor:,.0f}", "$0 (Replaced)", f"${sar_inspections:,.0f}", f"${data_share:,.0f}"]
})
st.table(df)

# --- CHART ---
chart_df = pd.DataFrame({
    "Category": ["Labor", "Aerial", "Inspections", "Data"],
    "Manual": [manual_labor, manual_aerial, manual_inspections, 0],
    "ICEYE": [sar_labor, 0, sar_inspections, data_share]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**The Advantage:** By sitting at a desk with ICEYE data, you clear **{int(t_assets - s_assets_wet)}** assets without leaving your desk, saving **${(t_assets - s_assets_wet) * 350:,.0f}** in field verification and **${manual_aerial:,.0f}** in aerial recon.")
