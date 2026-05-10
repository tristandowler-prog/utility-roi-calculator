import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Utility ROI Calculator", layout="wide")

def calculate_roi(investment, annual_savings, maintenance_cost, years):
    """Calculates yearly cash flow and ROI."""
    data = []
    cumulative_cash_flow = -investment
    
    for year in range(0, years + 1):
        if year == 0:
            net_savings = -investment
        else:
            net_savings = annual_savings - maintenance_cost
            cumulative_cash_flow += net_savings
            
        data.append({
            "Year": year,
            "Annual Net Savings": net_savings if year > 0 else -investment,
            "Cumulative Cash Flow": cumulative_cash_flow
        })
    
    df = pd.DataFrame(data)
    final_roi = ((cumulative_cash_flow + investment) / investment) * 100 if investment > 0 else 0
    return df, final_roi

# --- SIDEBAR INPUTS ---
st.sidebar.header("🔧 Investment Parameters")
inv_amount = st.sidebar.number_input("Total Investment ($)", min_value=0, value=50000, step=1000)
savings = st.sidebar.number_input("Estimated Annual Savings ($)", min_value=0, value=12000, step=500)
maint = st.sidebar.number_input("Annual Maintenance Cost ($)", min_value=0, value=1000, step=100)
duration = st.sidebar.slider("Analysis Period (Years)", min_value=1, max_value=30, value=10)

# --- MAIN CALCULATIONS ---
results_df, total_roi_pct = calculate_roi(inv_amount, savings, maint, duration)
payback_year = results_df[results_df["Cumulative Cash Flow"] >= 0]["Year"].min()

# --- DASHBOARD LAYOUT ---
st.title("📊 Utility Project ROI Calculator")
st.markdown("Estimate the financial impact of utility upgrades and infrastructure investments.")

col1, col2, col3 = st.columns(3)
col1.metric("Total ROI", f"{total_roi_pct:.2f}%")
col2.metric("Break-even Year", f"Year {payback_year}" if pd.notna(payback_year) else "Beyond Scope")
col3.metric("Net Profit", f"${results_df['Cumulative Cash Flow'].iloc[-1]:,.2f}")

st.divider()

# --- VISUALIZATION ---
fig = go.Figure()
fig.add_trace(go.Bar(
    x=results_df["Year"], 
    y=results_df["Annual Net Savings"],
    name="Annual Net Cash Flow",
    marker_color='rgb(55, 83, 109)'
))

fig.add_trace(go.Scatter(
    x=results_df["Year"], 
    y=results_df["Cumulative Cash Flow"],
    name="Cumulative ROI",
    line=dict(color='firebrick', width=4)
))

fig.update_layout(
    title="Financial Projection Over Time",
    xaxis_title="Year",
    yaxis_title="USD ($)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# --- DATA TABLE ---
with st.expander("See Detailed Breakdown"):
    st.table(results_df.style.format({
        "Annual Net Savings": "${:,.2f}",
        "Cumulative Cash Flow": "${:,.2f}"
    }))
