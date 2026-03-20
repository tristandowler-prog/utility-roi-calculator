import streamlit as st
import numpy as np
import pandas as pd

# --- SAFE PDF IMPORT ---
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    PDF_ENABLED = True
except ModuleNotFoundError:
    PDF_ENABLED = False

# --- PAGE CONFIG ---
st.set_page_config(page_title="Utility Flood ROI Model", layout="wide")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("⚙️ Customer Inputs")

    customer_name = st.text_input("Customer Name", "AGL Energy")
    uploaded_logo = st.file_uploader("Upload Logo", type=["png","jpg","jpeg"])

    st.markdown("### 📡 Subscription")
    sar_sub = st.number_input("Annual Subscription ($)", value=150000)

    st.markdown("### 🌊 Event Profile")
    events_per_year = st.slider("Flood Events / Year", 1, 10, 4)
    scenario = st.selectbox("Scenario", ["Urban Flood","Regional Storm","Severe Event"])

    st.markdown("### 🏗️ Network")
    total_assets = st.number_input("Total Assets", value=1200)
    inundation = st.slider("% Impacted", 1, 100, 25)

    st.markdown("### 🚛 Operations")
    crew_cost = st.number_input("Crew Cost ($)", value=850)
    base_search_time = st.number_input("Search Time (mins)", value=44)
    double_trip_risk = st.slider("Double Dispatch Risk (%)", 0, 100, 40)

    st.markdown("### ⚖️ Regulatory")
    stpis_penalty = st.number_input("Penalty ($/min/asset)", value=125)

    st.markdown("### ⏱️ Data")
    latency = st.select_slider("Latency", ["6h","12h","24h","48h"], value="12h")

# --- MODEL FACTORS ---
scenario_multiplier = {"Urban Flood":1.0,"Regional Storm":1.4,"Severe Event":2.0}[scenario]
latency_factor = {"6h":1.0,"12h":0.8,"24h":0.5,"48h":0.2}[latency]

# --- CORE CALCULATIONS ---
exposed_assets = int(total_assets * (inundation/100))
dry_assets = total_assets - exposed_assets

visibility = latency_factor * 100
blind_dispatch_rate = 100 - visibility

improved_time = base_search_time * latency_factor
time_saved = base_search_time - improved_time

search_waste = dry_assets * crew_cost
double_dispatch_cost = exposed_assets * (double_trip_risk/100) * crew_cost
regulatory_cost = exposed_assets * stpis_penalty * (time_saved * 60)

legacy_cost_per_event = (search_waste + double_dispatch_cost + regulatory_cost) * scenario_multiplier
solution_cost_per_event = exposed_assets * crew_cost

legacy_annual = legacy_cost_per_event * events_per_year
solution_annual = (solution_cost_per_event * events_per_year) + sar_sub

net_benefit = legacy_annual - solution_annual
roi = (net_benefit / sar_sub) * 100 if sar_sub > 0 else 0

# --- PAYBACK ---
payback_months = sar_sub / (net_benefit / 12) if net_benefit > 0 else 0
monthly_cost = sar_sub / 12
cost_per_event = sar_sub / events_per_year

# --- UI ---
st.title("Utility Flood ROI Model")
st.subheader("Cost-Benefit Analysis for Network Resilience")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Visibility", f"{visibility:.0f}%")
c2.metric("Blind Dispatch", f"{blind_dispatch_rate:.0f}%")
c3.metric("ROI", f"{roi:,.0f}%")
c4.metric("Payback", f"{payback_months:.1f} mo")

st.success(f"""
Prepared for: {customer_name}

Annual Net Benefit: ${net_benefit:,.0f}

Subscription:
- Monthly: ${monthly_cost:,.0f}
- Per Event: ${cost_per_event:,.0f}

Payback achieved in ~{payback_months:.1f} months
""")

st.error(f"Do Nothing Scenario: Annual Loss = ${legacy_annual:,.0f}")

# --- CHART ---
df = pd.DataFrame({
    "Category": ["Search Waste","Double Dispatch","Regulatory","Subscription"],
    "Cost": [
        search_waste*events_per_year,
        double_dispatch_cost*events_per_year,
        regulatory_cost*events_per_year,
        sar_sub
    ]
})
st.bar_chart(df.set_index("Category"))

# --- PDF GENERATION ---
if PDF_ENABLED:

    def generate_pdf():
        doc = SimpleDocTemplate("/mnt/data/flood_report.pdf", pagesize=A4)
        styles = getSampleStyleSheet()
        content = []

        # PAGE 1
        if uploaded_logo is not None:
            content.append(Image(uploaded_logo, width=120, height=60))

        content.append(Paragraph("Utility Flood ROI Model – Business Case Analysis", styles['Title']))
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"Prepared for: {customer_name}", styles['Normal']))
        content.append(Spacer(1, 20))

        content.append(Paragraph("Executive Summary", styles['Heading2']))
        content.append(Paragraph(
            f"Annual net benefit of ${net_benefit:,.0f}, ROI of {roi:.0f}%, "
            f"with payback in {payback_months:.1f} months.",
            styles['Normal']
        ))

        content.append(Spacer(1, 20))
        content.append(Paragraph(
            "Recommendation: Adoption is justified based on strong financial return and reduced operational risk.",
            styles['Normal']
        ))

        content.append(PageBreak())

        # PAGE 2
        content.append(Paragraph("Financial Breakdown", styles['Heading1']))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"Annual Loss (Do Nothing): ${legacy_annual:,.0f}", styles['Normal']))
        content.append(Paragraph(f"Annual Solution Cost: ${solution_annual:,.0f}", styles['Normal']))
        content.append(Paragraph(f"Net Benefit: ${net_benefit:,.0f}", styles['Normal']))

        content.append(Spacer(1, 20))
        content.append(Paragraph("Cost Drivers:", styles['Heading2']))
        content.append(Paragraph(f"Search Waste: ${search_waste*events_per_year:,.0f}", styles['Normal']))
        content.append(Paragraph(f"Double Dispatch: ${double_dispatch_cost*events_per_year:,.0f}", styles['Normal']))
        content.append(Paragraph(f"Regulatory Exposure: ${regulatory_cost*events_per_year:,.0f}", styles['Normal']))

        content.append(PageBreak())

        # PAGE 3
        content.append(Paragraph("Model Assumptions", styles['Heading1']))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"Total Assets: {total_assets}", styles['Normal']))
        content.append(Paragraph(f"Events per Year: {events_per_year}", styles['Normal']))
        content.append(Paragraph(f"Crew Cost: ${crew_cost}", styles['Normal']))
        content.append(Paragraph(f"Inundation Rate: {inundation}%", styles['Normal']))
        content.append(Paragraph(f"Latency: {latency}", styles['Normal']))

        doc.build(content)
        return "/mnt/data/flood_report.pdf"

    if st.button("📄 Generate Board PDF"):
        file_path = generate_pdf()
        with open(file_path, "rb") as f:
            st.download_button("Download Report", f, file_name="Utility_Flood_ROI_Report.pdf")

else:
    st.warning("PDF generation unavailable — install reportlab in requirements.txt")
