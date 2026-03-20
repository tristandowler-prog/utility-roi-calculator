import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR Boardroom ROI Auditor", layout="wide")

# --- DATA EXPORT ---
def create_download_link(df):
    report_text = f"SAR EXECUTIVE ROI AUDIT REPORT\n"
    report_text += f"------------------------------\n"
    report_text += f"DETAILED SCENARIO BREAKDOWN:\n{df.to_string()}"
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="SAR_Executive_Audit.txt" style="text-decoration:none;">📩 Download Full Audit Report</a>'

st.title("🛰️ SAR Strategic ROI: Boardroom Auditor")
st.markdown("### *Operational Efficiency & Cost-Avoidance for Utility Grids*")
st.divider()

# --- SIDEBAR: GLOBAL OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 15, 6)
    st.caption("Based on 2025/26 AU flood declarations.")
    
    st.divider()
    st.header("👥 2. Force Burn Rates")
    total_people = st.number_input("Internal Personnel Dispatched", value=120)
    labor_rate = st.number_input("Avg Labor Rate ($/hr)", value=175)
    contractor_crews = st.number_input("Contractor Crews Mobilized", value=15)
    mob_fee_per_crew = st.number_input("Mob Fee per Crew ($)", value=15000)
    
    # Internal + Contractor Burn
    hourly_burn = (total_people * labor_rate) + (contractor_crews * 2 * 350) 
    st.info(f"**Total Force Burn:** ${hourly_burn:,.0f}/hr")

# --- THE SENSITIVITY SLIDER (THE "TRUTH" FILTER) ---
st.subheader("🎯 Step 1: Set the Disaster Scope")
col_s1, col_s2 = st.columns(2)

with col_s1:
    total_assets_in_zone = st.slider("Total Assets in Flood Footprint", 50, 2000, 500)
    st.caption("The broad area utility crews must 'verify' after an event.")

with col_s2:
    wet_asset_ratio = st.slider("Percentage actually Damaged (%)", 5, 100, 20)
    actual_wet_assets = int(total_assets_in_zone * (wet_asset_ratio / 100))
    st.caption(f"SAR isolates the **{actual_wet_assets}** wet sites from the **{total_assets_in_zone - actual_wet_assets}** dry ones.")

# --- DATA SHARE ---
data_share = annual_sub / events_per_year

# --- SCENARIO PARAMETERS ---
scenarios = {
    "Pessimistic": {"search_hrs": 24, "double_trip_pct": 0.10, "mob_reduction": 0.10, "repair_hrs": 84, "aerial": 45000},
    "Likely": {"search_hrs": 48, "double_trip_pct": 0.30, "mob_reduction": 0.40, "repair_hrs": 72, "aerial": 85000},
    "Optimistic": {"search_hrs": 72, "double_trip_pct": 0.50, "mob_reduction": 0.70, "repair_hrs": 60, "aerial": 150000}
}

# --- CALCULATIONS ---
results = []
for name, s in scenarios.items():
    # LEGACY CALCULATIONS
    l_search_labor = hourly_burn * s["search_hrs"]
    l_mob = contractor_crews * mob_fee_per_crew
    l_base_visits = total_assets_in_zone * 450
    l_double_trips = (actual_wet_assets * s["double_trip_pct"]) * 450
    l_repair = hourly_burn * 96 
    l_total = l_search_labor + s["aerial"] + l_mob + l_base_visits + l_double_trips + l_repair
    
    # SAR CALCULATIONS
    s_desk = hourly_burn * 4
    s_mob = (contractor_crews * (1 - s["mob_reduction"])) * mob_fee_per_crew
    s_visits = actual_wet_assets * 450
    s_repair = hourly_burn * s["repair_hrs"]
    s_total = data_share + s_desk + s_mob + s_visits + s_repair
    
    savings = l_total - s_total
    results.append({
        "Scenario": name,
        "Annual Savings": savings * events_per_year,
        "ROI (%)": (savings * events_per_year / annual_sub) * 100,
        "Hours Saved": s["search_hrs"] - 4
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
        st.metric("ROI", f"{row['ROI (%)']:,.0f}%")
        st.caption(f"Accelerates Restoration by {row['Hours Saved']} Hours")

st.divider()

# --- THE AUDIT TABLE ---
st.subheader("📊 Operational Audit: Defensible Logic")
audit_df = pd.DataFrame({
    "Efficiency Driver": ["Blind Scouting Time", "Aerial Recon Budget", "Contractor Mob Reduction", "Repair Efficiency (Wrench Time)"],
    "Pessimistic": ["24 Hours", "$45k", "10% Reduction", "84 Hours"],
    "Likely": ["48 Hours", "$85k", "40% Reduction", "72 Hours"],
    "Optimistic": ["72 Hours", "$150k", "70% Reduction", "60 Hours"]
})
st.table(audit_df)

st.markdown("""
**Operational Definitions:**
* **Blind Scouting Time:** The phase where internal crews manually drive the network to verify 'wet' vs 'dry' status.
* **Aerial Recon:** Fixed costs for helicopter/drone surveying to determine safe access and damage extent.
* **Contractor Mob Reduction:** Savings from utilizing in-house teams for repairs earlier, bypassing the need for expensive outside contractors.
* **Repair Efficiency:** Faster 'Wrench-Time' because crews arrive with the correct depth-specific equipment on Trip 1.
""")

# --- CHART ---
st.subheader("Total Savings vs. Damage Scale")
chart_data = df_res[['Scenario', 'Annual Savings']].set_index('Scenario')
st.bar_chart(chart_data)

st.success("**The Financial Verdict:** Even in a pessimistic scenario, SAR eliminates the 'Search Phase' overhead, yielding a positive ROI. In a likely scenario, the subscription is paid for by the first major flood event of the season.")

# --- EXPORT ---
st.markdown(create_download_link(df_res), unsafe_allow_html=True)
