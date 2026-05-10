import streamlit as st
import plotly.graph_objects as go

# =========================================================
# THE MASTERPIECE CONFIG
# =========================================================
st.set_page_config(
    page_title="ICEYE | Precision Response Modeler",
    page_icon="▲",
    layout="wide"
)

# Refined Professional Theme
BG, CARD, BORDER, TEXT, MUTED = "#0B1220", "#111827", "#1E293B", "#F8FAFC", "#94A3B8"
PRIMARY, SUCCESS, WARNING, ACCENT = "#38BDF8", "#22C55E", "#F59E0B", "#6366F1"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, .stApp {{ 
        background-color: {BG}; 
        color: {TEXT}; 
        font-family: 'Inter', sans-serif; 
    }}
    
    /* Card Styling */
    .metric-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    /* Header Styling */
    .main-title {{
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #FFFFFF, {PRIMARY});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}
    
    .section-header {{
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.75rem;
        font-weight: 700;
        color: {PRIMARY};
        margin: 1.5rem 0 0.75rem 0;
        display: flex;
        align-items: center;
    }}
    
    .section-header::after {{
        content: "";
        flex: 1;
        height: 1px;
        background: {BORDER};
        margin-left: 10px;
    }}

    /* Formula Tags */
    .formula-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: {MUTED};
        background: rgba(255, 255, 255, 0.03);
        padding: 6px 10px;
        border-radius: 6px;
        border: 1px solid {BORDER};
        display: block;
        margin-top: 5px;
    }}
    
    /* Product Logic Box */
    .logic-container {{
        background: linear-gradient(145deg, #111827, #1e293b);
        border: 1px solid {ACCENT};
        padding: 2rem;
        border-radius: 20px;
        margin-top: 3rem;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - COMMAND CENTER
# =========================================================
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo-white.svg", width=120)
    st.markdown("### MODELLER SETTINGS")
    currency = st.selectbox("Currency", ["USD", "AUD", "EUR", "GBP"])
    sym = {"USD": "$", "AUD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    st.divider()
    sub_cost = st.number_input("Annual Subscription Cost", value=350000.0, step=10000.0)
    annual_events = st.slider("Annual Major Events", 1, 10, 3)
    
    st.divider()
    st.subheader("Global Logistics")
    mutual_aid = st.checkbox("Include Mobilization Trigger", value=True, help="Costs for interstate/regional support mobilization.")
    aid_fee = st.number_input("Mobilization Flat-Fee", value=125000.0) if mutual_aid else 0
    per_diem = st.number_input("Personnel Subsistence ($/day)", value=165.0)

# =========================================================
# CORE INPUT ENGINE
# =========================================================
def render_profile(prefix, defaults, color):
    st.markdown(f"## :{color}[{prefix.upper()}]")
    
    # 1. INTEL
    st.markdown('<div class="section-header">Intelligence Infrastructure</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    gp = c1.number_input("Analysts", value=defaults['gp'], key=f"{prefix}_gp")
    gh = c2.number_input("Hours", value=defaults['gh'], key=f"{prefix}_gh")
    gr = c3.number_input("Wage ($/hr)", value=95.0, key=f"{prefix}_gr")
    intel_val = gp * gh * gr
    st.markdown(f"<div class='formula-tag'>MATH: {gp}p × {gh}hrs × {sym}{gr} = {sym}{intel_val:,.0f}</div>", unsafe_allow_html=True)

    # 2. AERIAL
    st.markdown('<div class="section-header">Aerial Observation Profile</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    au = c1.number_input("Aircraft", value=defaults['au'], key=f"{prefix}_au")
    ah = c2.number_input("Hours/Unit", value=defaults['ah'], key=f"{prefix}_ah")
    ar = c3.number_input("Rate ($/hr)", value=defaults['ar'], key=f"{prefix}_ar")
    air_val = au * ah * ar
    st.markdown(f"<div class='formula-tag'>MATH: {au}u × {ah}hrs × {sym}{ar:,.0f} = {sym}{air_val:,.0f}</div>", unsafe_allow_html=True)

    # 3. FIELD
    st.markdown('<div class="section-header">Field Assets & Personnel</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    staff = c1.number_input("Personnel", value=defaults['staff'], key=f"{prefix}_st")
    days = c2.number_input("Days Active", value=defaults['days'], key=f"{prefix}_ds")
    
    c3, c4 = st.columns(2)
    f_wage = c3.number_input("Wage ($/hr)", value=48.0, key=f"{prefix}_fw")
    f_diet = c4.number_input("Per Diem ($/d)", value=per_diem, key=f"{prefix}_fd")
    
    # 12hr operational days
    field_val = (staff * (days * 12) * f_wage) + (staff * days * f_diet)
    st.markdown(f"<div class='formula-tag'>MATH: ({staff}p × {days*12}h × {sym}{f_wage}) + ({staff}p × {days}d × {sym}{f_diet}) = {sym}{field_val:,.0f}</div>", unsafe_allow_html=True)

    # 4. FLEET
    st.markdown('<div class="section-header">Ground Fleet Operations</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    hcv = c1.number_input("HCV Units", value=defaults['hcv'], key=f"{prefix}_hcv")
    std = c2.number_input("STD Units", value=defaults['std'], key=f"{prefix}_std")
    roll = c3.number_input("Roll Cost", value=defaults['roll'], key=f"{prefix}_rc")
    fleet_val = (hcv + std) * roll
    st.markdown(f"<div class='formula-tag'>MATH: {hcv+std} units × {sym}{roll} = {sym}{fleet_val:,.0f}</div>", unsafe_allow_html=True)

    # SUMMATION
    total = intel_val + air_val + field_val + fleet_val + (aid_fee if prefix == "Current" else 0)
    return {"total": total, "intel": intel_val, "air": air_val, "field": field_val, "fleet": fleet_val, "days": days, "staff": staff}

# =========================================================
# MAIN INTERFACE
# =========================================================
st.markdown('<h1 class="main-title">ICEYE Subscription ROI: Precision Response Modeler</h1>', unsafe_allow_html=True)
st.markdown(f"**Strategic Assessment:** Shift from *Wide-Area Search* to *Targeted Response* using SAR Ground Truth.")

st.divider()

col_left, col_right = st.columns(2, gap="large")

with col_left:
    current = render_profile("Current", {'gp':5, 'gh':160, 'au':4, 'ah':40, 'ar':5500.0, 'staff':650, 'days':9, 'hcv':80, 'std':200, 'roll':550.0}, "grey")

with col_right:
    targeted = render_profile("ICEYE", {'gp':2, 'gh':30, 'au':1, 'ah':10, 'ar':5500.0, 'staff':300, 'days':4, 'hcv':30, 'std':100, 'roll':550.0}, "blue")

# =========================================================
# ANALYTICS DASHBOARD
# =========================================================
st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)

ev_savings = current['total'] - targeted['total']
net_annual = (ev_savings * annual_events) - sub_cost
roi_pct = (net_annual / sub_cost) * 100

# Executive Metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="metric-card"><p style="color:{MUTED}; font-size:0.8rem;">EVENT SAVINGS DELTA</p><h2 style="margin:0;">{sym}{ev_savings:,.0f}</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><p style="color:{MUTED}; font-size:0.8rem;">ANNUAL NET DIVIDEND</p><h2 style="margin:0; color:{SUCCESS};">{sym}{net_annual:,.0f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><p style="color:{MUTED}; font-size:0.8rem;">STRATEGIC ROI</p><h2 style="margin:0; color:{PRIMARY};">{roi_pct:,.0f}%</h2></div>', unsafe_allow_html=True)

# Visual Comparison
c1, c2 = st.columns([2, 1])
with c1:
    fig = go.Figure()
    cats = ['Intel Cell', 'Aerial Recon', 'Field Ops', 'Ground Fleet']
    fig.add_trace(go.Bar(name='Current (Search)', x=cats, y=[current['intel'], current['air'], current['field'], current['fleet']], marker_color='#334155'))
    fig.add_trace(go.Bar(name='ICEYE (Precision)', x=cats, y=[targeted['intel'], targeted['air'], targeted['field'], targeted['fleet']], marker_color=PRIMARY))
    fig.update_layout(barmode='group', height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT), margin=dict(t=20))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER}; padding:24px; border-radius:16px; height: 100%;">
        <p style="text-transform:uppercase; font-size:0.75rem; color:{PRIMARY}; font-weight:700; margin-bottom:1rem;">Efficiency Audit</p>
        <div style="margin-bottom:1.5rem;">
            <p style="font-size:0.8rem; color:{MUTED}; margin:0;">Field Capacity Saved</p>
            <p style="font-size:1.5rem; font-weight:700; margin:0;">{current['staff'] - targeted['staff']} Personnel</p>
        </div>
        <div style="margin-bottom:1.5rem;">
            <p style="font-size:0.8rem; color:{MUTED}; margin:0;">Operational Time Compressed</p>
            <p style="font-size:1.5rem; font-weight:700; margin:0;">{current['days'] - targeted['days']} Days</p>
        </div>
        <div style="margin-bottom:1.5rem;">
            <p style="font-size:0.8rem; color:{MUTED}; margin:0;">Intel Latency Reduced</p>
            <p style="font-size:1.5rem; font-weight:700; margin:0;">82%</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# THE MASTERPIECE LOGIC BOX
# =========================================================
st.markdown(f"""
<div class="logic-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h2 style="margin-top:0; font-weight:700;">▲ Operational Intelligence Logic</h2>
        <span style="background:{ACCENT}; color:white; padding:4px 12px; border-radius:20px; font-size:0.7rem; font-weight:700;">AUDIT READY</span>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 20px;">
        <div>
            <h4 style="color:{PRIMARY}; margin-bottom:10px;">Flood Rapid Intelligence (6h)</h4>
            <p style="font-size:0.9rem; line-height:1.6; color:{MUTED};">
                Utilizing the world's largest SAR satellite constellation, ICEYE delivers <b>Flood Rapid Intelligence</b> with a 6-hourly revisit rate. 
                This allows the GIS Intel Cell to move from "Guessing via Gauge" to "Verification via Ground Truth," identifyingcommunity isolation risks and evacuation route viability while floodwaters are still rising.
            </p>
        </div>
        <div>
            <h4 style="color:{SUCCESS}; margin-bottom:10px;">Flood Insights (24h)</h4>
            <p style="font-size:0.9rem; line-height:1.6; color:{MUTED};">
                <b>Flood Insights</b> provides high-fidelity depth data at the individual building level. This is the primary driver for 
                <b>Asset Matching</b> logic: ensuring heavy, expensive HCV assets are only deployed where depth warrants, while protecting 
                standard vehicles from water-damage write-offs.
            </p>
        </div>
    </div>
    <div style="margin-top:25px; padding-top:20px; border-top: 1px solid {BORDER}; font-size:0.85rem; font-style:italic; color:{MUTED};">
        *This model assumes a 12-hour operational shift for field staff and calculates ROI based on extraordinary cost mitigation.
    </div>
</div>
""", unsafe_allow_html=True)
