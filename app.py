import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI Auditor", layout="wide")

st.title("🛰️ ICEYE SAR: Search Cost ROI")
st.markdown("### *Manual Recon vs. Satellite Subscription*")
st.divider()

# --- SIDEBAR: THE SPREADSHEET INPUTS ---
with st.sidebar:
    st.header("💰 1. The ICEYE Subscription")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Field Force Rates (Manual Search)")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    st.divider()
    st.header("🚁 3. Aerial Recon Rates (Manual Search)")
    helo_rate = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_rate = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE FIXED MATH ---
# Sub divided by events
data_share = annual_sub / events_per_year

# Hourly Burn for the scout team = (People * Rate) + (Cars * Rate)
hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Manual Scouting (Current)")
    t_search_hrs = st.number_input("Hours spent scouting/searching", value=48)
    t_helo_hrs = st.number_input("Helicopter Hours", value=15)
    t_drone_days = st.number_input("Drone Team Days", value=12)
    
    # Manual Costs
    manual_labor = hourly_burn * t_search_hrs
    manual_aerial = (t_helo_hrs * helo_rate) + (t_drone_days * drone_rate)
    manual_total = manual_labor + manual_aerial

with col_right:
    st.subheader("🔵 ICEYE Desk Review (SAR)")
    s_desk_hrs = st.number_input("Hours at desk to identify impact", value=4)
    
    # SAR Costs
    sar_labor = hourly_burn * s_desk_hrs
    # Total = Desk Labor + The slice of the subscription
    sar_total = sar_labor + data_share
    
    st.info(f"💡 **Subscription Share:** ${data_share:,.0f} per event")

# --- THE DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Manual Search Cost / Event", f"${manual_total:,.0f}")
m2.metric("SAR Truth Cost / Event", f"${sar_total:,.0f}", 
          delta=f"-${manual_total - sar_total:,.0f}", delta_color="inverse")

annual_net = (manual_total - sar_total) * events_per_year
m3.metric("Annual Net Savings", f"${annual_net:,.0f}")

# --- THE BREAKDOWN TABLE ---
st.subheader("Cost Comparison per Event")
df = pd.DataFrame({
    "Category": ["Field Labor (Search vs. Desk)", "Aerial Recon (Helo/Drone)", "Satellite Data Share"],
    "Manual Search ($)": [f"${manual_labor:,.0f}", f"${manual_aerial:,.0f}", "$0"],
    "SAR Truth ($)": [f"${sar_labor:,.0f}", "$0 (Replaced)", f"${data_share:,.0f}"]
})
st.table(df)

# --- CHART ---

st.subheader("Search Spend Analysis")
chart_df = pd.DataFrame({
    "Category": ["Field Labor", "Aerial Recon", "Data Cost"],
    "Manual": [manual_labor, manual_aerial, 0],
    "SAR": [sar_labor, 0, data_share]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**Value Realization:** By replacing manual field scouting with satellite truth, you eliminate **${manual_aerial:,.0f}** in aerial costs and **${manual_labor - sar_labor:,.0f}** in search labor per event.")
