# ===========================================================================
# Streamlit Dashboard: NYC CitiBike 2022 – Tasks 5 to 7
# ===========================================================================

# ✅ Step 5–7: Build Streamlit dashboard and embed plotly charts

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime as dt

# ------------------------------
# Step 6: Configure page settings
# ------------------------------
st.set_page_config(page_title='NYC CitiBike Strategy Dashboard', layout='wide')

# ------------------------------
# Step 6: Title and description
# ------------------------------
st.title("NYC CitiBike Strategy Dashboard")
st.markdown("""
This interactive dashboard explores patterns in CitiBike usage in New York City during 2022.

- Most popular start stations
- Monthly ride volume and its relationship with average temperature
- Geospatial patterns of routes (coming next)
""")

# ------------------------------
# Step 7: Load dataset
# ------------------------------
df = pd.read_csv('/Users/samarjitgehdu/Documents/Achievement 2/CitiBike_Weather_Merged_2022.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensure datetime format
df['month'] = df['date'].dt.month

# ------------------------------
# Step 7a: Bar chart – Top 10 start stations
# ------------------------------
st.subheader("Top 10 Most Popular Start Stations")

top10 = df['start_station_name'].value_counts().nlargest(10).reset_index()
top10.columns = ['Start Station', 'Trip Count']

fig = go.Figure(go.Bar(
    x=top10['Start Station'],
    y=top10['Trip Count'],
    marker={'color': top10['Trip Count'], 'colorscale': 'Blues'}
))
fig.update_layout(
    title='Top 10 Start Stations (2022)',
    xaxis_title='Station Name',
    yaxis_title='Number of Rides',
    width=900,
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Step 7b: Dual-axis chart – Monthly trips vs avg temperature
# ------------------------------
st.subheader("Monthly Ride Volume vs. Average Temperature")

monthly = df.groupby('month').agg({
    'ride_id': 'count',
    'avgTemp': 'mean'
}).reset_index()
monthly.columns = ['Month', 'Trip Count', 'Average Temperature']

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(
    go.Scatter(x=monthly['Month'], y=monthly['Trip Count'], name='Trip Count',
               marker={'color': 'blue'}),
    secondary_y=False
)
fig2.add_trace(
    go.Scatter(x=monthly['Month'], y=monthly['Average Temperature'], name='Avg Temp',
               marker={'color': 'red'}),
    secondary_y=True
)
fig2.update_layout(
    title='Monthly Trip Volume vs. Average Temperature (2022)',
    xaxis_title='Month',
    height=600
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# ✅ End of Step 7 – ready for Kepler
# ----------------------------------
st.markdown("---")
st.markdown("🚧 Coming next: Interactive map of station-to-station routes (Kepler.gl)")


# ------------------------------
# Step 8: Embed Kepler.gl HTML Map
# ------------------------------
st.subheader("Popular Bike Routes Across NYC (Kepler.gl)")

# Use stable Streamlit method to embed HTML
import streamlit.components.v1 as components

# Path to the exported Kepler map HTML file
kepler_map_path = '/Users/samarjitgehdu/Documents/Achievement 2/CitiBike_NYC_2022_Analysis/NYC_BikeTrips_2022.html'

# Load and render map in iframe
try:
    with open(kepler_map_path, "r", encoding="utf-8") as f:
        kepler_html = f.read()
    components.html(kepler_html, height=1000)
except FileNotFoundError:
    st.warning("⚠️ Kepler map file not found. Please ensure 'NYC_BikeTrips_2022.html' is in the working directory.")
