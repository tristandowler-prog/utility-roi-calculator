import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG & AGENCY THEME
# =========================================================
st.set_page_config(
    page_title="ICEYE Strategic ROI | Operational Command",
    page_icon="▲",
    layout="wide"
)

# Custom CSS for a professional "Command Center" Dashboard
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
# SIDEBAR - GLOBAL SETTINGS
# =========================================================
with st.sidebar:
    st.title("▲ ICEYE Strategic")
    st.markdown("---")
    currency = st.selectbox("Reporting Currency", ["USD", "AUD", "EUR", "GBP"])
    sym = {"USD": "$", "AUD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    annual_events = st.slider("Annual Major Events", 1, 12, 3)
    subscription = st.number_input("ICEYE Subscription Cost (Annual)", value=350000.0, step=10000.0)
    per_diem = st.number_input("Daily Subsistence (Per Person)", value=185.0)
    
    st.divider()
    st.subheader("External Support Logic")
    st.caption("Mutual Aid Activation Fee: The flat cost of mobilizing inter-regional support when local capacity is exceeded.")
    mutual_aid = st.checkbox("Include Mutual Aid Activation Fee", value=True)
    aid_fee = st.number_input("One-time Activation Fee", value=150000.0) if mutual_aid else 0

# =========================================================
# INPUT ENGINE
# =========================================================
def render_agency_pillar(prefix, defaults, theme_color):
    st.markdown(f"### :{theme_color}[{prefix.upper()}]")
    
    # Pillar 1: Intel Cell
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: gis_p = st.number_input("Analysts", value=defaults['gis_p'], key=f"{prefix}_gp")
    with c2: gis_h = st.number_input("Total Hours", value=defaults['gis_h'], key=f"{prefix}_gh")
    gis_rate = st.number_input("Analyst Wage ($/hr)", value=95.0, key=f"{prefix}_gr")
    intel_total = gis_p * gis_h * gis_rate
    st.markdown(f"<span class='formula-tag'>{gis_p}p × {gis_h}hrs × {sym}{gis_rate} = {sym}{intel_total:,.0f}</span>", unsafe_allow_html=True)

    # Pillar 2: Aerial Recon
    st.markdown('<div class="section-header">Aerial Observation Profile</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: air_u = st.number_input("Aircraft Units", value=defaults['air_u'], key=f"{prefix}_au")
    with c2: air_h = st.number_input("Flight Hours/Unit", value=defaults['air_h'], key=f"{prefix}_ah")
    air_rate = st.number_input(f"Flight Rate ({sym}/hr)", value=defaults['air_r'], key=f"{prefix}_ar")
    air_total = air_u * air_h * air_rate
    st.markdown(f"<span class='formula-tag'>{air_u}u × {air_h}hrs × {sym}{air_rate:,.0f} = {sym}{air_total:,.0f}</span>", unsafe_allow_html=True)

    # Pillar 3: Fleet
    st.markdown('<div class="section-header">Fleet & Resource Deployment</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: hcv = st.number_input("High-Clearance (HCV)", value=defaults['hcv'], key=f"{prefix}_hcv")
    with c2: std = st.number_input("Standard Vehicles", value=defaults['std'], key=f"{prefix}_std")
    ops_cost = st.number_input(f"Cost per Roll ({sym})", value=650.0, key=f"{prefix}_oc")
    fleet_total = (hcv + std) * ops_cost
    st.markdown(f"<span class='formula-tag'>({hcv+std} vehicles) × {sym}{ops_cost} = {sym}{fleet_total:,.0f}</span>", unsafe_allow_html=True)

    # Pillar 4: Staging
    st.markdown('<div class="section-header">Base of Operations (BoO)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: staff = st.number_input("Field Personnel", value=defaults['staff'], key=f"{prefix}_staff")
    with c2: days = st.number_input("Deployment Days", value=defaults['days'], key=f"{prefix}_days")
    staging_total = staff * days * per_diem
    st.markdown(f"<span class='formula-tag'>{staff}p × {days}d × {sym}{per_diem} = {sym}{staging_total:,.0f}</span>", unsafe_allow_html=True)

    # Activation fee logic
    activation = aid_fee if (prefix == "Current" and mutual_aid) else 0
    event_total = intel_total + air_total + fleet_total + staging_total + activation
    
    return {
        "total": event_total, "intel": intel_total, "air": air_total, 
        "fleet": fleet_total, "staging": staging_total,
        "metrics": {"days": days, "staff": staff, "total_fleet": hcv + std, "air_hrs": air_u * air_h}
    }

# =========================================================
# MAIN DASHBOARD
# =========================================================
st.title("Operational Command: ROI Modeling")
st.markdown("---")

col_current, col_targeted = st.columns(2)

with col_current:
    cur_data = render_agency_pillar("Current", {
        'gis_p': 5, 'gis_h': 140, 'air_u': 4, 'air_h': 40, 'air_r': 5500.0,
        'hcv': 60, 'std': 180, 'staff': 750, 'days': 8
    }, "grey")

with col_targeted:
    ice_data = render_agency_pillar("ICEYE", {
        'gis_p': 2, 'gis_h': 24, 'air_u': 1, 'air_h': 8, 'air_r': 5500.0,
        'hcv': 25, 'std': 75, 'staff': 350, 'days': 4
    }, "blue")

# =========================================================
# SUMMARY & CHART
# =========================================================
st.divider()
event_savings = cur_data['total'] - ice_data['total']
annual_net = (event_savings * annual_events) - subscription
roi = (annual_net / subscription) * 100 if subscription > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Cost / Event", f"{sym}{cur_data['total']:,.0f}")
m2.metric("Targeted Cost / Event", f"{sym}{ice_data['total']:,.0f}")
m3.metric("Net Annual Savings", f"{sym}{annual_net:,.0f}", f"{sym}{event_savings:,.0f} per event")
m4.metric("Strategic ROI", f"{roi:.0f}%")

c_left, c_right = st.columns([2, 1])
with c_left:
    fig = go.Figure()
    cats = ['Intel Cell', 'Aerial Recon', 'Ground Fleet', 'Staging (BoO)']
    fig.add_trace(go.Bar(name='Current (Broad)', x=cats, y=[cur_data['intel'], cur_data['air'], cur_data['fleet'], cur_data['staging']], marker_color='#475569'))
    fig.add_trace(go.Bar(name='ICEYE (Targeted)', x=cats, y=[ice_data['intel'], ice_data['air'], ice_data['fleet'], ice_data['staging']], marker_color=PRIMARY))
    fig.update_layout(barmode='group', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT), margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER}; padding:20px; border-radius:12px;">
        <p style="text-transform:uppercase; font-size:0.7rem; color:{MUTED}; letter-spacing:1px; margin-bottom:10px;">Audit Summary</p>
        <ul style="list-style:none; padding:0; font-size:0.85rem; color:{TEXT};">
            <li style="margin-bottom:12px;">✅ <b>Intel Efficiency:</b> {(1 - ice_data['intel']/cur_data['intel'])*100:.0f}% faster intelligence delivery.</li>
            <li style="margin-bottom:12px;">✅ <b>Aerial Preservation:</b> Flights reduced by {cur_data['metrics']['air_hrs'] - ice_data['metrics']['air_hrs']:.0f} mission hours.</li>
            <li style="margin-bottom:12px;">✅ <b>Logistics Compression:</b> Field duration reduced by {cur_data['metrics']['days'] - ice_data['metrics']['days']} days.</li>
            <li style="margin-bottom:12px;">✅ <b>Personnel Safety:</b> {cur_data['metrics']['staff'] - ice_data['metrics']['staff']} fewer staff in impact zones.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
