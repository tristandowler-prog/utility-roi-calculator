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

# Custom CSS for a professional "Dark Mode" Agency Dashboard
BG, CARD, BORDER, TEXT, MUTED = "#0B1220", "#111827", "#1E293B", "#F8FAFC", "#94A3B8"
PRIMARY, SUCCESS, WARNING, ACCENT = "#38BDF8", "#22C55E", "#F59E0B", "#6366F1"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    
    html, body, .stApp {{ 
        background-color: {BG}; 
        color: {TEXT}; 
        font-family: 'Inter', sans-serif; 
    }}
    .stMetric {{ 
        background-color: {CARD} !important; 
        border: 1px solid {BORDER} !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
    }}
    .formula-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: {PRIMARY};
        background: rgba(56, 189, 248, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
        margin-top: -10px;
        display: inline-block;
    }}
    .section-header {{
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
        font-weight: 700;
        color: {MUTED};
        margin-bottom: 15px;
        border-left: 3px solid {ACCENT};
        padding-left: 10px;
    }}
    div[data-testid="column"] {{
        padding: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - COMMAND SETTINGS
# =========================================================
with st.sidebar:
    st.title("▲ ICEYE Strategic")
    st.markdown("---")
    currency = st.selectbox("Reporting Currency", ["USD", "AUD", "EUR", "GBP"])
    sym = {"USD": "$", "AUD": "$", "EUR": "€", "GBP": "£"}[currency]
    
    st.subheader("Global Constants")
    annual_events = st.slider("Annual Major Events", 1, 12, 3)
    subscription = st.number_input("Annual Platform Fee", value=350000.0, step=10000.0)
    per_diem = st.number_input("Daily Subsistence (Per Person)", value=185.0)
    
    st.divider()
    st.subheader("External Support")
    mutual_aid = st.checkbox("Include Mutual Aid Activation Fee", value=True)
    aid_fee = st.number_input("One-time Activation Fee", value=150000.0) if mutual_aid else 0

# =========================================================
# CALCULATION ENGINE
# =========================================================
def render_agency_pillar(prefix, defaults, theme_color):
    st.markdown(f"### :{theme_color}[{prefix.upper()}]")
    
    # Pillar 1: Intel Cell
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        gis_p = st.number_input("Analysts", value=defaults['gis_p'], key=f"{prefix}_gp")
    with c2:
        gis_h = st.number_input("Total Hours", value=defaults['gis_h'], key=f"{prefix}_gh")
    gis_rate = 95.0
    intel_total = gis_p * gis_h * gis_rate
    st.markdown(f"<span class='formula-tag'>{gis_p} personnel × {gis_h} hrs × {sym}{gis_rate}/hr = {sym}{intel_total:,.0f}</span>", unsafe_allow_html=True)

    # Pillar 2: Aerial Recon
    st.markdown('<div class="section-header">Aerial Observation Profile</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        air_u = st.number_input("Aircraft Units", value=defaults['air_u'], key=f"{prefix}_au")
    with c2:
        air_h = st.number_input("Flight Hours/Unit", value=defaults['air_h'], key=f"{prefix}_ah")
    air_rate = defaults['air_r']
    air_total = air_u * air_h * air_rate
    st.markdown(f"<span class='formula-tag'>{air_u} units × {air_h} hrs × {sym}{air_rate:,.0f}/hr = {sym}{air_total:,.0f}</span>", unsafe_allow_html=True)

    # Pillar 3: Fleet Composition
    st.markdown('<div class="section-header">Fleet & Resource Deployment</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        hcv = st.number_input("High-Clearance (HCV)", value=defaults['hcv'], key=f"{prefix}_hcv")
    with c2:
        std = st.number_input("Standard Vehicles", value=defaults['std'], key=f"{prefix}_std")
    ops_cost = 650.0
    fleet_total = (hcv + std) * ops_cost
    st.markdown(f"<span class='formula-tag'>({hcv}hcv + {std}std) × {sym}{ops_cost}/roll = {sym}{fleet_total:,.0f}</span>", unsafe_allow_html=True)

    # Pillar 4: Staging Burn
    st.markdown('<div class="section-header">Base of Operations (BoO)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        staff = st.number_input("Field Personnel", value=defaults['staff'], key=f"{prefix}_staff")
    with c2:
        days = st.number_input("Deployment Days", value=defaults['days'], key=f"{prefix}_days")
    staging_total = staff * days * per_diem
    st.markdown(f"<span class='formula-tag'>{staff} pax × {days} days × {sym}{per_diem}/day = {sym}{staging_total:,.0f}</span>", unsafe_allow_html=True)

    activation = aid_fee if (prefix == "Current" and mutual_aid) else 0
    event_total = intel_total + air_total + fleet_total + staging_total + activation
    
    return {
        "total": event_total, "intel": intel_total, "air": air_total, 
        "fleet": fleet_total, "staging": staging_total, "activation": activation
    }

# =========================================================
# MAIN DASHBOARD
# =========================================================
st.title("Operational Command: ROI Modeling")
st.markdown(f"**Scenario Evaluation:** Quantifying the shift from **Wide-Area Search** to **Targeted SAR-Verified Response**")

# Comparison Columns
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
# EXECUTIVE SUMMARY
# =========================================================
st.divider()
event_savings = cur_data['total'] - ice_data['total']
annual_gross = event_savings * annual_events
annual_net = annual_gross - subscription
roi = (annual_net / subscription) * 100 if subscription > 0 else 0

st.markdown("### 📊 Executive Financial Summary")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Cost / Event", f"{sym}{cur_data['total']:,.0f}")
m2.metric("Targeted Cost / Event", f"{sym}{ice_data['total']:,.0f}")
m3.metric("Net Annual Dividend", f"{sym}{annual_net:,.0f}", f"{sym}{event_savings:,.0f} per event")
m4.metric("Strategic ROI", f"{roi:.0f}%")

# =========================================================
# VISUAL ANALYTICS
# =========================================================
c_left, c_right = st.columns([2, 1])

with c_left:
    fig = go.Figure()
    cats = ['Intel Cell', 'Aerial Recon', 'Ground Fleet', 'Staging (BoO)']
    fig.add_trace(go.Bar(name='Current Profile', x=cats, 
                         y=[cur_data['intel'], cur_data['air'], cur_data['fleet'], cur_data['staging']], marker_color='#475569'))
    fig.add_trace(go.Bar(name='Targeted Response', x=cats, 
                         y=[ice_data['intel'], ice_data['air'], ice_data['fleet'], ice_data['staging']], marker_color=PRIMARY))
    
    fig.update_layout(
        barmode='group', height=400, 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT), margin=dict(t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER}; padding:24px; border-radius:12px; height: 100%;">
        <p style="text-transform:uppercase; font-size:0.75rem; color:{MUTED}; letter-spacing:1px;">Audit Summary</p>
        <p style="font-size:1.8rem; font-weight:700; margin-bottom:0;">{sym}{event_savings:,.0f}</p>
        <p style="color:{SUCCESS}; font-size:0.9rem; margin-top:0;">Operational Delta per Event</p>
        <hr style="border:0; border-top:1px solid {BORDER}; margin:15px 0;">
        <ul style="list-style:none; padding:0; font-size:0.85rem; color:{MUTED};">
            <li style="margin-bottom:8px;">✅ <b>Intel Efficiency:</b> {(1 - ice_data['intel']/cur_data['intel'])*100:.0f}% reduction in manual GIS digitization.</li>
            <li style="margin-bottom:8px;">✅ <b>Aerial Preservation:</b> Flights pivoted from observation to tactical rescue.</li>
            <li style="margin-bottom:8px;">✅ <b>Logistics Compression:</b> Deployment days reduced by {cur_data['metrics']['Staging Days'] - ice_data['metrics']['Staging Days']} days.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# AUDITABLE FORMULA FOOTER
# =========================================================
with st.expander("🔍 VIEW AUDITABLE MATHEMATICAL LOGIC"):
    st.latex(r"Cost_{Event} = (P_{gis} \cdot H_{gis} \cdot R_{gis}) + (U_{air} \cdot H_{air} \cdot R_{air}) + (V_{hcv+std} \cdot C_{roll}) + (P_{field} \cdot D_{stage} \cdot C_{diet})")
    st.markdown(f"""
    *   **Intelligence:** Reductions are based on shifting GIS Analysts from "Data Generation" (manual digitization) to "Data Validation" using automated ICEYE SAR feeds.
    *   **Fleet:** Assets are matched to water depth; standard vehicles are not deployed to "at-risk" zones, reducing recovery and downtime costs.
    *   **Mutual Aid:** Current model assumes a trigger threshold that is avoided in the Targeted model through faster local response.
    """)
