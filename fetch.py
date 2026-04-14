"""
fetch.py
--------
Fetches 48 hours of hourly weather data from Open-Meteo API.
Accepts coordinates from geocode.py — no API key required.
"""

import requests
from config import API_BASE_URL, API_TIMEOUT_SEC, PAST_DAYS, HOURLY_VARIABLES
from logger import get_logger

log = get_logger(__name__)


def fetch_weather(lat: float, lon: float, city: str = "", country: str = "") -> dict:
    """
    Calls Open-Meteo API and returns raw JSON for a given location.

    Args:
        lat:     Latitude
        lon:     Longitude
        city:    City name (for logging only)
        country: Country name (for logging only)

    Returns:
        dict: Raw JSON response from the API, with city/country injected.

    Raises:
        requests.HTTPError: If the API returns a non-200 status.
    """
    label = f"{city}, {country}" if city else f"lat={lat}, lon={lon}"
    log.info(f"Fetching 48hr weather data for {label} ...")

    params = {
        "latitude":   lat,
        "longitude":  lon,
        "hourly":     HOURLY_VARIABLES,
        "timezone":   "auto",
        "past_days":  PAST_DAYS,
        "forecast_days": 0,
    }

    response = requests.get(API_BASE_URL, params=params, timeout=API_TIMEOUT_SEC)
    response.raise_for_status()

    data = response.json()
    records = len(data.get("hourly", {}).get("time", []))
    log.info(f"Received {records} hourly records for {label}")

    # Inject city metadata into raw data so clean.py can use it
    data["_city"]    = city
    data["_country"] = country

    return data


if __name__ == "__main__":
    import json
    from geocode import get_coordinates
    coords = get_coordinates("Lahore")
    raw = fetch_weather(
        lat=coords["latitude"],
        lon=coords["longitude"],
        city=coords["city"],
        country=coords["country"],
    )
    print(json.dumps(raw, indent=2))
