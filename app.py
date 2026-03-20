import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Strategic Audit | Utility Resilience", layout="wide")

# --- BIG 4 CONSULTING DESIGN SYSTEM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        padding: 2rem 1rem;
    }
    .report-card {
        background-color: #F9FAFB;
        border-radius: 8px;
        padding: 25px;
        border-left: 5px solid #111827;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 0.8rem;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    .kpi-box {
        text-align: center;
        padding: 20px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL LEVERS (AU STANDARD PLACEHOLDERS) ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Audit Filters</h2>", unsafe_allow_html=True)
    
    with st.expander("📡 DATA & SAR SPECS"):
        sar_sub = st.number_input("Annual SAR Subscription (AUD)", value=150000)
        sar_latency = st.select_slider("Data Refresh Cadence", options=["48h", "24h", "12h", "6h"], value="6h")
        processing_time = st.number_input("Processing Time (Hrs)", value=1)

    with st.expander("🚁 AERIAL RECONNAISSANCE"):
        helo_rate = st.number_input("Helicopter Hourly Rate (AUD)", value=2800)
        helo_hours = st.number_input("Helo Scouting / Event", value=12)
        drone_rate = st.number_input("Drone Team Rate (AUD)", value=450)
        drone_hours = st.number_input("Drone Scouting / Event", value=20)

    with st.expander("👥 FIELD FORCE & MOB"):
        labor_rate = st.number_input("Fully Burdened Labor ($/hr)", value=185)
        crew_size = st.number_input("Internal Staff Count", value=120)
        mob_fee = st.number_input("Contractor Mob Fee (per Crew)", value=15000)
        num_contractors = st.number_input("No. of Contractor Crews", value=10)

    with st.expander("⛈️ EVENT SCALE"):
        events_per_year = st.slider("Annual Flood Events", 1, 12, 6)
        total_assets = st.number_input("Total Assets in Zone", value=500)
        inundation_pct = st.slider("Actual Inundation (%)", 5, 100, 20)

# --- AUDIT CALCULATIONS ---
actual_wet = int(total_assets * (inundation_pct / 100))
hourly_burn = (crew_size * labor_rate) + (num_contractors * 750)

# LEGACY (BLIND) MODEL
legacy_aerial = (helo_rate * helo_hours) + (drone_rate * drone_hours)
legacy_search_labor = (hourly_burn * 48) # 2 days of manual verification
legacy_truck_rolls = total_assets * 450 # Rolling to every site
legacy_mob = num_contractors * mob_fee
legacy_total = legacy_aerial + legacy_search_labor + legacy_truck_rolls + legacy_mob

# SAR (TARGETED) MODEL
sar_data_per_event = sar_sub / events_per_year
sar_desk_eval = (hourly_burn * 4) # Desktop verification vs. Field search
sar_targeted_rolls = actual_wet * 450 # Only go to wet assets
sar_mob_optimized = legacy_mob * 0.4 # Reduce contractor callouts by 40%
sar_total = sar_data_per_event + sar_desk_eval + sar_targeted_rolls + (legacy_mob - sar_mob_optimized)

event_savings = legacy_total - sar_total
annual_savings = event_savings * events_per_year
roi = (annual_savings / sar_sub) * 100

# --- MAIN REPORT DISPLAY ---
st.markdown("<p class='section-header'>Strategic Advisory | Global Infrastructure</p>", unsafe_allow_html=True)
st.title("SAR-Enabled Flood Response Audit")
st.markdown("---")

# KPI STRIP
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Annual Cash Avoidance</p><h2>${annual_savings:,.0f}</h2></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Strategic ROI</p><h2 style='color:#059669;'>{roi:,.0f}%</h2></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Recovery Time Gain</p><h2 style='color:#2563EB;'>44 Hours</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# THE REPORT BODY
col_main, col_chart = st.columns([2, 1])

with col_main:
    st.markdown("### Executive Summary: The Scouting Differential")
    st.markdown(f"""
    Current response protocols for **{total_assets} assets** rely on manual validation. 
    By shifting to a **{sar_latency} refresh cadence**, the utility eliminates the 'Search Phase' 
    (traditionally 48 hours) in favor of immediate, targeted repair mobilization.
    """)
    
    # Audit Table
    audit_df = pd.DataFrame({
        "Cost Pillar": ["Aerial Recon (Helo/Drone)", "Search Phase Labor", "Asset Verification (Truck Rolls)", "Contractor Mobilization"],
        "Legacy Model (AUD)": [f"${legacy_aerial:,.0f}", f"${legacy_search_labor:,.0f}", f"${legacy_truck_rolls:,.0f}", f"${legacy_mob:,.0f}"],
        "SAR Model (AUD)": ["$0", f"${sar_desk_eval:,.0f}", f"${sar_targeted_rolls:,.0f}", f"${legacy_mob - sar_mob_optimized:,.0f}"],
        "Variance": ["-100%", "-92%", f"-{100 - inundation_pct}%", "-40%"]
    })
    st.table(audit_df)

with col_chart:
    st.markdown("#### Event Cost Comparison")
    chart_data = pd.DataFrame({"Model": ["Legacy", "SAR"], "Cost": [legacy_total, sar_total]}).set_index("Model")
    st.bar_chart(chart_data)

# THE OFFICIAL DOWNLOAD SECTION
st.divider()
st.markdown("<h4 style='text-align:center;'>Finalize Audit & Export</h4>", unsafe_allow_html=True)

# Create a clean CSV for the download
csv_buffer = io.StringIO()
audit_df.to_csv(csv_buffer, index=False)
st.download_button(
    label="📥 Download Executive Audit Report (CSV)",
    data=csv_buffer.getvalue(),
    file_name="SAR_Strategic_Audit.csv",
    mime="text/csv",
    use_container_width=True
)

st.markdown("<p style='text-align:center; color:#9CA3AF; font-size: 0.8rem;'>CONFIDENTIAL | PREPARED FOR BOARD REVIEW 2026</p>", unsafe_allow_html=True)
