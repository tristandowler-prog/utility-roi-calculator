import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="Flood Solutions | Strategic Audit", layout="wide")

# --- EXECUTIVE "GLASS" UI ---
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

# --- GLOBAL SIDEBAR ---
with st.sidebar:
    st.markdown("## 🛡️ Strategic Input Layer")
    st.info("Define the baseline data subscription and event frequency.")
    
    with st.expander("📡 DATA SERVICE CONFIG", expanded=True):
        sar_sub = st.number_input("Annual Data Subscription ($)", value=150000)
        data_latency = st.select_slider("Data Latency Window", options=["6h", "12h", "24h", "48h"], value="6h")
        latency_eff = {"6h": 1.0, "12h": 0.82, "24h": 0.55, "48h": 0.20}[data_latency]
    
    annual_events = st.slider("Significant Flood Events / Year", 1, 12, 4)

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
        crew_cost_u = st.number_input("Fully Burdened Crew Rate ($)", value=850)
        stpis_penalty_u = st.number_input("STPIS Penalty ($/Min)", value=125)
        double_trip_risk_u = st.slider("Mismatched Gear Risk (%)", 0, 100, 45)
    
    # Logic
    exposed_assets_u = int(total_assets * (inundation_rate / 100))
    dry_assets_u = total_assets - exposed_assets_u
    time_saved_hrs_u = 48 * latency_eff
    
    leg_aerial_u = 85000 
    leg_search_waste_u = (dry_assets_u * crew_cost_u)
    leg_double_trip_u = (exposed_assets_u * (double_trip_risk_u/100) * crew_cost_u)
    leg_stpis_u = (exposed_assets_u * stpis_penalty_u * ((time_saved_hrs_u + 4) * 60))
    
    u_legacy_event = leg_aerial_u + leg_search_waste_u + leg_double_trip_u + leg_stpis_u
    u_sar_event = (exposed_assets_u * crew_cost_u)
    u_annual_benefit = (u_legacy_event * annual_events) - (u_sar_event * annual_events) - sar_sub

    # Display Metrics
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="value-blade"><p class="metric-title">Assets Exposed</p><p class="metric-value">{exposed_assets_u:,}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="value-blade"><p class="metric-title">Lead-Time Gain</p><p class="metric-value">{time_saved_hrs_u:.1f}h</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="value-blade"><p class="metric-title">Value Protected</p><p class="metric-value">${u_annual_benefit:,.0f}</p></div>', unsafe_allow_html=True)
    
    st.bar_chart(pd.DataFrame({"Strategy": ["Legacy Response", "Targeted Solution"], "Annual Cost": [u_legacy_event * annual_events, u_sar_event * annual_events + sar_sub]}), x="Strategy", y="Annual Cost", color="#00D1FF")

# ==========================================
# TAB 2: GOVERNMENT (FULLY CUSTOMIZABLE)
# ==========================================
with tab2:
    st.markdown("<p style='color: #00D1FF; font-weight: 700; letter-spacing: 2px;'>GOVERNMENT COST-BENEFIT ANALYSIS</p>", unsafe_allow_html=True)
    st.title("Disaster Response & Social Resilience")
    st.info("Input your agency's actual operational costs below to generate a defendable ROI.")

    # --- CATEGORIZED INPUTS ---
    col_ga, col_gb = st.columns(2)

    with col_ga:
        with st.expander("🚁 Aviation Reconnaissance", expanded=True):
            heli_rate = st.number_input("Heli Charter Rate ($/hr)", value=3500)
            heli_hrs_day = st.number_input("Heli Hours/Day (Per Event)", value=10)
            fixed_wing_rate = st.number_input("Fixed-Wing Survey Rate ($/hr)", value=2200)
            flight_days = st.slider("Days of Active Air Recon", 1, 14, 4)
            
        with st.expander("🚛 Personnel & Field Operations", expanded=True):
            recon_crew_rate = st.number_input("Field Recon Crew ($/hr/person)", value=115)
            crew_size = st.number_input("Total Personnel Deployed", value=50)
            staging_burn = st.number_input("Staging Area Burn Rate ($/day/person)", value=450)
            wasted_dispatch_cost = st.number_input("Wasted Deployment Cost ($/event)", value=2800)
            num_wasted = st.slider("Est. Wasted Trips (Dry Runs) / Event", 0, 50, 10)

    with col_gb:
        with st.expander("🛣️ Infrastructure & Economics", expanded=True):
            hwy_loss_rate = st.number_input("Freight Corridor Downtime ($/hr)", value=15000)
            hwy_blockages = st.number_input("Major Corridors Impacted", value=2)
            downtime_hrs = st.number_input("Avg. Closure Duration (Hrs)", value=72)
            
        with st.expander("🏠 Recovery & Social Welfare", expanded=True):
            vsl_enable = st.toggle("Include Value of Statistical Life (Personnel Risk)", value=True)
            vsl_unit = st.number_input("Value of Statistical Life ($M)", value=5.87)
            housing_burn = st.number_input("Temporary Housing Cost ($/night)", value=350)
            displaced_families = st.number_input("Displaced Households", value=100)
            relief_latency_days = st.slider("Current Relief Delay (Days)", 7, 30, 14)

    # --- GOVERNMENT LOGIC ENGINE ---
    # 1. Aviation: Offsetting flights during 'Information Gap'
    annual_heli_offset = (heli_rate * heli_hrs_day * flight_days) * annual_events
    
    # 2. Operations: Personnel & Wasted deployments
    annual_personnel_burn = (crew_size * staging_burn * flight_days) * annual_events
    annual_waste_offset = (wasted_dispatch_cost * num_wasted) * annual_events
    
    # 3. Economics: Freight corridor reopening (Assuming 15% speed increase with SAR)
    recovery_gain_hrs = (downtime_hrs * 0.15) * latency_eff
    annual_economic_gain = (hwy_blockages * hwy_loss_rate * recovery_gain_hrs) * annual_events
    
    # 4. Social: VSL and Recovery
    annual_vsl_mitigation = (vsl_unit * 1000000 * 0.05) * annual_events if vsl_enable else 0 # 5% risk reduction
    housing_saving = (displaced_families * housing_burn * 3) * annual_events # Saving 3 days of temporary housing via faster verification

    total_gov_value = annual_heli_offset + annual_waste_offset + annual_economic_gain + annual_vsl_mitigation + housing_saving
    
    # --- OUTPUTS ---
    c_g1, c_g2, c_g3, c_g4 = st.columns(4)
    with c_g1:
        st.markdown(f'<div class="value-blade"><p class="metric-title">Aviation Offset</p><p class="metric-value">${annual_heli_offset:,.0f}</p></div>', unsafe_allow_html=True)
    with c_g2:
        st.markdown(f'<div class="value-blade"><p class="metric-title">Economic Yield</p><p class="metric-value">${annual_economic_gain:,.0f}</p></div>', unsafe_allow_html=True)
    with c_g3:
        st.markdown(f'<div class="value-blade"><p class="metric-title">Total Benefit</p><p class="metric-value">${total_gov_value:,.0f}</p></div>', unsafe_allow_html=True)
    with c_g4:
        gov_roi = (total_gov_value / sar_sub) * 100 if sar_sub > 0 else 0
        st.markdown(f'<div class="value-blade"><p class="metric-title">Gov ROI</p><p class="metric-value">{gov_roi:,.0f}%</p></div>', unsafe_allow_html=True)

    # VISUAL COMPARISON
    st.markdown("### 📊 Annual Financial Breakdown: Response Strategy Comparison")
    gov_chart_data = pd.DataFrame({
        "Category": ["Aviation", "Personnel Burn", "Waste/Dry-Runs", "Economic Loss", "Verification Latency"],
        "Current Model ($)": [annual_heli_offset, annual_personnel_burn, annual_waste_offset, annual_economic_gain, housing_saving],
        "Satellite Solution ($)": [0, annual_personnel_burn * 0.5, annual_waste_offset * 0.1, 0, 0]
    })
    st.bar_chart(gov_chart_data.set_index("Category"))

    # SUMMARY TABLE
    st.markdown("### 📊 Strategic Attribution Table")
    st.table(pd.DataFrame({
        "Expense Category": ["Aviation Recon", "Field Personnel Burn", "Economic Downtime", "Social Risk (VSL)", "Solution Subscription"],
        "User-Defined Rate": [f"${heli_rate}/hr", f"${staging_burn}/day", f"${hwy_loss_rate}/hr", f"${vsl_unit}M", f"${sar_sub}/yr"],
        "Operational Impact": ["100% Offset (All-Weather)", "50% Reduction (Targeted)", "15% Faster Recovery", "Personnel Risk Mitigation", "Strategic ROI Anchor"]
    }))

st.divider()
st.button("📄 GENERATE CUSTOMIZED GOVERNMENT BRIEFING (PDF)", use_container_width=True)
