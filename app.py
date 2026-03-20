import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Utility SAR ROI Engine", layout="wide")

st.title("🛰️ Satellite vs. Traditional Response ROI")
st.markdown("#### *Quantifying Operational & Regulatory Gains for Australian Utilities*")

# --- SIDEBAR: GLOBAL INPUTS ---
with st.sidebar:
    st.header("💰 Solution Investment")
    # Manual entry for the satellite sub cost
    annual_sub_cost = st.number_input("Annual Satellite Subscription (AUD)", value=150000, step=10000)
    
    st.header("⚡ Regulatory Context")
    # Updated 2026 AER VCR Rate
    vcr_rate = st.number_input("AER VCR Rate (AUD/MWh)", value=46500, help="Value of Customer Reliability (2026 Inflation Adjusted)")
    
    st.header("📅 Event Scale")
    events_per_year = st.slider("Major Events per Year", 1, 10, 3)

# --- TABS FOR CUSTOMER INPUTS ---
tab1, tab2, tab3 = st.tabs(["Field Operations", "The Recon Gap", "Economic & Compliance"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Labor Costs")
        crew_day_rate = st.number_input("Crew Day Rate (AUD)", value=3200, help="Includes labor, vehicle, and equipment.")
        num_crews = st.number_input("Crews Deployed per Event", value=15)
    with c2:
        st.subheader("Efficiency")
        total_assets = st.number_input("Assets to Inspect", value=1200)
        wasted_rolls_pct = st.slider("Current 'Wasted' Truck Rolls (%)", 0.0, 1.0, 0.7, help="% of sites visited that end up having NO damage.")

with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Traditional Recon")
        trad_recon_hrs = st.number_input("Hours to 'Ground Truth' (Manual)", value=48, help="Time spent waiting for weather + manual scouting.")
    with c4:
        st.subheader("Satellite Recon")
        sat_recon_hrs = st.number_input("Hours to 'Ground Truth' (SAR)", value=12, help="Time from event trigger to Change Detection map.")

with tab3:
    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Network Load")
        avg_load_mw = st.number_input("Avg. Load Affected (MW)", value=15.0)
    with c6:
        st.subheader("Audit & Compliance")
        audit_hrs_saved = st.number_input("Admin Hours Saved/Event", value=80, help="Reduction in manual photo-matching for DRFA claims.")
        audit_rate = st.number_input("Internal Hourly Rate (AUD)", value=150)

# --- CALCULATIONS ---

# 1. Field Labor Savings (The Triage Lever)
# Traditional: Inspect all
days_trad = total_assets / (12 * num_crews) # Assuming 12 sites/day/crew baseline
labor_cost_trad = days_trad * crew_day_rate * num_crews

# Satellite: Skip the "Wasted" ones
assets_with_change = total_assets * (1 - wasted_rolls_pct)
days_sat = assets_with_change / (12 * num_crews)
labor_cost_sat = days_sat * crew_day_rate * num_crews
field_savings = (labor_cost_trad - labor_cost_sat)

# 2. VCR Savings (The Regulatory Lever)
lead_time_gain = trad_recon_hrs - sat_recon_hrs
vcr_savings = lead_time_gain * avg_load_mw * vcr_rate

# 3. Compliance Savings
admin_savings = audit_hrs_saved * audit_rate

# 4. FINAL ROI
total_savings_event = field_savings + vcr_savings + admin_savings
total_annual_savings = total_savings_event * events_per_year
net_annual_benefit = total_annual_savings - annual_sub_cost
roi_ratio = (net_annual_benefit / annual_sub_cost) if annual_sub_cost > 0 else 0

# --- RESULTS DASHBOARD ---
st.divider()
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric("Net Annual Benefit", f"AUD ${net_annual_benefit:,.0f}")
with res_col2:
    st.metric("Annual ROI", f"{roi_ratio:.1%}")
with res_col3:
    st.metric("Total Lead Time Gained", f"{lead_time_gain} Hours")

# Visualization
st.subheader("Where the Value Comes From (Per Event)")
chart_data = pd.DataFrame({
    "Category": ["Field Labor", "VCR Protection", "Compliance"],
    "Value (AUD)": [field_savings, vcr_savings, admin_savings]
})
st.bar_chart(chart_data, x="Category", y="Value (AUD)", color="#005299")

st.info(f"""
**Business Case Logic:** By investing **${annual_sub_cost:,.0f}**, the utility removes 
**${field_savings:,.0f}** in wasted field labor per event and protects **${vcr_savings:,.0f}** in community economic value by restoring power **{lead_time_gain} hours sooner**.
""")