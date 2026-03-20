import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="SAR ROI Auditor", layout="wide")

# --- DATA EXPORT FUNCTION ---
def create_download_link(val1, val2, val3, df):
    report_text = f"SAR TECHNOLOGY ROI REPORT\n"
    report_text += f"-------------------------\n"
    report_text += f"Manual Scouting Cost per Event: {val1}\n"
    report_text += f"SAR Subscription Cost per Event: {val2}\n"
    report_text += f"Net Annual Savings: {val3}\n\n"
    report_text += f"DETAILED BREAKDOWN:\n{df.to_string()}"
    
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="SAR_ROI_Report.txt" style="text-decoration:none;">📩 Download ROI Summary Report</a>'

st.title("🛰️ SAR Satellite: Subscription ROI Auditor")
st.markdown("### *Manual Search Costs vs. Fixed SAR Subscription Share*")
st.divider()

# --- SIDEBAR: SPREADSHEET INPUTS ---
with st.sidebar:
    st.header("💰 1. SAR Subscription")
    annual_sub = st.number_input("Annual SAR Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 10) 
    
    st.divider()
    st.header("👥 2. Manual Search Force")
    total_people = st.number_input("Total Personnel Dispatched", value=120)
    labor_rate = st.number_input("Labor Rate ($/hr)", value=175)
    num_cars = st.number_input("Number of Vehicles", value=50)
    car_rate = st.number_input("Vehicle Rate ($/hr)", value=55)
    
    st.divider()
    st.header("🚁 3. Aerial Search Rates")
    helo_rate = st.number_input("Helicopter Rate ($/hr)", value=4500)
    drone_rate = st.number_input("Drone Team Rate ($/day)", value=2500)

# --- THE PURE MATH ---
# $150,000 / 10 = $15,000
data_cost_per_event = annual_sub / events_per_year
hourly_burn = (total_people * labor_rate) + (num_cars * car_rate)

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Manual Scouting (Current)")
    t_search_hrs = st.number_input("Hours spent scouting/searching", value=48)
    t_helo_hrs = st.number_input("Helicopter Hours", value=15)
    t_drone_days = st.number_input("Drone Team Days", value=12)
    
    manual_labor = hourly_burn * t_search_hrs
    manual_aerial = (t_helo_hrs * helo_rate) + (t_drone_days * drone_rate)
    manual_total = manual_labor + manual_aerial

with col_right:
    st.subheader("🔵 SAR Satellite Truth")
    sar_total = data_cost_per_event
    st.write("### SAR Cost Logic:")
    st.info(f"Subscription (${annual_sub:,.0f}) ÷ Events ({events_per_year}) = **${sar_total:,.0f} per event**")
    st.write("*(SAR replaces all manual field scouting and aerial recon costs)*")

# --- DASHBOARD (SYNTAX AUDITED) ---

