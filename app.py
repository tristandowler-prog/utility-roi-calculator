import streamlit as st
import pandas as pd
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Strategic Audit | ICEYE Powered", layout="wide")

# --- CUSTOM CSS: GLASS-MORPHISM & SAR THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* SAR-Inspired Background Effect */
    .stApp {
        background: linear-gradient(rgba(10, 20, 30, 0.85), rgba(10, 20, 30, 0.85)), 
                    url("https://www.iceye.com/hubfs/Seeing-the-world-through-SAR-Blog-Thumbnail.jpg");
        background-size: cover;
        background-attachment: fixed;
        color: #E5E7EB;
    }

    /* Clean Sidebar - No Black */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Bento Cards for Big 4 Look */
    .bento-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
    }

    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTROLS & TOGGLES ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Audit Controls</h2>", unsafe_allow_html=True)
    
    # MASTER TOGGLES
    st.markdown("### 🔘 Module Selection")
    enable_aerial = st.toggle("Aerial Reconnaissance", value=True)
    enable_field = st.toggle("Field Force / Truck Rolls", value=True)
    enable_mob = st.toggle("Contractor Mobilization", value=True)
    
    st.divider()
    
    with st.expander("🛠️ BASELINE VARIABLES"):
        labor_rate = st.number_input("AU Labor Rate (Burdened $/hr)", value=185)
        helo_rate = st.number_input("Helicopter Rate ($/hr)", value=2800)
        drone_rate = st.number_input("Drone Team Rate ($/hr)", value=450)
        truck_roll_cost = st.number_input("Cost per Field Visit ($)", value=450)
    
    with st.expander("📡 DATA CADENCE"):
        sar_sub = st.number_input("Annual SAR Sub (AUD)", value=150000)
        events_year = st.slider("Flood Events / Year", 1, 10, 6)
        latency = st.select_slider("Refresh Window", ["48h", "24h", "12h", "6h"], "6h")

# --- CALCULATION ENGINE ---
total_assets = 500
inundation_pct = 0.20
actual_wet = int(total_assets * inundation_pct)

# Legacy Logic
leg_aerial = (helo_rate * 12) + (drone_rate * 20) if enable_aerial else 0
leg_field = (120 * labor_rate * 48) + (total_assets * truck_roll_cost) if enable_field else 0
leg_mob = (10 * 15000) if enable_mob else 0
legacy_total = leg_aerial + leg_field + leg_mob

# SAR Logic
sar_aerial = 0
sar_field = (120 * labor_rate * 4) + (actual_wet * truck_roll_cost) if enable_field else 0
sar_mob = (leg_mob * 0.6) if enable_mob else 0 # 40% reduction through intel
sar_total = (sar_sub/events_year) + sar_field + sar_mob

annual_savings = (legacy_total - sar_total) * events_year
roi = (annual_savings / sar_sub) * 100

# --- MAIN REPORT SECTION ---
st.markdown("<p style='color: #60A5FA; font-weight: 700; letter-spacing: 1px;'>UTILITY STRATEGIC ADVISORY</p>", unsafe_allow_html=True)
st.title("SAR Efficiency Audit: Infrastructure Restoration")

# TOP LEVEL KPI GRID
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="bento-card"><p class="kpi-label">Annual Cash Avoidance</p><p class="kpi-value">${annual_savings:,.0f}</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="bento-card"><p class="kpi-label">Strategic ROI</p><p class="kpi-value" style="color:#34D399;">{roi:,.0f}%</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="bento-card"><p class="kpi-label">Restoration Acceleration</p><p class="kpi-value" style="color:#60A5FA;">44 Hrs</p></div>', unsafe_allow_html=True)

# DYNAMIC REPORT MODULES
st.markdown("### 🧩 Operational Intelligence Breakdown")

if enable_aerial:
    with st.expander("🚁 PILLAR: AERIAL RECONNAISSANCE", expanded=True):
        st.write("SAR provides wide-area flood extent through cloud and night, rendering legacy helicopter/drone scouting redundant.")
        

if enable_field:
    with st.expander("🚛 PILLAR: FIELD FORCE OPTIMIZATION", expanded=True):
        st.write(f"Intel-driven dispatch eliminates truck rolls to **{total_assets - actual_wet} dry assets**. Focus remains on high-value wet repairs.")
        

# THE CORE AUDIT TABLE (DARK MODE TABLE STYLE)
st.markdown("### 📊 Financial Variance Audit")
audit_table = pd.DataFrame({
    "Component": ["Aerial Recon", "Field Search Labor", "Site Verification", "Contractor Mob"],
    "Legacy Model (AUD)": [f"${leg_aerial:,.0f}", f"${(120*labor_rate*48):,.0f}", f"${(total_assets*truck_roll_cost):,.0f}", f"${leg_mob:,.0f}"],
    "SAR Model (AUD)": ["$0", f"${(120*labor_rate*4):,.0f}", f"${(actual_wet*truck_roll_cost):,.0f}", f"${sar_mob:,.0f}"],
    "Efficiency Gain": ["-100%", "-92%", "-80%", "-40%"]
})
st.table(audit_table)

# EXPORT
st.divider()
csv_file = io.StringIO()
audit_table.to_csv(csv_file, index=False)
st.download_button("📥 Export Board-Ready Audit (CSV)", csv_file.getvalue(), "SAR_Audit_Report.csv", "text/csv", use_container_width=True)
