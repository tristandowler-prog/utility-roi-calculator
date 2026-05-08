import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="ICEYE Strategic ROI", layout="wide", page_icon="🛰️")

# High-end Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .executive-card { 
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-left: 5px solid #38BDF8; border-radius: 10px; padding: 25px; margin-bottom: 20px;
    }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #38BDF8; }
    .metric-label { font-size: 1rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: GLOBAL COST ASSUMPTIONS ---
with st.sidebar:
    st.title("Strategic Settings")
    st.info("Input your baseline labor and contract rates below. These drive the calculations across all sectors.")
    
    gis_surge_rate = st.number_input("GIS Analyst Surge Rate ($/hr)", value=185, help="Fully burdened hourly rate for senior GIS staff during emergency activation.")
    admin_overhead = st.number_input("Admin/Ops Burn ($/Day)", value=12500, help="Daily cost of running a Command Center or Recovery Office.")
    events_per_year = st.slider("Significant Events per Annum", 1, 8, 3)
    subscription_cost = st.number_input("ICEYE Annual Subscription ($)", value=350000, step=50000)

# --- 3. HEADER ---
st.title("🛰️ ICEYE Intelligence: Strategic ROI Framework")
st.markdown("#### Transitioning from 'Anecdotal Response' to 'Data-Driven Recovery'")

tab1, tab2, tab3 = st.tabs(["🚨 COMMISSIONER (Emergency Services)", "🏛️ GENERAL MANAGER (Local Council)", "⚡ COO (Utility Networks)"])

# --- TAB 1: EMERGENCY SERVICES (Focus: Asset Reallocation) ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Asset & Team Inputs")
        heli_rate = st.number_input("Rotary-Wing Flight Rate ($/hr)", value=5200)
        recon_hrs = st.number_input("Mapping Flight Hours per Event", value=20)
        crew_turnbacks = st.slider("Recon Crew Turn-backs (Flooded Roads)", 0, 50, 15)
        gis_hours_saved = st.number_input("GIS Manual Digitization (Hrs/Event)", value=60)
        
    with col2:
        # Logic: Aviation Offset + Safety Gap + GIS Efficiency
        aviation_savings = heli_rate * recon_hrs
        crew_safety_val = crew_turnbacks * 8 * 125 # Estimate of wasted crew hours
        gis_val = gis_hours_saved * gis_surge_rate
        total_event_savings = (aviation_savings + crew_safety_val + gis_val) * events_per_year
        net_roi = total_event_savings - subscription_cost
        
        st.markdown(f"""
            <div class="executive-card">
                <div class="metric-label">Annual Capability Dividend</div>
                <div class="metric-value">${total_event_savings:,.0f}</div>
                <p>This represents the <b>Aviation Offset</b>. By replacing traditional recon flights with SAR data, you reallocate ~{recon_hrs * events_per_year} high-risk flight hours to life-saving winch and resupply missions.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 2: LOCAL COUNCIL (Focus: Capital Velocity) ---
with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Financial & Recovery Inputs")
        drfa_claim = st.number_input("Avg. DRFA Claim Value ($)", value=12000000)
        interest_rate = st.number_input("Cost of Working Capital (%)", value=6.2)
        days_saved = st.slider("Funding Acceleration (Days)", 1, 30, 14)
        inspection_labor = st.number_input("Manual RDA Crew Costs ($/Event)", value=85000)

    with col2:
        # Logic: (Claim Value * Interest / 365) * Days Saved
        funding_velocity_val = (drfa_claim * (interest_rate/100) / 365) * days_saved
        admin_savings = days_saved * (admin_overhead * 0.2) # 20% efficiency gain in recovery office
        total_council_val = (funding_velocity_val + admin_savings + (inspection_labor * 0.4)) * events_per_year
        
        st.markdown(f"""
            <div class="executive-card">
                <div class="metric-label">Capital Velocity & Labor Efficiency</div>
                <div class="metric-value">${total_council_val:,.0f}</div>
                <p>By providing <b>Building-Level Inundation Data</b> within 24 hours, you trigger Category C/D funding grants {days_saved} days faster than manual inspections allow.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 3: UTILITY COMPANIES (Focus: Regulatory Compliance) ---
with tab3:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Reliability & Regulatory Inputs")
        caidi_impact = st.number_input("Customer Minutes Saved (SAIDI)", value=1200000)
        voll_rate = st.number_input("Value of Lost Load ($/MWh)", value=35000) # Australian standard
        pass_through_risk = st.number_input("Emergency Capex at Risk ($)", value=15000000)
        audit_rejection_prob = st.slider("Historical Audit Rejection Rate (%)", 0, 10, 3)

    with col2:
        # Logic: Reliability gains + Regulatory certainty
        reliability_val = (caidi_impact / 60) * (voll_rate / 1000) # Rough MWh conversion
        regulatory_val = pass_through_risk * (audit_rejection_prob / 100)
        total_utility_val = (reliability_val + regulatory_val) * events_per_year
        
        st.markdown(f"""
            <div class="executive-card">
                <div class="metric-label">Regulatory & Reliability Value</div>
                <div class="metric-value">${total_utility_val:,.0f}</div>
                <p>Ensures <b>AER Compliance</b>. Providing SAR-backed evidence of "Force Majeure" protects your cost pass-through applications from regulatory claw-backs.</p>
            </div>
        """, unsafe_allow_html=True)

# --- 4. SUMMARY VISUALIZATION ---
st.divider()
final_data = pd.DataFrame({
    "Sector": ["Emergency Services", "Local Council", "Utility Networks"],
    "Gross Savings ($)": [total_event_savings, total_council_val, total_utility_val],
    "ICEYE Subscription ($)": [subscription_cost] * 3
})

fig = go.Figure()
fig.add_trace(go.Bar(name='Gross Annual Benefit', x=final_data["Sector"], y=final_data["Gross Savings ($)"], marker_color='#38BDF8'))
fig.add_trace(go.Scatter(name='Annual Subscription Cost', x=final_data["Sector"], y=final_data["ICEYE Subscription ($)"], mode='lines+markers', line=dict(color='#F43F5E', width=4)))

fig.update_layout(title="Multi-Sector ROI Summary", barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#E2E8F0"))
st.plotly_chart(fig, use_container_width=True)

st.success("Analysis Complete: This framework demonstrates that ICEYE pays for itself by reducing 'Decision Latency' across the three most expensive phases of Australian disaster management.")
