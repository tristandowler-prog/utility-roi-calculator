import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR Strategic ROI", layout="wide")

# --- DATA EXPORT ---
def create_download_link(val1, val2, val3, df):
    report_text = f"SAR STRATEGIC ROI REPORT\n"
    report_text += f"-------------------------\n"
    report_text += f"Legacy Total Cost: {val1}\n"
    report_text += f"SAR Total Cost: {val2}\n"
    report_text += f"Net Annual Position: {val3}\n\n"
    report_text += f"DETAILED BREAKDOWN:\n{df.to_string()}"
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="SAR_ROI_Report.txt" style="text-decoration:none;">📩 Download Full Audit Report</a>'

st.title("🛰️ SAR Strategic ROI: Operational Efficiency")
st.markdown("### *Modeling 'Wasted Visits' vs. 'Targeted Dispatch'*")
st.divider()

# --- SIDEBAR: OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 10)
    
    st.divider()
    st.header("👥 2. Fleet & Labor Rates")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)
    st.info(f"**Field Force Burn:** ${hourly_burn:,.0f}/hr")

# --- THE CALCULATIONS ---
data_share = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Blind Response)")
    t_search_hrs = st.number_input("Hours spent scouting/finding damage", value=48, key="leg_search")
    t_helo_costs = st.number_input("Aerial Recon Costs (Helos/Drones)", value=85000)
    
    # WASTED VISITS LOGIC
    t_total_assets = st.number_input("Total Assets in Flood Zone", value=500)
    t_visit_cost = st.number_input("Cost per Physical Site Visit ($)", value=450)
    t_waste_visits = t_total_assets * t_visit_cost
    
    t_repair_hrs = st.number_input("Repair Work (Total Hours)", value=96, key="leg_repair")
    
    search_labor = hourly_burn * t_search_hrs
    repair_labor_legacy = hourly_burn * t_repair_hrs
    legacy_total = search_labor + t_helo_costs + t_waste_visits + repair_labor_legacy

with col_right:
    st.subheader("🔵 SAR (Targeted Response)")
    s_desk_hrs = st.number_input("Hours at desk to identify 'Wet' sites", value=4, key="sar_desk")
    
    # TARGETED VISITS LOGIC
    s_wet_assets = st.number_input("Confirmed 'Wet' Assets (Targeted)", value=55)
    s_targeted_visits = s_wet_assets * t_visit_cost
    
    s_repair_hrs = st.number_input("Repair Work (Total Hours)", value=72, key="sar_repair")
    
    sar_desk_labor = hourly_burn * s_desk_hrs
    repair_labor_sar = hourly_burn * s_repair_hrs
    sar_total = data_share + sar_desk_labor + s_targeted_visits + repair_labor_sar
    
    st.info(f"💡 **Remote Clearance:** SAR cleared **{int(t_total_assets - s_wet_assets)}** dry assets from your desk, saving **${(t_total_assets - s_wet_assets) * t_visit_cost:,.0f}** in wasted truck rolls.")

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

leg_str = f"${legacy_total:,.0f}"
sar_str = f"${sar_total:,.0f}"
delta_str = f"-${legacy_total - sar_total:,.0f}"
annual_net_str = f"${(legacy_total - sar_total) * events_per_year:,.0f}"

m1.metric("Legacy Total / Event", leg_str)
m2.metric("SAR Total / Event", sar_str, delta=delta_str, delta_color="inverse")
m3.metric("Annual ROI (Net Savings)", annual_net_str)

# --- THE COMPARISON TABLE ---
st.subheader("Cost Breakdown: Blind vs. Targeted")
comparison_df = pd.DataFrame({
    "Operational Phase": ["Field Scouting (Labor)", "Aerial Recon (Helo/Drone)", "Site Visits (Truck Rolls)", "Repair Phase (The Work)", "SAR Technology Access"],
    "Legacy ($)": [f"${search_labor:,.0f}", f"${t_helo_costs:,.0f}", f"${t_waste_visits:,.0f}", f"${repair_labor_legacy:,.0f}", "$0"],
    "SAR ($)": [f"${sar_desk_labor:,.0f}", "$0 (Replaced)", f"${s_targeted_visits:,.0f}", f"${repair_labor_sar:,.0f}", f"${data_share:,.0f}"]
})
st.table(comparison_df)

# --- EXPORT ---
st.markdown(create_download_link(leg_str, sar_str, annual_net_str, comparison_df), unsafe_allow_html=True)

# --- CHART ---

st.subheader("Cost Allocation per Event")
chart_df = pd.DataFrame({
    "Activity": ["Scouting", "Aerial", "Visits", "Repairs", "SAR Data"],
    "Legacy": [search_labor, t_helo_costs, t_waste_visits, repair_labor_legacy, 0],
    "SAR": [sar_desk_labor, 0, s_targeted_visits, repair_labor_sar, data_share]
})
st.bar_chart(chart_df.set_index("Activity"))

st.success(f"**Efficiency Verdict:** SAR eliminates **${(t_total_assets - s_wet_assets) * t_visit_cost:,.0f}** in wasted truck rolls by providing ground truth before the first vehicle leaves the yard.")
