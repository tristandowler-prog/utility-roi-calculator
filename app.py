import streamlit as st
import pandas as pd
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Strategic Insight Engine | SAR", layout="wide")

# --- BIG 4 DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    /* Global Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F9FAFB;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: white;
    }
    
    /* Bento Box Cards */
    .bento-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    
    .kpi-label {
        color: #6B7280;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .kpi-value {
        color: #111827;
        font-size: 2.25rem;
        font-weight: 800;
        margin-top: 8px;
    }
    
    .kpi-delta {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-weight: 600;
        font-size: 16px;
        color: #6B7280;
    }
    .stTabs [aria-selected="true"] {
        color: #111827 !important;
        border-bottom-color: #111827 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CALCULATIONS ---
with st.sidebar:
    st.markdown("### ⚙️ PARAMETERS")
    annual_sub = st.number_input("Annual Investment", value=150000)
    events_per_year = st.slider("Annual Events", 1, 15, 6)
    st.divider()
    total_assets = st.slider("Total Assets in Scope", 100, 1000, 500)
    damage_ratio = st.slider("Actual Inundation %", 5, 100, 20)
    
    # Constants
    labor_rate = 175
    ppl = 120
    contractors = 15
    hourly_burn = (ppl * labor_rate) + (contractors * 700)
    actual_wet = int(total_assets * (damage_ratio/100))

# Scenario Logic
scenarios = {
    "Base Case": {"search": 48, "reduction": 0.40, "aerial": 85000},
    "High Impact": {"search": 72, "reduction": 0.70, "aerial": 150000}
}

res = []
for name, s in scenarios.items():
    l_total = (hourly_burn * s["search"]) + s["aerial"] + (total_assets * 450) + (hourly_burn * 96)
    s_total = (annual_sub/events_per_year) + (hourly_burn * 4) + (actual_wet * 450) + (hourly_burn * 72)
    savings = l_total - s_total
    res.append({"Scenario": name, "Savings": savings * events_per_year, "ROI": (savings * events_per_year / annual_sub) * 100})

# --- UI LAYOUT ---
st.markdown("<p style='color: #6B7280; font-weight: 600;'>STRATEGIC ADVISORY | UTILITY SECTOR</p>", unsafe_allow_html=True)
st.markdown("<h1 style='margin-top: -10px;'>Grid Resilience & SAR Efficiency Audit</h1>", unsafe_allow_html=True)

# THE BENTO GRID (TOP LINE METRICS)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="bento-card">
        <div class="kpi-label">Projected Annual Cost Avoidance</div>
        <div class="kpi-value">${res[0]['Savings']:,.0f}</div>
        <div class="kpi-delta" style="color: #059669;">↑ Based on Base Case</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="bento-card">
        <div class="kpi-label">Strategic ROI</div>
        <div class="kpi-value">{res[0]['ROI']:,.0f}%</div>
        <div class="kpi-delta" style="color: #059669;">Capital Optimized</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="bento-card">
        <div class="kpi-label">Phase 1 Time Buy-Back</div>
        <div class="kpi-value">44 Hours</div>
        <div class="kpi-delta" style="color: #059669;">Accelerated Restoration</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# TABS FOR DRILL-DOWN
t1, t2 = st.tabs(["Operational Defensibility", "Sensitivity Analysis"])

with t1:
    st.markdown("### The Efficiency Differential")
    audit_data = {
        "Response Pillar": ["Asset Validation (The Scouting Phase)", "Aerial Reconnaissance (Helo/Drone)", "Resource Mobilization", "Wrench-Time Efficiency"],
        "Legacy Model": ["Manual Grid Verification", "Variable Hourly Contracts", "Full Force Mobilization", "Blind Dispatch"],
        "SAR-Enabled Model": ["Remote Detection (Desk-Based)", "Asset-Targeted Scouting", "Optimized Core-Crew Only", "Targeted Equipment Dispatch"],
        "Impact": ["-90% Time", "-100% Waste", "-40% Mob Cost", "Trip 1 Resolution"]
    }
    st.table(pd.DataFrame(audit_data))
    
    st.info("**Methodology Note:** Savings are derived from the decoupling of 'Damage Discovery' from 'Physical Site Visits.' By isolating impacted assets in the Cloud, we eliminate 'Zero-Value' truck rolls to dry sites.")

with t2:
    st.subheader("Financial Sensitivity Mapping")
    chart_df = pd
