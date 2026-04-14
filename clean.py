"""
clean.py
--------
Cleans raw JSON from fetch.py into a tidy pandas DataFrame.
- Removes null rows
- Fixes column types
- Adds city, country, timezone, fetched_at metadata
"""

import pandas as pd
from datetime import datetime, timezone
from logger import get_logger

log = get_logger(__name__)


def clean_weather(raw: dict) -> pd.DataFrame:
    """
    Cleans raw Open-Meteo JSON into a tidy DataFrame.

    Args:
        raw: Raw JSON dict from fetch.fetch_weather()

    Returns:
        pd.DataFrame: Cleaned weather data with proper types.

    Raises:
        KeyError: If expected keys are missing.
        ValueError: If DataFrame is empty after cleaning.
    """
    hourly = raw.get("hourly")
    if not hourly:
        raise KeyError("'hourly' key missing from raw data.")

    city    = raw.get("_city", "")
    country = raw.get("_country", "")
    label   = f"{city}, {country}" if city else "unknown location"

    log.info(f"Cleaning data for {label} ...")

    df = pd.DataFrame({
        "time":          hourly["time"],
        "temperature":   hourly["temperature_2m"],
        "humidity":      hourly["relative_humidity_2m"],
        "precipitation": hourly["precipitation"],
        "wind_speed":    hourly["wind_speed_10m"],
    })

    log.debug(f"Raw rows: {len(df)}")
    df.dropna(inplace=True)
    log.debug(f"Rows after dropping nulls: {len(df)}")

    if df.empty:
        raise ValueError(f"DataFrame is empty after cleaning for {label}.")

    # Fix types
    df["time"]          = pd.to_datetime(df["time"])
    df["temperature"]   = df["temperature"].astype(float)
    df["humidity"]      = df["humidity"].astype(float)
    df["precipitation"] = df["precipitation"].astype(float)
    df["wind_speed"]    = df["wind_speed"].astype(float)

    # Add metadata columns
    df["city"]       = city
    df["country"]    = country
    df["latitude"]   = raw.get("latitude")
    df["longitude"]  = raw.get("longitude")
    df["timezone"]   = raw.get("timezone")
    df["fetched_at"] = datetime.now(timezone.utc).isoformat()

    log.info(f"Cleaning complete for {label} — {len(df)} rows ready.")
    return df


if __name__ == "__main__":
    from geocode import get_coordinates
    from fetch import fetch_weather

    coords = get_coordinates("Lahore")
    raw = fetch_weather(**coords)
    df = clean_weather(raw)
    print(df.dtypes)
    print(df.head())
