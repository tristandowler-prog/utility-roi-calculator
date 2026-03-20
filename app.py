import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pure SAR Utility ROI", layout="wide")

st.title("🛰️ Satellite Flood ROI: Pure SAR vs. Legacy Recon")
st.markdown("### *Eliminating Helicopters, Drones, and Information Darkness*")
st.divider()

# --- SIDEBAR: THE INVESTMENT ---
with st.sidebar:
    st.header("🏢 1. Satellite Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Major Flood Events / Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Field Force Scale")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    st.header("🚁 3. Legacy Recon Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_team_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- CALCULATIONS ---
# Amortize the sub across the events
sub_per_event = annual_sub / events_per_year
num_vehicles = total_people / 2.5

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy Response (Manual/Aerial)")
    t_wait = st.number_input("Wait for Weather/Access (Hrs)", value=48)
    t_assets = st.number_input("Total Assets in Flood Zone", value=2000)
    t_helo_hrs = st.number_input("Manual Helo Hours", value=15)
    t_drone_days = st.number_input("Manual Drone Days", value=12)

with col_right:
    st.subheader("🔵 Pure SAR Response (ICEYE)")
    s_wait = st.number_input("SAR Delivery Time (Hrs)", value=8)
    s_assets_verified = st.number_input("SAR-Verified Damage Sites", value=150)
    st.info("💡 **Zero Recon Cost:** SAR replaces all Helicopter and Drone discovery flights.")

# --- THE MATH ---
# 1. Legacy Totals
t_standby = (total_people * person_hr + num_vehicles * vehicle_hr) * t_wait
t_inspect = t_assets * 350
t_aerial = (t_helo_hrs * helo_hr) + (t_drone_days * drone_team_day)
t_total_event = t_standby + t_inspect + t_aerial

# 2. SAR Totals (Aerial is $0 because SAR is the recon tool)
s_standby = (total_people * person_hr + num_vehicles * vehicle_hr) * s_wait
s_inspect = s_assets_verified * 350
s_aerial_cost = 0 
s_total_event = s_standby + s_inspect + s_aerial_cost + sub_per_event

# --- RESULTS DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Legacy Cost / Event", f"${t_total_event:,.0f}")
m2.metric("True SAR Cost / Event", f"${s_total_event:,.0f}", 
          delta=f"-${t_total_event - s_total_event:,.0f}", delta_color="inverse")
m3.metric("Annual Net Benefit", f"${(t_total_event - s_total_event) * events_per_year:,.0f}")

# --- COMPARISON TABLE ---
st.subheader("Cost Comparison Table (Per Event)")
comparison_df = pd.DataFrame({
    "Category": ["Personnel Standby (Wait Time)", "Aerial Recon (Helo/Drones)", "Field Inspections (Truck Rolls)", "Satellite Data Cost"],
    "Legacy Method ($)": [f"${t_standby:,.0f}", f"${t_aerial:,.0f}", f"${t_inspect:,.0f}", "$0"],
    "Pure SAR Method ($)": [f"${s_standby:,.0f}", "$0 (Replaced by SAR)", f"${s_inspect:,.0f}", f"${sub_per_event:,.0f}"]
})
st.table(comparison_df)

# --- BAR CHART ---
st.subheader("Operational Spend: Legacy vs. Pure SAR")
chart_df = pd.DataFrame({
    "Category": ["Standby", "Recon", "Inspections"],
    "Legacy": [t_standby, t_aerial, t_inspect],
    "Pure SAR": [s_standby, 0, s_inspect]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"By eliminating **${t_aerial:,.0f}** in aerial recon and avoiding **{t_assets - s_assets_verified}** unnecessary truck rolls, the SAR solution creates a hard-cost saving of **${t_total_event - s_total_event:,.0f}** per event.")
