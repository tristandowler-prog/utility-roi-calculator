import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ICEYE Strategic ROI",
    page_icon="▲",
    layout="wide"
)

# =========================================================
# THEME & CSS
# =========================================================

BG = "#0B1220"
CARD = "#111827"
BORDER = "#1E293B"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
PRIMARY = "#38BDF8"
SUCCESS = "#22C55E"

st.markdown(
    f"""
<style>
html, body, .stApp {{ background-color: {BG}; color: {TEXT}; font-family: Inter, sans-serif; }}
.block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1450px; }}
h1, h2, h3 {{ color: {TEXT}; }}
div[data-testid="stMetric"] {{ background-color: {CARD}; border: 1px solid {BORDER}; padding: 20px; border-radius: 14px; }}
div[data-testid="stMetricLabel"] {{ color: {MUTED}; }}
div[data-testid="stMetricValue"] {{ color: white; }}
section[data-testid="stSidebar"] {{ background-color: #0F172A; border-right: 1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{ font-size: 0.95rem; font-weight: 600; }}
</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("Strategic Inputs")
    currency = st.selectbox("Reporting Currency", ["USD", "AUD", "EUR", "NZD"])
    currency_symbol = {"USD": "$", "AUD": "$", "EUR": "€", "NZD": "$"}[currency]
    annual_events = st.slider("Annual Major Events", min_value=1, max_value=20, value=4)
    subscription = st.number_input("Annual Platform Cost", min_value=0.0, value=385000.0, step=10000.0)
    st.divider()
    st.subheader("Operational Assumptions")
    labor_reduction = st.slider("Labor Reduction %", 0, 100, 80) / 100
    aviation_reduction = st.slider("Aviation Reduction %", 0, 100, 80) / 100
    logistics_reduction = st.slider("Truck Roll Reduction %", 0, 100, 85) / 100
    gis_reduction = st.slider("GIS Automation %", 0, 100, 92) / 100

# =========================================================
# HEADER
# =========================================================

st.title("Strategic ROI & Operational Impact")
st.markdown(f'<div style="padding-bottom: 24px; color: {MUTED}; font-size: 1.05rem;">Satellite-enabled disaster response optimization modeling</div>', unsafe_allow_html=True)

# =========================================================
# INPUT COMPONENT
# =========================================================

def vertical_inputs(prefix):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        teams = st.number_input("Field Teams", min_value=1, value=12, key=f"{prefix}_teams")
        people_per_team = st.number_input("People Per Team", min_value=1, value=3, key=f"{prefix}_p_per_t")
        team_hours = st.number_input("Hours Per Person", min_value=1, value=40, key=f"{prefix}_team_hours")
        avg_wage = st.number_input("Avg Wage ($/hr)", min_value=10.0, value=75.0, key=f"{prefix}_wage")
    with c2:
        helicopters = st.number_input("Helicopters", min_value=0, value=2, key=f"{prefix}_heli")
        heli_rate = st.number_input("Heli Rate ($/hr)", min_value=1000.0, value=6500.0, key=f"{prefix}_heli_rate")
        heli_hours = st.number_input("Heli Hours (Per Heli)", min_value=0, value=30, key=f"{prefix}_heli_hours")
    with c3:
        trucks = st.number_input("Truck Rolls", min_value=0, value=150, key=f"{prefix}_trucks")
        truck_cost = st.number_input("Truck Roll Cost", min_value=50.0, value=650.0, key=f"{prefix}_truck_cost")
    with c4:
        gis_hours = st.number_input("GIS Hours", min_value=1, value=140, key=f"{prefix}_gis_hours")
        gis_rate = st.number_input("GIS Rate ($/hr)", min_value=50.0, value=185.0, key=f"{prefix}_gis_rate")

    return {
        "teams": teams, "people_per_team": people_per_team, "team_hours": team_hours, "avg_wage": avg_wage,
        "helicopters": helicopters, "heli_rate": heli_rate, "heli_hours": heli_hours,
        "trucks": trucks, "truck_cost": truck_cost, "gis_hours": gis_hours, "gis_rate": gis_rate
    }

# =========================================================
# CALCULATIONS
# =========================================================

def calculate(data):
    # Updated labor formula to use user-defined team_hours instead of hardcoded 40
    team_hourly_burden = data["people_per_team"] * data["avg_wage"]
    labor = (data["teams"] * data["team_hours"] * team_hourly_burden)
    
    aviation = (data["helicopters"] * data["heli_hours"] * data["heli_rate"])
    logistics = (data["trucks"] * data["truck_cost"])
    gis = (data["gis_hours"] * data["gis_rate"])
    manual_total = labor + aviation + logistics + gis

    optimized_labor = labor * (1 - labor_reduction)
    optimized_aviation = aviation * (1 - aviation_reduction)
    optimized_logistics = logistics * (1 - logistics_reduction)
    optimized_gis = gis * (1 - gis_reduction)
    optimized_total = optimized_labor + optimized_aviation + optimized_logistics + optimized_gis

    savings = manual_total - optimized_total
    roi = (((savings * annual_events) - subscription) / subscription) * 100 if subscription > 0 else 0

    return {
        "manual_total": manual_total, "optimized_total": optimized_total, "savings": savings, "roi": roi,
        "manual_breakdown": {"Labor": labor, "Aviation": aviation, "Logistics": logistics, "GIS": gis},
        "optimized_breakdown": {"Labor": optimized_labor, "Aviation": optimized_aviation, "Logistics": optimized_logistics, "GIS": optimized_gis}
    }

# =========================================================
# TABS & VISUALS
# =========================================================

tabs = st.tabs(["EMERGENCY SERVICES"])
results = []
for idx, tab in enumerate(tabs):
    with tab:
        st.subheader("Operational Inputs")
        data = vertical_inputs(f"vertical_{idx}")
        result = calculate(data)
        results.append(result)
        
        st.markdown("")
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Per Event Savings", f"{currency_symbol}{result['savings']:,.0f}")
        with m2: st.metric("Estimated ROI", f"{result['roi']:.0f}%")
        with m3:
            payback = subscription / result["savings"] if result["savings"] > 0 else 0
            st.metric("Payback Period", f"{payback:.1f} Events")

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Manual", x=list(result["manual_breakdown"].keys()), y=list(result["manual_breakdown"].values()), marker_color="#475569"))
        fig.add_trace(go.Bar(name="Optimized", x=list(result["optimized_breakdown"].keys()), y=list(result["optimized_breakdown"].values()), marker_color=PRIMARY))
        fig.update_layout(height=420, barmode="group", paper_bgcolor=BG, plot_bgcolor=BG, font=dict(color=TEXT, size=13), margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

manual_annual = sum(r["manual_total"] for r in results) * annual_events
optimized_annual = (sum(r["optimized_total"] for r in results) * annual_events) + subscription
net_dividend = manual_annual - optimized_annual

st.divider()
summary_1, summary_2, summary_3 = st.columns(3)
with summary_1: st.metric("Annual Manual Cost", f"{currency_symbol}{manual_annual:,.0f}")
with summary_2: st.metric("Annual Optimized Cost", f"{currency_symbol}{optimized_annual:,.0f}")
with summary_3: st.metric("Net Annual Savings", f"{currency_symbol}{net_dividend:,.0f}")

st.markdown(f"""
<div style="padding: 28px; background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 16px;">
    <div style="font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; color: {MUTED}; margin-bottom: 12px;">Executive Summary</div>
    <div style="font-size: 2.2rem; font-weight: 700; color: white; margin-bottom: 10px;">{currency_symbol}{net_dividend:,.0f}</div>
    <div style="color: {MUTED}; font-size: 1rem;">Estimated annual operational savings including subscription costs and deployment optimization efficiencies.</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# UPDATED: METHODOLOGY BREAKDOWN
# =========================================================

st.markdown("")
with st.expander("🔍 FINANCIAL METHODOLOGY & AUDIT LOGIC"):
    st.markdown(f"""
    ### 1. Baseline Expenditure Model (Status Quo)
    The manual cost baseline is established through a four-pillar resource aggregation model. This represents the "Gross Operational Burn" per catastrophic event prior to SAR-integrated intelligence.
    
    *   **Field Labor Liability:** Calculated as $L = T \\times Hrs \\times (P \\times W)$, where $T$ is the number of teams, $Hrs$ is the total hours worked per person, $P$ is personnel per team, and $W$ is the hourly wage. 
    *   **Aviation Asset Burn:** Calculated as $A = H \\times Hrs_{{heli}} \\times R$, where $H$ is total helicopters, $Hrs_{{heli}}$ is mission duration, and $R$ is wet-lease hourly rate.
    *   **Logistics Overhead:** Calculated as $Log = TK \\times TC$, accounting for fuel, maintenance, and administrative cost per physical truck roll.
    *   **Intelligence Latency:** Calculated as $I = G_h \\times G_r$, representing manual GIS processing time and analyst billables.
    
    ### 2. ICEYE Efficiency Framework (Optimized State)
    The optimized state applies reduction coefficients to the baseline, derived from the accelerated "Time-to-Insight" provided by ICEYE SAR constellations.
    
    *   **Tactical Deployment Gain:** Satellite intelligence allows for the immediate "clearing" of non-impacted zones, reducing **Labor** and **Logistics** requirements by specifically targeting high-risk areas.
    *   **Aviation Optimization:** High-frequency SAR imaging reduces the need for broad-area aerial reconnaissance, pivoting aviation assets from "Discovery" to "Tactical Rescue."
    *   **Intelligence Automation:** ICEYE data-feeds automate flood extent mapping, reducing manual GIS analyst hours by up to 92%.
    
    ### 3. ROI & Net Dividend Calculation
    The Net Annual Strategic Dividend is the final auditable value, calculated as:
    $$Net Dividend = [(\\sum Manual Costs - \\sum Optimized Costs) \\times Annual Events] - Annual Subscription$$
    
    *This framework ensures that the projected savings are not merely theoretical, but represent a direct reduction in tangible operational expenditure.*
    """)
