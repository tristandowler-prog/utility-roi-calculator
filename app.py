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
    t_people = st.number_input("People Deployed", value=60, key="t_people")
    t_fleet = st.number_input("Vehicles Deployed", value=25, key="t_fleet")
    t_helo = st.number_input("Helicopter Hours Needed", value=15, key="t_helo")
    t_waste_pct = st.slider("Wasted Visit Rate (%)", 0.0, 1.0, 0.75, key="t_waste")

with col_right:
    st.subheader("🔵 SAR-Guided Response")
    s_wait = st.number_input("Wait Time for SAR (Hrs)", value=8, key="s_wait")
    s_people = st.number_input("People Deployed", value=60, key="s_people") 
    s_fleet = st.number_input("Vehicles Deployed", value=25, key="s_fleet")
    s_helo = st.number_input("Helicopter Hours (Backup Only)", value=2, key="s_helo")
    s_waste_pct = st.slider("Wasted Visit Rate (%)", 0.0, 1.0, 0.15, key="s_waste")

# --- CALCULATION LOGIC ---
def calc_event_breakdown(wait, people, fleet, helo, waste_pct):
    standby = (people * person_hr + fleet * vehicle_hr) * wait
    aerial = helo * helo_hr
    # Triage friction: Assuming 1000 planned visits @ $350 avg cost per visit
    friction = (1000 * waste_pct) * 350 
    total = standby + aerial + friction
    return total, standby, aerial, friction

# Run Calculations
t_total, t_standby, t_aerial, t_friction = calc_event_breakdown(t_wait, t_people, t_fleet, t_helo, t_waste_pct)
s_total, s_standby, s_aerial, s_friction = calc_event_breakdown(s_wait, s_people, s_fleet, s_helo, s_waste_pct)

# --- THE RESULTS DASHBOARD ---
st.divider()
res1, res2 = st.columns(2)

with res1:
    st.metric("Trad. Cost per Event", f"AUD ${t_total:,.0f}")
    st.error(f"Manual response is driven by {t_wait} hours of 'Information Darkness'.")

with res2:
    st.metric("SAR Cost per Event", f"AUD ${s_total:,.0f}", delta=f"-${t_total - s_total:,.0f}", delta_color="inverse")
    st.success(
