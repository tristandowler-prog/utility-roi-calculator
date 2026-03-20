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

st.title("🛰️ SAR Strategic ROI: The Efficiency Filter")
st.markdown("### *Why Legacy Costs are 'Fixed Waste' while SAR is 'Scalable Work'*")
st.divider()

# --- SIDEBAR: OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 15, 10)
    
    st.divider()
    st.header("👥 2. Fleet & Labor Rates")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)
    st.info(f"**Field Force Burn:** ${hourly_burn:,.0f}/hr")

# --- DATA SHARE ---
data_share = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Fixed Search Cost)")
    t_search_hrs = st.number_input("Blind Scouting Hours", value=48, key="leg_search")
    
    with st.expander("🚁 Aerial Recon (Editable)", expanded=True):
        helo_rate = st.number_input("Helicopter Rate ($/hr)", value=4500)
        helo_count = st.number_input("Number of Helicopters", value=2)
        helo_hrs = st.number_input("Flight Hours per Helo", value=8)
        drone_fixed = st.number_input("Drone Team Total ($)", value=15000)
        total_aerial = (helo_rate * helo_count * helo_hrs) + drone_fixed

    t_total_assets = st.number_input("Total Assets in Flood Zone", value=500)
    t_visit_cost = st.number_input("Cost per Site Visit ($)", value=450)
    t_repair_hrs = st.number_input("Legacy Repair Hours", value=96, key="leg_repair")
    
    # LEGACY MATH: You pay for the search of ALL assets
    legacy_search_labor = hourly_burn * t_search_hrs
    legacy_visits = t_total_assets * t_visit_cost  # EVERY asset is visited
    legacy_repair_labor = hourly_burn * t_repair_hrs
    legacy_total = legacy_search_labor + total_aerial + legacy_visits + legacy_repair_labor

with col_right:
    st.subheader("🔵 SAR (Variable Work Cost)")
    s_desk_hrs = st.number_input("Desk Review Hours (Targeting)", value=4, key="sar_desk")
    
    # THE VARIABLE: Confirmed Wet Sites
    s_wet_assets = st.number_input("Confirmed 'Wet' Assets (Targeted)", value=55)
    s_repair_hrs = st.number_input("Targeted Repair Hours", value=72, key="sar_repair")
    
    # SAR MATH: Only pay for the search of WET assets
    sar_desk_labor = hourly_burn * s_desk_hrs
    sar_targeted_visits = s_wet_assets * t_visit_cost # ONLY wet assets are visited
    sar_repair_labor = hourly_burn * s_repair_hrs
    sar_total = data_share + sar_desk_labor + sar_targeted_visits + sar_repair_labor
    
    # Analysis of the Waste
    wasted_visits = (t_total_assets - s_wet_assets)
    wasted_dollars = wasted_visits * t_visit_cost
    st.error(f"⚠️ **Legacy Inefficiency:** You are paying **${wasted_dollars:,.0f}** to visit {wasted_visits} assets that aren't even wet.")

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Legacy Cost / Event", f"${legacy_total:,.0f}")
m2.metric("SAR Cost / Event", f"${sar_total:,.0f}", 
          delta=f"-${legacy_total - sar_total:,.0f}", delta_color="inverse")
m3.metric("Annual ROI (Net Savings)", f"${(legacy_total - sar_total) * events_per_year:,.0f}")

# --- THE BREAKDOWN TABLE ---
st.subheader("Why Legacy is 'Flat': Search vs. Fix")
comparison_df = pd.DataFrame({
    "Phase": ["Discovery (Search/Aerial)", "Wasted Truck Rolls (Dry Sites)", "Productive Truck Rolls (Wet Sites)", "Repair Labor", "SAR Data Access"],
    "Legacy ($)": [f"${legacy_search_labor + total_aerial:,.0f}", f"${wasted_dollars:,.0f}", f"${sar_targeted_visits:,.0f}", f"${legacy_repair_labor:,.0f}", "$0"],
    "SAR ($)": [f"${sar_desk_labor:,.0f}", "$0 (Bypassed)", f"${sar_targeted_visits:,.0f}", f"${sar_repair_labor:,.0f}", f"${data_share:,.0f}"]
})
st.table(comparison_df)

# --- CHART ---
st.subheader("Operational Spend Analysis")
chart_df = pd.DataFrame({
    "Activity": ["Search Waste", "Productive Work", "Data Subscription"],
    "Legacy": [legacy_search_labor + total_aerial + wasted_dollars, sar_targeted_visits + legacy_repair_labor, 0],
    "SAR": [sar_desk_labor, sar_targeted_visits + sar_repair_labor, data_share]
})
st.bar_chart(chart_df.set_index("Activity"))

st.success(f"**The Verdict:** Even if damage is 100%, SAR wins by eliminating helicopters and scouting labor. But when damage is low (the typical case), SAR wins by **millions** by preventing 100s of useless site visits.")

# --- EXPORT ---
st.markdown(create_download_link(f"${legacy_total:,.0f}", f"${sar_total:,.0f}", f"${(legacy_total - sar_total) * events_per_year:,.0f}", comparison_df), unsafe_allow_html=True)
