import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIG & THEME (Must be first) ---
st.set_page_config(page_title="ICEYE Intelligence ROI", layout="wide", page_icon="🛰️")

# Executive Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .executive-card { 
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-left: 5px solid #38BDF8; border-radius: 10px; padding: 25px; margin-bottom: 20px;
    }
    .waste-card { 
        background: rgba(244, 63, 94, 0.1); border: 1px solid #F43F5E; border-radius: 10px; padding: 15px;
    }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #38BDF8; }
    .waste-value { color: #F43F5E; font-size: 1.8rem; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL OPERATIONAL COSTS (The 'Hard Burn') ---
with st.sidebar:
    st.title("🛠️ Operational Baseline")
    st.info("Define the 'Burn Rate' of your current tools and people.")
    
    # Tool Costs
    st.subheader("Asset Rates")
    heli_rate = st.number_input("Heli Rate (All-in $/hr)", value=5500)
    crew_rate = st.number_input("Field Crew (2p + 4WD $/hr)", value=320)
    drone_crew_day = st.number_input("Drone Team (Daily Rate $)", value=4500)
    
    # People & Lab
    st.subheader("Human Capital")
    gis_rate = st.number_input("GIS Analyst Surge ($/hr)", value=195)
    admin_burn = st.number_input("Recovery Office Ops ($/day)", value=12500)
    
    st.divider()
    events_pa = st.slider("Significant Events per Year", 1, 8, 3)
    iceye_sub = st.number_input("ICEYE Annual Subscription ($)", value=350000)

# --- 3. THE ANALYTIC ENGINE ---
st.title("🛰️ ICEYE Strategic ROI: The Intelligence Advantage")

tab1, tab2, tab3 = st.tabs(["🚨 EMERGENCY SERVICES", "🏛️ LOCAL COUNCIL", "⚡ UTILITIES"])

# --- TAB 1: EMERGENCY SERVICES (Aviation & Recon) ---
with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### Response Friction")
        recon_flight_hrs = st.number_input("Recon Hours per Event", value=25)
        grounded_days = st.slider("Heli Standby (Weather Delay)", 1, 7, 3)
        failed_missions = st.number_input("Crew Turn-backs (No Ground Truth)", value=12)
        mapping_hrs = st.number_input("Manual SitRep Mapping (Hrs)", value=40)
        
    with c2:
        # Hard Burn Logic
        aviation_burn = (recon_flight_hrs * heli_rate) + (grounded_days * 4500) # Standby fee
        recon_waste = (failed_missions * 4 * crew_rate)
        labor_burn = (mapping_hrs * gis_rate)
        total_event_burn = aviation_burn + recon_waste + labor_burn
        
        st.markdown(f"""
            <div class="executive-card">
                <div class="metric-label">Annual Operational Offset</div>
                <div class="metric-value">${(total_event_burn * events_pa):,.0f}</div>
                <p>By bypassing the 'Cloud-Blind Window', you reallocate <b>{recon_flight_hrs * events_pa} hours</b> of high-risk flight time from looking for damage to active life-saving missions.</p>
            </div>
            <div class="waste-card">
                <p><b>⚠️ Inefficiency Tax:</b> You currently spend approximately <span class="waste-value">${(aviation_burn * events_pa):,.0f}</span> per year on aviation assets that are either grounded or searching blindly.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 2: LOCAL COUNCIL (Funding Velocity) ---
with tab2:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### Recovery & Audit")
        drfa_claim_size = st.number_input("Avg. DRFA Claim ($M)", value=15.0) * 1_000_000
        days_saved_funding = st.slider("Acceleration (Days to Claim)", 1, 30, 14)
        audit_risk = st.slider("DRFA Rejection Risk (%)", 0, 15, 3)
        
    with c2:
        # Financial Logic
        interest_saved = (drfa_claim_size * 0.065 / 365) * days_saved_funding
        audit_protection = drfa_claim_size * (audit_risk / 100)
        labor_gain = (days_saved_funding * admin_burn * 0.15) # 15% efficiency gain
        total_council_val = (interest_saved + audit_protection + labor_gain)
        
        st.markdown(f"""
            <div class="executive-card">
                <div class="metric-label">Capital & Audit Security</div>
                <div class="metric-value">${(total_council_val * events_pa):,.0f}</div>
                <p>Accelerating the <b>Proof of Impact</b> triggers funding earlier and secures claims against Federal audits using immutable SAR evidence.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 3: UTILITY COMPANIES (Regulatory Protection) ---
with tab3:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### Reliability & Compliance")
        substations_flooded = st.number_input("Substations to Clear", value=35)
        restoration_lag = st.slider("Restoration Acceleration (Hrs)", 1, 12, 6)
        outage_cost_hr = st.number_input("Value of Lost Load ($/hr)", value=45000)
        
    with c2:
        reliability_val = restoration_lag * outage_cost_hr
        # Visualizing the value of "Safe Re-energization"
        st.markdown(f"""
            <div class="executive-card">
                <div class="metric-label">Grid Reliability Value</div>
                <div class="metric-value">${(reliability_val * events_pa):,.0f}</div>
                <p>Speeding up substation clearance by <b>{restoration_lag} hours</b> directly reduces SAIDI/CAIDI penalties and improves community safety.</p>
            </div>
        """, unsafe_allow_html=True)

# --- 4. SUMMARY GRAPH ---
st.divider()
summary_data = pd.DataFrame({
    "Sector": ["Emerg. Services", "Council", "Utilities"],
    "Annual Benefit ($)": [total_event_burn * events_pa, total_council_val * events_pa, reliability_val * events_pa],
    "ICEYE Cost ($)": [iceye_sub] * 3
})

fig = go.Figure()
fig.add_trace(go.Bar(name='Net Operational Benefit', x=summary_data["Sector"], y=summary_data["Annual Benefit ($)"], marker_color='#38BDF8'))
fig.add_trace(go.Scatter(name='Subscription Cost', x=summary_data["Sector"], y=summary_data["ICEYE Cost ($)"], mode='lines+markers', line=dict(color='#F43F5E', width=4)))
fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)
