import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR Executive ROI & ESG", layout="wide")

# --- DATA EXPORT ---
def create_download_link(df):
    report_text = f"SAR EXECUTIVE ROI & ESG AUDIT\n"
    report_text += f"------------------------------\n"
    report_text += f"DETAILED SCENARIO BREAKDOWN:\n{df.to_string()}"
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="SAR_Executive_ESG_Audit.txt" style="text-decoration:none;">📩 Download Full Audit & ESG Report</a>'

st.title("🛰️ SAR Strategic ROI: The ESG Auditor")
st.markdown("### *Financial Efficiency & Carbon Mitigation for Grid Resilience*")
st.divider()

# --- SIDEBAR: GLOBAL OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 15, 10)
    
    st.divider()
    st.header("👥 2. Force Burn Rates")
    total_people = st.number_input("Internal Personnel Dispatched", value=120)
    labor_rate = st.number_input("Avg Labor Rate ($/hr)", value=175)
    contractor_crews = st.number_input("Contractor Crews Mobilized", value=10)
    mob_fee_per_crew = st.number_input("Mob Fee per Crew ($)", value=15000)
    
    hourly_burn = (total_people * labor_rate) + (contractor_crews * 2 * 300) 
    st.info(f"**Total Force Burn:** ${hourly_burn:,.0f}/hr")

# --- THE SENSITIVITY SLIDER ---
st.subheader("🎯 Step 1: Set the Disaster Scope")
total_assets_in_zone = st.slider("Total Assets within Flood Extent", 50, 1000, 500)
wet_asset_ratio = st.slider("Percentage of Assets actually Sustaining Damage (%)", 5, 100, 30)
actual_wet_assets = int(total_assets_in_zone * (wet_asset_ratio / 100))

st.write(f"**Model Scope:** Analyzing response to **{total_assets_in_zone}** potential sites, with **{actual_wet_assets}** confirmed wet assets.")

# --- DATA SHARE ---
data_share = annual_sub / events_per_year

# --- SCENARIO PARAMETERS ---
scenarios = {
    "Pessimistic": {"search_hrs": 24, "double_trip_pct": 0.10, "mob_reduction": 0.10, "repair_hrs": 84, "aerial": 45000, "co2_mult": 0.8},
    "Likely": {"search_hrs": 48, "double_trip_pct": 0.30, "mob_reduction": 0.40, "repair_hrs": 72, "aerial": 85000, "co2_mult": 1.0},
    "Optimistic": {"search_hrs": 72, "double_trip_pct": 0.50, "mob_reduction": 0.70, "repair_hrs": 60, "aerial": 125000, "co2_mult": 1.2}
}

# --- CALCULATIONS ---
results = []
for name, s in scenarios.items():
    # LEGACY CALCULATIONS
    l_search_labor = hourly_burn * s["search_hrs"]
    l_mob = contractor_crews * mob_fee_per_crew
    l_visits = total_assets_in_zone * 450
    l_double_trips = (actual_wet_assets * s["double_trip_pct"]) * 450
    l_repair = hourly_burn * 96 
    l_total = l_search_labor + s["aerial"] + l_mob + l_visits + l_double_trips + l_repair
    
    # SAR CALCULATIONS
    s_desk = hourly_burn * 4
    s_mob = (contractor_crews * (1 - s["mob_reduction"])) * mob_fee_per_crew
    s_visits = actual_wet_assets * 450
    s_repair = hourly_burn * s["repair_hrs"]
    s_total = data_share + s_desk + s_mob + s_visits + s_repair
    
    # ESG LOGIC (CO2 Metric Tons)
    # Assumes: Helo = 0.5 tons/hr, Truck = 0.02 tons/visit
    l_co2 = (s["search_hrs"] * 0.5) + (total_assets_in_zone * 0.02) + (actual_wet_assets * s["double_trip_pct"] * 0.02)
    s_co2 = (actual_wet_assets * 0.02)
    co2_saved = (l_co2 - s_co2) * s["co2_mult"]
    
    savings = l_total - s_total
    results.append({
        "Scenario": name,
        "Annual Savings": savings * events_per_year,
        "ROI (%)": (savings * events_per_year / annual_sub) * 100,
        "CO2 Saved (Tons)": co2_saved * events_per_year
    })

df_res = pd.DataFrame(results)

# --- DASHBOARD ---
st.divider()
cols = st.columns(3)
for i, name in enumerate(["Pessimistic", "Likely", "Optimistic"]):
    with cols[i]:
        row = df_res.iloc[i]
        st.subheader(f"{name} View")
        st.metric("Annual Savings", f"${row['Annual Savings']:,.0f}")
        st.metric("Annual CO2 Reduction", f"{row['CO2 Saved (Tons)']:,.1f} MT")
        st.metric("ROI", f"{row['ROI (%)']:,.0f}%")

# --- THE ESG EXPLAINER ---
st.info("💡 **ESG Impact:** Carbon savings are driven by grounding fuel-heavy helicopters and eliminating thousands of miles of 'blind' truck rolls to dry assets.")

st.divider()

# --- TABLE FOR THE AUDITORS ---
st.subheader("📊 Operational Audit: Defensible Logic")
audit_df = pd.DataFrame({
    "Variable": ["Blind Scouting Time", "Aerial Recon Budget", "Contractor Reduction", "Targeted Repair Time"],
    "Pessimistic": ["24 Hours", "$45k", "10% Reduction", "84 Hours"],
    "Likely": ["48 Hours", "$85k", "40% Reduction", "72 Hours"],
    "Optimistic": ["72 Hours", "$125k", "70% Reduction", "60 Hours"]
})
st.table(audit_df)

# Explainers under the table
st.markdown("""
**Glossary of Executive Metrics:**
* **Blind Scouting Time:** The man-hours internal crews spend driving through flood zones to manually find 'wet' assets.
* **Aerial Recon Budget:** The hard cost of helicopter and drone contracts triggered per disaster event.
* **Contractor Reduction:** The percentage of mutual aid/contractor fees avoided by freeing up internal staff from search tasks.
* **Targeted Repair Time:** The efficiency gained by arriving with the correct depth-specific equipment on the first trip.
""")

# --- CHART ---
st.subheader("Annual Financial Impact vs. Carbon Mitigation")

chart_data = df_res[['Scenario', 'Annual Savings']].set_index('Scenario')
st.bar_chart(chart_data)

st.success("**Final Verdict:** SAR delivers a triple-bottom-line win: Significant financial ROI, drastically reduced restoration times, and a measurable reduction in the disaster-response carbon footprint.")

# --- EXPORT ---
st.markdown(create_download_link(df_res), unsafe_allow_html=True)
