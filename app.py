import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR Strategic ROI", layout="wide")

# --- DATA EXPORT ---
def create_download_link(val1, val2, val3, df):
    report_text = f"SAR STRATEGIC ROI REPORT\n"
    report_text += f"-------------------------\n"
    report_text += f"Legacy Search Cost: {val1}\n"
    report_text += f"SAR Targeted Cost: {val2}\n"
    report_text += f"Net Annual Position: {val3}\n\n"
    report_text += f"DETAILED BREAKDOWN:\n{df.to_string()}"
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="SAR_ROI_Report.txt" style="text-decoration:none;">📩 Download Full Audit Report</a>'

st.title("🛰️ SAR Strategic ROI: Operational Efficiency")
st.markdown("### *Comparing 'Blind Search' vs. 'Targeted Response'*")
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
    
    # Hourly burn for the whole field force
    hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)
    st.write(f"**Field Force Burn:** ${hourly_burn:,.0f}/hr")

# --- THE CALCULATIONS ---
data_share = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 WITHOUT SAR (Blind Response)")
    t_search_hrs = st.number_input("Hours spent scouting/finding damage", value=48)
    t_helo_costs = st.number_input("Aerial Recon Costs (Helos/Drones)", value=85000)
    t_repair_hrs = st.number_input("Hours spent performing repairs", value=72)
    
    # Logic: Search Labor + Aerial + Repair Labor
    search_cost = (hourly_burn * t_search_hrs) + t_helo_costs
    repair_cost_legacy = (hourly_burn * t_repair_hrs)
    legacy_total = search_cost + repair_cost_legacy

with col_right:
    st.subheader("🔵 WITH SAR (Targeted Response)")
    s_desk_hrs = st.number_input("Hours at desk to identify 'Wet' sites", value=4)
    s_repair_hrs = st.number_input("Hours spent performing repairs", value=72)
    
    # Logic: Data Share + Desk Labor + Repair Labor (No Search, No Aerial)
    sar_data_cost = data_share
    sar_desk_labor = (hourly_burn * s_desk_hrs)
    repair_cost_sar = (hourly_burn * s_repair_hrs)
    sar_total = sar_data_cost + sar_desk_labor + repair_cost_sar
    
    st.info(f"💡 **SAR Logic:** Data cost is ${data_share:,.0f}. You've eliminated the {t_search_hrs}hr search and {t_helo_costs:,.0f} aerial bill.")

# --- THE DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

# Metrics
leg_str = f"${legacy_total:,.0f}"
sar_str = f"${sar_total:,.0f}"
delta_str = f"-${legacy_total - sar_total:,.0f}"
annual_net_str = f"${(legacy_total - sar_total) * events_per_year:,.0f}"

m1.metric("Legacy Total / Event", leg_str)
m2.metric("SAR Total / Event", sar_str, delta=delta_str, delta_color="inverse")
m3.metric("Annual ROI (Net)", annual_net_str)

# --- THE COMPARISON TABLE ---
st.subheader("Operational Phase Comparison")
comparison_df = pd.DataFrame({
    "Response Phase": ["Initial Search (Field Scouting)", "Aerial Recon (Fixed Cost)", "Repair Phase (The Work)", "SAR Technology Access"],
    "Legacy Approach ($)": [f"${hourly_burn * t_search_hrs:,.0f}", f"${t_helo_costs:,.0f}", f"${repair_cost_legacy:,.0f}", "$0"],
    "SAR Approach ($)": [f"${sar_desk_labor:,.0f} (Desk only)", "$0 (Replaced)", f"${repair_cost_sar:,.0f}", f"${data_share:,.0f}"]
})
st.table(comparison_df)

# --- EXPORT ---
st.markdown(create_download_link(leg_str, sar_str, annual_net_str, comparison_df), unsafe_allow_html=True)

# --- CHART ---

st.subheader("Time Allocation: Search vs. Fix")
chart_df = pd.DataFrame({
    "Activity": ["Blind Search Labor", "Aerial Recon", "Direct Repair Labor", "SAR Subscription"],
    "Legacy": [(hourly_burn * t_search_hrs), t_helo_costs, repair_cost_legacy, 0],
    "SAR": [sar_desk_labor, 0, repair_cost_sar, data_share]
})
st.bar_chart(chart_df.set_index("Activity"))

st.success(f"**Value Statement:** By bypassing the manual search phase, you accelerate the start of repairs by **{int(t_search_hrs - s_desk_hrs)} hours** and redirect **${(hourly_burn * t_search_hrs) - sar_desk_labor:,.0f}** in labor from 'looking' to 'fixing'.")
