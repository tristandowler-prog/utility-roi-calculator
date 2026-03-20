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

st.title("🛰️ SAR Strategic ROI: The Efficiency Scaler")
st.markdown("### *Watch the Subscription Cost Per Event Drop as Utilization Increases*")
st.divider()

# --- SIDEBAR: OPERATIONAL CONSTANTS ---
with st.sidebar:
    st.header("💰 1. SAR Investment")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    # The SLIDER now drives the 'Cost Per Event' logic live
    events_per_year = st.slider("Number of Flood Events Observed", 1, 15, 10)
    
    st.divider()
    st.header("👥 2. Fleet & Labor Rates")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)
    st.info(f"**Field Force Burn:** ${hourly_burn:,.0f}/hr")

# --- THE PIVOT: MARGINAL COST LOGIC ---
# This is what you were looking for: The cost per event coming down
current_data_cost_per_event = annual_sub / events_per_year

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Full Field Search)")
    t_search_hrs = st.number_input("Search/Scouting Hours", value=48, key="leg_search")
    t_helo_costs = st.number_input("Aerial Recon (Helo/Drone)", value=85000)
    t_total_assets = st.number_input("Total Assets in Flood Zone", value=500)
    t_visit_cost = st.number_input("Cost per Physical Site Visit ($)", value=450)
    
    # Legacy Math
    legacy_search_labor = hourly_burn * t_search_hrs
    legacy_visits = t_total_assets * t_visit_cost
    legacy_event_total = legacy_search_labor + t_helo_costs + legacy_visits

with col_right:
    st.subheader("🔵 SAR (Targeted Dispatch)")
    s_desk_hrs = st.number_input("Desk Review Hours", value=4, key="sar_desk")
    s_wet_assets = st.number_input("Confirmed 'Wet' Assets", value=55)
    
    # SAR Math
    sar_desk_labor = hourly_burn * s_desk_hrs
    sar_targeted_visits = s_wet_assets * t_visit_cost
    # THE CORE VARIABLE: Current data cost based on the slider
    sar_event_total = current_data_cost_per_event + sar_desk_labor + sar_targeted_visits
    
    st.info(f"📈 **Subscription Efficiency:** At {events_per_year} events, your data cost is **${current_data_cost_per_event:,.0f}/event**.")

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Legacy Cost / Event", f"${legacy_event_total:,.0f}")
m2.metric("SAR Cost / Event", f"${sar_event_total:,.0f}", 
          delta=f"-${legacy_event_total - sar_event_total:,.0f}", delta_color="inverse")
m3.metric("SAR Data Cost / Event", f"${current_data_cost_per_event:,.0f}", 
          help="Annual Sub divided by number of events.")

# --- THE EFFICIENCY GRAPH ---
st.subheader("The Subscription Advantage: Cost Per Event vs. Utilization")


# Generate data for the curve
event_range = list(range(1, 16))
cost_curve = [annual_sub / e for e in event_range]
curve_df = pd.DataFrame({"Events": event_range, "Data Cost per Event ($)": cost_curve})
st.line_chart(curve_df.set_index("Events"))

# --- THE BREAKDOWN TABLE ---
st.subheader("Comparative Breakdown")
comparison_df = pd.DataFrame({
    "Category": ["Scouting Labor", "Aerial Recon", "Site Visits (Truck Rolls)", "Data Subscription Share"],
    "Legacy ($)": [f"${legacy_search_labor:,.0f}", f"${t_helo_costs:,.0f}", f"${legacy_visits:,.0f}", "$0"],
    "SAR ($)": [f"${sar_desk_labor:,.0f}", "$0", f"${sar_targeted_visits:,.0f}", f"${current_data_cost_per_event:,.0f}"]
})
st.table(comparison_df)

# --- EXPORT ---
st.markdown(create_download_link(f"${legacy_event_total:,.0f}", f"${sar_event_total:,.0f}", f"${(legacy_event_total - sar_event_total) * events_per_year:,.0f}", comparison_df), unsafe_allow_html=True)

st.success(f"**The Bottom Line:** By the {events_per_year}th event, you are getting ground truth for **${current_data_cost_per_event:,.0f}**, while Legacy costs remain fixed at **${legacy_event_total:,.0f}** every single time.")
