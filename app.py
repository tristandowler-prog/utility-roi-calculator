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

    .logic-container {{
        background: linear-gradient(145deg, #111827, #1e293b);
        border: 1px solid {BORDER};
        padding: 2.5rem;
        border-radius: 20px;
        margin-top: 4rem;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR & GLOBAL CONTROLS
# =========================================================
with st.sidebar:
    st.markdown("## ▲ ICEYE")
    st.markdown("### Modeller Controls")
    currency = st.selectbox("Currency", ["AUD", "USD", "EUR", "GBP"])
    sym = {"AUD": "$", "USD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    st.divider()
    sub_cost = st.number_input("Annual ICEYE Subscription", value=350000.0, step=10000.0)
    annual_events = st.slider("Annual Major Flood Events", 1, 10, 3)
    
    st.divider()
    st.subheader("Mobilisation Logistics")
    st.caption("One-off costs for regional activation (Applied to 'Current' only).")
    include_mob = st.toggle("Include Mobilisation Costs", value=False)
    mob_fee = st.number_input(f"Mobilisation Fee ({sym})", value=125000.0) if include_mob else 0

# =========================================================
# OPERATIONAL PILLAR ENGINE
# =========================================================
def render_profile(prefix, defaults, color):
    st.markdown(f"## :{color}[{prefix.upper()} RESPONSE]")
    
    # 1. INTEL CELL
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    intel_on = st.toggle(f"Include Intel Cell ({prefix})", value=True, key=f"{prefix}_intel_on")
    c1, c2, c3 = st.columns(3)
    gp = c1.number_input(f"{prefix} Analysts", value=defaults['gp'], key=f"{prefix}_gp")
    gh = c2.number_input(f"{prefix} Total Hours", value=defaults['gh'], key=f"{prefix}_gh")
    gr = c3.number_input(f"{prefix} Hourly Rate", value=95.0, key=f"{prefix}_gr")
    intel_val = (gp * gh * gr) if intel_on else 0
    st.markdown(f"<div class='formula-tag'>Intel Total: {sym}{intel_val:,.0f}</div>", unsafe_allow_html=True)

    # 2. AERIAL RECON
    st.markdown('<div class="section-header">Aerial Observation</div>', unsafe_allow_html=True)
    air_on = st.toggle(f"Include Aerial Recon ({prefix})", value=True, key=f"{prefix}_air_on")
    c1, c2, c3 = st.columns(3)
    au = c1.number_input(f"{prefix} Aircraft", value=defaults['au'], key=f"{prefix}_au")
    ah = c2.number_input(f"{prefix} Flight Hrs", value=defaults['ah'], key=f"{prefix}_ah")
    ar = c3.number_input(f"{prefix} Dry Rate/Hr", value=defaults['ar'], key=f"{prefix}_ar")
    air_val = (au * ah * ar) if air_on else 0
    st.markdown(f"<div class='formula-tag'>Aerial Total: {sym}{air_val:,.0f}</div>", unsafe_allow_html=True)

    # 3. FIELD OPERATIONS
    st.markdown('<div class="section-header">Field Personnel</div>', unsafe_allow_html=True)
    field_on = st.toggle(f"Include Field Ops ({prefix})", value=True, key=f"{prefix}_field_on")
    c1, c2 = st.columns(2)
    staff = c1.number_input(f"{prefix} Personnel Count", value=defaults['staff'], key=f"{prefix}_st")
    days = c2.number_input(f"{prefix} Deployment Days", value=defaults['days'], key=f"{prefix}_ds")
    
    c3, c4 = st.columns(2)
    f_wage = c3.number_input(f"{prefix} Personnel Rate", value=48.0, key=f"{prefix}_fw")
    f_diet = c4.number_input(f"{prefix} Subsistence/Day", value=165.0, key=f"{prefix}_fd")
    
    field_val = ((staff * (days * 12) * f_wage) + (staff * days * f_diet)) if field_on else 0
    st.markdown(f"<div class='formula-tag'>Personnel Total: {sym}{field_val:,.0f}</div>", unsafe_allow_html=True)

    # 4. TRUCK ROLLS & FLEET (THE CORE SAVINGS LEVER)
    st.markdown('<div class="section-header">Truck Rolls & Fleet Logistics</div>', unsafe_allow_html=True)
    fleet_on = st.toggle(f"Include Fleet Logistics ({prefix})", value=True, key=f"{prefix}_fleet_on")
    
    # The primary "Volume" field
    num_rolls = st.number_input(f"Total Number of Truck Rolls ({prefix})", value=defaults.get('rolls', 10), key=f"{prefix}_rolls")
    
    col_hcv, col_std = st.columns(2)
    with col_hcv:
        hcv_per_roll = st.number_input(f"HCVs per Roll", value=defaults.get('hcv_per', 2), key=f"{prefix}_hcv_p")
        hcv_cost = st.number_input(f"HCV Roll Cost ({sym})", value=850.0, key=f"{prefix}_hcv_c")
    with col_std:
        std_per_roll = st.number_input(f"STDs per Roll", value=defaults.get('std_per', 4), key=f"{prefix}_std_p")
        std_cost = st.number_input(f"STD Roll Cost ({sym})", value=450.0, key=f"{prefix}_std_c")
    
    # Aborted Missions
    st.markdown('<div style="font-size:0.8rem; color:#94A3B8; margin-top:10px;">Operational Inefficiency (Aborted Rolls)</div>', unsafe_allow_html=True)
    f5, f6 = st.columns(2)
    abort_units = f5.number_input(f"Aborted Missions ({prefix})", value=defaults.get('aborts', 5), key=f"{prefix}_abt")
    abort_cost = f6.number_input(f"Sunk Cost/Abort", value=550.0, key=f"{prefix}_abt_c")
    
    # Calculation Logic
    if fleet_on:
        roll_ops = num_rolls * ((hcv_per_roll * hcv_cost) + (std_per_roll * std_cost))
        abort_ops = abort_units * abort_cost
        fleet_val = roll_ops + abort_ops
    else:
        fleet_val = 0
    
    st.markdown(f"<div class='formula-tag'>Fleet Total: {sym}{fleet_val:,.0f}</div>", unsafe_allow_html=True)

    # TOTAL SUMMATION
    final_mob = mob_fee if (prefix == "Current" and include_mob) else 0
    total = intel_val + air_val + field_val + fleet_val + final_mob
    return {"total": total, "intel": intel_val, "air": air_val, "field": field_val, "fleet": fleet_val, "days": days, "rolls": num_rolls}

# =========================================================
# MAIN DASHBOARD
# =========================================================
st.markdown('<h1 style="color:white; margin-top:-30px;">ICEYE Subscription ROI: Precision Response Modeller</h1>', unsafe_allow_html=True)
st.markdown(f"**Operational Objective:** Reducing truck roll volume and mission latency through SAR ground truth.")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    current = render_profile("Current", {
        'gp':5, 'gh':160, 'au':4, 'ah':40, 'ar':5500.0, 
        'staff':650, 'days':9, 'rolls': 80, 'hcv_per': 2, 'std_per': 5, 'aborts': 35
    }, "grey")

with col_right:
    targeted = render_profile("ICEYE", {
        'gp':2, 'gh':30, 'au':1, 'ah':10, 'ar':5500.0, 
        'staff':300, 'days':4, 'rolls': 25, 'hcv_per': 1, 'std_per': 2, 'aborts': 2
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
    st.metric("ROLL REDUCTION", f"{current['rolls'] - targeted['rolls']} Fewer Rolls")

# Visual Chart
fig = go.Figure()
cats = ['Intel Cell', 'Aerial Recon', 'Field Ops', 'Ground Fleet']
fig.add_trace(go.Bar(name='Current (Search)', x=cats, y=[current['intel'], current['air'], current['field'], current['fleet']], marker_color='#334155'))
fig.add_trace(go.Bar(name='ICEYE (Precision)', x=cats, y=[targeted['intel'], targeted['air'], targeted['field'], targeted['fleet']], marker_color=PRIMARY))
fig.update_layout(
    barmode='group', height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
    font=dict(color=TEXT), margin=dict(t=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# =========================================================
# PRODUCT LOGIC BOX
# =========================================================
st.markdown(f"""
<div class="logic-container">
    <h2 style="margin-top:0; font-weight:700;">▲ Operational Intelligence Logic</h2>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 20px;">
        <div>
            <h4 style="color:{PRIMARY}; margin-bottom:10px;">Flood Rapid Intelligence (6h)</h4>
            <p style="font-size:0.95rem; line-height:1.6; color:{MUTED};">
                By utilising the world's largest SAR constellation, ICEYE provides 6-hourly <b>flood extent</b> updates. 
                This allows the GIS Intel Cell to track the "leading edge" of floodwaters through cloud and night, 
                eliminating the need for continuous wide-area aerial recon flights.
            </p>
        </div>
        <div>
            <h4 style="color:{SUCCESS}; margin-bottom:10px;">Flood Insights (24h)</h4>
            <p style="font-size:0.95rem; line-height:1.6; color:{MUTED};">
                <b>Flood Insights</b> provides building-level <b>flood depth</b>. This is the primary driver for 
                <b>Asset Matching</b>: Command can identify exact road-over-topping depths, ensuring standard vehicles 
                don't roll into impassable zones. This directly reduces "Aborted Missions" and high-value asset damage.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
