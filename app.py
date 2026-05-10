import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ICEYE | Precision Response Modeller",
    page_icon="▲",
    layout="wide"
)

# =========================================================
# THEME
# =========================================================
BG = "#0B1220"
CARD = "#111827"
BORDER = "#1E293B"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"

PRIMARY = "#38BDF8"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
ACCENT = "#6366F1"

# =========================================================
# STYLING
# =========================================================
st.markdown(
    f"""
<style>
html, body, .stApp {{
    background-color: {BG};
    color: {TEXT};
    font-family: Inter, system-ui, sans-serif;
}}

.block-container {{
    padding-top: 2rem;
}}

.section-header {{
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.78rem;
    font-weight: 700;
    color: {PRIMARY};
    margin: 1.7rem 0 0.3rem 0;
    display: flex;
    align-items: center;
}}

.section-header::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: {BORDER};
    margin-left: 12px;
}}

.section-desc {{
    font-size: 0.88rem;
    color: {MUTED};
    margin-bottom: 1rem;
    line-height: 1.5;
}}

.formula-tag {{
    font-size: 0.78rem;
    color: {MUTED};
    background: rgba(255,255,255,0.04);
    border: 1px solid {BORDER};
    padding: 10px 14px;
    border-radius: 10px;
    margin-top: 10px;
}}

.logic-container {{
    background: linear-gradient(145deg, #111827, #1E293B);
    border: 1px solid {BORDER};
    padding: 2.5rem;
    border-radius: 22px;
    margin-top: 4rem;
}}

.logic-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 20px;
}}

@media (max-width: 900px) {{
    .logic-grid {{
        grid-template-columns: 1fr;
    }}
}}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## ▲ ICEYE")
    st.markdown("### Modeller Controls")

    currency = st.selectbox("Currency", ["AUD", "USD", "EUR", "GBP"])
    sym = {"AUD": "$", "USD": "$", "EUR": "€", "GBP": "£"}[currency]

    st.divider()

    sub_cost = st.number_input(
        "Annual ICEYE Subscription",
        value=350000,
        step=10000,
        format="%d",
        min_value=0,
    )

    annual_events = st.slider("Annual Major Flood Events", 1, 10, 3)

    st.divider()

    st.subheader("Mobilisation Logistics")
    st.caption("One-off regional activation costs applied to Current-state operations only.")

    include_mob = st.toggle("Include Mobilisation Costs", value=False)

    mob_fee = (
        st.number_input(
            f"Mobilisation Fee ({sym})",
            value=125000,
            step=5000,
            format="%d",
            min_value=0,
        )
        if include_mob
        else 0
    )

# =========================================================
# CALC ENGINE
# =========================================================
def calculate_profile(data, include_mob_fee=0):
    intel_val = (data["gp"] * data["gh"] * data["gr"]) if data["intel_on"] else 0

    air_val = (data["au"] * data["ah"] * data["ar"]) if data["air_on"] else 0

    field_val = (
        (data["staff"] * (data["days"] * data["shift_hours"]) * data["f_wage"])
        + (data["staff"] * data["days"] * data["f_diet"])
    ) if data["field_on"] else 0

    if data["fleet_on"]:
        mission_ops = data["num_missions"] * (
            (data["hcv_per_tf"] * data["hcv_cost"]) + (data["lv_per_tf"] * data["lv_cost"])
        )
        abort_ops = data["abort_units"] * data["abort_cost"]
        fleet_val = mission_ops + abort_ops
    else:
        fleet_val = 0

    total = intel_val + air_val + field_val + fleet_val + include_mob_fee

    return {
        "total": total,
        "intel": intel_val,
        "air": air_val,
        "field": field_val,
        "fleet": fleet_val,
        "missions": data["num_missions"],
        "days": data["days"],
    }

# =========================================================
# PROFILE RENDERER
# =========================================================
def render_profile(prefix, defaults, heading_color):
    st.markdown(
        f"<h2 style='color:{heading_color}; margin-bottom:0.5rem;'>{prefix.upper()} RESPONSE</h2>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # 1. INTEL
    # -----------------------------------------------------
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Remote sensing and GIS analysis to determine flood extent and depth.</div>',
        unsafe_allow_html=True,
    )

    intel_on = st.toggle(f"Enable Intel Cell ({prefix})", value=True, key=f"{prefix}_intel_t")

    c1, c2, c3 = st.columns(3)
    gp = c1.number_input(
        f"{prefix} Analysts",
        min_value=0,
        step=1,
        value=defaults["gp"],
        key=f"{prefix}_gp",
    )
    gh = c2.number_input(
        f"{prefix} Total Hours",
        min_value=0,
        step=1,
        value=defaults["gh"],
        key=f"{prefix}_gh",
    )
    gr = c3.number_input(
        f"{prefix} Hourly Rate",
        min_value=0,
        step=5,
        value=int(defaults["gr"]),
        format="%d",
        key=f"{prefix}_gr",
    )

    intel_preview = (gp * gh * gr) if intel_on else 0
    st.markdown(f"<div class='formula-tag'>Intel Total: {sym}{intel_preview:,.0f}</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 2. AERIAL
    # -----------------------------------------------------
    st.markdown('<div class="section-header">Aerial Observation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Fixed-wing or rotary assets for visual scouting.</div>',
        unsafe_allow_html=True,
    )

    air_on = st.toggle(f"Enable Aerial Recon ({prefix})", value=True, key=f"{prefix}_air_t")

    c1, c2, c3 = st.columns(3)
    au = c1.number_input(
        f"{prefix} Aircraft",
        min_value=0,
        step=1,
        value=defaults["au"],
        key=f"{prefix}_au",
    )
    ah = c2.number_input(
        f"{prefix} Flight Hours",
        min_value=0,
        step=1,
        value=defaults["ah"],
        key=f"{prefix}_ah",
    )
    ar = c3.number_input(
        f"{prefix} Dry Rate/Hr",
        min_value=0,
        step=100,
        value=int(defaults["ar"]),
        format="%d",
        key=f"{prefix}_ar",
    )

    air_preview = (au * ah * ar) if air_on else 0
    st.markdown(f"<div class='formula-tag'>Aerial Total: {sym}{air_preview:,.0f}</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 3. FIELD OPS
    # -----------------------------------------------------
    st.markdown('<div class="section-header">Field Personnel</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Deployment costs for boots on the ground.</div>',
        unsafe_allow_html=True,
    )

    field_on = st.toggle(f"Enable Field Ops ({prefix})", value=True, key=f"{prefix}_field_t")

    c1, c2 = st.columns(2)
    staff = c1.number_input(
        f"{prefix} Personnel Count",
        min_value=0,
        step=1,
        value=defaults["staff"],
        key=f"{prefix}_st",
    )
    days = c2.number_input(
        f"{prefix} Deployment Days",
        min_value=0,
        step=1,
        value=defaults["days"],
        key=f"{prefix}_ds",
    )

    c3, c4, c5 = st.columns(3)
    shift_hours = c3.number_input(
        f"{prefix} Shift Hours",
        min_value=1,
        max_value=24,
        step=1,
        value=12,
        key=f"{prefix}_shift",
    )
    f_wage = c4.number_input(
        f"{prefix} Personnel Rate",
        min_value=0,
        step=1,
        value=48,
        format="%d",
        key=f"{prefix}_fw",
    )
    f_diet = c5.number_input(
        f"{prefix} Subsistence/Day",
        min_value=0,
        step=5,
        value=165,
        format="%d",
        key=f"{prefix}_fd",
    )

    field_preview = (
        (staff * (days * shift_hours) * f_wage) + (staff * days * f_diet)
    ) if field_on else 0

    st.markdown(f"<div class='formula-tag'>Personnel Total: {sym}{field_preview:,.0f}</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 4. LOGISTICS
    # -----------------------------------------------------
    st.markdown('<div class="section-header">Taskforce & Asset Logistics</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Fleet movements and deployment costs tied to taskforce activity.</div>',
        unsafe_allow_html=True,
    )

    fleet_on = st.toggle(f"Enable Asset Logistics ({prefix})", value=True, key=f"{prefix}_fleet_t")

    num_missions = st.number_input(
        f"Total Taskforce Deployments ({prefix})",
        min_value=0,
        step=1,
        value=defaults.get("rolls", 10),
        key=f"{prefix}_missions",
    )

    col_hcv, col_lv = st.columns(2)

    with col_hcv:
        hcv_per_tf = st.number_input(
            "HCVs per Taskforce",
            min_value=0,
            step=1,
            value=defaults.get("hcv_per", 2),
            key=f"{prefix}_hcv_p",
        )
        hcv_cost = st.number_input(
            f"HCV Cost/Mission ({sym})",
            min_value=0,
            step=50,
            value=850,
            format="%d",
            key=f"{prefix}_hcv_c",
        )

    with col_lv:
        lv_per_tf = st.number_input(
            "LVs per Taskforce",
            min_value=0,
            step=1,
            value=defaults.get("lv_per", 4),
            key=f"{prefix}_lv_p",
        )
        lv_cost = st.number_input(
            f"LV Cost/Mission ({sym})",
            min_value=0,
            step=50,
            value=450,
            format="%d",
            key=f"{prefix}_lv_c",
        )

    st.markdown(
        "<div style='font-size:0.82rem; color:#F87171; font-weight:600; margin-top:14px;'>Operational Washouts (Aborted Efforts)</div>",
        unsafe_allow_html=True,
    )

    f5, f6 = st.columns(2)
    abort_units = f5.number_input(
        f"Number of Aborted Missions ({prefix})",
        min_value=0,
        step=1,
        value=defaults.get("aborts", 5),
        key=f"{prefix}_abt",
    )
    abort_cost = f6.number_input(
        "Sunk Cost per Abort",
        min_value=0,
        step=50,
        value=550,
        format="%d",
        key=f"{prefix}_abt_c",
    )

    mission_ops = num_missions * ((hcv_per_tf * hcv_cost) + (lv_per_tf * lv_cost))
    abort_ops = abort_units * abort_cost
    fleet_preview = (mission_ops + abort_ops) if fleet_on else 0

    st.markdown(f"<div class='formula-tag'>Logistics Total: {sym}{fleet_preview:,.0f}</div>", unsafe_allow_html=True)

    return {
        "intel_on": intel_on,
        "air_on": air_on,
        "field_on": field_on,
        "fleet_on": fleet_on,
        "gp": gp,
        "gh": gh,
        "gr": gr,
        "au": au,
        "ah": ah,
        "ar": ar,
        "staff": staff,
        "days": days,
        "shift_hours": shift_hours,
        "f_wage": f_wage,
        "f_diet": f_diet,
        "num_missions": num_missions,
        "hcv_per_tf": hcv_per_tf,
        "hcv_cost": hcv_cost,
        "lv_per_tf": lv_per_tf,
        "lv_cost": lv_cost,
        "abort_units": abort_units,
        "abort_cost": abort_cost,
    }

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <h1 style="color:white; margin-top:-20px;">
    ICEYE Subscription ROI: Precision Response Modeller
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown("**Operational Objective:** Minimising taskforce washouts and asset risk through SAR ground truth.")

# =========================================================
# PROFILES
# =========================================================
col_left, col_right = st.columns(2, gap="large")

with col_left:
    current_inputs = render_profile(
        "Current",
        {
            "gp": 5,
            "gh": 160,
            "au": 4,
            "ah": 40,
            "ar": 5500,
            "staff": 650,
            "days": 9,
            "rolls": 80,
            "hcv_per": 2,
            "lv_per": 5,
            "aborts": 35,
        },
        "#94A3B8",
    )

with col_right:
    targeted_inputs = render_profile(
        "ICEYE",
        {
            "gp": 2,
            "gh": 30,
            "au": 1,
            "ah": 10,
            "ar": 5500,
            "staff": 300,
            "days": 4,
            "rolls": 25,
            "hcv_per": 1,
            "lv_per": 2,
            "aborts": 2,
        },
        PRIMARY,
    )

# =========================================================
# CALCULATIONS
# =========================================================
current = calculate_profile(current_inputs, mob_fee if include_mob else 0)
targeted = calculate_profile(targeted_inputs, 0)

ev_savings = current["total"] - targeted["total"]
net_annual = (ev_savings * annual_events) - sub_cost
roi_pct = (net_annual / sub_cost) * 100 if sub_cost > 0 else 0

# =========================================================
# KPI DASHBOARD
# =========================================================
st.divider()

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("EVENT SAVINGS DELTA", f"{sym}{ev_savings:,.0f}")

with m2:
    st.metric(
        "ANNUAL NET DIVIDEND",
        f"{sym}{net_annual:,.0f}",
        delta=f"{roi_pct:,.0f}% ROI",
        delta_color="normal",
    )

with m3:
    st.metric("MISSION EFFICIENCY", f"{current['missions'] - targeted['missions']} Fewer Deployments")

# =========================================================
# CHART
# =========================================================
fig = go.Figure()

cats = ["Intel Cell", "Aerial Recon", "Field Ops", "Logistics & Fleet"]

current_vals = [current["intel"], current["air"], current["field"], current["fleet"]]
targeted_vals = [targeted["intel"], targeted["air"], targeted["field"], targeted["fleet"]]

fig.add_trace(
    go.Bar(
        name="Current",
        x=cats,
        y=current_vals,
        text=[f"{sym}{v:,.0f}" for v in current_vals],
        textposition="outside",
        marker_color="#475569",
    )
)

fig.add_trace(
    go.Bar(
        name="ICEYE",
        x=cats,
        y=targeted_vals,
        text=[f"{sym}{v:,.0f}" for v in targeted_vals],
        textposition="outside",
        marker_color=PRIMARY,
    )
)

fig.update_layout(
    barmode="group",
    height=460,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT),
    margin=dict(t=50),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# LOGIC BOX
# =========================================================
st.markdown(
    f"""
<div class="logic-container">
    <h2 style="margin-top:0; font-weight:700;">▲ Operational Intelligence Logic</h2>
    <div class="logic-grid">
        <div>
            <h4 style="color:{PRIMARY}; margin-bottom:10px;">Flood Rapid Intelligence (6h)</h4>
            <p style="font-size:0.95rem; line-height:1.6; color:{MUTED};">
                By utilising the world's largest SAR constellation, ICEYE provides 6-hourly flood extent updates.
                This allows GIS teams to track the leading edge of floodwaters through cloud and night, reducing
                dependence on broad aerial reconnaissance.
            </p>
        </div>
        <div>
            <h4 style="color:{SUCCESS}; margin-bottom:10px;">Flood Insights (24h)</h4>
            <p style="font-size:0.95rem; line-height:1.6; color:{MUTED};">
                Flood Insights provides building-level flood depth. This supports asset matching, helping command
                keep light vehicles out of impassable zones and reducing operational washouts and fleet damage.
            </p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
