"""
config.py
---------
All project settings in one place.
Change anything here — no need to touch other files.
"""

from pathlib import Path

# --- API ---
API_BASE_URL     = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL      = "https://geocoding-api.open-meteo.com/v1/search"
API_TIMEOUT_SEC  = 10
PAST_DAYS        = 2   # Fetch last 48 hours of data
HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]

# --- Default Cities (used when no --cities argument is given) ---
DEFAULT_CITIES = ["Lahore", "London", "New York"]

# --- Storage ---
DATA_DIR     = Path("data")
PARQUET_FILE = DATA_DIR / "weather.parquet"
CSV_FILE     = DATA_DIR / "weather.csv"

# --- Logging ---
LOG_DIR   = Path("logs")
LOG_FILE  = LOG_DIR / "pipeline.log"
LOG_LEVEL = "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR
