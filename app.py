import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI: Fixed Cost Logic", layout="wide")

st.title("🛰️ ICEYE SAR: Fixed-Cost Subscription ROI")
st.markdown("### *Logic: High Utilization = Lower Per-Event Cost*")
st.divider()

# --- SIDEBAR: THE FIXED INVESTMENT ---
with st.sidebar:
    st.header("💰 1. The ICEYE Check")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Operational Rates")
    total_people = st.number_input("Total Personnel", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    
    st.header("🚁 3. Legacy Search Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_day_rate = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE "ACCOUNTING" MATH ---
data_cost_per_event = annual_sub / events_per_year
num_vehicles = total_people / 2.5
hourly_burn = (total_people * person_hr) + (num_vehicles * vehicle_hr)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Manual Search)")
    t_wait = st.number_input("Wait Time (Hrs)", value=48)
    t_assets = st.number_input("Total Assets in Zone", value=2000)
    t_helo_hrs = st.number_input("Helo Search Hours", value=15)
    t_drone_days = st.number_input("Drone Search Days", value=12)

with col_right:
    st.subheader("🔵 ICEYE (Observed Truth)")
    s_wait = st.number_input("SAR Delivery Time (Hrs)", value=8)
    s_assets_wet = st.number_input("Confirmed Wet Assets", value=140)
    st.info(f"💡 **Data Cost:** Your ${annual_sub:,.0f} sub currently costs **${data_cost_per_event:,.0f} per event**.")

# --- THE CALCULATIONS ---
t_standby_cost = hourly_burn * t_wait
t_recon_cost = (t_helo_hrs * helo_hr) + (t_drone_days * drone_day_rate)
t_visit_cost = t_assets * 350
t_event_total = t_standby_cost + t_recon_cost + t_visit_cost

s_standby_cost = hourly_burn * s_wait
s_visit_cost = s_assets_wet * 350
s_event_total = s_standby_cost + s_visit_cost + data_cost_per_event

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Legacy Cost / Event", f"${t_event_total:,.0f}")
m2.metric("True SAR Cost / Event", f"${s_event_total:,.0f}", delta=f"-${t_event_total - s_event_total:,.0f}", delta_color="inverse")

annual_net_benefit = (t_event_total - s_event_total) * events_per_year
m3.metric("Net Annual Position", f"${annual_net_benefit:,.0f}", help="Total yearly savings after paying the sub.")

# --- TABLE (FIXED SYNTAX) ---
st.subheader("Cost Breakdown (Per Event)")

# Formatting strings outside the dict to avoid SyntaxErrors
l_standby = f"${t_standby_cost:,.0f}"
l_recon = f"${t_recon_cost:,.0f}"
l_visit = f"${t_visit_cost:,.0f}"

s_standby = f"${s_standby_cost:,.0f}"
s_recon = "$0 (Replaced by SAR)"
s_visit = f"${s_visit_cost:,.0f}"
s_data = f"${data_cost_per_event:,.0f}"

comparison_data = {
    "Expense Category": ["Field Standby (Wait Time)", "Aerial Recon (Helo/Drone)", "Physical Site Inspections", "Satellite Data (Subscription Share)"],
    "Legacy Method": [l_standby, l_recon, l_visit, "$0"],
    "ICEYE Method": [s_standby, s_recon, s_visit, s_data]
}
st.table(pd.DataFrame(comparison_data))

# --- CHART ---
st.subheader("Cost Comparison per Event")
chart_df = pd.DataFrame({
    "Category": ["Standby", "Recon", "Inspections", "Data Cost"],
    "Legacy": [t_standby_cost, t_recon_cost, t_visit_cost, 0],
    "ICEYE": [s_standby_cost, 0, s_visit_cost, data_cost_per_event]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**Value Proposition:** ICEYE remotely clears **{int(t_assets - s_assets_wet)}** assets. You eliminate **${t_recon_cost:,.0f}** in search flights and **${t_visit_cost - s_visit_cost:,.0f}**
