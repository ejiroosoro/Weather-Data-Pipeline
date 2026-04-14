"""
geocode.py
----------
Converts a city name to latitude/longitude
using the Open-Meteo Geocoding API.
Free — no API key required.
"""

import requests
from config import GEOCODE_URL, API_TIMEOUT_SEC
from logger import get_logger

log = get_logger(__name__)


def get_coordinates(city: str) -> dict:
    """
    Looks up a city name and returns its coordinates.

    Args:
        city: City name e.g. "Lahore", "London", "New York"

    Returns:
        dict with keys: city, country, latitude, longitude

    Raises:
        ValueError: If the city is not found.
        requests.HTTPError: If the API call fails.
    """
    log.info(f"Looking up coordinates for '{city}' ...")

    response = requests.get(
        GEOCODE_URL,
        params={
            "name":     city,
            "count":    1,
            "language": "en",
            "format":   "json",
        },
        timeout=API_TIMEOUT_SEC,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        raise ValueError(f"City '{city}' not found. Check the spelling.")

    result = results[0]
    coords = {
        "city":      result.get("name"),
        "country":   result.get("country"),
        "latitude":  result.get("latitude"),
        "longitude": result.get("longitude"),
    }

    log.info(f"Found → {coords['city']}, {coords['country']} "
             f"(lat={coords['latitude']}, lon={coords['longitude']})")
    return coords


if __name__ == "__main__":
    for city in ["Lahore", "London", "New York", "Tokyo", "Dubai"]:
        print(get_coordinates(city))
