import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE ROI Auditor", layout="wide")

st.title("🛰️ ICEYE SAR: Subscription ROI Auditor")
st.markdown("### *Compare Manual Spreadsheet Inputs vs. ICEYE SAR Strategy*")
st.divider()

# --- SIDEBAR: COLLEAGUE INPUTS ---
with st.sidebar:
    st.header("💰 1. The ICEYE Contract")
    annual_sub = st.number_input("Annual Subscription ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("🚁 2. Search & Rescue Costs")
    recon_cost = st.number_input("Helo/Drone Recon per Event ($)", value=85000)
    visit_cost = st.number_input("Cost per Physical Site Visit ($)", value=350)

# --- THE LOGIC (SUB / EVENTS) ---
data_share = annual_sub / events_per_year

# --- SCENARIOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Manual Search)")
    t_assets = st.number_input("Total Assets in Flood Zone", value=2000)
    # Calculation: Recon + (Every Asset * Visit Cost)
    t_total = recon_cost + (t_assets * visit_cost)

with col_right:
    st.subheader("🔵 ICEYE (GIS-Directed)")
    s_assets_wet = st.number_input("GIS-Confirmed 'Wet' Assets", value=140)
    # Calculation: Data Share + (Only Wet Assets * Visit Cost)
    s_total = data_share + (s_assets_wet * visit_cost)
    st.info(f"💡 **Data Value:** At {events_per_year} events, data is **${data_share:,.0f}** per event.")

# --- THE DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Legacy Cost / Event", f"${t_total:,.0f}")
m2.metric("True SAR Cost / Event", f"${s_total:,.0f}", 
          delta=f"-${t_total - s_total:,.0f}", delta_color="inverse")

annual_net = (t_total - s_total) * events_per_year
m3.metric("Annual Net Position", f"${annual_net:,.0f}", help="Total annual savings after paying the 150k.")

# --- THE BREAKDOWN TABLE ---
st.subheader("Cost Comparison per Event")
df = pd.DataFrame({
    "Expense Category": ["Aerial Recon (Avoided)", "Field Inspection Waste", "Satellite Data (Sub Share)"],
    "Legacy Method ($)": [f"${recon_cost:,.0f}", f"${t_assets * visit_cost:,.0f}", "$0"],
    "ICEYE Method ($)": ["$0", f"${s_assets_wet * visit_cost:,.0f}", f"${data_share:,.0f}"]
})
st.table(df)

# --- CHART ---
chart_df = pd.DataFrame({
    "Category": ["Aerial Recon", "Field Inspections", "Data Cost"],
    "Legacy": [recon_cost, (t_assets * visit_cost), 0],
    "ICEYE": [0, (s_assets_wet * visit_cost), data_share]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**Remote Clearance:** By using the ICEYE GIS layer, you cleared **{int(t_assets - s_assets_wet)}** assets remotely. This eliminates **${(t_assets - s_assets_wet) * visit_cost:,.0f}** in field labor waste.")
