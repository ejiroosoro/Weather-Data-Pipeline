"""
dashboard.py
------------
Streamlit dashboard for the weather data pipeline.
Reads saved Parquet data and displays interactive charts.

Usage:
    streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from save import load_weather
from config import PARQUET_FILE

# --- Page Config ---
st.set_page_config(
    page_title="Weather Pipeline Dashboard",
    page_icon="🌤️",
    layout="wide",
)

# --- Header ---
st.title("🌤️ Weather Data Pipeline")
st.markdown(
    "Live 48-hour weather dashboard powered by "
    "[Open-Meteo](https://open-meteo.com) — no API key required."
)
st.divider()


# --- Load Data ---
@st.cache_data(ttl=60)
def load_data() -> pd.DataFrame:
    if not PARQUET_FILE.exists():
        return pd.DataFrame()
    df = load_weather()
    df["time"] = pd.to_datetime(df["time"])
    return df


df = load_data()

if df.empty:
    st.warning("⚠️ No data found. Run the pipeline first.")
    st.code("python run.py --cities Lahore London 'New York'", language="bash")
    st.stop()


# --- Sidebar ---
st.sidebar.header("⚙️ Filters")

# City filter
all_cities = sorted(df["city"].unique().tolist())
selected_cities = st.sidebar.multiselect(
    "🌍 Select Cities",
    options=all_cities,
    default=all_cities,
)

if not selected_cities:
    st.warning("Please select at least one city from the sidebar.")
    st.stop()

df = df[df["city"].isin(selected_cities)]

# Date filter
min_date = df["time"].min().date()
max_date = df["time"].max().date()

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) == 2:
    df = df[
        (df["time"].dt.date >= date_range[0]) &
        (df["time"].dt.date <= date_range[1])
    ]

st.sidebar.divider()
st.sidebar.markdown(f"**Records shown:** {len(df):,}")
st.sidebar.markdown(f"**Cities:** {', '.join(selected_cities)}")


# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌡️ Avg Temperature", f"{df['temperature'].mean():.1f} °C",
              f"Max: {df['temperature'].max():.1f} °C")
with col2:
    st.metric("💧 Avg Humidity", f"{df['humidity'].mean():.1f} %",
              f"Max: {df['humidity'].max():.1f} %")
with col3:
    st.metric("🌧️ Total Precipitation", f"{df['precipitation'].sum():.1f} mm",
              f"Max 1hr: {df['precipitation'].max():.1f} mm")
with col4:
    st.metric("💨 Avg Wind Speed", f"{df['wind_speed'].mean():.1f} km/h",
              f"Max: {df['wind_speed'].max():.1f} km/h")

st.divider()


# --- Charts ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌡️ Temperature")
    fig = px.line(df, x="time", y="temperature", color="city",
                  labels={"temperature": "°C", "time": "Time", "city": "City"})
    fig.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("💧 Humidity")
    fig = px.line(df, x="time", y="humidity", color="city",
                  labels={"humidity": "%", "time": "Time", "city": "City"})
    fig.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("🌧️ Precipitation")
    fig = px.bar(df, x="time", y="precipitation", color="city",
                 labels={"precipitation": "mm", "time": "Time", "city": "City"},
                 barmode="group")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with col_right2:
    st.subheader("💨 Wind Speed")
    fig = px.area(df, x="time", y="wind_speed", color="city",
                  labels={"wind_speed": "km/h", "time": "Time", "city": "City"})
    fig.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


# --- Raw Data ---
st.divider()
st.subheader("📋 Raw Data")

with st.expander("Show raw data table"):
    st.dataframe(
        df.sort_values(["city", "time"], ascending=[True, False]),
        use_container_width=True,
        height=300,
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "weather_data.csv", "text/csv")
