"""
save.py
-------
Saves cleaned weather DataFrame to Parquet + CSV.
Appends new data and deduplicates on (time, city).
"""

import pandas as pd
from config import DATA_DIR, PARQUET_FILE, CSV_FILE
from logger import get_logger

log = get_logger(__name__)


def save_weather(df: pd.DataFrame) -> None:
    """
    Appends cleaned data to Parquet + CSV, deduplicating rows.

    Args:
        df: Cleaned DataFrame from clean.clean_weather()
    """
    DATA_DIR.mkdir(exist_ok=True)

    if PARQUET_FILE.exists():
        existing = pd.read_parquet(PARQUET_FILE)
        combined = pd.concat([existing, df], ignore_index=True)
        before = len(combined)
        combined.drop_duplicates(subset=["time", "city"], inplace=True)
        dupes = before - len(combined)
        if dupes > 0:
            log.debug(f"Removed {dupes} duplicate rows.")
    else:
        combined = df

    combined.to_parquet(PARQUET_FILE, index=False)
    combined.to_csv(CSV_FILE, index=False)

    log.info(f"Saved {len(combined)} total rows → {PARQUET_FILE} + {CSV_FILE}")


def load_weather() -> pd.DataFrame:
    """
    Loads saved Parquet file for inspection or dashboard.

    Returns:
        pd.DataFrame

    Raises:
        FileNotFoundError: If no data has been saved yet.
    """
    if not PARQUET_FILE.exists():
        raise FileNotFoundError(
            f"No data at {PARQUET_FILE}. Run 'python run.py' first."
        )
    return pd.read_parquet(PARQUET_FILE)


if __name__ == "__main__":
    df = load_weather()
    print(f"Loaded {len(df)} rows.")
    print(df.tail())
