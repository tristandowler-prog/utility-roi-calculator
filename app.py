import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEYE Utility ROI", layout="wide")

st.title("🛰️ ICEYE SAR: Operational ROI")
st.markdown("### *Logic: Subscription Slicing & Targeted Inspections*")
st.divider()

# --- INPUTS ---
with st.sidebar:
    st.header("💰 1. The Subscription")
    annual_sub = st.number_input("Annual ICEYE Sub ($)", value=150000)
    events_per_year = st.slider("Flood Events Per Year", 1, 10, 2)
    
    st.divider()
    st.header("🚁 2. Legacy Costs")
    recon_cost = st.number_input("Helo/Drone Recon per Event ($)", value=85000)
    visit_cost = st.number_input("Cost per Site Visit ($)", value=350)

# --- THE SPREADSHEET MATH ---
data_share = annual_sub / events_per_year

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Legacy (Manual)")
    t_assets = st.number_input("Total Assets in Area", value=2000)
    # Total Legacy = Recon + (All Assets * Visit Cost)
    t_total = recon_cost + (t_assets * visit_cost)

with col_right:
    st.subheader("🔵 ICEYE (Directed)")
    s_assets_wet = st.number_input("Confirmed Wet Assets", value=140)
    # Total SAR = Data Share + (Wet Assets * Visit Cost)
    s_total = data_share + (s_assets_wet * visit_cost)
    st.info(f"💡 **Data Cost:** ${data_share:,.0f} per event")

# --- DASHBOARD ---
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Legacy Cost / Event", f"${t_total:,.0f}")
m2.metric("True SAR Cost / Event", f"${s_total:,.0f}", 
          delta=f"-${t_total - s_total:,.0f}", delta_color="inverse")

annual_net = (t_total - s_total) * events_per_year
m3.metric("Annual Net Position", f"${annual_net:,.0f}")

# --- TABLE ---
st.subheader("Breakdown per Event")
df = pd.DataFrame({
    "Category": ["Aerial Recon", "Field Inspections", "Satellite Data Share"],
    "Legacy ($)": [f"${recon_cost:,.0f}", f"${t_assets * visit_cost:,.0f}", "$0"],
    "ICEYE ($)": ["$0", f"${s_assets_wet * visit_cost:,.0f}", f"${data_share:,.0f}"]
})
st.table(df)

# --- CHART ---
chart_df = pd.DataFrame({
    "Category": ["Recon", "Inspections", "Data"],
    "Legacy": [recon_cost, (t_assets * visit_cost), 0],
    "ICEYE": [0, (s_assets_wet * visit_cost), data_share]
})
st.bar_chart(chart_df.set_index("Category"))

st.success(f"**The Filter:** By using ICEYE, you cleared **{int(t_assets - s_assets_wet)}** assets remotely and saved **${(t_assets - s_assets_wet) * visit_cost:,.0f}** in field waste.")
