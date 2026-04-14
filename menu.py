"""
menu.py
-------
Interactive local menu with major world cities grouped by region.
Mirrors the GitHub Actions dropdown experience locally.

Usage:
    python menu.py
"""

import sys
import shlex
from run import run_pipeline
from logger import get_logger

log = get_logger(__name__)

# --- City presets grouped by region ---
PRESETS = {
    # --- Asia ---
    "1":  {"label": "South Asia      — Lahore, Karachi, Mumbai, Delhi, Dhaka",
           "cities": ["Lahore", "Karachi", "Mumbai", "Delhi", "Dhaka"]},
    "2":  {"label": "East Asia       — Tokyo, Beijing, Shanghai, Seoul, Hong Kong",
           "cities": ["Tokyo", "Beijing", "Shanghai", "Seoul", "Hong Kong"]},
    "3":  {"label": "Southeast Asia  — Bangkok, Singapore, Jakarta, Manila, Kuala Lumpur",
           "cities": ["Bangkok", "Singapore", "Jakarta", "Manila", "Kuala Lumpur"]},
    "4":  {"label": "Middle East     — Dubai, Riyadh, Doha, Abu Dhabi, Tehran",
           "cities": ["Dubai", "Riyadh", "Doha", "Abu Dhabi", "Tehran"]},
    "5":  {"label": "Central Asia    — Tashkent, Almaty, Kabul, Baku, Tbilisi",
           "cities": ["Tashkent", "Almaty", "Kabul", "Baku", "Tbilisi"]},

    # --- Europe ---
    "6":  {"label": "Western Europe  — London, Paris, Berlin, Madrid, Rome",
           "cities": ["London", "Paris", "Berlin", "Madrid", "Rome"]},
    "7":  {"label": "Northern Europe — Amsterdam, Brussels, Stockholm, Oslo, Copenhagen",
           "cities": ["Amsterdam", "Brussels", "Stockholm", "Oslo", "Copenhagen"]},
    "8":  {"label": "Eastern Europe  — Moscow, Warsaw, Prague, Budapest, Bucharest",
           "cities": ["Moscow", "Warsaw", "Prague", "Budapest", "Bucharest"]},
    "9":  {"label": "Southern Europe — Athens, Lisbon, Vienna, Zurich, Barcelona",
           "cities": ["Athens", "Lisbon", "Vienna", "Zurich", "Barcelona"]},

    # --- Americas ---
    "10": {"label": "North America   — New York, Los Angeles, Chicago, Toronto, Vancouver",
           "cities": ["New York", "Los Angeles", "Chicago", "Toronto", "Vancouver"]},
    "11": {"label": "Central America — Mexico City, Guadalajara, Guatemala City, San Jose, Panama City",
           "cities": ["Mexico City", "Guadalajara", "Guatemala City", "San Jose", "Panama City"]},
    "12": {"label": "South America   — Sao Paulo, Buenos Aires, Bogota, Lima, Santiago",
           "cities": ["Sao Paulo", "Buenos Aires", "Bogota", "Lima", "Santiago"]},

    # --- Africa ---
    "13": {"label": "North Africa    — Cairo, Casablanca, Tunis, Algiers, Tripoli",
           "cities": ["Cairo", "Casablanca", "Tunis", "Algiers", "Tripoli"]},
    "14": {"label": "West Africa     — Lagos, Accra, Dakar, Abidjan, Nairobi",
           "cities": ["Lagos", "Accra", "Dakar", "Abidjan", "Nairobi"]},
    "15": {"label": "Southern Africa — Johannesburg, Cape Town, Nairobi, Lusaka, Harare",
           "cities": ["Johannesburg", "Cape Town", "Nairobi", "Lusaka", "Harare"]},

    # --- Oceania ---
    "16": {"label": "Oceania         — Sydney, Melbourne, Brisbane, Auckland, Perth",
           "cities": ["Sydney", "Melbourne", "Brisbane", "Auckland", "Perth"]},

    # --- Custom ---
    "17": {"label": "Custom          — Enter your own cities",
           "cities": []},
}


def print_menu() -> None:
    print("\n" + "=" * 65)
    print("  🌤️  WEATHER DATA PIPELINE — CITY SELECTOR")
    print("=" * 65)
    print()

    regions = [
        ("🌏 ASIA",         ["1", "2", "3", "4", "5"]),
        ("🌍 EUROPE",       ["6", "7", "8", "9"]),
        ("🌎 AMERICAS",     ["10", "11", "12"]),
        ("🌍 AFRICA",       ["13", "14", "15"]),
        ("🌏 OCEANIA",      ["16"]),
        ("✏️  CUSTOM",       ["17"]),
    ]

    for region_label, keys in regions:
        print(f"  {region_label}")
        for key in keys:
            print(f"    [{key:>2}] {PRESETS[key]['label']}")
        print()

    print("=" * 65)


def get_custom_cities() -> list[str]:
    print("\n  Enter city names separated by spaces.")
    print("  Use quotes for multi-word cities.")
    print("  Example: Lahore London 'New York' Tokyo\n")
    raw = input("  Cities: ").strip()

    if not raw:
        print("  ❌ No cities entered. Exiting.")
        sys.exit(1)

    return shlex.split(raw)


def main() -> None:
    print_menu()

    choice = input("  Enter choice [1-17]: ").strip()

    if choice not in PRESETS:
        print(f"\n  ❌ Invalid choice '{choice}'. Please enter 1-17.")
        sys.exit(1)

    preset = PRESETS[choice]

    if choice == "17":
        cities = get_custom_cities()
    else:
        cities = preset["cities"]
        print(f"\n  ✅ Selected: {preset['label']}")

    print(f"\n  Cities to fetch: {', '.join(cities)}\n")

    confirm = input("  Confirm and run? [Y/n]: ").strip().lower()
    if confirm in ("n", "no"):
        print("  Cancelled.")
        sys.exit(0)

    run_pipeline(cities=cities)


if __name__ == "__main__":
    main()
