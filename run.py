"""
run.py
------
Entry point. Runs fetch → clean → save for one or more cities.

Usage:
    # Use default cities from config.py
    python run.py

    # Pass specific cities by name
    python run.py --cities Lahore London "New York" Tokyo Dubai
"""

import argparse
import sys
from geocode import get_coordinates
from fetch import fetch_weather
from clean import clean_weather
from save import save_weather
from config import DEFAULT_CITIES
from logger import get_logger

log = get_logger(__name__)


def run_pipeline(cities: list[str]) -> None:
    """
    Runs the full pipeline for a list of city names.

    Args:
        cities: List of city name strings e.g. ["Lahore", "London"]
    """
    log.info("=" * 50)
    log.info("  WEATHER DATA PIPELINE STARTED")
    log.info(f"  Cities: {', '.join(cities)}")
    log.info("=" * 50)

    success = []
    failed  = []

    for city in cities:
        log.info(f"\n--- Processing: {city} ---")
        try:
            # Step 1: Geocode city name → coordinates
            coords = get_coordinates(city)

            # Step 2: Fetch 48hrs of weather data
            raw = fetch_weather(
                lat=coords["latitude"],
                lon=coords["longitude"],
                city=coords["city"],
                country=coords["country"],
            )

            # Step 3: Clean
            df = clean_weather(raw)

            # Step 4: Save
            save_weather(df)

            success.append(coords["city"])

        except Exception as e:
            log.error(f"Failed for '{city}': {e}")
            failed.append(city)

    # Summary
    log.info("\n" + "=" * 50)
    log.info(f"  PIPELINE COMPLETE")
    log.info(f"  ✓ Success : {', '.join(success) if success else 'none'}")
    log.info(f"  ✗ Failed  : {', '.join(failed)  if failed  else 'none'}")
    log.info("=" * 50)

    if failed:
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch 48hr weather data for one or more cities."
    )
    parser.add_argument(
        "--cities",
        nargs="+",
        default=DEFAULT_CITIES,
        metavar="CITY",
        help=(
            'One or more city names. Use quotes for multi-word cities. '
            'Example: --cities Lahore London "New York" Tokyo'
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(cities=args.cities)
