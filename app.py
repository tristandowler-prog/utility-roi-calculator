import streamlit as st
import pandas as pd

st.set_page_config(page_title="Utility Flood ROI", layout="wide")

st.title("🛰️ Satellite Flood ROI: Operational Excellence")
st.markdown("### *A Data-Driven Comparison of Traditional Recon vs. SAR-Led Triage*")
st.divider()

# --- SIDEBAR: UNIT COSTS ---
with st.sidebar:
    st.header("👥 1. Field Force Units")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    person_hr = st.number_input("Labor Rate ($/hr/person)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr/vehicle)", value=55)
    
    st.divider()
    st.header("🏢 2. Annual Investment")
    annual_sub = st.number_input("Annual Satellite Sub ($)", value=150000)
    events_per_year = st.slider("Major Flood Events / Year", 1, 5, 2)
    contract_years = st.slider("Contract Term (Years)", 1, 5, 3)
    
    st.header("🚁 3. Aerial Unit Rates")
    helo_hr = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_team_day = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- SCENARIO INPUTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Traditional Response")
    recon_method = st.selectbox("Primary Tool", ["Helicopter", "Drone Fleet", "Hybrid"])
    t_wait = st.number_input("Recon Wait Time (Hrs)", value=48)
    t_assets = st.number_input("Total Assets in Zone", value=2000)
    
    t_helo_hrs = st.number_input("Manual Helo Hours", value=15) if recon_method in ["Helicopter", "Hybrid"] else 0
    t_drone_days = st.number_input("Manual Drone Days", value=12) if recon_method in ["Drone Fleet", "Hybrid"] else 0

with col_right:
    st.subheader("🔵 Satellite-Led Strategy")
    s_wait = st.number_input("SAR Map Delivery (Hrs)", value=8)
    s_assets_verified = st.number_input("SAR-Verified Damage Sites", value=150)
    s_helo_hrs = st.number_input("Targeted Helo Hours", value=2)
    s_drone_days = st.number_input("Targeted Drone Days", value=2)

# --- CALCULATION LOGIC ---
num_vehicles = total_people / 2.5

def get_breakdown(wait, assets, helo, drone):
    standby_labor = (total_people * person_hr) * wait
    standby_fleet = (num_vehicles * vehicle_hr) * wait
    inspections = assets * 350 # Direct cost per site visit
    aerial = (helo * helo_hr) + (drone * drone_team_day)
    return standby_labor, standby_fleet, inspections, aerial

# Get Values
t_lab, t_flt, t_ins, t_aer = get_breakdown(t_wait, t_assets, t_helo_hrs, t_drone_days)
s_lab, s_flt, s_ins, s_aer = get_breakdown(s_wait, s_assets_verified, s_helo_hrs, s_drone_days)

# --- RESULTS DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Manual Cost / Event", f"${(t_lab+t_flt+t_ins+t_aer):,.0f}")
m2.metric("SAR Cost / Event", f"${(s_lab+s_flt+s_ins+s_aer):,.0f}")
m3.metric("Net Annual Benefit", f"${((t_lab+t_flt+t_ins+t_aer - (s_lab+s_flt+s_ins+s_aer)) * events_per_year) - annual_sub:,.0f}")

# --- RESTORED: SAVINGS TABLE ---
st.subheader("💰 Detailed Savings Breakdown (Per Event)")
savings_data = {
    "Expense Category": ["Field Labor (Standby)", "Fleet (Idle/Wasted)", "Physical Inspections", "Aerial (Helo/Drone)"],
    "Traditional Cost": [f"${t_lab:,.0f}", f"${t_flt:,.0f}", f"${t_ins:,.0f}", f"${t_aer:,.0f}"],
    "Satellite Cost": [f"${s_lab:,.0f}", f"${s_flt:,.0f}", f"${s_ins:,.0f}", f"${s_aer:,.0f}"],
    "Hard Saving": [f"${t_lab-s_lab:,.0f}", f"${t_flt-s_flt:,.0f}", f"${t_ins-s_ins:,.0f}", f"${t_aer-s_aer:,.0f}"]
}
st.table(pd.DataFrame(savings_data))

# --- COMPARISON CHART ---
st.subheader("Operational Cost Comparison")
chart_df = pd.DataFrame({
    "Category": ["Labor", "Fleet", "Inspections", "Aerial"],
    "Traditional": [t_lab, t_flt, t_ins, t_aer],
    "Satellite": [s_lab, s_flt, s_ins, s_aer]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"Over **{contract_years} years**, this strategy delivers a total net benefit of **${(((t_lab+t_flt+t_ins+t_aer - (s_lab+s_flt+s_ins+s_aer)) * events_per_year) - annual_sub) * contract_years:,.0f}**.")
