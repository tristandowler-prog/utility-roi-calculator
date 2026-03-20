import streamlit as st
import pandas as pd

st.set_page_config(page_title="Flood ROI Comparison", layout="wide")

st.title("🛰️ Satellite Flood ROI: Manual vs. SAR Comparison")
st.markdown("---")

# --- SIDEBAR: UNIT RATES ---
with st.sidebar:
    st.header("👤 Labor & Fleet Units")
    person_hr = st.number_input("Person Hourly Rate ($)", value=175)
    vehicle_hr = st.number_input("Vehicle Hourly Rate ($)", value=55)
    helo_hr = st.number_input("Helicopter Hourly Rate ($)", value=4500)
    st.divider()
    st.header("🏢 Annual Investment")
    annual_sub = st.number_input("Satellite Subscription (AUD)", value=150000)

# --- SCENARIO INPUTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Traditional Response (Manual/Drone)")
    t_wait = st.number_input("Wait Time for Access (Hrs)", value=48, key="t_wait")
    t_people = st.number_input("People Deployed", value=50, key="t_people")
    t_fleet = st.number_input("Vehicles Deployed", value=20, key="t_fleet")
    t_helo = st.number_input("Helicopter Hours Needed", value=15, key="t_helo")
    t_waste_pct = st.slider("Wasted Visit Rate (%)", 0.0, 1.0, 0.75, key="t_waste")

with col_right:
    st.subheader("🔵 SAR-Guided Response")
    s_wait = st.number_input("Wait Time for SAR (Hrs)", value=8, key="s_wait")
    s_people = st.number_input("People Deployed", value=50, key="s_people") # Usually same headcount, just faster
    s_fleet = st.number_input("Vehicles Deployed", value=20, key="s_fleet")
    s_helo = st.number_input("Helicopter Hours (Backup Only)", value=2, key="s_helo")
    s_waste_pct = st.slider("Wasted Visit Rate (%)", 0.0, 1.0, 0.15, key="s_waste")

# --- CALCULATION LOGIC ---
def calc_costs(wait, people, fleet, helo, waste_pct):
    standby_cost = (people * person_hr + fleet * vehicle_hr) * wait
    aerial_cost = helo * helo_hr
    # Triage friction: Assuming 1000 planned visits @ $300 avg cost
    friction_cost = (1000 * waste_pct) * 300 
    return standby_cost + aerial_cost + friction_cost

trad_total = calc_costs(t_wait, t_people, t_fleet, t_helo, t_waste_pct)
sar_total = calc_costs(s_wait, s_people, s_fleet, s_helo, s_waste_pct)
savings_per_event = trad_total - sar_total

# --- THE COMPARISON CHART (RESTORED) ---
st.divider()
st.subheader("Event Cost Comparison: Manual vs. Satellite")

chart_data = pd.DataFrame({
    "Scenario": ["Manual (Status Quo)", "Satellite (SAR)"],
    "Total Cost (AUD)": [trad_total, sar_total]
})

# Displaying the comparison chart
st.bar_chart(chart_data, x="Scenario", y="Total Cost (AUD)", color="#D32F2F")

# --- KEY PERFORMANCE METRICS ---
m1, m2, m3 = st.columns(3)
m1.metric("Gross Savings / Event", f"AUD ${savings_per_event:,.0f}")
m2.metric("Headstart Gained", f"{t_wait - s_wait} Hours")
m3.metric("Wasted Visits Avoided", f"{int((t_waste_pct - s_waste_pct) * 1000)}")

st.success(f"**Annual ROI:** Based on 2 major floods, your net benefit is **${(savings_per_event * 2) - annual_sub:,.0f}** after the subscription cost.")
