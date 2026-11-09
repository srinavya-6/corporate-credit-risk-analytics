import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Corporate Credit Risk Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Corporate Credit Risk & Financial Statement Analysis")
st.markdown(
    "Automated credit evaluation, financial ratio analysis, and Altman Z-Score"
    " risk scoring."
)

# ---------------------------------------------------------
# Built-In Financial Dataset (Fail-Safe Offline Storage)
# ---------------------------------------------------------
PRELOADED_DATA = {
    "AAPL": {
        "Company Name": "Apple Inc.",
        "Total Assets": 352.58,  # in Billions USD
        "Total Liabilities": 290.43,
        "Current Assets": 143.56,
        "Current Liabilities": 145.31,
        "Retained Earnings": 214.33,
        "Total Revenue": 383.29,
        "EBIT": 114.30,
        "Total Debt": 111.08,
        "Market Cap": 3400.00,
        "Historical": {
            "2021": {"Revenue": 365.8, "EBIT": 108.9},
            "2022": {"Revenue": 394.3, "EBIT": 119.4},
            "2023": {"Revenue": 383.3, "EBIT": 114.3},
        },
    },
    "MSFT": {
        "Company Name": "Microsoft Corporation",
        "Total Assets": 411.97,
        "Total Liabilities": 205.75,
        "Current Assets": 184.25,
        "Current Liabilities": 104.15,
        "Retained Earnings": 118.85,
        "Total Revenue": 211.91,
        "EBIT": 88.52,
        "Total Debt": 59.96,
        "Market Cap": 3100.00,
        "Historical": {
            "2021": {"Revenue": 168.1, "EBIT": 69.9},
            "2022": {"Revenue": 198.3, "EBIT": 83.4},
            "2023": {"Revenue": 211.9, "EBIT": 88.5},
        },
    },
    "GOOGL": {
        "Company Name": "Alphabet Inc.",
        "Total Assets": 402.39,
        "Total Liabilities": 109.12,
        "Current Assets": 165.11,
        "Current Liabilities": 88.24,
        "Retained Earnings": 195.42,
        "Total Revenue": 307.39,
        "EBIT": 84.29,
        "Total Debt": 28.38,
        "Market Cap": 2100.00,
        "Historical": {
            "2021": {"Revenue": 257.6, "EBIT": 78.7},
            "2022": {"Revenue": 282.8, "EBIT": 74.8},
            "2023": {"Revenue": 307.4, "EBIT": 84.3},
        },
    },
    "TSLA": {
        "Company Name": "Tesla, Inc.",
        "Total Assets": 106.62,
        "Total Liabilities": 43.01,
        "Current Assets": 49.62,
        "Current Liabilities": 28.74,
        "Retained Earnings": 27.88,
        "Total Revenue": 96.77,
        "EBIT": 8.89,
        "Total Debt": 9.58,
        "Market Cap": 750.00,
        "Historical": {
            "2021": {"Revenue": 53.8, "EBIT": 6.5},
            "2022": {"Revenue": 81.5, "EBIT": 13.7},
            "2023": {"Revenue": 96.8, "EBIT": 8.9},
        },
    },
    "INFY.NS": {
        "Company Name": "Infosys Limited",
        "Total Assets": 16.50,
        "Total Liabilities": 5.20,
        "Current Assets": 10.20,
        "Current Liabilities": 4.10,
        "Retained Earnings": 8.50,
        "Total Revenue": 18.60,
        "EBIT": 4.20,
        "Total Debt": 1.10,
        "Market Cap": 78.00,
        "Historical": {
            "2021": {"Revenue": 13.5, "EBIT": 3.2},
            "2022": {"Revenue": 16.3, "EBIT": 3.8},
            "2023": {"Revenue": 18.6, "EBIT": 4.2},
        },
    },
}

# ---------------------------------------------------------
# Sidebar - Selector & Controls
# ---------------------------------------------------------
st.sidebar.header("Configuration")
selected_ticker = st.sidebar.selectbox(
    "Select Preloaded Entity:",
    options=list(PRELOADED_DATA.keys()),
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Custom Input Mode")
use_custom = st.sidebar.checkbox("Input Custom Financial Data")

if use_custom:
  company_name = st.sidebar.text_input("Company Name", "Custom Corp")
  total_assets = st.sidebar.number_input("Total Assets ($B)", value=100.0)
  total_liabilities = st.sidebar.number_input(
      "Total Liabilities ($B)", value=50.0
  )
  current_assets = st.sidebar.number_input("Current Assets ($B)", value=40.0)
  current_liabilities = st.sidebar.number_input(
      "Current Liabilities ($B)", value=30.0
  )
  retained_earnings = st.sidebar.number_input(
      "Retained Earnings ($B)", value=20.0
  )
  revenue = st.sidebar.number_input("Total Revenue ($B)", value=80.0)
  ebit = st.sidebar.number_input("EBIT ($B)", value=15.0)
  total_debt = st.sidebar.number_input("Total Debt ($B)", value=25.0)
  market_cap = st.sidebar.number_input("Market Cap ($B)", value=200.0)

  data = {
      "Company Name": company_name,
      "Total Assets": total_assets,
      "Total Liabilities": total_liabilities,
      "Current Assets": current_assets,
      "Current Liabilities": current_liabilities,
      "Retained Earnings": retained_earnings,
      "Total Revenue": revenue,
      "EBIT": ebit,
      "Total Debt": total_debt,
      "Market Cap": market_cap,
      "Historical": {
          "2021": {"Revenue": revenue * 0.8, "EBIT": ebit * 0.8},
          "2022": {"Revenue": revenue * 0.9, "EBIT": ebit * 0.9},
          "2023": {"Revenue": revenue, "EBIT": ebit},
      },
  }
else:
  data = PRELOADED_DATA[selected_ticker]

# ---------------------------------------------------------
# Calculate Financial Metrics & Altman Z-Score
# ---------------------------------------------------------
working_capital = data["Current Assets"] - data["Current Liabilities"]
current_ratio = (
    data["Current Assets"] / data["Current Liabilities"]
    if data["Current Liabilities"] > 0
    else 0
)
equity = data["Total Assets"] - data["Total Liabilities"]
debt_to_equity = data["Total Debt"] / equity if equity > 0 else 0
operating_margin = (
    data["EBIT"] / data["Total Revenue"] if data["Total Revenue"] > 0 else 0
)

# Altman Z-Score Formula: Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5
x1 = working_capital / data["Total Assets"]
x2 = data["Retained Earnings"] / data["Total Assets"]
x3 = data["EBIT"] / data["Total Assets"]
x4 = data["Market Cap"] / data["Total Liabilities"]
x5 = data["Total Revenue"] / data["Total Assets"]
z_score = (1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (0.999 * x5)

# ---------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------
st.subheader(f"Entity: {data['Company Name']}")
st.caption("Standardized Financial & Credit Assessment Report")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Ratio (Liquidity)", f"{current_ratio:.2f}")
col2.metric("Debt-to-Equity (Leverage)", f"{debt_to_equity:.2f}")
col3.metric("Operating Margin", f"{operating_margin * 100:.1f}%")
col4.metric("Altman Z-Score", f"{z_score:.2f}")

st.markdown("---")
st.subheader("Credit Risk Assessment")

if z_score > 2.99:
  st.success(
      f"🟢 **LOW CREDIT RISK (Safe Zone - Z-Score: {z_score:.2f})**: Strong"
      " balance sheet, sound liquidity, and negligible 2-year default risk."
  )
elif z_score >= 1.81:
  st.warning(
      f"🟡 **MODERATE RISK (Grey Zone - Z-Score: {z_score:.2f})**: Moderate credit"
      " risk profile. Monitor cash flows and leverage exposure."
  )
else:
  st.error(
      f"🔴 **HIGH CREDIT RISK (Distress Zone - Z-Score: {z_score:.2f})**: Elevated"
      " probability of distress. High leverage or constrained liquidity."
  )

st.markdown("---")
st.subheader("Historical Performance (2021 - 2023)")

df_trend = pd.DataFrame(data["Historical"]).T.reset_index()
df_trend.columns = ["Year", "Revenue ($B)", "EBIT ($B)"]

fig = px.bar(
    df_trend,
    x="Year",
    y=["Revenue ($B)", "EBIT ($B)"],
    barmode="group",
    title="Revenue vs. Operating Income Trend",
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("View Input Data Summary"):
  st.json(data)