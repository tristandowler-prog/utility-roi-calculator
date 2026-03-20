import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Strategic Audit | Utility Resilience", layout="wide")

# --- BIG 4 CONSULTING DESIGN SYSTEM (CLEAN & MODERN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
    }

    /* Professional Sidebar - No Black */
    [data-testid="stSidebar"] {
        background-color: #F3F4F6;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Section Cards */
    .report-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 25px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .kpi-box {
        text-align: center;
        padding: 25px;
        background: #F9FAFB;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
    }

    .section-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO IMAGE: SAR FLOOD EXTENT ---

st.markdown("<p style='text-align: right; font-size: 10px; color: #9CA3AF;'>GROUND TRUTH: SATELLITE RADAR (SAR) FLOOD ANALYSIS</p>", unsafe_allow_html=True)

# --- SIDEBAR: LEVERS & TOGGLES ---
with st.sidebar:
    st.markdown("<h2 style='color:#111827;'>Audit Controls</h2>", unsafe_allow_html=True)
    
    st.markdown("### 🔘 Enable Audit Modules")
    show_aerial = st.toggle("Aerial Reconnaissance", value=True)
    show_field = st.toggle("Field Force & Labor", value=True)
    show_contractors = st.toggle("Contractor Mobilization", value=True)
    
    st.divider()
    
    with st.expander("📡 DATA & SAR SPECS"):
        sar_sub = st.number_input("Annual SAR Subscription (AUD)", value=150000)
        events_per_year = st.slider("Annual Flood Events", 1, 12, 6)
        sar_latency = st.select_slider("Refresh Cadence", options=["48h", "24h", "12h", "6h"], value="6h")

    with st.expander("🏗️ NETWORK SCALE"):
        total_assets = st.number_input("Substations in Footprint", value=500)
        inundation_pct = st.slider("Actual Inundation (%)", 5, 100, 20)
        labor_rate = st.number_input("Labor Rate ($/hr)", value=185)

# --- CALCULATIONS ---
actual_wet = int(total_assets * (inundation_pct / 100))
data_share = sar_sub / events_per_year

# LEGACY VS SAR PILLARS
# 1. Aerial
leg_aerial = (2800 * 12) + (450 * 20) if show_aerial else 0
sar_aerial = 0

# 2. Labor
leg_labor = (120 * labor_rate * 48) + (total_assets * 450) if show_field else 0
sar_labor = (120 * labor_rate * 4) + (actual_wet * 450) if show_field else 0

# 3. Contractors
leg_mob = (10 * 15000) if show_contractors else 0
sar_mob = (leg_mob * 0.6) if show_contractors else 0 # 40% reduction

# Totals
legacy_total = leg_aerial + leg_labor + leg_mob
sar_total = data_share + sar_aerial + sar_labor + sar_mob

annual_savings = (legacy_total - sar_total) * events_per_year
roi = (annual_savings / sar_sub) * 100

# --- MAIN REPORT ---
st.markdown("<p class='section-header'>Strategic Insight Engine</p>", unsafe_allow_html=True)
st.title("Utility Flood Response: Operational Audit")
st.markdown(f"**Network Scope:** {total_assets} Assets | **Scenario:** {inundation_pct}% Inundated")

# KPI STRIP
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Annual Cash Avoidance</p><h2>${annual_savings:,.0f}</h2></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Projected ROI</p><h2 style='color:#059669;'>{roi:,.0f}%</h2></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi-box'><p class='section-header'>Restoration Advance</p><h2 style='color:#2563EB;'>44 Hours</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# THE DYNAMIC REPORT SECTIONS
st.markdown("### Executive Audit Breakdown")

if show_aerial:
    with st.container():
        st.markdown("""<div class='report-card'><strong>Pillar 1: Aerial Reconnaissance</strong><br>
        Traditional response relies on helicopter/drone scouting to 'find' the flood line. SAR provides this digitally, allowing 
        immediate stand-down of aerial contracts.</div>""", unsafe_allow_html=True)
        

if show_field:
    with st.container():
        st.markdown(f"""<div class='report-card'><strong>Pillar 2: Field Force Optimization</strong><br>
        By eliminating 'Dry Site' visits, you avoid <strong>{total_assets - actual_wet} wasted truck rolls</strong>. 
        Field teams move directly to impacted substations for Trip 1 resolution.</div>""", unsafe_allow_html=True)
        

if show_contractors:
    with st.container():
        st.markdown("""<div class='report-card'><strong>Pillar 3: Contractor Mobilization</strong><br>
        Precise damage intelligence allows the utility to defer or cancel expensive mutual aid crews until 
        the specific scope of work is confirmed.</div>""", unsafe_allow_html=True)

# AUDIT TABLE
st.subheader("Financial Variance Audit")
audit_data = {
    "Operational Module": ["Aerial Recon", "Search Labor", "Asset Visits", "Contractor Mob"],
    "Legacy Model (AUD)": [f"${leg_aerial:,.0f}", f"${(120 * labor_rate * 48):,.0f}", f"${(total_assets * 450):,.0f}", f"${leg_mob:,.0f}"],
    "SAR Model (AUD)": ["$0", f"${(120 * labor_rate * 4):,.0f}", f"${(actual_wet * 450):,.0f}", f"${sar_mob:,.0f}"],
}
st.table(pd.DataFrame(audit_data))

# DOWNLOAD BUTTON
st.divider()
csv_buffer = io.StringIO()
pd.DataFrame(audit_data).to_csv(csv_buffer, index=False)
st.download_button(
    label="📥 Download Strategic Audit Report",
    data=csv_buffer.getvalue(),
    file_name="Utility_Strategic_Audit.csv",
    mime="text/csv",
    use_container_width=True
)

st.markdown("<p style='text-align:center; color:#9CA3AF; font-size: 0.8rem;'>PREPARED FOR BOARD REVIEW | © 2026 STRATEGIC INSIGHT ENGINE</p>", unsafe_allow_html=True)
