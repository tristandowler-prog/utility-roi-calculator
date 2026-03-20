import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI: Strategic Value", layout="wide")

st.title("🛰️ ICEYE SAR: Strategic Utility ROI")
st.markdown("### *Beyond Cost: Impact on Restoration & Safety*")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("💰 1. Annual Investment")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("👥 2. Operational Rates")
    total_people = st.number_input("Total Personnel", value=120)
    person_hr = st.number_input("Labor Rate ($/hr)", value=175)
    vehicle_hr = st.number_input("Fleet Rate ($/hr)", value=55)
    burn_hr = (total_people * person_hr) + ((total_people / 2.5) * vehicle_hr)

# --- CALCULATIONS ---
data_per_event = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy Response")
    t_wait = st.number_input("Time to Start Repairs (Hrs)", value=48)
    t_assets = st.number_input("Total Assets to Inspect", value=2000)
    t_visit_cost = t_assets * 350
    t_event_total = (burn_hr * t_wait) + t_visit_cost + 85000 # 85k for aerial recon

with col_right:
    st.subheader("🔵 ICEYE Directed Response")
    s_wait = st.number_input("Time to Data Delivery (Hrs)", value=8)
    s_assets_wet = st.number_input("GIS-Confirmed Wet Assets", value=140)
    s_visit_cost = s_assets_wet * 350
    s_event_total = (burn_hr * s_wait) + s_visit_cost + data_per_event

# --- STRATEGIC METRICS ---
st.divider()
st.subheader("📈 Strategic Impact Metrics")
c1, c2, c3 = st.columns(3)

# 1. Restoration Head-start
time_saved = t_wait - s_wait
c1.metric("Restoration Head-Start", f"{time_saved} Hours", help="Hours saved by bypassing manual recon.")

# 2. Wasted Field Labor
# Assuming 30 mins per 'clearance' visit
wasted_hrs = (t_assets - s_assets_wet) * 0.5 
c2.metric("Wasted Man-Hours Eliminated", f"{int(wasted_hrs):,} Hrs", help="Labor redirected from checking dry assets to making repairs.")

# 3. Financial Delta
annual_net = (t_event_total - s_event_total) * events_per_year
c3.metric("Net Annual Position", f"${annual_net:,.0f}")

# --- RECOVERY TIMELINE VISUAL ---
st.subheader("Restoration Timeline: Search vs. Repair")

st.info("ICEYE data allows 'Repair' crews to be dispatched to specific locations while Legacy crews are still in the 'Search/Wait' phase.")

# --- THE DATA TABLE ---
df = pd.DataFrame({
    "Category": ["Field Labor Standby", "Aerial Recon", "Site Inspections", "Data Cost Share"],
    "Legacy ($)": [f"${burn_hr * t_wait:,.0f}", "$85,000", f"${t_visit_cost:,.0f}", "$0"],
    "ICEYE ($)": [f"${burn_hr * s_wait:,.0f}", "$0", f"${s_visit_cost:,.0f}", f"${data_per_event:,.0f}"]
})
st.table(df)
