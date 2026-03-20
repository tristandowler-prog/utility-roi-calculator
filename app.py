import streamlit as st
import pandas as pd

st.set_page_config(page_title="Utility Flood ROI - Final", layout="wide")

st.title("🛰️ Satellite Flood ROI: The Strategic Asset View")
st.markdown("---")

# --- SIDEBAR: UNIT RATES & SCALE ---
with st.sidebar:
    st.header("🏢 Annual Scale & Contract")
    contract_years = st.slider("Contract Term (Years)", 1, 5, 3)
    annual_sub = st.number_input("Annual Subscription (AUD)", value=150000)
    events_per_year = st.slider("Major Flood Events / Year", 1, 5, 2)
    
    st.divider()
    st.header("👤 Labor & Fleet Units")
    people_deployed = st.number_input("Total Personnel", value=60)
    person_hr = st.number_input("Person Hourly Rate ($)", value=175)
    vehicle_hr = st.number_input("Vehicle Hourly Rate ($)", value=55)
    helo_hr = st.number_input("Helicopter Hourly Rate ($)", value=4500)

# --- SCENARIO INPUTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Traditional Response")
    t_wait = st.number_input("Wait for Access (Hrs)", value=48)
    t_assets = st.number_input("Total Assets to Inspect", value=2000, help="Every pole/transformer in the blue zone.")
    t_waste_pct = st.slider("Wasted Visit Rate (%)", 0.0, 1.0, 0.85, help="Percentage of sites visited that are found to be undamaged.")
    t_helo = st.number_input("Helicopter Hours Needed", value=15)

with col_right:
    st.subheader("🔵 SAR-Guided Response")
    s_wait = st.number_input("Wait for SAR (Hrs)", value=8)
    s_assets_triaged = st.number_input("Assets Flagged as 'Damaged'", value=150, help="Only these sites receive a physical visit.")
    s_waste_pct = st.slider("Residual Waste Rate (%)", 0.0, 1.0, 0.10)
    s_helo = st.number_input("Helicopter Hours (Targeted)", value=2)

# --- CALCULATIONS ---
def calc_event_costs(wait, assets, waste_pct, helo):
    # Standby Cost (People + Fleet)
    standby = (people_deployed * person_hr + (people_deployed/2.5) * vehicle_hr) * wait
    # Inspection Cost (Assuming $350 per physical visit)
    inspection_cost = assets * 350 
    # Aerial
    aerial = helo * helo_hr
    return standby + inspection_cost + aerial, standby, inspection_cost, aerial

# Run Calculations
t_total, t_standby, t_inspect, t_aerial = calc_event_costs(t_wait, t_assets, t_waste_pct, t_helo)
# For SAR, we only inspect the triaged assets
s_total, s_standby, s_inspect, s_aerial = calc_event_costs(s_wait, s_assets_triaged, s_waste_pct, s_helo)

# --- RESULTS ---
savings_per_event = t_total - s_total
total_annual_savings = savings_per_event * events_per_year
net_annual_position = total_annual_savings - annual_sub

st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("Trad. Cost per Event", f"AUD ${t_total:,.0f}")
res2.metric("SAR Cost per Event", f"AUD ${s_total:,.0f}")
res3.metric("Annual Net Benefit", f"AUD ${net_annual_position:,.0f}", delta=f"${total_annual_savings:,.0f} Gross")

# --- COMPARISON CHART ---
st.subheader("Where the Money Goes: Manual vs. SAR")
chart_data = pd.DataFrame({
    "Category": ["Labor Standby", "Physical Inspections", "Aerial Surveys"],
    "Traditional (Manual)": [t_standby, t_inspect, t_aerial],
    "Satellite (SAR)": [s_standby, s_inspect, s_aerial]
})
st.bar_chart(chart_data.set_index("Category"))

st.success(f"By triaging **{t_assets} impacted assets** down to just **{s_assets_triaged} verified targets**, you eliminate **${t_inspect - s_inspect:,.0f}** in unnecessary field inspections.")
