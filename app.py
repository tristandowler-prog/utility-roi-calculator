import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ICEYE Strategic ROI: Precision Response",
    page_icon="▲",
    layout="wide"
)

# =========================================================
# THEME & CSS
# =========================================================
BG, CARD, BORDER, TEXT, MUTED = "#0B1220", "#111827", "#1E293B", "#F8FAFC", "#94A3B8"
PRIMARY, SUCCESS, WARNING = "#38BDF8", "#22C55E", "#F59E0B"

st.markdown(f"""
<style>
html, body, .stApp {{ background-color: {BG}; color: {TEXT}; font-family: Inter, sans-serif; }}
.block-container {{ padding-top: 1.5rem; max-width: 1500px; }}
div[data-testid="stMetric"] {{ background-color: {CARD}; border: 1px solid {BORDER}; padding: 15px; border-radius: 12px; }}
section[data-testid="stSidebar"] {{ background-color: #0F172A; border-right: 1px solid {BORDER}; }}
.header-box {{ padding: 20px; background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px; margin-bottom: 20px; }}
hr {{ border: 0; border-top: 1px solid {BORDER}; margin: 20px 0; }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - GLOBAL SETTINGS
# =========================================================
with st.sidebar:
    st.title("Global Parameters")
    currency = st.selectbox("Currency", ["USD", "AUD", "EUR", "GBP"])
    sym = {"USD": "$", "AUD": "$", "EUR": "€", "GBP": "£"}[currency]
    annual_events = st.slider("Major Events Per Year", 1, 20, 4)
    platform_cost = st.number_input("Annual ICEYE Subscription", value=385000.0, step=10000.0)
    st.divider()
    st.markdown(f"**Annual Fixed Costs:** {sym}{platform_cost:,.0f}")

# =========================================================
# INPUT ENGINE
# =========================================================
def input_column(title, prefix, defaults, color):
    st.markdown(f"### :{color}[{title}]")
    with st.container():
        st.markdown("#### 👥 Field Personnel")
        teams = st.number_input("Field Teams", value=defaults['teams'], key=f"{prefix}_t")
        ppp = st.number_input("People Per Team", value=defaults['ppp'], key=f"{prefix}_p")
        hrs = st.number_input("Total Hours (Per Person)", value=defaults['hrs'], key=f"{prefix}_h")
        wage = st.number_input("Avg Wage ($/hr)", value=defaults['wage'], key=f"{prefix}_w")
        
        st.markdown("---")
        st.markdown("#### 🚁 Aviation & Logistics")
        helis = st.number_input("Helicopters", value=defaults['heli'], key=f"{prefix}_he")
        h_rate = st.number_input("Heli Rate ($/hr)", value=defaults['h_rate'], key=f"{prefix}_hr")
        h_hrs = st.number_input("Heli Hours (Total)", value=defaults['h_hrs'], key=f"{prefix}_hh")
        trucks = st.number_input("Truck Rolls", value=defaults['trucks'], key=f"{prefix}_tr")
        t_cost = st.number_input("Cost Per Roll", value=defaults['t_cost'], key=f"{prefix}_tc")
        # Direct Waste Slider in the column
        waste = st.slider("Deployment Waste % (Inefficiency)", 0, 100, defaults['waste'], key=f"{prefix}_ws") / 100

        st.markdown("---")
        st.markdown("#### 💻 Intelligence & Analysis")
        gis_hrs = st.number_input("Manual GIS / Analysis Hours", value=defaults['gis'], key=f"{prefix}_gh")
        gis_rate = st.number_input("Analyst Rate ($/hr)", value=185.0, key=f"{prefix}_gr")

    # Calculations
    labor_cost = teams * ppp * hrs * wage
    aviation_cost = helis * h_rate * h_hrs
    # Logistics includes the "Waste Factor" as a multiplier on rolls
    logistics_cost = (trucks * t_cost) * (1 + waste)
    intel_cost = gis_hrs * gis_rate
    total = labor_cost + aviation_cost + logistics_cost + intel_cost
    
    return {
        "total": total, "labor": labor_cost, "aviation": aviation_cost, 
        "logistics": logistics_cost, "intel": intel_cost
    }

# =========================================================
# MAIN INTERFACE
# =========================================================
st.title("Strategic ROI: Precision vs. Broad Search")
st.markdown("Quantify the impact of moving from **unverified broad deployments** to **SAR-verified targeted response.**")

col_left, col_right = st.columns(2)

with col_left:
    current = input_column("Current Method: Broad Search", "cur", {
        'teams': 15, 'ppp': 3, 'hrs': 80, 'wage': 75.0,
        'heli': 3, 'h_rate': 6500.0, 'h_hrs': 45,
        'trucks': 200, 't_cost': 650.0, 'waste': 35, 'gis': 160
    }, "grey")

with col_right:
    targeted = input_column("ICEYE: Targeted Response", "ice", {
        'teams': 10, 'ppp': 3, 'hrs': 42, 'wage': 75.0,
        'heli': 1, 'h_rate': 6500.0, 'h_hrs': 8,
        'trucks': 110, 't_cost': 650.0, 'waste': 5, 'gis': 18
    }, "blue")

# =========================================================
# METRICS & VISUALS
# =========================================================
st.markdown("---")
event_savings = current['total'] - targeted['total']
annual_gross_savings = event_savings * annual_events
annual_net_savings = annual_gross_savings - platform_cost
roi = (annual_net_savings / platform_cost) * 100 if platform_cost > 0 else 0

m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Current Cost / Event", f"{sym}{current['total']:,.0f}")
with m2: st.metric("Targeted Cost / Event", f"{sym}{targeted['total']:,.0f}")
with m3: st.metric("Net Annual Savings", f"{sym}{annual_net_savings:,.0f}", f"{sym}{event_savings:,.0f} per event")
with m4: st.metric("Strategic ROI", f"{roi:.0f}%")

# Comparison Chart
fig = go.Figure()
categories = ['Field Labor', 'Aviation', 'Logistics (incl. Waste)', 'Intelligence']
fig.add_trace(go.Bar(name='Current (Broad)', x=categories, 
                     y=[current['labor'], current['aviation'], current['logistics'], current['intel']], 
                     marker_color='#475569'))
fig.add_trace(go.Bar(name='ICEYE (Targeted)', x=categories, 
                     y=[targeted['labor'], targeted['aviation'], targeted['logistics'], targeted['intel']], 
                     marker_color=PRIMARY))

fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                  font=dict(color=TEXT), height=450, margin=dict(t=10, b=10),
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# =========================================================
# AUDIT LOGIC
# =========================================================
with st.expander("🔍 FINANCIAL METHODOLOGY & LOGIC"):
    st.markdown(f"""
    ### 1. The "Ghost Roll" Logic (Logistics)
    The **Deployment Waste %** slider accounts for the operational friction of sending resources into unknown zones. 
    *   **Baseline:** High waste represents teams sent to roads that are already cleared or locations that turn out to be dry.
    *   **Targeted:** Low waste reflects that SAR imagery has confirmed water-on-ground, meaning every "roll" is a high-confidence deployment.

    ### 2. Time-to-Actionable Insight
    Labor costs are primarily driven by the **Total Hours** field. In a targeted response, hours are reduced not because the work is easier, but because the **Discovery Phase** (finding where the damage is) is eliminated.

    ### 3. Calculation Breakdown
    *   **Event Delta:** {sym}{current['total']:,.2f} - {sym}{targeted['total']:,.2f} = **{sym}{event_savings:,.2f}**
    *   **Annual Operating Margin:** ({sym}{event_savings:,.2f} × {annual_events}) - {sym}{platform_cost:,.2f} = **{sym}{annual_net_savings:,.2f}**
    """)
