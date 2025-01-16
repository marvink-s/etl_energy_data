import requests
import pandas as pd
from tqdm import tqdm
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://smard.api.proxy.bund.dev/app/chart_data"
FILTER_ID = 4169  # 4169 - Marktpreis: Deutschland/Luxemburg
COUNTRY_CODE = "DE"


def fetch_json(url: str) -> dict:
    """Fetch JSON data from the given URL with error handling."""
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request failed for URL: {url}, Error: {e}")
        return {}


def fetch_timestamps() -> List[int]:
    """Fetch the list of timestamps."""
    url = f"{BASE_URL}/{FILTER_ID}/{COUNTRY_CODE}/index_hour.json"
    data = fetch_json(url)
    return data.get("timestamps", [])


def fetch_timeseries_data(timestamp: int) -> pd.DataFrame:
    """Fetch time series data for a given timestamp and return it as a DataFrame."""
    url = f"{BASE_URL}/{FILTER_ID}/{COUNTRY_CODE}/{FILTER_ID}_{COUNTRY_CODE}_hour_{timestamp}.json"
    data = fetch_json(url)
    if "series" in data:
        df = pd.DataFrame(data["series"], columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    else:
        logging.warning(f"No series data found for timestamp: {timestamp}")
        return pd.DataFrame()


def main():
    """Main function to orchestrate data fetching and processing."""
    logging.info("Fetching timestamps...")
    timestamps = fetch_timestamps()
    if not timestamps:
        logging.error("No timestamps fetched. Exiting.")
        return

    logging.info(f"Fetched {len(timestamps)} timestamps. Starting data collection...")

    data_frames = []
    for ts in tqdm(timestamps, desc="Processing timestamps"):
        df = fetch_timeseries_data(ts)
        if not df.empty:
            data_frames.append(df)

    if data_frames:
        df_final = pd.concat(data_frames, ignore_index=True)
        logging.info("Data collection complete.")
        # Save or return the final DataFrame as needed
        df_final.to_csv("market_prices.csv", index=False)
        logging.info("Data saved to market_prices.csv")
    else:
        logging.warning("No data collected. Exiting.")


if __name__ == "__main__":
    main()
