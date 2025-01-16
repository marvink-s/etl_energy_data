import requests
import pandas as pd
from tqdm import tqdm

# 4169 - Marktpreis: Deutschland/Luxemburg
timestamp_url = (
    "https://smard.api.proxy.bund.dev/app/chart_data/4169/DE/index_hour.json"
)
timestamp_response = requests.get(timestamp_url)
timestamps = timestamp_response.json()
list_timestamps = timestamps.get("timestamps")

df_final = pd.DataFrame()

for i in tqdm(list_timestamps):
    timeseries_url = (
        f"https://smard.api.proxy.bund.dev/app/chart_data/4169/DE/4169_DE_hour_{i}.json"
    )
    timeseries_response = requests.get(timeseries_url)
    data = timeseries_response.json()
    df = pd.DataFrame(data["series"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    df_final = pd.concat([df_final, df], ignore_index=True)


# print(response.status_code)
# print(response.json())
