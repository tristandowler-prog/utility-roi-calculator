import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="ICEYE | Utility ROI Calculator", layout="wide")

def local_css():
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #003366; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #003366; color: white; }
        .report-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; }
        </style>
    """, unsafe_content_as_html=True)

local_css()

# --- 2. PDF GENERATION ENGINE ---
class ROI_PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "ICEYE Operational Impact Report", ln=True, align="C")
        self.line(10, 20, 200, 20)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Generated on {datetime.date.today()} - Confidential ROI Analysis", align="C")

def generate_pdf(data_dict):
    pdf = ROI_PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    for key, value in data_dict.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    
    return pdf.output()

# --- 3. SIDEBAR / GLOBAL INPUTS ---
with st.sidebar:
    st.image("https://www.iceye.com/hubfs/iceye-logo.svg", width=150) # Placeholder logo URL
    st.header("Global Parameters")
    events_pa = st.slider("Significant Weather Events / Year", 1, 20, 4)
    annual_sub = st.number_input("ICEYE Annual Subscription ($)", value=250000.0, step=10000.0)
    sar_latency = st.slider("ICEYE Data Latency (Hours)", 1, 24, 8)

# --- 4. INPUT COLUMNS ---
st.title("🛰️ Utility Recovery ROI Calculator")
st.markdown("Compare legacy reconnaissance workflows against ICEYE's SAR-enabled rapid response.")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🚁 Aviation Assets")
    heli_rate = st.number_input("Heli Hourly Rate ($)", value=3500.0)
    heli_hrs = st.number_input("Heli Flight Hrs/Event", value=8.0)
    heli_standby = st.number_input("Heli Daily Standby ($)", value=5000.0)
    drone_rate = st.number_input("Drone Hourly Rate ($)", value=250.0)
    drone_hrs = st.number_input("Drone Flight Hrs/Event", value=15.0)
    drone_standby = st.number_input("Drone Standby/Day ($)", value=1200.0)

with c2:
    st.subheader("🚛 Field Strike Teams")
    team_count = st.number_input("Number of Active Teams", value=6)
    team_daily_burn = st.number_input("Daily Team Operating Burn ($)", value=12500.0)
    cloud_wait_days = st.number_input("Blind Window (Days)", value=2.0, step=0.5)
    dry_run_penalty = st.number_input("Dry Run Penalty ($)", value=2800.0)
    dry_runs_per_event = st.number_input("Wasted Deployments / Event", value=10)

with c3:
    st.subheader("🖥️ GIS & Mapping")
    gis_staff_count = st.number_input("Number of GIS Staff", value=2)
    gis_hourly_rate = st.number_input("GIS Hourly Rate ($)", value=120.0)
    leg_processing_hrs = st.number_input("Legacy Manual Mapping (Hrs)", value=12.0)
    iceye_processing_hrs = st.number_input("ICEYE SAR Prep (Hrs)", value=2.0)

# --- 5. MATH ENGINE ---
# Legacy Totals
leg_air_event = (heli_rate * heli_hrs) + (heli_standby * cloud_wait_days) + \
                (drone_rate * drone_hrs) + (drone_standby * cloud_wait_days)
leg_gis_event = (gis_staff_count * gis_hourly_rate * leg_processing_hrs)
leg_field_waste_event = (team_count * team_daily_burn * cloud_wait_days) + (dry_runs_per_event * dry_run_penalty)
annual_legacy_total = (leg_air_event + leg_gis_event + leg_field_waste_event) * events_pa

# ICEYE Totals
iceye_gis_event = (gis_staff_count * gis_hourly_rate * iceye_processing_hrs)
iceye_field_waste_event = (team_count * team_daily_burn * (sar_latency / 24.0))
annual_iceye_total = ((iceye_gis_event + iceye_field_waste_event) * events_pa) + annual_sub

net_annual_recovery = annual_legacy_total - annual_iceye_total
gis_hours_saved = (leg_processing_hrs - iceye_processing_hrs) * events_pa

# --- 6. RESULTS & VISUALS ---
st.divider()
res_col1, res_col2 = st.columns([2, 1])

with res_col1:
    st.subheader("Strategic Annual Impact")
    r1, r2, r3 = st.columns(3)
    r1.metric("Net Operational Recovery", f"${net_annual_recovery:,.2f}", 
              delta=f"{(net_annual_recovery/annual_legacy_total)*100:.1f}% Savings")
    r2.metric("GIS Time Recovered", f"{gis_hours_saved:,.1f} Hours")
    r3.metric("Aviation Offset", f"${leg_air_event * events_pa:,.2f}")

    chart_data = {
        "Category": ["Aviation Recon", "GIS Manual Labor", "Field Readiness Waste", "ICEYE Subscription"],
        "Legacy Model ($)": [leg_air_event*events_pa, leg_gis_event*events_pa, leg_field_waste_event*events_pa, 0],
        "ICEYE Model ($)": [0, iceye_gis_event*events_pa, iceye_field_waste_event*events_pa, annual_sub]
    }
    df_chart = pd.DataFrame(chart_data).set_index("Category")
    st.bar_chart(df_chart, height=400, use_container_width=True)

with res_col2:
    st.subheader("Export Results")
    with st.container():
        st.markdown('<div class="report-box">', unsafe_content_as_html=True)
        st.write("Click below to generate a PDF summary of these calculations for your business case.")
        
        pdf_content = {
            "Annual Events": events_pa,
            "Total Legacy Cost": f"${annual_legacy_total:,.2f}",
            "Total ICEYE Cost": f"${annual_iceye_total:,.2f}",
            "Net Annual Savings": f"${net_annual_recovery:,.2f}",
            "GIS Productivity Gain": f"{gis_hours_saved} Hours"
        }
        
        if st.button("Generate PDF Report"):
            pdf_bytes = generate_pdf(pdf_content)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"ICEYE_ROI_Report_{datetime.date.today()}.pdf",
                mime="application/pdf"
            )
        st.markdown('</div>', unsafe_content_as_html=True)

# --- 7. INSIGHTS ---
st.divider()
st.subheader("Operational Audit Findings")
col_inf1, col_inf2 = st.columns(2)
with col_inf1:
    st.info(f"**Efficiency Gain:** Your GIS team currently spends {leg_processing_hrs * events_pa:,.0f} hours annually on manual digitizing. ICEYE automation reduces this by **{((leg_processing_hrs-iceye_processing_hrs)/leg_processing_hrs)*100:.0f}%**.")
with col_inf2:
    st.success(f"**Information Gap:** By reducing the 'Blind Window' from {cloud_wait_days} days to {sar_latency} hours, you eliminate **${(leg_field_waste_event - iceye_field_waste_event) * events_pa:,.2f}** in field labor downtime.")
