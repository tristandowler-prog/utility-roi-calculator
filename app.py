import streamlit as st
import pandas as pd

st.set_page_config(page_title="Flood ROI - Multi-Year", layout="wide")

st.title("🛰️ Satellite Flood ROI: Multi-Year Strategic View")
st.markdown("---")

# --- SIDEBAR: PROCUREMENT & UNIT RATES ---
with st.sidebar:
    st.header("📅 1. Contract Terms")
    contract_years = st.slider("Contract Term (Years)", 1, 5, 3)
    base_annual_sub = st.number_input("Base Annual Sub (AUD)", value=150000)
    
    # Apply a standard multi-year discount (5% per year after year 1, capped at 20%)
    discount_factor = min((contract_years - 1) * 0.05, 0.20)
    discounted_sub = base_annual_sub * (1 - discount_factor)
    
    st.info(f"💡 {int(discount_factor*100)}% Multi-year discount applied.")
    st.write(f"**Adjusted Annual Cost:** ${discounted_sub:,.0f}")

    st.divider()
    st.header("🏢 Annual Scale")
    events_per_year = st.slider("Major Flood Events / Year", 1, 5, 2)
    
    st.header("👤 Unit Rates")
    person_hr = st.number_input("Person Hourly Rate ($)", value=175)
    vehicle_hr = st.number_input("Vehicle Hourly Rate ($)", value=55)
    helo_hr = st.number_input("Helicopter Hourly Rate ($)", value=4500)

# --- SCENARIO INPUTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Traditional Response")
    t_wait = st.number_input("Wait for Access (Hrs)", value=48, key="t_wait")
    t_people = st.number_input("People Deployed", value=60, key="t_people")
    t_fleet = st.number_input("Vehicles Deployed", value=25, key="t_fleet")
    t_helo = st.number_input("Helo Hours", value=15, key="t_helo")
    t_waste_pct = st.slider("Wasted Visit %", 0.0, 1.0, 0.75, key="t_waste")

with col_right:
    st.subheader("🔵 SAR-Guided Response")
    s_wait = st.number_input("Wait for SAR (Hrs)", value=8, key="s_wait")
    s_people = st.number_input("People Deployed", value=60, key="s_people") 
    s_fleet = st.number_input("Vehicles Deployed", value=25, key="s_fleet")
    s_helo = st.number_input("Helo Hours", value=2, key="s_helo")
    s_waste_pct = st.slider("Wasted Visit %", 0.0, 1.0, 0.15, key="s_waste")

# --- CALCULATIONS ---
def calc_costs(wait, people, fleet, helo, waste_pct):
    standby = (people * person_hr + fleet * vehicle_hr) * wait
    aerial = helo * helo_hr
    friction = (1000 * waste_pct) * 350 
    return standby + aerial + friction

t_event_cost = calc_costs(t_wait, t_people, t_fleet, t_helo, t_waste_pct)
s_event_cost = calc_costs(s_wait, s_people, s_fleet, s_helo, s_waste_pct)

# Multi-Year Totals
savings_per_event = t_event_cost - s_event_cost
total_savings_life = (savings_per_event * events_per_year) * contract_years
total_cost_life = discounted_sub * contract_years
net_benefit_life = total_savings_life - total_cost_life

# --- DASHBOARD ---
st.divider()
st.subheader(f"Strategic {contract_years}-Year Outlook")

m1, m2, m3 = st.columns(3)
m1.metric(f"Total {contract_years}-Year Net Benefit", f"AUD ${net_benefit_life:,.0f}")
m2.metric("Annual ROI %", f"{((savings_per_event * events_per_year) / discounted_sub * 100):,.0f}%")
m3.metric("Payback Speed", f"{(discounted_sub / savings_per_event):.1f} Events")

# --- MULTI-YEAR CHART ---
years = list(range(1, contract_years + 1))
cumulative_savings = [(savings_per_event * events_per_year * y) for y in years]
cumulative_cost = [discounted_sub * y for y in years]

multi_year_df = pd.DataFrame({
    "Year": years,
    "Cumulative Savings": cumulative_savings,
    "Cumulative Investment": cumulative_cost
})

st.line_chart(multi_year_df.set_index("Year"))

st.success(f"Over a **{contract_years}-year** term, the satellite solution generates **${total_savings_life:,.0f}** in operational savings against an investment of **${total_cost_life:,.0f}**.")
