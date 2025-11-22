
# ================================================================
# Streamlit Dashboard: NYC CitiBike 2022 — Exercise 2.6 (Steps 5–8)
# ================================================================
# This Streamlit app uses *reduced* CSV files exported from your
# Jupyter Notebook (Charts_for_Dashboard.ipynb).
#
# Why reduced files?
# - The merged CitiBike+Weather dataset is ~6GB, which cannot be
#   uploaded to GitHub or loaded on Streamlit Cloud (assignment Step 9).
# - Exercise 2.6 only requires:
#     (1) Top 10 Start Stations bar chart (Plotly)
#     (2) Dual-axis line chart: Monthly Trip Count vs Avg Temperature (Plotly)
# - Therefore, we export only those two small dataframes:
#     top10_start_stations_2022.csv
#     monthly_trips_temp_2022.csv
#   and load them here.
# ================================================================

import os
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ---------------------------
# Step 6: Page config + title
# ---------------------------
st.set_page_config(page_title="NYC CitiBike Strategy Dashboard", layout="wide")

st.title("NYC CitiBike Strategy Dashboard")
st.markdown("""
This interactive dashboard explores patterns in CitiBike usage in New York City during 2022.

**Exercise 2.6 Visualizations**
- Top 10 most popular start stations (Plotly bar chart)
- Monthly ride volume vs average temperature (Plotly dual-axis line chart)
""")

# ---------------------------
# Step 7: Load reduced datasets
# ---------------------------
BASE_DIR = os.path.dirname(__file__)

top10_path = os.path.join(BASE_DIR, "top10_start_stations_2022.csv")
monthly_path = os.path.join(BASE_DIR, "monthly_trips_temp_2022.csv")

# Load reduced CSVs created in the notebook
top10 = pd.read_csv(top10_path)
monthly = pd.read_csv(monthly_path)

# ---------------------------
# Step 7a: Plotly bar chart — Top 10 start stations
# ---------------------------
st.subheader("Top 10 Most Popular Start Stations")

bar_fig = go.Figure(
    go.Bar(
        x=top10["Start Station"],
        y=top10["Trip Count"],
        marker={"color": top10["Trip Count"], "colorscale": "Blues"},
    )
)

bar_fig.update_layout(
    title="Top 10 Most Popular Start Stations in NYC (2022)",
    xaxis_title="Station Name",
    yaxis_title="Number of Rides",
    height=600,
)

st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")

# ---------------------------
# Step 7b: Dual-axis Plotly line chart — Monthly trips vs avg temp
# ---------------------------
st.subheader("Monthly Trip Volume vs Average Temperature")

line_fig = make_subplots(specs=[[{"secondary_y": True}]])

line_fig.add_trace(
    go.Scatter(
        x=monthly["Month"],
        y=monthly["Trip Count"],
        name="Trip Count",
        mode="lines+markers",
    ),
    secondary_y=False,
)

line_fig.add_trace(
    go.Scatter(
        x=monthly["Month"],
        y=monthly["Average Temperature"],
        name="Average Temperature",
        mode="lines+markers",
    ),
    secondary_y=True,
)

line_fig.update_layout(
    title="Monthly Trip Volume vs. Average Temperature (2022)",
    xaxis_title="Month",
    legend_title="Legend",
    height=600,
)

line_fig.update_yaxes(title_text="Trip Count", secondary_y=False)
line_fig.update_yaxes(title_text="Average Temperature", secondary_y=True)

st.plotly_chart(line_fig, use_container_width=True)

st.markdown("---")

# ---------------------------
# Step 8: Embed Kepler.gl HTML map
# ---------------------------
st.subheader("Kepler.gl Map of CitiBike Trips")

kepler_html_path = os.path.join(BASE_DIR, "NYC_BikeTrips_2022.html")

try:
    with open(kepler_html_path, "r", encoding="utf-8") as f:
        kepler_html = f.read()
    components.html(kepler_html, height=1000, scrolling=True)
except FileNotFoundError:
    st.warning(
        "Kepler map HTML not found. "
        "Place 'NYC_BikeTrips_2022.html' in the same GitHub folder as this app."
    )
