"""
Sales Forecasting & Demand Intelligence Dashboard
Task 7 — Streamlit deployment for the Superstore sales forecasting project.

This app reads pre-computed data/model outputs from dashboard_data/
(exported at the end of analysis.ipynb) rather than retraining
SARIMA/Prophet/XGBoost live, since those models are too slow to fit
interactively on every page load.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Forecasting & Demand Intelligence", layout="wide")

# ----------------------------------------------------------------
# Data loading (cached so it only runs once per session)
# ----------------------------------------------------------------
@st.cache_data
def load_data():
    daily = pd.read_csv("dashboard_data/cleaned_daily_sales.csv", parse_dates=["Order Date", "Ship Date"])
    monthly = pd.read_csv("dashboard_data/monthly_sales.csv", parse_dates=["Date"])
    comparison = pd.read_csv("dashboard_data/model_comparison.csv")
    segment_forecasts = pd.read_csv("dashboard_data/segment_forecasts.csv", parse_dates=["Date"])
    anomalies = pd.read_csv("dashboard_data/weekly_anomalies.csv", parse_dates=["Week_Start"])
    clusters = pd.read_csv("dashboard_data/product_clusters.csv")
    return daily, monthly, comparison, segment_forecasts, anomalies, clusters

daily, monthly, comparison, segment_forecasts, anomalies, clusters = load_data()

st.sidebar.title("📊 Sales Forecasting")
page = st.sidebar.radio(
    "Navigate",
    ["Sales Overview", "Forecast Explorer", "Anomaly Report", "Product Demand Segments"],
)

# ==================================================================
# PAGE 1 — SALES OVERVIEW DASHBOARD
# ==================================================================
if page == "Sales Overview":
    st.title("Sales Overview Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Total Sales by Year")
        yearly = daily.groupby(daily["Order Date"].dt.year)["Sales"].sum().reset_index()
        yearly.columns = ["Year", "Sales"]
        fig = px.bar(yearly, x="Year", y="Sales", text_auto=".2s")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Monthly Sales Trend")
        fig = px.line(monthly, x="Date", y="Sales", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sales by Region & Category")
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        region_filter = st.multiselect(
            "Filter by Region", options=sorted(daily["Region"].unique()),
            default=sorted(daily["Region"].unique())
        )
    with filter_col2:
        category_filter = st.multiselect(
            "Filter by Category", options=sorted(daily["Category"].unique()),
            default=sorted(daily["Category"].unique())
        )

    filtered = daily[daily["Region"].isin(region_filter) & daily["Category"].isin(category_filter)]
    breakdown = filtered.groupby(["Region", "Category"])["Sales"].sum().reset_index()
    fig = px.bar(breakdown, x="Region", y="Sales", color="Category", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# ==================================================================
# PAGE 2 — FORECAST EXPLORER
# ==================================================================
elif page == "Forecast Explorer":
    st.title("Forecast Explorer")

    available_segments = sorted(segment_forecasts["Segment"].unique())
    selected_segment = st.selectbox("Select Category or Region", available_segments)

    horizon = st.slider("Forecast horizon (months ahead)", min_value=1, max_value=3, value=3)

    seg_data = segment_forecasts[segment_forecasts["Segment"] == selected_segment].sort_values("Date")
    seg_data = seg_data.head(horizon)

    st.subheader(f"Forecast for: {selected_segment}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=seg_data["Date"], y=seg_data["Forecast"], mode="lines+markers", name="Forecast"))
    fig.update_layout(xaxis_title="Month", yaxis_title="Forecasted Sales ($)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Overall Model Performance (XGBoost — winning model from Task 3)")
    best_row = comparison.sort_values("MAPE (%)").iloc[0]
    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"${best_row['MAE']:,.2f}")
    m2.metric("RMSE", f"${best_row['RMSE']:,.2f}")
    m3.metric("MAPE", f"{best_row['MAPE (%)']:.2f}%")

    st.caption(
        "MAE/RMSE/MAPE shown here are from the company-wide model comparison in Task 3. "
        "Segment-level forecasts use the same XGBoost approach but are fit on less data, "
        "so treat segment-level error as higher than the figures above."
    )

    with st.expander("See full model comparison table"):
        st.dataframe(comparison)

# ==================================================================
# PAGE 3 — ANOMALY REPORT
# ==================================================================
elif page == "Anomaly Report":
    st.title("Anomaly Report")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=anomalies["Week_Start"], y=anomalies["Sales"], mode="lines", name="Weekly Sales"))

    iso_pts = anomalies[anomalies["iso_anomaly"] == True]
    z_pts = anomalies[anomalies["z_anomaly"] == True]

    fig.add_trace(go.Scatter(x=iso_pts["Week_Start"], y=iso_pts["Sales"], mode="markers",
                              marker=dict(color="red", size=12, symbol="x"), name="Isolation Forest anomaly"))
    fig.add_trace(go.Scatter(x=z_pts["Week_Start"], y=z_pts["Sales"], mode="markers",
                              marker=dict(color="orange", size=12, symbol="diamond-open"), name="Z-score anomaly"))
    fig.update_layout(xaxis_title="Week", yaxis_title="Weekly Sales ($)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detected Anomaly Weeks")
    anomaly_table = anomalies[(anomalies["iso_anomaly"] == True) | (anomalies["z_anomaly"] == True)]
    anomaly_table = anomaly_table[["Week_Start", "Sales", "iso_anomaly", "z_anomaly"]].sort_values(
        "Week_Start"
    )
    st.dataframe(anomaly_table, use_container_width=True)

# ==================================================================
# PAGE 4 — PRODUCT DEMAND SEGMENTS
# ==================================================================
elif page == "Product Demand Segments":
    st.title("Product Demand Segments")

    fig = px.scatter(
        clusters, x="PC1", y="PC2", color="Cluster_Label", text="Sub-Category",
        size="TotalSales", hover_data=["YoY_Growth", "Volatility", "AvgOrderValue"]
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sub-Category → Cluster Mapping")
    st.dataframe(
        clusters[["Sub-Category", "Cluster_Label", "TotalSales", "YoY_Growth", "Volatility", "AvgOrderValue"]]
        .sort_values("Cluster_Label"),
        use_container_width=True,
    )
