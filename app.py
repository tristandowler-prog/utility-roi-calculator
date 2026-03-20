import streamlit as st
import pandas as pd

st.set_page_config(page_title="Utility Flood ROI Engine", layout="wide")

st.title("🛰️ Satellite Flood Response ROI")
st.markdown("#### *Quantifying 'Lead Time' & Operational Friction for Queensland Utilities*")

# --- SIDEBAR: THE INVESTMENT & BASELINE ---
with st.sidebar:
    st.header("💳 1. The Investment")
    annual_sub = st.number_input("Annual Satellite Subscription (AUD)", value=150000)
    events_per_year = st.slider("Major Flood Events per Year", 1, 5, 2)
    
    st.header("👥 2. Crew Baseline")
    num_crews = st.number_input("Crews Deployed per Event", value=20)
    crew_cost_hr = st.number_input("Crew Hourly Rate (AUD)", value=400, help="Fully loaded: Labor + 4WD + Gear")
    crew_cost_day = st.number_input("Crew Cost per Day (AUD)", value=3200)

# --- INPUT TABS: THE FRICTION LEVERS ---
t1, t2, t3 = st.tabs(["The Recon Gap (Time)", "Field & Aerial Friction", "Compliance & Recovery"])

with t1:
    st.subheader("The 'Blindness' Period")
    col1, col2 = st.columns(2)
    with col1:
        trad_recon_hrs = st.number_input("Hours until Ground/Drone Access (Manual)", value=48, help="Time waiting for floodwaters to recede or roads to clear.")
    with col2:
        sat_recon_hrs = st.number_input("Hours to SAR Change Detection Map", value=8, help="Time from flood trigger to actionable triage data.")
    
    hrs_gained = trad_recon_hrs - sat_recon_hrs
    st.info(f"💡 **Operational Lead Time:** Satellite provides a **{hrs_gained} hour** headstart.")

with t2:
    st.subheader("Field & Aerial Hard Costs")
    col3, col4 = st.columns(2)
    with col3:
        st.write("**Aerial Surveys (Helo/Drone)**")
        helo_hrs_event = st.number_input("Helicopter Flight Hours per Event", value=12)
        helo_rate = st.number_input("Helicopter Hourly Rate (AUD)", value=4500)
        drone_team_days = st.number_input("Drone Pilot Team Days", value=5)
        drone_day_rate = st.number_input("Drone Team Day Rate (AUD)", value=2500)
    with col4:
        st.write("**Wasted Attempts (Closed Roads/No Damage)**")
        total_inspections = st.number_input("Total Potential Sites to Inspect", value=1500)
        wasted_attempt_rate = st.slider("Wasted Visits % (Blocked/No Damage)", 0.0, 1.0, 0.75)
        cost_per_attempt = st.number_input("Cost per Wasted Attempt (Fuel/Time)", value=350)

with t3:
    st.subheader("Post-Event Recovery & QRA/DRFA")
    col5, col6 = st.columns(2)
    with col5:
        comp_hrs_event = st.number_input("Compliance/Audit Hours per Event", value=160, help="Time spent matching photos to assets for QRA/DRFA.")
        comp_rate = st.number_input("Compliance Hourly Rate (AUD)", value=185)
    with col6:
        recovery_costs_base = st.number_input("Baseline Recovery Costs (AUD)", value=1000000, help="Repair materials and contract labor.")

# --- THE HARD SAVINGS CALCULATIONS ---

# 1. Lead Time Labor Saving (Standby/Recon)
# Saving 40 hours of 'blind' time for 20 crews is a massive direct saving.
standby_savings = hrs_gained * num_crews * crew_cost_hr

# 2. Aerial Survey Replacement
aerial_savings = (helo_hrs_event * helo_rate) + (drone_team_days * drone_day_rate)

# 3. Wasted Attempt Avoidance (The 'Closed Road' Lever)
# SAR identifies flooded roads and undamaged sites so we skip them.
triage_savings = (total_inspections * wasted_attempt_rate) * cost_per_attempt

# 4. Compliance Efficiency
# SAR provides a digital receipt for QRA/DRFA, slashing admin time by 50%.
admin_savings = (comp_hrs_event * 0.5) * comp_rate

# --- TOTALS ---
event_savings = standby_savings + aerial_savings + triage_savings + admin_savings
annual_savings = event_savings * events_per_year
net_benefit = annual_savings - annual_sub

# --- DASHBOARD ---
st.divider()



m1, m2, m3 = st.columns(3)
m1.metric("Net Annual Hard Benefit", f"AUD ${net_benefit:,.0f}")
m2.metric("Savings per Event", f"AUD ${event_savings:,.0f}")
m3.metric("Lead Time Gained", f"{hrs_gained} Hours")

st.divider()
st.subheader("Direct Cost Recovery Breakdown (Per Event)")
breakdown = pd.DataFrame({
    "Category": ["Crew Standby (Time)", "Aerial Surveys", "Wasted Visits", "Compliance/Audit"],
    "Savings (AUD)": [standby_savings, aerial_savings, triage_savings, admin_savings]
})
st.bar_chart(breakdown, x="Category", y="Savings (AUD)", color="#D32F2F")

st.success(f"""
**The Ergon Business Case:** By bypassing **{total_inspections * wasted_attempt_rate:,.0f}** wasted site visits 
and gaining a **{hrs_gained}-hour** headstart, the utility recovers the annual satellite investment 
within **{(annual_sub / event_savings) if event_savings > 0 else 0:.1f}** major flood events.
""")
