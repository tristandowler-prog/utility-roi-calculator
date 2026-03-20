import streamlit as st
import numpy as np
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Flood Intelligence | Command Platform", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
.stApp {
    background: #0A1623;
    color: #F1F5F9;
}
.metric {
    padding: 20px;
    border-left: 4px solid #00D1FF;
    background: rgba(255,255,255,0.03);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Scenario Builder")

    scenario = st.selectbox("Event Type", [
        "Urban Flood",
        "Regional Storm",
        "Severe Black Swan"
    ])

    latency = st.select_slider("Satellite Latency", ["6h","12h","24h","48h"], value="12h")

    total_assets = st.number_input("Total Network Assets", value=1200)
    inundation = st.slider("% Assets Impacted", 1, 100, 25)

    crew_cost = st.number_input("Crew Dispatch Cost ($)", value=850)
    events_per_year = st.slider("Events / Year", 1, 10, 4)

# --- SCENARIO LOGIC ---
scenario_multiplier = {
    "Urban Flood": 1.0,
    "Regional Storm": 1.4,
    "Severe Black Swan": 2.2
}[scenario]

latency_factor = {"6h":1.0,"12h":0.8,"24h":0.5,"48h":0.2}[latency]

exposed_assets = int(total_assets * (inundation/100))
blind_dispatch_rate = (1 - latency_factor) * 100

# --- DECISION ENGINE ---
base_decision_delay = 40
improved_decision_time = base_decision_delay * latency_factor

time_saved = base_decision_delay - improved_decision_time

blind_dispatches = int(exposed_assets * (blind_dispatch_rate/100))

cost_blind_dispatch = blind_dispatches * crew_cost * scenario_multiplier

# --- ROI SIMULATION ---
simulations = np.random.normal(loc=events_per_year, scale=1.2, size=500)
annual_savings_sim = simulations * cost_blind_dispatch

p50 = np.percentile(annual_savings_sim, 50)
p80 = np.percentile(annual_savings_sim, 80)

# --- HEADER ---
st.title("Flood Intelligence Command Platform")
st.subheader("From Reactive Response → Real-Time Decision Advantage")

# --- KPI ROW ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='metric'><b>Network Visibility</b><br><h2>{latency_factor*100:.0f}%</h2></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='metric'><b>Blind Dispatch Rate</b><br><h2>{blind_dispatch_rate:.0f}%</h2></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='metric'><b>Time to Decision</b><br><h2>{improved_decision_time:.1f} min</h2></div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='metric'><b>Assets Impacted</b><br><h2>{exposed_assets}</h2></div>", unsafe_allow_html=True)

# --- NARRATIVE OUTPUT ---
st.success(f"""
With {latency} satellite latency, your control room operates at {latency_factor*100:.0f}% visibility.

This reduces blind dispatches by {blind_dispatch_rate:.0f}% and accelerates first decision-making by {time_saved:.1f} minutes.

Estimated avoided cost per event: ${cost_blind_dispatch:,.0f}
""")

# --- SIMULATION OUTPUT ---
st.markdown("## 📊 Annual Impact (Simulated)")

st.write(f"**Median Annual Savings:** ${p50:,.0f}")
st.write(f"**80th Percentile Upside:** ${p80:,.0f}")

# --- CHART ---
chart_df = pd.DataFrame({"Simulated Savings": annual_savings_sim})
st.bar_chart(chart_df)

# --- STRATEGIC MESSAGE ---
st.markdown("---")
st.markdown("## 🧠 What This Means for Operations")

st.info("""
Without real-time flood intelligence:
- Crews are dispatched blind
- Restoration is delayed
- Regulatory exposure increases

With this platform:
- You see impacted assets immediately
- You send the right crew, first time
- You restore faster and protect revenue
""")

# --- CTA ---
st.button("Generate Executive Brief")
