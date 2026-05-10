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
        min_value=0,
        value=350000,
        step=10000,
        format="%d"
    )

    annual_events = st.slider("Annual Major Flood Events", 1, 10, 3)

    st.divider()

    include_mob = st.toggle("Include Mobilisation Costs", value=False)

    mob_fee = 0
    if include_mob:
        mob_fee = st.number_input(
            f"Mobilisation Fee ({sym})",
            min_value=0,
            value=125000,
            step=5000,
            format="%d"
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
            (data["hcv_per_tf"] * data["hcv_cost"]) +
            (data["lv_per_tf"] * data["lv_cost"])
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
        "missions": data["num_missions"]
    }

# =========================================================
# PROFILE RENDERER
# =========================================================
def render_profile(prefix, defaults, heading_color):

    st.markdown(
        f"<h2 style='color:{heading_color}; margin-bottom:0.5rem;'>{prefix.upper()} RESPONSE</h2>",
        unsafe_allow_html=True
    )

    # ---------------- INTEL ----------------
    st.markdown('<div class="section-header">Intelligence & GIS Cell</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Remote sensing and GIS analysis.</div>', unsafe_allow_html=True)

    intel_on = st.toggle(f"Enable Intel Cell ({prefix})", value=True, key=f"{prefix}_intel")

    c1, c2, c3 = st.columns(3)
    gp = c1.number_input("Analysts", min_value=0, value=defaults["gp"], step=1, key=f"{prefix}_gp")
    gh = c2.number_input("Hours", min_value=0, value=defaults["gh"], step=1, key=f"{prefix}_gh")
    gr = c3.number_input("Rate", min_value=0, value=defaults["gr"], step=5, key=f"{prefix}_gr")

    intel_preview = gp * gh * gr if intel_on else 0
    st.markdown(f"<div class='formula-tag'>Intel: {sym}{intel_preview:,.0f}</div>", unsafe_allow_html=True)

    # ---------------- AIR ----------------
    st.markdown('<div class="section-header">Aerial Observation</div>', unsafe_allow_html=True)

    air_on = st.toggle(f"Enable Aerial ({prefix})", value=True, key=f"{prefix}_air")

    c1, c2, c3 = st.columns(3)
    au = c1.number_input("Aircraft", min_value=0, value=defaults["au"], step=1, key=f"{prefix}_au")
    ah = c2.number_input("Hours", min_value=0, value=defaults["ah"], step=1, key=f"{prefix}_ah")
    ar = c3.number_input("Rate", min_value=0, value=defaults["ar"], step=100, key=f"{prefix}_ar")

    air_preview = au * ah * ar if air_on else 0
    st.markdown(f"<div class='formula-tag'>Air: {sym}{air_preview:,.0f}</div>", unsafe_allow_html=True)

    # ---------------- FIELD ----------------
    st.markdown('<div class="section-header">Field Personnel</div>', unsafe_allow_html=True)

    field_on = st.toggle(f"Enable Field ({prefix})", value=True, key=f"{prefix}_field")

    c1, c2 = st.columns(2)
    staff = c1.number_input("Staff", min_value=0, value=defaults["staff"], step=1, key=f"{prefix}_staff")
    days = c2.number_input("Days", min_value=0, value=defaults["days"], step=1, key=f"{prefix}_days")

    c3, c4, c5 = st.columns(3)
    shift_hours = c3.number_input("Shift Hours", min_value=1, max_value=24, value=12, key=f"{prefix}_shift")
    f_wage = c4.number_input("Rate", min_value=0, value=48, key=f"{prefix}_wage")
    f_diet = c5.number_input("Diet", min_value=0, value=165, key=f"{prefix}_diet")

    field_preview = (
        (staff * days * shift_hours * f_wage) +
        (staff * days * f_diet)
    ) if field_on else 0

    st.markdown(f"<div class='formula-tag'>Field: {sym}{field_preview:,.0f}</div>", unsafe_allow_html=True)

    # ---------------- LOGISTICS ----------------
    st.markdown('<div class="section-header">Logistics</div>', unsafe_allow_html=True)

    fleet_on = st.toggle(f"Enable Fleet ({prefix})", value=True, key=f"{prefix}_fleet")

    num_missions = st.number_input("Missions", min_value=0, value=defaults["rolls"], step=1, key=f"{prefix}_missions")

    c1, c2 = st.columns(2)
    hcv_per_tf = c1.number_input("HCV per TF", min_value=0, value=defaults["hcv_per"], key=f"{prefix}_hcvp")
    hcv_cost = c2.number_input("HCV Cost", min_value=0, value=850, key=f"{prefix}_hcv")

    c3, c4 = st.columns(2)
    lv_per_tf = c3.number_input("LV per TF", min_value=0, value=defaults["lv_per"], key=f"{prefix}_lvp")
    lv_cost = c4.number_input("LV Cost", min_value=0, value=450, key=f"{prefix}_lv")

    abort_units = st.number_input("Aborted Missions", min_value=0, value=defaults["aborts"], key=f"{prefix}_abort")
    abort_cost = st.number_input("Abort Cost", min_value=0, value=550, key=f"{prefix}_abortc")

    mission_ops = num_missions * ((hcv_per_tf * hcv_cost) + (lv_per_tf * lv_cost))
    abort_ops = abort_units * abort_cost
    fleet_preview = (mission_ops + abort_ops) if fleet_on else 0

    st.markdown(f"<div class='formula-tag'>Fleet: {sym}{fleet_preview:,.0f}</div>", unsafe_allow_html=True)

    return {
        "intel_on": intel_on,
        "air_on": air_on,
        "field_on": field_on,
        "fleet_on": fleet_on,
        "gp": gp, "gh": gh, "gr": gr,
        "au": au, "ah": ah, "ar": ar,
        "staff": staff, "days": days,
        "shift_hours": shift_hours,
        "f_wage": f_wage,
        "f_diet": f_diet,
        "num_missions": num_missions,
        "hcv_per_tf": hcv_per_tf,
        "hcv_cost": hcv_cost,
        "lv_per_tf": lv_per_tf,
        "lv_cost": lv_cost,
        "abort_units": abort_units,
        "abort_cost": abort_cost
    }

# =========================================================
# HEADER
# =========================================================
st.markdown("<h1 style='color:white'>ICEYE ROI Modeller</h1>", unsafe_allow_html=True)

# =========================================================
# PROFILES
# =========================================================
col1, col2 = st.columns(2)

with col1:
    current = render_profile("Current", {
        "gp": 5, "gh": 160, "gr": 95,
        "au": 4, "ah": 40, "ar": 5500,
        "staff": 650, "days": 9,
        "rolls": 80, "hcv_per": 2,
        "lv_per": 5, "aborts": 35
    }, "#94A3B8")

with col2:
    iceye = render_profile("ICEYE", {
        "gp": 2, "gh": 30, "gr": 95,
        "au": 1, "ah": 10, "ar": 5500,
        "staff": 300, "days": 4,
        "rolls": 25, "hcv_per": 1,
        "lv_per": 2, "aborts": 2
    }, PRIMARY)

# =========================================================
# CALCS
# =========================================================
current_total = calculate_profile(current, mob_fee)
iceye_total = calculate_profile(iceye)

savings = current_total["total"] - iceye_total["total"]
net = (savings * annual_events) - sub_cost
roi = (net / sub_cost) * 100 if sub_cost else 0

# =========================================================
# KPIs
# =========================================================
st.divider()

c1, c2, c3 = st.columns(3)

c1.metric("Savings / Event", f"{sym}{savings:,.0f}")
c2.metric("Net Annual", f"{sym}{net:,.0f}", delta=f"{roi:.0f}% ROI")
c3.metric("Deployments Saved", current_total["missions"] - iceye_total["missions"])

# =========================================================
# CHART
# =========================================================
fig = go.Figure()

cats = ["Intel", "Air", "Field", "Fleet"]

fig.add_trace(go.Bar(
    x=cats,
    y=[current_total["intel"], current_total["air"], current_total["field"], current_total["fleet"]],
    name="Current",
    marker_color="#475569"
))

fig.add_trace(go.Bar(
    x=cats,
    y=[iceye_total["intel"], iceye_total["air"], iceye_total["field"], iceye_total["fleet"]],
    name="ICEYE",
    marker_color=PRIMARY
))

fig.update_layout(
    barmode="group",
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT)
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FINAL LOGIC BOX (FIXED HTML RENDER)
# =========================================================
st.markdown(
    f"""
<div class="logic-container">

<h2 style="margin-top:0; font-weight:700;">
▲ Operational Intelligence Logic
</h2>

<div class="logic-grid">

<div>

<h4 style="color:{PRIMARY}; margin-bottom:10px;">
Flood Rapid Intelligence (6h)
</h4>

<p style="font-size:0.95rem; line-height:1.6; color:{MUTED};">
ICEYE SAR enables 6-hour flood monitoring through cloud and night,
reducing reliance on aerial reconnaissance and improving situational awareness.
</p>

</div>

<div>

<h4 style="color:{SUCCESS}; margin-bottom:10px;">
Flood Insights (24h)
</h4>

<p style="font-size:0.95rem; line-height:1.6; color:{MUTED};">
Building-level flood depth intelligence enables better asset routing,
reducing washouts, delays, and operational loss.
</p>

</div>

</div>

</div>
""",
    unsafe_allow_html=True
)
