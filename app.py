import streamlit as st

# --- 1. THE COMMAND CENTER UI ---
st.set_page_config(page_title="ICEYE | Precision ROI", layout="wide")
ICEYE_BLUE = "#39BBF0"
ICEYE_DARK = "#0B0C10"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {ICEYE_DARK}; color: #FFFFFF; font-family: 'Inter', sans-serif; }}
    .formula-card {{ background: #111827; border: 1px solid {ICEYE_BLUE}44; padding: 20px; border-radius: 8px; margin: 10px 0; }}
    .latency-tag {{ color: {ICEYE_BLUE}; font-weight: bold; border: 1px solid {ICEYE_BLUE}; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }}
    .math-text {{ font-family: 'Courier New', monospace; color: {ICEYE_BLUE}; font-size: 0.85rem; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE HARD COST SIDEBAR (UNIT RATES) ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=150)
    st.markdown("### 📊 UNIT COST BASELINE")
    
    with st.expander("🚁 AVIATION ASSETS", expanded=True):
        heli_hr = st.number_input("Heli (Twin) $/hr", value=6500)
        plane_hr = st.number_input("Fixed-Wing $/hr", value=2800)
        
    with st.expander("🚛 GROUND & ANALYST", expanded=True):
        crew_hr = st.number_input("Field Crew (Singular) $/hr", value=175)
        gis_hr = st.number_input("GIS Analyst $/hr", value=210)
    
    st.divider()
    iceye_sub = st.number_input("ICEYE Annual Subscription ($)", value=385000)

# --- 3. THE CALCULATOR ---
st.title("Strategic ROI: Temporal & Operational Advantage")

t1, t2, t3 = st.tabs(["🚨 PUBLIC SAFETY", "🏛️ LOCAL COUNCIL", "⚡ UTILITIES"])

# --- TAB 1: PUBLIC SAFETY (AERIAL DEPLOYMENT) ---
with t1:
    st.header("Public Safety: Aerial Reconnaissance")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Manual Aerial Discovery")
        heli_qty = st.number_input("Number of Helis Deployed", 1, 10, 2)
        heli_ops_hr = st.number_input("Total Flight Hrs (per Heli)", 5, 100, 30)
        plane_qty = st.number_input("Number of Planes Deployed", 1, 5, 1)
        plane_ops_hr = st.number_input("Total Flight Hrs (per Plane)", 5, 100, 20)
        
        manual_ps = (heli_qty * heli_ops_hr * heli_hr) + (plane_qty * plane_ops_hr * plane_hr)
        
        st.markdown(f"""<div class='formula-card'>
        <p class='math-text'>( {heli_qty} Heli * {heli_ops_hr}hr * ${heli_hr} ) + ( {plane_qty} Plane * {plane_ops_hr}hr * ${plane_hr} )</p>
        <h2 style='color:#FF4B4B'>${manual_ps:,.0f}</h2>
        <p style='font-size:0.8rem'>*Cost purely for discovery/observation flight time.</p></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 ICEYE Rapid Impact Data")
        st.markdown("<span class='latency-tag'>6-HOUR OBSERVED EXTENT</span>", unsafe_allow_html=True)
        # ICEYE data allows for "Sniper" heli deployments only for life-safety
        iceye_heli_recon = st.number_input("Tactical Heli Hrs (Post-SAR)", value=5)
        iceye_ps = (iceye_heli_recon * heli_hr)
        
        st.markdown(f"""<div class='formula-card'>
        <p class='math-text'>( {iceye_heli_recon} Tactical Hrs * ${heli_hr} )</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_ps:,.0f}</h2>
        <p style='font-size:0.8rem'>*Observation replaced by 6-hourly SAR extent monitoring.</p></div>""", unsafe_allow_html=True)

# --- TAB 2: COUNCIL (GIS LATENCY) ---
with t2:
    st.header("Council: GIS Data Processing")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Manual Data Synthesis")
        gis_analysts = st.number_input("GIS Team Size", 1, 10, 3)
        processing_days = st.slider("Days to produce Flood Map (Manual)", 1, 14, 5)
        # Manual digitizing from optical/heli footage
        manual_gis = (gis_analysts * 8 * processing_days * gis_hr)
        
        st.markdown(f"""<div class='formula-card'>
        <p class='math-text'>( {gis_analysts} Analysts * {processing_days*8} Working Hrs * ${gis_hr} )</p>
        <h2 style='color:#FF4B4B'>${manual_gis:,.0f}</h2>
        <p style='font-size:0.8rem'>*Includes time to clean, digitize, and verify non-standard data.</p></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 ICEYE Flood Insights")
        st.markdown("<span class='latency-tag'>24-HOUR DEPTH & EXTENT (READY-TO-USE)</span>", unsafe_allow_html=True)
        # ICEYE data plugs directly into GIS via API/GeoJSON
        integration_hrs = st.number_input("GIS Integration/QC Hrs", value=4)
        iceye_gis = (integration_hrs * gis_hr)
        
        st.markdown(f"""<div class='formula-card'>
        <p class='math-text'>( {integration_hrs} Data QC Hrs * ${gis_hr} )</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_gis:,.0f}</h2>
        <p style='font-size:0.8rem'>*Assumes ICEYE GeoJSON/Raster API ingestion (plug-and-play).</p></div>""", unsafe_allow_html=True)

# --- TAB 3: UTILITIES (FIELD DEPLOYMENT) ---
with t3:
    st.header("Utility: Field Force Optimization")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Blind Field Deployment")
        crew_qty = st.number_input("Number of Crews", 1, 50, 10)
        shift_len = st.number_input("Avg Shift Duration (Hrs)", 1, 14, 10)
        days_active = st.number_input("Deployment Duration (Days)", 1, 30, 7)
        manual_u = (crew_qty * shift_len * days_active * crew_hr)
        
        st.markdown(f"""<div class='formula-card'>
        <p class='math-text'>( {crew_qty} Crews * {shift_len}hrs * {days_active}days * ${crew_hr} )</p>
        <h2 style='color:#FF4B4B'>${manual_u:,.0f}</h2></div>""", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🟢 SAR-Informed Deployment")
        # Direct efficiency gain: knowing where NOT to go.
        efficiency_gain = st.slider("Field Force Optimization %", 10, 80, 50, help="Reduction in redundant 'checks' due to SAR clearance.")
        iceye_u = manual_u * (1 - (efficiency_gain/100))
        
        st.markdown(f"""<div class='formula-card'>
        <p class='math-text'>( Manual Cost ${manual_u:,.0f} ) * (1 - {efficiency_gain}%)</p>
        <h2 style='color:{ICEYE_BLUE}'>${iceye_u:,.0f}</h2></div>""", unsafe_allow_html=True)

# --- 4. THE CAPABILITY DIVIDEND ---
st.divider()
total_manual = (manual_ps + manual_gis + manual_u)
total_iceye = (iceye_ps + iceye_gis + iceye_u)
# Per event savings
event_gain = total_manual - total_iceye
# Annual logic
annual_gain = (event_gain * 2) - iceye_sub # Assuming 2 major events as standard

st.markdown(f"""
<div style="text-align: center; border: 1px solid {ICEYE_BLUE}; padding: 40px;">
    <p style="letter-spacing: 5px; color: {ICEYE_BLUE}; font-weight: 900;">NET EVENT OPERATIONAL SAVING</p>
    <h1 style="font-size: 5rem; margin: 0;">${event_gain:,.0f}</h1>
    <p style="color: #94A3B8;">ICEYE Rapid Impact (6h) & Insights (24h) eliminates the 'Search' cost from the budget.</p>
</div>
""", unsafe_allow_html=True)
