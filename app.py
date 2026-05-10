import streamlit as st
import plotly.graph_objects as go

# =========================================================
# THE MASTERPIECE CONFIG
# =========================================================
st.set_page_config(
    page_title="ICEYE | Precision Response Modeller",
    page_icon="▲",
    layout="wide"
)

# Reliable branding - Using a standard clear PNG
LOGO_URL = "https://www.iceye.com/hubfs/iceye-logo-white.svg"

# Refined Professional Theme
BG, CARD, BORDER, TEXT, MUTED = "#0B1220", "#111827", "#1E293B", "#F8FAFC", "#94A3B8"
PRIMARY, SUCCESS, WARNING, ACCENT = "#38BDF8", "#22C55E", "#F59E0B", "#6366F1"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, .stApp {{ 
        background-color: {BG}; 
        color: {TEXT}; 
        font-family: 'Inter', sans-serif; 
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

    .formula-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: {MUTED};
        background: rgba(255, 255, 255, 0.05);
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid {BORDER};
        display: block;
        margin-top: 5px;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR & GLOBAL CONTROLS
# =========================================================
with st.sidebar:
    st.image(LOGO_URL, width=180)
    st.markdown("### Modeller Controls")
    currency = st.selectbox("Currency", ["AUD", "USD", "EUR", "GBP"])
    sym = {"AUD": "$", "USD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    st.divider()
    sub_cost = st.number_input("Annual ICEYE Subscription", value=350000.0, step=10000.0)
    annual_events = st.slider("Annual Major Flood Events", 1, 10, 3)
    
    st.divider()
    st.subheader("Global Mobilisation")
    st.caption("Toggle this for interstate deployments or major regional activations requiring external task-forces.")
    include_mob = st.toggle("Include Mobilisation Costs", value=False)
    mob_fee = st.number_input(f"One-off Mobilisation Cost ({sym})", value=125000.0) if include_mob else 0

# =========================================================
# OPERATIONAL PILLAR ENGINE
# =========================================================
def render_profile(prefix, defaults, color):
    st.markdown(f"## :{color}[{prefix.upper()} RESPONSE]")
    
    # 1. INTEL CELL
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    gp = c1.number_input(f"{prefix} Analysts", value=defaults['gp'], key=f"{prefix}_gp")
    gh = c2.number_input(f"{prefix} Hours", value=defaults['gh'], key=f"{prefix}_gh")
    gr = c3.number_input(f"{prefix} $/hr", value=95.0, key=f"{prefix}_gr")
    intel_val = gp * gh * gr
    st.markdown(f"<div class='formula-tag'>Subtotal: {sym}{intel_val:,.0f}</div>", unsafe_allow_html=True)

    # 2. AERIAL RECON
    st.markdown('<div class="section-header">Aerial Observation</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    au = c1.number_input(f"{prefix} Aircraft", value=defaults['au'], key=f"{prefix}_au")
    ah = c2.number_input(f"{prefix} Flight Hrs", value=defaults['ah'], key=f"{prefix}_ah")
    ar = c3.number_input(f"{prefix} Rate/Hr", value=defaults['ar'], key=f"{prefix}_ar")
    air_val = au * ah * ar
    st.markdown(f"<div class='formula-tag'>Subtotal: {sym}{air_val:,.0f}</div>", unsafe_allow_html=True)

    # 3. FIELD OPERATIONS
    st.markdown('<div class="section-header">Field Crews & Subsistence</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    staff = c1.number_input(f"{prefix} Personnel", value=defaults['staff'], key=f"{prefix}_st")
    days = c2.number_input(f"{prefix} Days", value=defaults['days'], key=f"{prefix}_ds")
    
    c3, c4 = st.columns(2)
    f_wage = c3.number_input(f"{prefix} Wage $/hr", value=48.0, key=f"{prefix}_fw")
    f_diet = c4.number_input(f"{prefix} Subsistence/Day", value=165.0, key=f"{prefix}_fd")
    
    field_val = (staff * (days * 12) * f_wage) + (staff * days * f_diet)
    st.markdown(f"<div class='formula-tag'>Subtotal: {sym}{field_val:,.0f}</div>", unsafe_allow_html=True)

    # 4. FLEET - EVERY COMPONENT EDITABLE
    st.markdown('<div class="section-header">Ground Fleet & Logistics</div>', unsafe_allow_html=True)
    
    f1, f2 = st.columns(2)
    hcv_units = f1.number_input(f"{prefix} HCV Units", value=defaults['hcv'], key=f"{prefix}_hcv")
    hcv_roll = f2.number_input(f"{prefix} HCV Roll Cost", value=defaults.get('hcv_r', 850.0), key=f"{prefix}_hcv_r")
    
    f3, f4 = st.columns(2)
    std_units = f3.number_input(f"{prefix} STD Units", value=defaults['std'], key=f"{prefix}_std")
    std_roll = f4.number_input(f"{prefix} STD Roll Cost", value=defaults.get('std_r', 450.0), key=f"{prefix}_std_r")
    
    st.markdown('<div style="font-size:0.8rem; color:#94A3B8; margin-top:10px;">Operational Inefficiency (Aborted Rolls/Turnarounds)</div>', unsafe_allow_html=True)
    f5, f6 = st.columns(2)
    abort_units = f5.number_input(f"{prefix} Aborted Rolls", value=defaults.get('aborts', 40), key=f"{prefix}_abt")
    abort_cost = f6.number_input(f"{prefix} Cost/Abort", value=550.0, key=f"{prefix}_abt_c")
    
    fleet_val = (hcv_units * hcv_roll) + (std_units * std_roll) + (abort_units * abort_cost)
    st.markdown(f"<div class='formula-tag'>Fleet Total: {sym}{fleet_val:,.0f}</div>", unsafe_allow_html=True)

    # SUMMATION
    # Add mobilisation fee only to the "Current" profile if toggled
    final_mob = mob_fee if (prefix == "Current" and include_mob) else 0
    total = intel_val + air_val + field_val + fleet_val + final_mob
    return {"total": total, "intel": intel_val, "air": air_val, "field": field_val, "fleet": fleet_val, "days": days, "staff": staff}

# =========================================================
# MAIN DASHBOARD
# =========================================================
st.markdown('<h1 style="color:white; margin-top:-50px;">ICEYE Subscription ROI: Precision Response Modeller</h1>', unsafe_allow_html=True)
st.markdown(f"**Operational Objective:** Quantifying the reduction in mission latency and 'Sunk Cost' deployments using SAR ground truth.")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    current = render_profile("Current", {
        'gp':5, 'gh':160, 'au':4, 'ah':40, 'ar':5500.0, 
        'staff':650, 'days':9, 'hcv':80, 'hcv_r':850.0, 
        'std':200, 'std_r':450.0, 'aborts':45
    }, "grey")

with col_right:
    targeted = render_profile("ICEYE", {
        'gp':2, 'gh':30, 'au':1, 'ah':10, 'ar':5500.0, 
        'staff':300, 'days':4, 'hcv':30, 'hcv_r':850.0, 
        'std':100, 'std_r':450.0, 'aborts':5
    }, "blue")

# =========================================================
# ANALYTICS DASHBOARD
# =========================================================
st.divider()
ev_savings = current['total'] - targeted['total']
net_annual = (ev_savings * annual_events) - sub_cost
roi_pct = (net_annual / sub_cost) * 100 if sub_cost > 0 else 0

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("EVENT SAVINGS DELTA", f"{sym}{ev_savings:,.0f}")
with m2:
    st.metric("ANNUAL NET DIVIDEND", f"{sym}{net_annual:,.0f}", delta=f"{roi_pct:.0f}% ROI")
with m3:
    st.metric("EFFICIENCY GAIN", f"{current['days'] - targeted['days']} Days Saved")

# Visual Chart
fig = go.Figure()
cats = ['Intel Cell', 'Aerial Recon', 'Field Ops', 'Ground Fleet']
fig.add_trace(go.Bar(name='Current (Broad Search)', x=cats, y=[current['intel'], current['air'], current['field'], current['fleet']], marker_color='#334155'))
fig.add_trace(go.Bar(name='ICEYE (Targeted)', x=cats, y=[targeted['intel'], targeted['air'], targeted['field'], targeted['fleet']], marker_color=PRIMARY))
fig.update_layout(
    barmode='group', 
    height=400, 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)', 
    font=dict(color=TEXT), 
    margin=dict(t=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)
