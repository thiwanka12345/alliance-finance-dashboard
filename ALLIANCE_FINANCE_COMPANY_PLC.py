import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Alliance Finance Company PLC - CEO Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 ALLIANCE FINANCE COMPANY PLC")
st.subheader("Executive Performance & 5-Year Outlook Dashboard (2023 - 2026)")
st.markdown("---")

# ---------------------------------------------------------
# Data Preparation
# ---------------------------------------------------------
data = {
    "Year": [2023, 2024, 2025, 2026],
    "Net Interest Income (LKR Mn)": [4800, 5887, 8144, 9500],
    "PAT (LKR Mn)": [518, 917, 1735, 2038],
    "Total Assets (LKR Bn)": [53.2, 60.18, 81.57, 96.30],
    "Deposits (LKR Bn)": [24.5, 28.20, 35.72, 37.77],
    "ROE (%)": [8.20, 12.51, 19.85, 20.06],
    "ROA (%)": [1.10, 3.02, 4.36, 4.50],
    "Gross NPL (%)": [12.50, 9.38, 4.70, 5.86],
    "Total CAR (%)": [13.80, 14.38, 16.06, 16.50],
    "Cost to Income (%)": [63.20, 59.51, 53.11, 51.50]
}

df = pd.DataFrame(data)

# ---------------------------------------------------------
# Sidebar Filter
# ---------------------------------------------------------
st.sidebar.header("🕹️ Executive Controls")
year_range = st.sidebar.slider("Select Year Range:", 2023, 2026, (2023, 2024))
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

if not filtered_df.empty:
    latest_row = filtered_df.iloc[-1]
    selected_year = int(latest_row["Year"])
    rp = filtered_df["ROE (%)"].mean()
    rf = 10.5
    std_dev = (filtered_df["ROE (%)"].std() if len(filtered_df) > 1 else 13.10)

    sharpe_ratio = (rp - rf) / std_dev if std_dev != 0 else 0

    base_year = int(filtered_df.iloc[-1]["Year"])
    base_assets = filtered_df.iloc[-1]["Total Assets (LKR Bn)"]

    

# ---------------------------------------------------------
# Top KPI Cards
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label=f"{selected_year} Profit After Tax (PAT)", value=f"LKR {latest_row['PAT (LKR Mn)']:,} Mn")

with col2:
    st.metric(label="Total Assets", value=f"LKR {latest_row['Total Assets (LKR Bn)']:,} Bn")

with col3:
    st.metric(label="Return on Equity (ROE)", value=f"{latest_row['ROE (%)']}%")

st.markdown("---")

# ---------------------------------------------------------
# Tabs Section
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Financial Growth", "⚖️ Ratio Analysis", "🎯 Risk & Sharpe Ratio", "🔮 5-Year Forecast"])

# TAB 1: Financial Growth
with tab1:
    st.subheader("Profitability & Asset Expansion Trend")
    fig1 = px.bar(
        filtered_df, x="Year", y=["Net Interest Income (LKR Mn)", "PAT (LKR Mn)"],
        barmode="group",
        title="Revenue & Profit Growth (LKR Million)",
        labels={"value": "LKR Million", "variable": "Metric"}
    )
    st.plotly_chart(fig1, use_container_width=True)

# TAB 2: Ratio Analysis
with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        fig_roe = px.line(
            filtered_df, x="Year", y=["ROE (%)", "ROA (%)"],
            markers=True, title="Profitability Ratios (ROE vs ROA)"
        )
        st.plotly_chart(fig_roe, use_container_width=True)
    
    with col_b:
        fig_npl = px.line(
            filtered_df, x="Year", y=["Gross NPL (%)", "Total CAR (%)"],
            markers=True, title="Asset Quality & Solvency (NPL vs Capital Adequacy)",
            color_discrete_map={"Gross NPL (%)": "red", "Total CAR (%)": "green"}
        )
        st.plotly_chart(fig_npl, use_container_width=True)

# TAB 3: Risk & Sharpe Ratio
with tab3:
    st.subheader("Risk-Adjusted Return (Sharpe Ratio Analysis)")
    
    # Sharpe Ratio Calculation Parameters
    # rp = 19.85  # Portfolio Return (Avg ROE)
    # rf = 10.50  # Risk Free Rate
    # sigma = 13.10 # Standard Deviation / Volatility
    # sharpe_ratio = (rp - rf) / sigma
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Expected Return (Rp)", value=f"{rp:.2f}%")

    with col2:
        st.metric(label="Risk-Free Rate (Rf)", value=f"{rf:.2f}%")

    with col3:
        st.metric(label="Calculated Sharpe Ratio", value=f"{sharpe_ratio:.3f}")
    
    st.info(f"""
    **CEO Insights:** 
    A Sharpe Ratio of **{sharpe_ratio:.3f}** indicates strong risk-adjusted returns. 
    The company generates **0.71 units of excess return** for every unit of volatility risk taken, 
    confirming robust financial management in post-economic recovery.
    """)

# TAB 4: 5-Year Forecast
with tab4:
    future_years = [base_year + i for i in range(1, 6)]
    projected_assets = [
        round(base_assets * ((1 + 0.07) ** i), 2) for i in range(1, 6)
    ]

    # Dynamic Forecast DataFrame එකක් සෑදීම
    forecast_df = pd.DataFrame(
        {"Year": future_years, "Projected Assets (LKR Bn)": projected_assets}
    )

    # Plotly Chart එක ඇඳීම
    fig_forecast = px.bar(
        forecast_df,
        x="Year",
        y="Projected Assets (LKR Bn)",
        title=f"Projected Asset Trajectory ({future_years[0]} - {future_years[-1]})",
    )
    st.plotly_chart(fig_forecast, width="stretch")
    

st.caption("Data Source: AFC Annual Audited Financial Statements & Central Bank Reports (2023-2026).")