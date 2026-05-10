import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG & AGENCY THEME
# =========================================================
st.set_page_config(page_title="ICEYE Strategic ROI | Operational Command", page_icon="▲", layout="wide")

BG, CARD, BORDER, TEXT, MUTED = "#0B1220", "#111827", "#1E293B", "#F8FAFC", "#94A3B8"
PRIMARY, SUCCESS, WARNING, ACCENT = "#38BDF8", "#22C55E", "#F59E0B", "#6366F1"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    html, body, .stApp {{ background-color: {BG}; color: {TEXT}; font-family: 'Inter', sans-serif; }}
    .stMetric {{ background-color: {CARD} !important; border: 1px solid {BORDER} !important; padding: 20px !important; border-radius: 12px !important; }}
    .formula-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {PRIMARY}; background: rgba(56, 189, 248, 0.1); padding: 4px 8px; border-radius: 4px; margin-top: -10px; display: inline-block; }}
    .section-header {{ text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.85rem; font-weight: 700; color: {MUTED}; margin-bottom: 15px; border-left: 3px solid {ACCENT}; padding-left: 10px; }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - GLOBAL FINANCIALS
# =========================================================
with st.sidebar:
    st.title("▲ ICEYE Strategic")
    st.markdown("---")
    currency = st.selectbox("Reporting Currency", ["USD", "AUD", "EUR", "GBP"])
    sym = {"USD": "$", "AUD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    st.subheader("Fixed Investments")
    sub_cost = st.number_input("ICEYE Subscription Cost (Annual)", value=350000.0, step=10000.0)
    annual_events = st.slider("Annual Major Events", 1, 12, 3)
    
    st.divider()
    st.subheader("Mobilization Logistics")
    st.caption("Interstate/Regional Mobilization: The cost of transporting crews, establishing a BoO, and fleet transit when local capacity is exceeded.")
    mutual_aid = st.checkbox("Include Mobilization Trigger", value=True)
    aid_fee = st.number_input("Mobilization Cost", value=120000.0) if mutual_aid else 0

# =========================================================
# THE INPUT ENGINE
# =========================================================
def render_operational_pillar(prefix, defaults, theme_color):
    st.markdown(f"### :{theme_color}[{prefix.upper()} PROFILE]")
    
    # 1. INTEL CELL
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: gp = st.number_input("Analysts", value=defaults['gp'], key=f"{prefix}_gp")
    with c2: gh = st.number_input("Hours/Event", value=defaults['gh'], key=f"{prefix}_gh")
    with c3: gr = st.number_input("Hourly Wage", value=95.0, key=f"{prefix}_gr")
    intel_total = gp * gh * gr
    st.markdown(f"<span class='formula-tag'>{gp}p × {gh}hrs × {sym}{gr} = {sym}{intel_total:,.0f}</span>", unsafe_allow_html=True)

    # 2. AERIAL RECON
    st.markdown('<div class="section-header">Aerial Observation</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: au = st.number_input("Aircraft", value=defaults['au'], key=f"{prefix}_au")
    with c2: ah = st.number_input("Hours/Unit", value=defaults['ah'], key=f"{prefix}_ah")
    with c3: ar = st.number_input("Wet Lease/hr", value=defaults['ar'], key=f"{prefix}_ar")
    air_total = au * ah * ar
    st.markdown(f"<span class='formula-tag'>{au}u × {ah}hrs × {sym}{ar:,.0f} = {sym}{air_total:,.0f}</span>", unsafe_allow_html=True)

    # 3. FIELD PERSONNEL (WAGES + SUBSISTENCE)
    st.markdown('<div class="section-header">Field Operations & BoO</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: staff = st.number_input("Total Personnel", value=defaults['staff'], key=f"{prefix}_st")
    with c2: days = st.number_input("Deployment Days", value=defaults['days'], key=f"{prefix}_ds")
    
    c3, c4 = st.columns(2)
    with c3: wage = st.number_input("Avg Wage ($/hr)", value=45.0, key=f"{prefix}_wg")
    with c4: diet = st.number_input("Subsistence ($/day)", value=150.0, key=f"{prefix}_dt")
    
    # Logic: 12-hour operational shifts
    wage_total = staff * (days * 12) * wage
    diet_total = staff * days * diet
    staging_total = wage_total + diet_total
    st.markdown(f"<span class='formula-tag'>({staff}p × {days*12}hrs × {sym}{wage}) + ({staff}p × {days}d × {sym}{diet}) = {sym}{staging_total:,.0f}</span>", unsafe_allow_html=True)

    # 4. GROUND FLEET
    st.markdown('<div class="section-header">Ground Fleet</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: hcv = st.number_input("HCV Units", value=defaults['hcv'], key=f"{prefix}_hcv")
    with c2: std = st.number_input("STD Units", value=defaults['std'], key=f"{prefix}_std")
    with c3: roll = st.number_input("Ops Cost/Unit", value=450.0, key=f"{prefix}_oc")
    fleet_total = (hcv + std) * roll
    st.markdown(f"<span class='formula-tag'>{hcv+std} units × {sym}{roll} = {sym}{fleet_total:,.0f}</span>", unsafe_allow_html=True)

    act_fee = aid_fee if (prefix == "Current" and mutual_aid) else 0
    grand_total = intel_total + air_total + staging_total + fleet_total + act_fee
    
    return {
        "total": grand_total, "intel": intel_total, "air": air_total, "staging": staging_total, "fleet": fleet_total,
        "metrics": {"days": days, "staff": staff, "air_h": au*ah}
    }

# =========================================================
# MAIN DASHBOARD
# =========================================================
st.title("Agency Command: ROI Modeling")
st.markdown("Quantifying the transition from **Wide-Area Search** to **Targeted Response** using SAR ground-truth.")

col_cur, col_ice = st.columns(2)
with col_cur:
    cur = render_operational_pillar("Current", {'gp':4, 'gh':120, 'au':3, 'ah':30, 'ar':4500.0, 'staff':400, 'days':7, 'hcv':40, 'std':100}, "grey")
with col_ice:
    ice = render_operational_pillar("ICEYE", {'gp':2, 'gh':24, 'au':1, 'ah':10, 'ar':4500.0, 'staff':150, 'days':3, 'hcv':15, 'std':40}, "blue")

# =========================================================
# RESULTS
# =========================================================
st.divider()
ev_sav = cur['total'] - ice['total']
ann_net = (ev_sav * annual_events) - sub_cost
roi = (ann_net / sub_cost) * 100 if sub_cost > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Event Cost", f"{sym}{cur['total']:,.0f}")
m2.metric("Targeted Event Cost", f"{sym}{ice['total']:,.0f}")
m3.metric("Annual Net Dividend", f"{sym}{ann_net:,.0f}", f"{sym}{ev_sav:,.0f} /event")
m4.metric("Strategic ROI", f"{roi:.0f}%")

c_left, c_right = st.columns([2, 1])
with c_left:
    fig = go.Figure()
    cats = ['Intel', 'Aerial', 'Field Ops', 'Fleet']
    fig.add_trace(go.Bar(name='Current', x=cats, y=[cur['intel'], cur['air'], cur['staging'], cur['fleet']], marker_color='#475569'))
    fig.add_trace(go.Bar(name='ICEYE', x=cats, y=[ice['intel'], ice['air'], ice['staging'], ice['fleet']], marker_color=PRIMARY))
    fig.update_layout(barmode='group', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT), margin=dict(t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER}; padding:20px; border-radius:12px;">
        <p style="text-transform:uppercase; font-size:0.7rem; color:{MUTED}; letter-spacing:1px;">Audit Summary</p>
        <ul style="list-style:none; padding:0; font-size:0.85rem; color:{TEXT};">
            <li style="margin-bottom:12px;">✅ <b>Resource Reduction:</b> {cur['metrics']['staff'] - ice['metrics']['staff']} fewer personnel deployed.</li>
            <li style="margin-bottom:12px;">✅ <b>Time Efficiency:</b> {cur['metrics']['days'] - ice['metrics']['days']} days saved per mission.</li>
            <li style="margin-bottom:12px;">✅ <b>Fleet Preservation:</b> {cur['metrics']['air_h'] - ice['metrics']['air_h']} aircraft hours mitigated.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
