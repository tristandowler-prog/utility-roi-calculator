import streamlit as st
import pandas as pd

st.set_page_config(page_title="Utility Hard Savings ROI", layout="wide")

st.title("🛰️ Satellite Response: Hard Cost ROI")
st.markdown("#### *Focus: Direct Budgetary Savings vs. Manual Operations*")

# --- SIDEBAR: THE INVESTMENT ---
with st.sidebar:
    st.header("💳 The Investment")
    sat_annual_sub = st.number_input("Annual Satellite Subscription (AUD)", value=150000)
    events_per_year = st.slider("Events per Year", 1, 10, 3)

# --- INPUTS: THE "CASH" LEVERS ---
t1, t2 = st.tabs(["Field & Aerial Savings", "Compliance & Admin"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Field Ops (Triage)")
        total_sites = st.number_input("Total Sites in Disaster Zone", value=1200)
        waste_rate = st.slider("Wasted Visit Rate (%)", 0.0, 1.0, 0.75, help="% of sites checked that are found to be 'OK'.")
        cost_per_visit = st.number_input("Cost per Emergency Visit (AUD)", value=350)
    with col2:
        st.subheader("Aerial Surveys")
        helo_hrs = st.number_input("Helicopter Hours per Event", value=12)
        helo_rate = st.number_input("Helicopter Rate (AUD/hr)", value=4500)

with t2:
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Compliance (DRFA)")
        admin_hrs_saved = st.number_input("Audit Hours Saved per Event", value=120)
        internal_rate = st.number_input("Staff Hourly Rate (AUD)", value=165)
    with col4:
        st.subheader("Logistics")
        gen_hire_avoided = st.number_input("Avoided Temp Power/Gen Costs", value=25000)

# --- THE HARD MATH ---
# 1. Labor Savings
labor_savings = (total_sites * waste_rate) * cost_per_site_visit if 'cost_per_site_visit' in locals() else (total_sites * waste_rate) * cost_per_visit
# 2. Aerial Savings
aerial_savings = helo_hrs * helo_rate
# 3. Admin/Audit
admin_savings = admin_hrs_saved * internal_rate
# 4. Total per Event
event_total = labor_savings + aerial_savings + admin_savings + gen_hire_avoided
# 5. Annual Total
annual_hard_savings = event_total * events_per_year
net_benefit = annual_hard_savings - sat_annual_sub

# --- DASHBOARD ---
st.divider()

m1, m2, m3 = st.columns(3)
m1.metric("Net Cash Benefit (Annual)", f"AUD ${net_benefit:,.0f}")
m2.metric("Savings per Event", f"AUD ${event_total:,.0f}")
m3.metric("Payback Period", f"{(sat_annual_sub / event_total) if event_total > 0 else 0:.1f} Events")

st.divider()
st.subheader("Hard Savings Breakdown")
breakdown = pd.DataFrame({
    "Category": ["Avoided Field Waste", "Aerial Survey Replacement", "Compliance Efficiency", "Logistics/Generators"],
    "Savings (AUD)": [labor_savings, aerial_savings, admin_savings, gen_hire_avoided]
})
st.bar_chart(breakdown, x="Category", y="Savings (AUD)", color="#2E8B57")

st.info(f"**The CFO Pitch:** This investment pays for itself within **{((sat_annual_sub / event_total) if event_total > 0 else 0):.1f}** major events. By using SAR to bypass **{total_sites * waste_rate:,.0f}** unnecessary inspections, we recover the subscription cost through field efficiency alone.")
