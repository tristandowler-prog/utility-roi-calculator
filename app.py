import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ICEYE Strategic ROI",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DESIGN SYSTEM
# =========================================================

BG = "#060B14"
CARD = "#111827"
CARD_2 = "#0F172A"

PRIMARY = "#38BDF8"
SUCCESS = "#22C55E"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
BORDER = "rgba(255,255,255,0.06)"

# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    f"""
<style>

html, body, .stApp {{
    font-family: Inter, sans-serif;
    background: linear-gradient(180deg, #020617 0%, #0B1120 100%);
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    background: rgba(15,23,42,0.96);
    border-right: 1px solid {BORDER};
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}}

.metric-card {{
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}}

.hero {{
    padding: 42px;
    border-radius: 30px;

    background:
        radial-gradient(circle at top left,
        rgba(56,189,248,0.22),
        transparent 30%),

        linear-gradient(
            135deg,
            #0F172A 0%,
            #020617 100%
        );

    border: 1px solid rgba(255,255,255,0.06);

    margin-bottom: 28px;
}}

.hero-title {{
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1;
    color: white;
}}

.hero-sub {{
    color: {MUTED};
    font-size: 1.1rem;
    margin-top: 14px;
}}

.label {{
    color: {MUTED};
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}}

.big-number {{
    font-size: 3rem;
    font-weight: 800;
    color: white;
}}

div[data-baseweb="input"] {{
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
}}

.stTabs [data-baseweb="tab"] {{
    font-size: 1rem;
    font-weight: 700;
}}

.stTabs [aria-selected="true"] {{
    color: white;
}}

hr {{
    border-color: rgba(255,255,255,0.08);
}}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## Strategic Inputs")

    currency = st.selectbox(
        "Reporting Currency",
        ["USD", "AUD", "EUR", "NZD"]
    )

    currency_symbol = {
        "USD": "$",
        "AUD": "$",
        "EUR": "€",
        "NZD": "$"
    }[currency]

    annual_events = st.slider(
        "Annual Major Events",
        min_value=1,
        max_value=20,
        value=4
    )

    subscription = st.number_input(
        "Annual Platform Cost",
        min_value=0.0,
        max_value=10000000.0,
        value=385000.0,
        step=10000.0
    )

    st.markdown("---")

    st.markdown("### Efficiency Assumptions")

    labor_reduction = (
        st.slider(
            "Labor Reduction %",
            0,
            100,
            80
        ) / 100
    )

    logistics_reduction = (
        st.slider(
            "Truck Roll Reduction %",
            0,
            100,
            85
        ) / 100
    )

    aviation_reduction = (
        st.slider(
            "Aviation Reduction %",
            0,
            100,
            80
        ) / 100
    )

    gis_reduction = (
        st.slider(
            "GIS Automation %",
            0,
            100,
            92
        ) / 100
    )

# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    f"""
<div class="hero">

    <div class="hero-title">
        Strategic ROI & Operational Impact
    </div>

    <div class="hero-sub">
        Satellite-enabled disaster response optimization modeling
    </div>

</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# INPUT COMPONENTS
# =========================================================

def vertical_inputs(prefix):

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        teams = st.number_input(
            "Field Teams",
            min_value=1,
            max_value=1000,
            value=12,
            key=f"{prefix}_teams"
        )

        team_rate = st.number_input(
            "Team Rate ($/hr)",
            min_value=50.0,
            max_value=10000.0,
            value=225.0,
            step=25.0,
            key=f"{prefix}_team_rate"
        )

    with c2:

        helicopters = st.number_input(
            "Helicopters",
            min_value=0,
            max_value=100,
            value=2,
            key=f"{prefix}_heli"
        )

        heli_rate = st.number_input(
            "Helicopter Rate ($/hr)",
            min_value=1000.0,
            max_value=50000.0,
            value=6500.0,
            step=500.0,
            key=f"{prefix}_heli_rate"
        )

    with c3:

        trucks = st.number_input(
            "Truck Rolls",
            min_value=0,
            max_value=10000,
            value=150,
            key=f"{prefix}_trucks"
        )

        truck_cost = st.number_input(
            "Truck Roll Cost",
            min_value=50.0,
            max_value=10000.0,
            value=650.0,
            step=50.0,
            key=f"{prefix}_truck_cost"
        )

    with c4:

        gis_hours = st.number_input(
            "GIS Hours",
            min_value=1,
            max_value=10000,
            value=140,
            key=f"{prefix}_gis_hours"
        )

        gis_rate = st.number_input(
            "GIS Rate ($/hr)",
            min_value=50.0,
            max_value=1000.0,
            value=185.0,
            step=10.0,
            key=f"{prefix}_gis_rate"
        )

    return {
        "teams": teams,
        "team_rate": team_rate,
        "helicopters": helicopters,
        "heli_rate": heli_rate,
        "trucks": trucks,
        "truck_cost": truck_cost,
        "gis_hours": gis_hours,
        "gis_rate": gis_rate
    }

# =========================================================
# CALCULATION ENGINE
# =========================================================

def calculate(data):

    # -----------------------------
    # MANUAL COSTS
    # -----------------------------

    labor = (
        data["teams"]
        * 40
        * data["team_rate"]
    )

    aviation = (
        data["helicopters"]
        * 30
        * data["heli_rate"]
    )

    logistics = (
        data["trucks"]
        * data["truck_cost"]
    )

    gis = (
        data["gis_hours"]
        * data["gis_rate"]
    )

    manual_total = (
        labor
        + aviation
        + logistics
        + gis
    )

    # -----------------------------
    # OPTIMIZED COSTS
    # -----------------------------

    optimized_labor = (
        labor * (1 - labor_reduction)
    )

    optimized_aviation = (
        aviation * (1 - aviation_reduction)
    )

    optimized_logistics = (
        logistics * (1 - logistics_reduction)
    )

    optimized_gis = (
        gis * (1 - gis_reduction)
    )

    optimized_total = (
        optimized_labor
        + optimized_aviation
        + optimized_logistics
        + optimized_gis
    )

    savings = (
        manual_total
        - optimized_total
    )

    if subscription > 0:
        roi = (
            (
                (savings * annual_events)
                - subscription
            )
            / subscription
        ) * 100
    else:
        roi = 0

    breakdown_manual = {
        "Labor": labor,
        "Aviation": aviation,
        "Logistics": logistics,
        "GIS": gis
    }

    breakdown_optimized = {
        "Labor": optimized_labor,
        "Aviation": optimized_aviation,
        "Logistics": optimized_logistics,
        "GIS": optimized_gis
    }

    return {
        "manual_total": manual_total,
        "optimized_total": optimized_total,
        "savings": savings,
        "roi": roi,
        "manual_breakdown": breakdown_manual,
        "optimized_breakdown": breakdown_optimized
    }

# =========================================================
# TABS
# =========================================================

tabs = st.tabs([
    "LOCAL COUNCIL",
    "EMERGENCY SERVICES",
    "UTILITIES"
])

results = []

for idx, tab in enumerate(tabs):

    with tab:

        st.markdown("### Operational Inputs")

        data = vertical_inputs(f"vertical_{idx}")

        result = calculate(data)

        results.append(result)

        # =================================================
        # KPI CARDS
        # =================================================

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
<div class="metric-card">

    <div class="label">
        Per Event Savings
    </div>

    <div class="big-number">
        {currency_symbol}{result['savings']:,.0f}
    </div>

</div>
""",
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
<div class="metric-card">

    <div class="label">
        Estimated ROI
    </div>

    <div class="big-number">
        {result['roi']:.0f}%
    </div>

</div>
""",
                unsafe_allow_html=True
            )

        with c3:

            if result['savings'] > 0:
                payback = (
                    subscription
                    / result['savings']
                )
            else:
                payback = 0

            st.markdown(
                f"""
<div class="metric-card">

    <div class="label">
        Payback Period
    </div>

    <div class="big-number">
        {payback:.1f} Events
    </div>

</div>
""",
                unsafe_allow_html=True
            )

        st.markdown("")

        # =================================================
        # CHART
        # =================================================

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="Manual",
                x=list(result["manual_breakdown"].keys()),
                y=list(result["manual_breakdown"].values())
            )
        )

        fig.add_trace(
            go.Bar(
                name="ICEYE Optimized",
                x=list(result["optimized_breakdown"].keys()),
                y=list(result["optimized_breakdown"].values())
            )
        )

        fig.update_layout(
            height=420,
            barmode="group",
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            font_color=TEXT,
            margin=dict(
                l=0,
                r=0,
                t=30,
                b=0
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        fig.update_xaxes(
            showgrid=False,
            color="#CBD5E1"
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            color="#CBD5E1"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"chart_{idx}"
        )

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

manual_annual = (
    sum(r["manual_total"] for r in results)
    * annual_events
)

optimized_annual = (
    (
        sum(r["optimized_total"] for r in results)
        * annual_events
    )
    + subscription
)

net_dividend = (
    manual_annual
    - optimized_annual
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="hero">

    <div class="label">
        Net Annual Operational Dividend
    </div>

    <div class="hero-title">
        {currency_symbol}{net_dividend:,.0f}
    </div>

    <div class="hero-sub">
        Including subscription licensing and operational optimization
    </div>

</div>
""",
    unsafe_allow_html=True,
)
