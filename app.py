import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="Flood Solutions | Strategic Audit", layout="wide")

# --- EXECUTIVE "GLASS" UI (PERSISTENT STYLE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp {
        background: linear-gradient(rgba(10, 22, 35, 0.96), rgba(10, 22, 35, 0.96)), 
                    url("https://share.google/KpUEQWOjnCWCGErW5");
        background-size: cover; background-attachment: fixed; color: #F1F5F9;
    }
    .value-blade {
        background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #00D1FF; padding: 22px; margin-bottom: 20px; border-radius: 4px; backdrop-filter: blur(15px);
    }
    .metric-title { font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; }
    .metric-value { font-size: 2.4rem; font-weight: 800; color: #FFFFFF; line-height: 1.1; }
    .metric-sub { font-size: 0.85rem; color: #00D1FF; font-weight: 600; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("## 🛡️ Strategic Input Layer")
    st.info("Cross-Sector Intelligence Calibration.")
    
    with st.expander("📡 DATA SUBSCRIPTION & LATENCY", expanded=True):
        sar_sub = st.number_input("Annual Data Subscription ($)", value=150000)
        data_latency = st.select_slider("Data Delivery Window (Latency)", options=["6h", "12h", "24h", "48h"], value="6h")
        latency_eff = {"6h": 1.0, "12h": 0.82, "24h": 0.55, "48h": 0.20}[data_latency]
    
    annual_events = st.slider("Significant Flood Events / Year", 1, 10, 4)

# --- TAB NAVIGATION ---
tab1, tab2 = st.tabs(["⚡ INFRASTRUCTURE / UTILITIES", "🏛️ GOVERNMENT & DISASTER RESPONSE"])

# ==========================================
# TAB 1: UTILITIES (REMAINS UNCHANGED)
# ==========================================
with tab1:
    st.markdown("<p style='color: #00D1FF; font-weight: 700; letter-spacing: 2px;'>UTILITY AUDIT REPORT</p>", unsafe_allow_html=True)
    st.title("Network Recovery & STPIS Benchmark")
    
    col_u1, col_u2 = st.columns([1, 2])
    with col_u1:
        total_assets = st.number_input("Total Assets in Region", value=1200)
        inundation_rate = st.slider("Impact Rate (%)", 5, 100, 20)
        crew_cost = st.number_input("Crew Rate ($)", value=850)
        stpis_penalty = st.number_input("STPIS Penalty ($/Min)", value=125)
        double_trip_risk = st.slider("Mismatched Gear Risk (%)", 0, 100, 45)
    
    # Logic
    exposed_assets = int(total_assets * (inundation_rate / 100))
    dry_assets = total_assets - exposed_assets
    time_saved_hrs = 48 * latency_eff
    
    leg_aerial = 85000 
    leg_search_waste = (dry_assets * crew_cost)
    leg_double_trip = (exposed_assets * (double_trip_risk/100) * crew_cost)
    leg_stpis = (exposed_assets * stpis_penalty * ((time_saved_hrs + 4) * 60))
    
    u_legacy_event = leg_aerial + leg_search_waste + leg_double_trip + leg_stpis
    u_sar_event = (exposed_assets * crew_cost)
    u_annual_benefit = (u_legacy_event * annual_events) - (u_sar_event * annual_events) - sar_sub

    # Display Metrics
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="value-blade"><p class="metric-title">Assets Exposed</p><p class="metric-value">{exposed_assets:,}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="value-blade"><p class="metric-title">Lead-Time Gain</p><p class="metric-value">{time_saved_hrs:.1f}h</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="value-blade"><p class="metric-title">Value Protected</p><p class="metric-value">${u_annual_benefit:,.0f}</p></div>', unsafe_allow_html=True)
    
    st.bar_chart(pd.DataFrame({"Strategy": ["Legacy", "Satellite"], "Annual Cost": [u_legacy_event * annual_events, u_sar_event * annual_events + sar_sub]}), x="Strategy", y="Annual Cost", color="#00D1FF")

# ==========================================
# TAB 2: GOVERNMENT (CSV-DRIVEN)
# ==========================================
with tab2:
    st.markdown("<p style='color: #00D1FF; font-weight: 700; letter-spacing: 2px;'>GOVERNMENT STRATEGIC AUDIT</p>", unsafe_allow_html=True)
    st.title("Disaster Response & Economic Resilience")
    
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.markdown("### 🚁 Aviation & Personnel")
        heli_hours = st.number_input("Heli-Hours/Day (Information Gap)", value=10)
        heli_rate = 3500 # From CSV
        recon_personnel = st.number_input("Field Recon Personnel", value=50)
        personnel_rate = 115 # From CSV ($/hr)
        
        st.markdown("### 🛣️ Infrastructure & Social")
        freight_corridors = st.number_input("Critical Hwy Blockages", value=2)
        freight_loss_rate = 15000 # From CSV ($/hr)
        vsl_impact = st.checkbox("Include Personnel Risk (VSL)", value=True)
        vsl_value = 5.87 # Million from CSV

    # Government Value Logic
    # 1. Aviation Recon: Helis are grounded during weather/night (Information Gap)
    recon_duration_days = 3
    total_heli_cost = (heli_hours * heli_rate * recon_duration_days) * annual_events
    
    # 2. Operations: Wasted Deployments (Dry Runs)
    wasted_deployment_cost = (2800 * 5) * annual_events # 5 wasted per event
    
    # 3. Infrastructure: Freight Downtime (Reducing the delay by 12-24h using SAR)
    downtime_reduction_hrs = 12 * latency_eff
    total_freight_saving = (freight_corridors * freight_loss_rate * downtime_reduction_hrs) * annual_events
    
    # 4. Social: VSL
    total_vsl_protected = (vsl_value * 1000000 * 0.1) * annual_events if vsl_impact else 0 # 10% risk reduction

    gov_annual_savings = total_heli_cost + wasted_deployment_cost + total_freight_saving + total_vsl_protected
    
    # Display Government Metrics
    cg1, cg2, cg3 = st.columns(3)
    with cg1:
        st.markdown(f'<div class="value-blade"><p class="metric-title">Gov. Aviation Offset</p><p class="metric-value">${total_heli_cost:,.0f}</p><p class="metric-sub">Annual Rotor Offset</p></div>', unsafe_allow_html=True)
    with cg2:
        st.markdown(f'<div class="value-blade"><p class="metric-title">Economic Resilience</p><p class="metric-value">${total_freight_saving:,.0f}</p><p class="metric-sub">Hwy Downtime Mitigated</p></div>', unsafe_allow_html=True)
    with cg3:
        st.markdown(f'<div class="value-blade"><p class="metric-title">Net Societal Benefit</p><p class="metric-value">${gov_annual_savings:,.0f}</p><p class="metric-sub">Total Value Protected</p></div>', unsafe_allow_html=True)

    st.markdown("### 🧩 Government Strategic Value Defensibility")
    
    col_ga, col_gb = st.columns(2)
    with col_ga:
        st.markdown(f"""
        <div class="value-blade">
        <strong>Bridging the 'Information Gap'</strong><br>
        Traditional optical/aerial recon is 0% effective during heavy cloud cover and night-ops (12h/day). 
        By utilizing all-weather satellite data, the state prevents <b>48-72 hours</b> of operational paralysis.
        <br><br><i>Aviation Cost Avoided: ${total_heli_cost:,.0f}/yr</i>
        </div>
        """, unsafe_allow_html=True)

    with col_gb:
        st.markdown(f"""
        <div class="value-blade">
        <strong>Freight Corridor Recovery</strong><br>
        Major highway closures (e.g. Pacific Hwy) cost the economy <b>${freight_loss_rate:,.0f} per hour</b>. 
        Accelerating flood-depth verification allows corridors to reopen <b>{downtime_reduction_hrs:.1f} hours</b> sooner.
        <br><br><i>Economic Loss Mitigated: ${total_freight_saving:,.0f}/yr</i>
        </div>
        """, unsafe_allow_html=True)

    # GOV AUDIT TABLE
    st.markdown("### 📊 Government Financial Attribution Matrix")
    gov_audit_df = pd.DataFrame({
        "Category": ["Aviation Reconnaissance", "Wasted Field Deployments", "Freight Corridor Impact", "Personnel Risk (VSL)", "Satellite Subscription"],
        "Current Method": [f"${total_heli_cost:,.0f}", f"${wasted_deployment_cost:,.0f}", f"${total_freight_saving:,.0f}", f"${total_vsl_protected:,.0f}", "$0"],
        "Targeted Solution": ["$0 (Cloud Penetration)", "$280 (Verified)", "Optimized Recovery", "Risk Reduced", f"${sar_sub:,.0f}"],
        "ROI Logic": ["CSV: Medium Turbine Rates", "90% Efficiency Gain", "CSV: $15k/hr Downtime", "VSL Standard ($5.87M)", "Unified Sector Data"]
    })
    st.table(gov_audit_df)

st.divider()
st.button("📥 EXPORT MULTI-SECTOR STRATEGIC REPORT (PDF)", use_container_width=True)
