import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ICEYE Strategic ROI",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# DESIGN SYSTEM
# ---------------------------------------------------

BG = "#060B14"
CARD = "#111827"
CARD_2 = "#0F172A"

PRIMARY = "#38BDF8"
SUCCESS = "#22C55E"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
BORDER = "rgba(255,255,255,0.06)"

st.markdown(f"""
<style>

html, body, [class*="css"] {{
    font-family: Inter, sans-serif;
}}

.stApp {{
    background: linear-gradient(180deg, #020617 0%, #0B1120 100%);
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    background: rgba(15,23,42,0.95);
    border-right: 1px solid {BORDER};
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

.metric-card {{
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}}

.hero {{
    padding: 40px;
    border-radius: 28px;
    background:
        radial-gradient(circle at top left, rgba(56,189,248,0.25), transparent 30%),
        linear-gradient(135deg, #0F172A 0%, #020617 100%);
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 28px;
}}

.hero-title {{
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
}}

.hero-sub {{
    color: {MUTED};
    font-size: 1.1rem;
    margin-top: 12px;
}}

.label {{
    color: {MUTED};
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 1px;
}}

.big-number {{
    font-size: 3rem;
    font-weight: 800;
}}

div[data-baseweb="input"] {{
    background: rgba(255,255,255,0.03);
}}

.stTabs [data-baseweb="tab"] {{
    font-size: 1rem;
    font-weight: 600;
}}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("## Strategic Inputs")

    currency = st.selectbox(
        "Currency",
        ["USD", "AUD", "EUR", "NZD"]
    )

    annual_events = st.slider(
        "Annual Events",
        1,
        20,
        4
    )

    subscription = st.number_input(
        "Annual Platform Cost",
        value=385000,
        step=10000
    )

    st.markdown("---")

    st.markdown("### Operational Efficiency")

    labor_reduction = st.slider(
        "Labor Reduction %",
        0,
        100,
        80
    ) / 100

    logistics_reduction = st.slider(
        "Truck Roll Reduction %",
        0,
        100,
        85
    ) / 100

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(f"""
<div class="hero">
    <div class="hero-title">
        Strategic ROI & Operational Impact
    </div>

    <div class="hero-sub">
        Satellite-enabled disaster response optimization modeling
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUTS
# ---------------------------------------------------

def vertical_inputs(prefix):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        teams = st.number_input(
            "Field Teams",
            1,
            100,
            12,
            key=f"{prefix}_teams"
        )

        team_rate = st.number_input(
            "Team Rate",
            50,
            10000,
            225,
            key=f"{prefix}_teamrate"
        )

    with c2:

        helicopters = st.number_input(
            "Helicopters",
            0,
            20,
            2,
            key=f"{prefix}_heli"
        )

        heli_rate = st.number_input(
            "Heli Hourly Rate",
            1000,
            20000,
            6500,
            key=f"{prefix}_helirate"
        )

    with c3:

        trucks = st.number_input(
            "Truck Rolls",
            0,
            5000,
            150,
            key=f"{prefix}_truck"
        )

        truck_cost = st.number_input(
            "Cost Per Truck Roll",
            50,
            10000,
            650,
            key=f"{prefix}_truckcost"
        )

    with c4:

        gis_hours = st.number_input(
            "GIS Hours",
            1,
            5000,
            140,
            key=f"{prefix}_gis"
        )

        gis_rate = st.number_input(
            "GIS Hourly Rate",
            50,
            1000,
            185,
            key=f"{prefix}_gisrate"
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

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------

def calculate(data):

    labor = data["teams"] * 40 * data["team_rate"]

    aviation = (
        data["helicopters"]
        * 30
        * data["heli_rate"]
    )

    logistics = (
        data["trucks"]
        * data["truck_cost"]
    )

    intelligence = (
        data["gis_hours"]
        * data["gis_rate"]
    )

    manual_total = (
        labor
        + aviation
        + logistics
        + intelligence
    )

    optimized_total = (
        labor * (1 - labor_reduction)
        + aviation * 0.20
        + logistics * (1 - logistics_reduction)
        + intelligence * 0.08
    )

    savings = manual_total - optimized_total

    roi = (
        (savings * annual_events - subscription)
        / subscription
    ) * 100

    return {
        "manual": manual_total,
        "optimized": optimized_total,
        "savings": savings,
        "roi": roi,
        "breakdown": {
            "Labor": labor,
            "Aviation": aviation,
            "Logistics": logistics,
            "GIS": intelligence
        }
    }

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tabs = st.tabs([
    "Local Council",
    "Emergency Services",
    "Utilities"
])

results = []

for idx, tab in enumerate(tabs):

    with tab:

        data = vertical_inputs(f"v{idx}")

        result = calculate(data)

        results.append(result)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Per Event Savings</div>
                <div class="big-number">
                    ${result['savings']:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Estimated ROI</div>
                <div class="big-number">
                    {result['roi']:.0f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            payback = subscription / max(result['savings'], 1)

            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Payback Period</div>
                <div class="big-number">
                    {payback:.1f} Events
                </div>
            </div>
            """, unsafe_allow_html=True)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name="Manual",
            x=list(result["breakdown"].keys()),
            y=list(result["breakdown"].values())
        ))

        fig.add_trace(go.Bar(
            name="ICEYE Optimized",
            x=list(result["breakdown"].keys()),
            y=[v * 0.2 for v in result["breakdown"].values()]
        ))

        fig.update_layout(
            height=420,
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=TEXT,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------------------
# EXEC SUMMARY
# ---------------------------------------------------

manual_annual = sum(r["manual"] for r in results) * annual_events
optimized_annual = (
    sum(r["optimized"] for r in results)
    * annual_events
) + subscription

net = manual_annual - optimized_annual

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">

    <div class="label">
        Net Annual Operational Dividend
    </div>

    <div class="hero-title">
        ${net:,.0f}
    </div>

    <div class="hero-sub">
        Including platform licensing and operational optimization
    </div>

</div>
""", unsafe_allow_html=True)
