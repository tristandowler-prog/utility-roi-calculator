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
    st.info("Adjust the columns below to compare your 'Broad Search' baseline against an 'ICEYE Targeted' response.")

# =========================================================
# INPUT ENGINE
# =========================================================
def input_column(title, prefix, defaults):
    st.subheader(title)
    with st.container():
        st.markdown("**Field Personnel**")
        teams = st.number_input("Field Teams", value=defaults['teams'], key=f"{prefix}_t")
        ppp = st.number_input("People Per Team", value=defaults['ppp'], key=f"{prefix}_p")
        hrs = st.number_input("Hours Worked (Per Person)", value=defaults['hrs'], key=f"{prefix}_h")
        wage = st.number_input("Avg Wage ($/hr)", value=defaults['wage'], key=f"{prefix}_w")
        
        st.divider()
        st.markdown("**Aviation & Logistics**")
        helis = st.number_input("Helicopters", value=defaults['heli'], key=f"{prefix}_he")
        h_rate = st.number_input("Heli Rate ($/hr)", value=defaults['h_rate'], key=f"{prefix}_hr")
        h_hrs = st.number_input("Heli Hours (Total)", value=defaults['h_hrs'], key=f"{prefix}_hh")
        trucks = st.number_input("Truck Rolls", value=defaults['trucks'], key=f"{prefix}_tr")
        t_cost = st.number_input("Cost Per Roll", value=defaults['t_cost'], key=f"{prefix}_tc")
        waste = st.slider("Deployment Waste %", 0, 100, defaults['waste'], key=f"{prefix}_ws") / 100

        st.divider()
        st.markdown("**Intelligence & Analysis**")
        gis_hrs = st.number_input("GIS / Manual Analysis Hours", value=defaults['gis'], key=f"{prefix}_gh")
        gis_rate = st.number_input("GIS Analyst Rate ($/hr)", value=185.0, key=f"{prefix}_gr")

    # Calculations
    labor_cost = teams * ppp * hrs * wage
    aviation_cost = helis * h_rate * h_hrs
    logistics_cost = (trucks * t_cost) * (1 + waste)
    intel_cost = gis_hrs * gis_rate
    total = labor_cost + aviation_cost + logistics_cost + intel_cost
    
    return {
        "total": total, "labor": labor_cost, "aviation": aviation_cost, 
        "logistics": logistics_cost, "intel": intel_cost, "waste_val": (trucks * t_cost) * waste
    }

# =========================================================
# MAIN INTERFACE
# =========================================================
st.title("Operational ROI: Targeted Response Modeling")
st.markdown("Compare the cost of **Broad-Area Search** (Status Quo) vs. **Precision-Targeted Response** (ICEYE Enabled).")

col1, col2 = st.columns(2)

with col1:
    # Baseline Defaults
    current = input_column("Current Method (Broad Search)", "cur", {
        'teams': 15, 'ppp': 3, 'hrs': 80, 'wage': 75.0,
        'heli': 3, 'h_rate': 6500.0, 'h_hrs': 45,
        'trucks': 200, 't_cost': 650.0, 'waste': 35, 'gis': 160
    })

with col2:
    # Optimized Defaults
    targeted = input_column("ICEYE Targeted Response", "ice", {
        'teams': 10, 'ppp': 3, 'hrs': 40, 'wage': 75.0,
        'heli': 1, 'h_rate': 6500.0, 'h_hrs': 10,
        'trucks': 120, 't_cost': 650.0, 'waste': 5, 'gis': 20
    })

# =========================================================
# RESULTS & VISUALS
# =========================================================
st.divider()
event_savings = current['total'] - targeted['total']
annual_savings = (event_savings * annual_events) - platform_cost
roi = (annual_savings / platform_cost) * 100 if platform_cost > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Cost / Event", f"{sym}{current['total']:,.0f}")
m2.metric("Targeted Cost / Event", f"{sym}{targeted['total']:,.0f}")
m3.metric("Net Annual Savings", f"{sym}{annual_savings:,.0f}")
m4.metric("Strategic ROI", f"{roi:.0f}%")

# Charting the Delta
fig = go.Figure()
categories = ['Field Labor', 'Aviation', 'Logistics (incl. Waste)', 'Intelligence']
fig.add_trace(go.Bar(name='Current Method', x=categories, 
                     y=[current['labor'], current['aviation'], current['logistics'], current['intel']], marker_color='#475569'))
fig.add_trace(go.Bar(name='Targeted Response', x=categories, 
                     y=[targeted['labor'], targeted['aviation'], targeted['logistics'], targeted['intel']], marker_color=PRIMARY))

fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                  font=dict(color=TEXT), height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

# =========================================================
# METHODOLOGY
# =========================================================
with st.expander("🔍 HOW THIS MODEL CALCULATES TRUTH"):
    st.markdown(f"""
    ### 1. The Deployment Waste Factor
    In the **Current Method**, high "Deployment Waste" represents the cost of "Ghost Rolls"—sending trucks and teams to locations that are eventually cleared or found to be inaccessible. ICEYE reduces this by providing high-resolution SAR proof of impact before wheels turn.

    ### 2. The Intelligence Gap
    *   **Manual (Status Quo):** GIS hours reflect the time spent manually aggregating social media, drone feeds, and ground reports.
    *   **Targeted (ICEYE):** GIS hours are reduced by **{((current['intel']-targeted['intel'])/current['intel']*100) if current['intel']>0 else 0:.0f}%** due to automated flood-extent polygons.

    ### 3. Personnel Utilization
    Labor ROI isn't just about fewer people; it's about **Total Event Duration**. By knowing exactly where to go, teams complete remediation in fewer hours, reducing the total "Burn Duration" per event.

    **Calculated Annual Net Dividend:**
    $$ (({current['total']:,.0f} - {targeted['total']:,.0f}) \\times {annual_events}) - {platform_cost:,.0f} = {annual_savings:,.0f} $$
    """)
