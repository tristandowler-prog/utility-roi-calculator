import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR Strategic ROI", layout="wide")

# --- DATA EXPORT ---
def create_download_link(val1, val2, val3, df):
    report_text = f"SAR STRATEGIC ROI REPORT\n"
    report_text += f"-------------------------\n"
    report_text += f"Legacy Event Total: {val1}\n"
    report_text += f"SAR Event Total: {val2}\n"
    report_text += f"Net Annual Position: {val3}\n\n"
    report_text += f"DETAILED BREAKDOWN:\n{df.to_string()}"
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="SAR_ROI_Report.txt" style="text-decoration:none;">📩 Download Full Audit Report</a>'

st.title("🛰️ SAR Strategic ROI: Mobilization & Efficiency")
st.markdown("### *Why Intel Wins Even When Every Asset is Wet*")
st.divider()

# --- SIDEBAR: OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Observed Per Year", 1, 15, 10)
    
    st.divider()
    st.header("👥 2. Force Multipliers")
    total_people = st.number_input("Internal Personnel Dispatched", value=120)
    labor_rate = st.number_input("Internal Labor Rate ($/hr)", value=175)
    
    st.divider()
    st.header("🏗️ 3. Mobilization (Contractors)")
    contractor_crews = st.number_input("Contractor Crews Called In", value=10)
    mob_fee_per_crew = st.number_input("Mobilization Fee per Crew ($)", value=15000)
    
    # Internal burn + Contractor burn
    hourly_burn = (total_people * labor_rate) + (contractor_crews * 2 * 300) 
    st.info(f"**Total Force Burn:** ${hourly_burn:,.0f}/hr")

# --- DATA SHARE ---
data_share = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Manual Response)")
    
    t_search_hrs = st.number_input("Blind Scouting Hours", value=48, key="leg_search")
    st.caption("**Scouting:** Time internal crews spend 'hunting' for damage while the clock is ticking.")
    
    total_aerial = st.number_input("Total Aerial Recon Cost / Event ($)", value=85000)
    st.caption("**Aerial Recon:** Fixed costs for helicopters to map the flood extent.")

    t_mob_cost = contractor_crews * mob_fee_per_crew
    st.caption(f"**Mobilization:** ${t_mob_cost:,.0f} spent on contractor call-out fees due to internal search delays.")
    
    t_total_assets = st.number_input("Total Assets in Flood Zone", value=500)
    t_double_trip_rate = st.slider("Legacy 'Double Trip' %", 0, 100, 30)
    st.caption("**The Blind Penalty:** Percentage of sites requiring a second visit because Trip 1 lacked the right gear.")
    
    t_repair_hrs = st.number_input("Legacy Repair Hours", value=96, key="leg_repair")
    st.caption("**Wrench Time:** Slower repair execution due to 'arriving and assessing' instead of 'arriving and fixing'.")
    
    # Legacy Math
    legacy_search_labor = hourly_burn * t_search_hrs
    legacy_base_visits = t_total_assets * 450
    legacy_double_trips = (t_total_assets * (t_double_trip_rate/100)) * 450
    legacy_repair_labor = hourly_burn * t_repair_hrs
    legacy_total = legacy_search_labor + total_aerial + t_mob_cost + legacy_base_visits + legacy_double_trips + legacy_repair_labor

with col_right:
    st.subheader("🔵 SAR (Intelligence-Led)")
    
    s_desk_hrs = st.number_input("Desk Review Hours", value=4, key="sar_desk")
    st.caption("**Targeting:** Rapid identification of wet/dry sites from the office using SAR ground truth.")
    
    s_mob_reduction = st.slider("Contractor Reduction with SAR (%)", 0, 100, 50)
    st.caption("**Force Optimization:** Since internal crews skip 'scouting,' they can start 'fixing' immediately, reducing contractor dependency.")
    
    s_mob_cost = (contractor_crews * (1 - s_mob_reduction/100)) * mob_fee_per_crew
    
    s_wet_assets = st.number_input("Confirmed 'Wet' Assets", value=500)
    s_repair_hrs = st.number_input("Targeted Repair Hours", value=72, key="sar_repair")
    st.caption("**Logistics Speed:** Faster execution because crews know exactly which pumps and vehicles to bring on Trip 1.")
    
    # SAR Math
    sar_desk_labor = hourly_burn * s_desk_hrs
    sar_targeted_visits = s_wet_assets * 450
    sar_repair_labor = hourly_burn * s_repair_hrs
    sar_total = data_share + sar_desk_labor + s_mob_cost + sar_targeted_visits + sar_repair_labor
    
    st.success(f"💡 **SAR ROI:** Data share is **${data_share:,.0f}**. Total saved on call-outs: **${t_mob_cost - s_mob_cost:,.0f}**.")

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

l_total_str = f"${legacy_total:,.0f}"
s_total_str = f"${sar_total:,.0f}"
net_annual = f"${(legacy_total - sar_total) * events_per_year:,.0f}"

m1.metric("Legacy Cost / Event", l_total_str)
m2.metric("SAR Cost / Event", s_total_str, delta=f"-${legacy_total - sar_total:,.0f}", delta_color="inverse")
m3.metric("Annual ROI (Net Savings)", net_annual)

# --- THE COMPARISON TABLE ---
st.subheader("Operational Efficiency Audit")
comparison_df = pd.DataFrame({
    "Cost Driver": ["Discovery (Search/Helos)", "Contractor Mobilization", "Site Visits (Incl. Waste)", "Repair Labor (Wrench Time)", "SAR Subscription"],
    "Legacy Approach ($)": [f"${legacy_search_labor + total_aerial:,.0f}", f"${t_mob_cost:,.0f}", f"${legacy_base_visits + legacy_double_trips:,.0f}", f"${legacy_repair_labor:,.0f}", "$0"],
    "SAR Approach ($)": [f"${sar_desk_labor:,.0f}", f"${s_mob_cost:,.0f}", f"${sar_targeted_visits:,.0f}", f"${sar_repair_labor:,.0f}", f"${data_share:,.0f}"]
})
st.table(comparison_df)

# --- CHART ---
st.subheader("Resource Allocation per Event")
chart_df = pd.DataFrame({
    "Activity": ["Scouting Waste", "Contractor Mob", "Direct Repairs", "SAR Subscription"],
    "Legacy": [legacy_search_labor + total_aerial + legacy_double_trips, t_mob_cost, legacy_repair_labor + legacy_base_visits, 0],
    "SAR": [sar_desk_labor, s_mob_cost, sar_repair_labor + sar_targeted_visits, data_share]
})
st.bar_chart(chart_df.set_index("Activity"))


st.success(f"**Executive Verdict:** SAR converts **${legacy_search_labor + legacy_double_trips + (t_mob_cost - s_mob_cost):,.0f}** in operational friction into bottom-line savings per event.")

# --- EXPORT ---
st.markdown(create_download_link(l_total_str, s_total_str, net_annual, comparison_df), unsafe_allow_html=True)
