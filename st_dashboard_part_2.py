# ================================================================
# Streamlit Dashboard: NYC CitiBike 2022 — Exercise 2.7 (Part 2)
# File: st_dashboard_part_2.py
# ================================================================
# This script FINALIZES the dashboard by:
# 1) Using a <25MB random sample of the main merged dataset
#    (reduced_data_to_plot_7.csv).
# 2) Creating a multi-page dashboard with:
#    - Intro page
#    - Weather vs trips page
#    - Top stations page with season filter
#    - Embedded Kepler map
#    - Recommendations page
# 3) Following EXACTLY the CareerFoundry Exercise 2.7 instructions.
# ================================================================

import os
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ---------------------------
# Global paths
# ---------------------------
BASE_DIR = os.path.dirname(__file__)

sample_path = os.path.join(BASE_DIR, "reduced_data_to_plot_7.csv")
top10_path = os.path.join(BASE_DIR, "top10_start_stations_2022.csv")
monthly_path = os.path.join(BASE_DIR, "monthly_trips_temp_2022.csv")
kepler_html_path = os.path.join(BASE_DIR, "NYC_BikeTrips_2022.html")

# ---------------------------
# Loaders with caching
# ---------------------------
@st.cache_data
def load_sample():
    df = pd.read_csv(sample_path)
    if "started_at" in df.columns:
        df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

@st.cache_data
def load_top10():
    return pd.read_csv(top10_path)

@st.cache_data
def load_monthly():
    return pd.read_csv(monthly_path)

df_sample = load_sample()
top10 = load_top10()
monthly = load_monthly()

# ---------------------------
# Streamlit page config
# ---------------------------
st.set_page_config(page_title="NYC CitiBike Strategy Dashboard", layout="wide")
st.title("NYC CitiBike Strategy Dashboard (2022)")
st.caption("Exercise 2.7 — Final Multipage Dashboard")

# ---------------------------
# Sidebar Navigation
# ---------------------------
page = st.sidebar.selectbox(
    "Select an aspect of the analysis",
    [
        "Intro page",
        "Weather component and bike usage",
        "Most popular stations",
        "Interactive map with aggregated bike trips",
        "Recommendations",
    ],
)

# ---------------------------
# Helper for seasons
# ---------------------------
def month_to_season(m):
    if m in [12, 1, 2]:
        return "Winter"
    if m in [3, 4, 5]:
        return "Spring"
    if m in [6, 7, 8]:
        return "Summer"
    if m in [9, 10, 11]:
        return "Fall"
    return "Unknown"

# ================================================================
# PAGE 1 — INTRO PAGE
# ================================================================
if page == "Intro page":
    st.header("Intro")

    st.markdown("""
Welcome! This dashboard explores CitiBike usage patterns in NYC during **2022**.
It follows the structure required in **Exercise 2.7**, including:

- A weather vs trip-demand page  
- A top stations page with seasonal filtering  
- An embedded Kepler map  
- A recommendations section  
""")

    st.metric("Total rides in random sample", f"{len(df_sample):,}")

    with st.expander("Preview sample data"):
        st.dataframe(df_sample.head())

# ================================================================
# PAGE 2 — WEATHER COMPONENT AND BIKE USAGE
# ================================================================
elif page == "Weather component and bike usage":
    st.header("Weather Component and Bike Usage")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=monthly["Month"], y=monthly["Trip Count"],
                   name="Trip Count", mode="lines+markers"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=monthly["Month"], y=monthly["Average Temperature"],
                   name="Avg Temperature (°C)", mode="lines+markers"),
        secondary_y=True,
    )

    fig.update_layout(
        title="Monthly Trip Volume vs Average Temperature (2022)",
        height=600
    )

    fig.update_yaxes(title_text="Trip Count", secondary_y=False)
    fig.update_yaxes(title_text="Avg Temperature (°C)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

# ================================================================
# PAGE 3 — MOST POPULAR STATIONS
# ================================================================
elif page == "Most popular stations":
    st.header("Most Popular Start Stations")

    if "date" in df_sample.columns:
        df_sample["month"] = df_sample["date"].dt.month
    elif "started_at" in df_sample.columns:
        df_sample["month"] = df_sample["started_at"].dt.month

    df_sample["season"] = df_sample["month"].apply(month_to_season)

    season_choice = st.selectbox("Filter by season", ["All", "Winter", "Spring", "Summer", "Fall"])

    if season_choice != "All":
        filtered = df_sample[df_sample["season"] == season_choice]
        chart_df = filtered["start_station_name"].value_counts().nlargest(10).reset_index()
        chart_df.columns = ["Start Station", "Trip Count"]
    else:
        chart_df = top10

    bar_fig = go.Figure(
        go.Bar(
            x=chart_df["Start Station"],
            y=chart_df["Trip Count"],
            marker={"color": chart_df["Trip Count"], "colorscale": "Blues"},
        )
    )

    bar_fig.update_layout(title="Top 10 Start Stations", height=600)

    st.plotly_chart(bar_fig, use_container_width=True)

# ================================================================
# PAGE 4 — KEPLER MAP
# ================================================================
elif page == "Interactive map with aggregated bike trips":
    st.header("Interactive Kepler Map")

    try:
        with open(kepler_html_path, "r", encoding="utf-8") as f:
            html_data = f.read()
        components.html(html_data, height=900, scrolling=True)
    except:
        st.error("Error: The Kepler HTML file was not found.")

# ================================================================
# PAGE 5 — RECOMMENDATIONS
# ================================================================
elif page == "Recommendations":
    st.header("Recommendations")

    st.markdown("""
### Based on the analysis:

**1. Increase bike supply in summer months**  
Trip demand is strongly correlated with temperature.

**2. Reinforce high-traffic commuter stations**  
Top stations show consistently high volume.

**3. Enhance rebalancing along major corridors**  
Kepler map identifies strong directional flows.

**4. Seasonal adjustments**  
Lower supply and rebalancing needed during cold months.
""")
