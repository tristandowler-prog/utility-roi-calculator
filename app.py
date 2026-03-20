import streamlit as st
import pandas as pd
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="CEO Business Case | Infrastructure Resilience", layout="wide")

# --- BIG 4 EXECUTIVE THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.92)), 
                    url("https://share.google/KpUEQWOjnCWCGErW5");
        background-size: cover;
        background-attachment: fixed;
        color: #F8FAFC;
    }
    .bento-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .kpi-value { font-size: 2.2rem; font-weight: 800; color: #FFFFFF; margin: 0; }
    .kpi-label { font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.2px; }
    .status-tag { padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CEO-LEVEL LEVERS ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Executive Levers</h2>", unsafe_allow_html=True)
    
    with st.expander("⚖️ REGULATORY & COMPLIANCE", expanded=True):
        stpis_penalty = st.number_input("STPIS Penalty (Avg $/min)", value=120, help="Service Target Performance Incentive Scheme (AU Standard).")
        customers_per_sub = st.number_input("Avg Customers per Substation", value=5000)
    
    with st.expander("👷 PERSONNEL SAFETY (OH&S)"):
        hazard_hours_reduction = st.slider("Reduction in 'In-Flood' Exposure (%)", 10, 90, 75)
        
    with st.expander("📦 ASSET PROTECTION"):
        transformer_value = st.number_input("Avg Transformer Replacement ($M)", value=2.5)
        failure_risk_red = st.slider("Prevention of Total Loss (%)", 1, 20, 5)

# --- CALCULATIONS (THE CEO MATH) ---
# Previous Logic Carryover
time_saved_hrs = 42 # Derived from search phase elimination
actual_wet = 100 # Default for 500 sub footprint at 20%
sar_sub_annual = 150000

# 1. STPIS Savings (Regulatory)
total_outage_mins_saved = time_saved_hrs * 60
regulatory_savings = (stpis_penalty * total_outage_mins_saved) * (actual_wet / 10) # Weighted impact

# 2. Asset Risk Mitigation (Insurance/CAPEX)
capex_protection = (transformer_value * 1000000) * (failure_risk_red / 100) * (actual_wet / 20)

# 3. Operational Savings (The "Small" Stuff)
op_savings = 850000 # Placeholder for Labor/Helo from previous tool

total_business_value = regulatory_savings + capex_protection + op_savings
roi = (total_business_value / sar_sub_annual) * 100

# --- MAIN DASHBOARD ---
st.markdown("<p style='color: #38BDF8; font-weight: 700;'>EXECUTIVE BRIEFING: DISASTER RESPONSE REFORMATION</p>", unsafe_allow_html=True)
st.title("Strategic Value & Grid Continuity Audit")

# BENTO TOP LINE
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="bento-card"><p class="kpi-label">Regulatory & CAPEX Protection</p><p class="kpi-value">${total_business_value:,.0f}</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="bento-card"><p class="kpi-label">Strategic ROI</p><p class="kpi-value" style="color:#34D399;">{roi:,.0f}%</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="bento-card"><p class="kpi-label">OH&S Hazard Mitigation</p><p class="kpi-value" style="color:#38BDF8;">-{hazard_hours_reduction}%</p></div>', unsafe_allow_html=True)

# THE THREE PILLARS OF THE CEO CASE
st.markdown("### 🔍 The Business Case: Beyond Labor Savings")

t1, t2, t3 = st.tabs(["Regulatory (STPIS)", "Personnel Safety (S)", "Asset Longevity"])

with t1:
    st.markdown(f"""
    <div class="bento-card">
    <strong>Regulatory Compliance & STPIS Performance:</strong><br>
    The Australian Energy Regulator (AER) penalizes downtime heavily. By accelerating re-energization by <strong>{time_saved_hrs} hours</strong>, 
    the utility significantly reduces its STPIS liability. This move shifts the organization from 'Reactive' to 'Defensible Resilience.'
    </div>
    """, unsafe_allow_html=True)
    

with t2:
    st.markdown(f"""
    <div class="bento-card">
    <strong>Personnel Safety & Duty of Care:</strong><br>
    The most dangerous hours are the 'Blind Search' hours. By using SAR, we eliminate the need for crews to drive through receding 
    floodwaters to 'check' dry assets. We reduce physical exposure to hazards by <strong>{hazard_hours_reduction}%</strong>.
    </div>
    """, unsafe_allow_html=True)
    

with t3:
    st.markdown(f"""
    <div class="bento-card">
    <strong>CAPEX Preservation:</strong><br>
    Submerged transformers have a critical 'Point of No Return.' Early detection allows for immediate pumping or 
    isolation, potentially saving a <strong>${transformer_value}M asset</strong> from permanent catastrophic failure.
    </div>
    """, unsafe_allow_html=True)
    

# FINAL AUDIT TABLE
st.subheader("Financial Attribution Matrix")
audit_data = {
    "Value Pillar": ["Regulatory/STPIS Offset", "Asset Loss Prevention", "Operational Labor/Aerial"],
    "Strategic Value": [f"${regulatory_savings:,.0f}", f"${capex_protection:,.0f}", f"${op_savings:,.0f}"],
    "CEO Focus": ["Compliance & Revenue", "CAPEX Preservation", "OPEX Efficiency"]
}
st.table(pd.DataFrame(audit_data))

# EXPORT
st.divider()
st.download_button("📥 Export CEO Briefing (CSV)", "Audit Data", use_container_width=True)
