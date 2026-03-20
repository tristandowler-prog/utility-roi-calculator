import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR ROI Scaler", layout="wide")

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

st.title("🛰️ SAR Strategic ROI: Targeted Dispatch Auditor")
st.markdown("### *Comparing 'Blind Search' vs. 'Targeted Repair Execution'*")
st.divider()

# --- SIDEBAR: OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Observed per Year", 1, 15, 10)
    
    st.divider()
    st.header("👥 2. Fleet & Labor Rates")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)
    st.info(f"**Field Force Burn:** ${hourly_burn:,.0f}/hr")

# --- MARGINAL COST CALCULATION ---
current_data_share = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Blind Response)")
    t_search_hrs = st.number_input("Field Scouting/Search Hours", value=48, key="leg_search")
    t_helo_costs = st.number_input("Aerial Recon Costs (Helo/Drone)", value=85000)
    
    t_total_assets = st.number_input("Total Assets in Flood Zone", value=500)
    t_visit_cost = st.number_input("Cost per Physical Site Visit ($)", value=450)
    
    t_repair_hrs = st.number_input("Repair Execution Hours", value=96, key="leg_repair")
    
    # Legacy Math
    legacy_search_labor = hourly_burn * t_search_hrs
    legacy_visits = t_total_assets * t_visit_cost
    legacy_repair_labor = hourly_burn * t_repair_hrs
    legacy_total = legacy_search_labor + t_helo_costs + legacy_visits + legacy_repair_labor

with col_right:
    st.subheader("🔵 SAR (Targeted Response)")
    s_desk_hrs = st.number_input("Desk Review Hours (ID Wet Sites)", value=4, key="sar_desk")
    s_wet_assets = st.number_input("Confirmed 'Wet' Assets (Targeted)", value=55)
    
    # Targeted Logic
    s_targeted_visits = s_wet_assets * t_visit_cost
    s_repair_hrs = st.number_input("Targeted Repair Hours", value=72, key="sar_repair")
    
    # SAR Math
    sar_desk_labor = hourly_burn * s_desk_hrs
    sar_visit_total = s_targeted_visits
    sar_repair_labor = hourly_burn * s_repair_hrs
    # The variable data cost based on the slider
    sar_total = current_data_share + sar_desk_labor + sar_visit_total + sar_repair_labor
    
    st.info(f"💡 **Targeted Gain:** By the {events_per_year}th event, your data cost is **${current_data_share:,.0f}**. You skipped **{t_total_assets - s_wet_assets}** dry sites.")

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Legacy Cost / Event", f"${legacy_total:,.0f}")
m2.metric("SAR Cost / Event", f"${sar_total:,.0f}", 
          delta=f"-${legacy_total - sar_total:,.0f}", delta_color="inverse")
m3.metric("Data Cost per Event", f"${current_data_share:,.0f}")

# --- THE EFFICIENCY GRAPH ---
st.subheader("The Subscription Advantage: Cost Per Event vs. Utilization")

event_range = list(range(1, 16))
cost_curve = [annual_sub / e for e in event_range]
curve_df = pd.DataFrame({"Events": event_range, "Data Cost per Event ($)": cost_curve})
st.line_chart(curve_df.set_index("Events"))

# --- THE COMPARISON TABLE ---
st.subheader("Final Phase Breakdown")
comparison_df = pd.DataFrame({
    "Operational Phase": ["Initial Scouting (Labor)", "Aerial Recon (Aerial Search)", "Site Visits (Truck Rolls)", "Repair Phase (Wrench Time)", "SAR Subscription Share"],
    "Legacy Approach ($)": [f"${legacy_search_labor:,.0f}", f"${t_helo_costs:,.0f}", f"${legacy_visits:,.0f}", f"${legacy_repair_labor:,.0f}", "$0"],
    "SAR Approach ($)": [f"${sar_desk_labor:,.0f}", "$0", f"${sar_visit_total:,.0f}", f"${sar_repair_labor:,.0f}", f"${current_data_share:,.0f}"]
})
st.table(comparison_df)

# --- EXPORT ---
st.markdown(create_download_link(f"${legacy_total:,.0f}", f"${sar_total:,.0f}", f"${(legacy_total - sar_total) * events_per_year:,.0f}", comparison_df), unsafe_allow_html=True)

st.success(f"**Strategic Verdict:** SAR creates an **ROI of ${(legacy_total - sar_total):,.0f} per event**. By using the data {events_per_year} times, you drive the cost of information down to **${current_data_share:,.0f}** while the cost of manual search stays fixed.")
