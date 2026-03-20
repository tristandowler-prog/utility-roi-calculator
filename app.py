import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI Auditor", layout="wide")

st.title("🛰️ ICEYE SAR: Subscription ROI Auditor")
st.markdown("### *Logic: Manual Search Costs vs. Fixed Subscription Share*")
st.divider()

# --- SIDEBAR: THE SPREADSHEET INPUTS ---
with st.sidebar:
    st.header("💰 1. The ICEYE Subscription")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 10) # Set to 10 for your test
    
    st.divider()
    st.header("👥 2. Manual Search Force (Current)")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    st.divider()
    st.header("🚁 3. Aerial Search Rates (Current)")
    helo_rate = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_rate = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE PURE MATH ---
# 150,000 / 10 = 15,000
data_cost_per_event = annual_sub / events_per_year

# Hourly Burn for the search team
hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Manual Scouting (Current)")
    t_search_hrs = st.number_input("Hours spent scouting/searching", value=48)
    t_helo_hrs = st.number_input("Helicopter Hours", value=15)
    t_drone_days = st.number_input("Drone Team Days", value=12)
    
    # Total Manual Search Spend
    manual_labor = hourly_burn * t_search_hrs
    manual_aerial = (t_helo_hrs * helo_rate) + (t_drone_days * drone_rate)
    manual_total = manual_labor + manual_aerial

with col_right:
    st.subheader("🔵 ICEYE Truth (SAR)")
    # The 'True' cost is strictly the subscription slice
    sar_total = data_cost_per_event
    
    st.write("### SAR Cost Logic:")
    st.info(f"Subscription (${annual_sub:,.0f}) ÷ Events ({events_per_year}) = **${sar_total:,.0f} per event**")
    st.write("*(Assuming desk review labor is negligible vs. field scouting)*")

# --- THE DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Manual Search Cost / Event", f"${manual_total:,.0f}")
# This will now show EXACTLY $15,000 if sub=150k and events=10
m2.metric("True SAR Cost / Event", f"${sar_total:,.0f}", 
          delta=f"-${manual_total - sar_total:,.0f}", delta_color="inverse")

# Annual Net: (Total Manual Costs for all events) - (The 150k Sub)
annual_net = (manual_total * events_per_year) - annual_sub
m3.metric("Net Annual Savings", f"${annual_net:,.0f}")

# --- THE BREAKDOWN TABLE ---
st.subheader("Cost Comparison per Event")
df = pd.DataFrame({
    "Category": ["Field Search Labor (Wages + Fuel)", "Aerial Search (Helo + Drone)", "Satellite Data (Subscription Share)"],
    "Manual Search ($)": [f"${manual_labor:,.0f}", f"${manual_aerial:,.0f}", "$0"],
    "SAR Truth ($)": ["$0 (Replaced)", "$0 (Replaced)", f"${data_cost_per_event:,.0f}"]
})
st.table(df)

# --- CHART ---

st.subheader("Manual Search Spend vs. Satellite Subscription")
chart_df = pd.DataFrame({
    "Category": ["Manual Labor", "Aerial Recon", "Data Sub"],
    "Manual": [manual_labor, manual_aerial, 0],
    "SAR": [0, 0, data_cost_per_event]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**The Logic:** You are trading **${manual_total:,.0f}** in manual scouting costs per event for a **${data_cost_per_event:,.0f}** share of a satellite subscription.")
