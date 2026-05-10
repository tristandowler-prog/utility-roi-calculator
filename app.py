import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG & AGENCY THEME
# =========================================================
st.set_page_config(page_title="ICEYE Subscription ROI Calculator", page_icon="▲", layout="wide")

BG, CARD, BORDER, TEXT, MUTED = "#0B1220", "#111827", "#1E293B", "#F8FAFC", "#94A3B8"
PRIMARY, SUCCESS, WARNING, ACCENT = "#38BDF8", "#22C55E", "#F59E0B", "#6366F1"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    html, body, .stApp {{ background-color: {BG}; color: {TEXT}; font-family: 'Inter', sans-serif; }}
    .stMetric {{ background-color: {CARD} !important; border: 1px solid {BORDER} !important; padding: 20px !important; border-radius: 12px !important; }}
    .formula-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {PRIMARY}; background: rgba(56, 189, 248, 0.1); padding: 4px 8px; border-radius: 4px; margin-top: -10px; display: inline-block; }}
    .section-header {{ text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.85rem; font-weight: 700; color: {MUTED}; margin-bottom: 15px; border-left: 3px solid {ACCENT}; padding-left: 10px; }}
    .logic-box {{ background: {CARD}; border: 1px solid {BORDER}; padding: 25px; border-radius: 12px; margin-top: 30px; }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - UPDATED TO SUBSCRIPTION ROI
# =========================================================
with st.sidebar:
    st.title("ICEYE Subscription ROI Calculator")
    st.markdown("---")
    currency = st.selectbox("Reporting Currency", ["USD", "AUD", "EUR", "GBP"])
    sym = {"USD": "$", "AUD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    st.subheader("Subscription Details")
    sub_cost = st.number_input("Annual ICEYE Subscription", value=350000.0, step=10000.0)
    annual_events = st.slider("Annual Major Flood Events", 1, 12, 3)
    
    st.divider()
    st.subheader("Mobilization Logistics")
    st.caption("Includes interstate/regional transport, Base of Operations setup, and fleet logistics triggered when local capacity is exceeded.")
    mutual_aid = st.checkbox("Include Mobilization Costs", value=True)
    aid_fee = st.number_input("Mobilization Cost per Event", value=120000.0) if mutual_aid else 0

# =========================================================
# OPERATIONAL PILLAR FUNCTION
# =========================================================
def render_operational_pillar(prefix, defaults, theme_color):
    st.markdown(f"### :{theme_color}[{prefix.upper()} PROFILE]")
    
    # 1. INTEL CELL
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: gp = st.number_input("GIS Analysts", value=defaults['gp'], key=f"{prefix}_gp")
    with c2: gh = st.number_input("Analysis Hours", value=defaults['gh'], key=f"{prefix}_gh")
    with c3: gr = st.number_input("Analyst Wage ($/hr)", value=95.0, key=f"{prefix}_gr")
    intel_total = gp * gh * gr
    st.markdown(f"<span class='formula-tag'>{gp}p × {gh}hrs × {sym}{gr} = {sym}{intel_total:,.0f}</span>", unsafe_allow_html=True)

    # 2. AERIAL RECON
    st.markdown('<div class="section-header">Aerial Observation Profile</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: au = st.number_input("Aircraft Units", value=defaults['au'], key=f"{prefix}_au")
    with c2: ah = st.number_input("Hours per Unit", value=defaults['ah'], key=f"{prefix}_ah")
    with c3: ar = st.number_input("Wet Lease Rate ($/hr)", value=defaults['ar'], key=f"{prefix}_ar")
    air_total = au * ah * ar
    st.markdown(f"<span class='formula-tag'>{au}u × {ah}hrs × {sym}{ar:,.0f} = {sym}{air_total:,.0f}</span>", unsafe_allow_html=True)

    # 3. FIELD OPERATIONS (MANUAL WAGES)
    st.markdown('<div class="section-header">Field Operations & BoO Staging</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: staff = st.number_input("Field Personnel", value=defaults['staff'], key=f"{prefix}_st")
    with c2: days = st.number_input("Deployment Duration (Days)", value=defaults['days'], key=f"{prefix}_ds")
    
    c3, c4 = st.columns(2)
    with c3: wage = st.number_input("Field Staff Wage ($/hr)", value=45.0, key=f"{prefix}_wg")
    with c4: diet = st.number_input("Per Diem/Subsistence ($/day)", value=150.0, key=f"{prefix}_dt")
    
    wage_total = staff * (days * 12) * wage # Assumes 12hr operational shifts
    diet_total = staff * days * diet
    staging_total = wage_total + diet_total
    st.markdown(f"<span class='formula-tag'>({staff}p × {days*12}hrs × {sym}{wage}) + ({staff}p × {days}d × {sym}{diet}) = {sym}{staging_total:,.0f}</span>", unsafe_allow_html=True)

    # 4. GROUND FLEET
    st.markdown('<div class="section-header">Ground Fleet Allocation</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: hcv = st.number_input("HCV Units", value=defaults['hcv'], key=f"{prefix}_hcv")
    with c2: std = st.number_input("STD Units", value=defaults['std'], key=f"{prefix}_std")
    with c3: roll = st.number_input("Cost per Roll ($)", value=450.0, key=f"{prefix}_oc")
    fleet_total = (hcv + std) * roll
    st.markdown(f"<span class='formula-tag'>{hcv+std} vehicles × {sym}{roll} = {sym}{fleet_total:,.0f}</span>", unsafe_allow_html=True)

    act_fee = aid_fee if (prefix == "Current" and mutual_aid) else 0
    grand_total = intel_total + air_total + staging_total + fleet_total + act_fee
    
    return {"total": grand_total, "intel": intel_total, "air": air_total, "staging": staging_total, "fleet": fleet_total, "days": days}

# =========================================================
# MAIN DASHBOARD
# =========================================================
st.title("Strategic Command: ICEYE ROI Analysis")
col_cur, col_ice = st.columns(2)

with col_cur:
    cur = render_operational_pillar("Current", {'gp':4, 'gh':140, 'au':4, 'ah':40, 'ar':5500.0, 'staff':600, 'days':8, 'hcv':60, 'std':180}, "grey")
with col_ice:
    ice = render_operational_pillar("ICEYE", {'gp':2, 'gh':24, 'au':1, 'ah':8, 'ar':5500.0, 'staff':300, 'days':4, 'hcv':20, 'std':80}, "blue")

# =========================================================
# RESULTS & EXECUTIVE SUMMARY
# =========================================================
st.divider()
ev_sav = cur['total'] - ice['total']
ann_net = (ev_sav * annual_events) - sub_cost
roi = (ann_net / sub_cost) * 100 if sub_cost > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Event Cost", f"{sym}{cur['total']:,.0f}")
m2.metric("Targeted Event Cost", f"{sym}{ice['total']:,.0f}")
m3.metric("Annual Net Dividend", f"{sym}{ann_net:,.0f}", f"{sym}{ev_sav:,.0f} per event")
m4.metric("Strategic ROI", f"{roi:.0f}%")

# =========================================================
# ICEYE PRODUCT LOGIC BOX (THE ADD-BACK)
# =========================================================
st.markdown(f"""
<div class="logic-box">
    <h3 style="color:{PRIMARY}; margin-top:0;">▲ ICEYE Flood Intelligence Product Logic</h3>
    <div style="display: flex; gap: 20px;">
        <div style="flex: 1; border-right: 1px solid {BORDER}; padding-right: 20px;">
            <h4 style="color:{WARNING};">Flood Rapid Intelligence</h4>
            <p style="font-size: 0.9rem; color:{MUTED};"><b>Update Cycle: Every 6 Hours</b></p>
            <p style="font-size: 0.85rem;">Provides continuous <b>flood extent</b> monitoring during high-velocity events. This frequent revisit rate allows agencies to track the "leading edge" of floodwaters, identifying community isolation risks and evacuation route viability in near real-time.</p>
        </div>
        <div style="flex: 1;">
            <h4 style="color:{SUCCESS};">Flood Insights</h4>
            <p style="font-size: 0.9rem; color:{MUTED};"><b>Update Cycle: 24-Hourly (Post-Peak Focus)</b></p>
            <p style="font-size: 0.85rem;">Delivers high-fidelity <b>flood depth</b> and extent at the individual building level. This data is critical for <b>Asset Matching</b>—ensuring High-Clearance Vehicles (HCV) are prioritized for deep zones while standard assets manage the periphery, significantly reducing vehicle damage and recovery costs.</p>
        </div>
    </div>
    <hr style="border: 0; border-top: 1px solid {BORDER}; margin: 20px 0;">
    <p style="font-size: 0.85rem; color:{MUTED};"><b>Strategic Impact:</b> The transition to SAR-verified intelligence reduces the "Observation Void" (where teams wait for aircraft or weather clearings). By receiving 6-hourly extent updates, agencies can compress deployment durations by an average of <b>{cur['days'] - ice['days']} days</b> per event.</p>
</div>
""", unsafe_allow_html=True)
