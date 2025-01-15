import requests
import json
import pandas as pd
from datetime import datetime

timestamp_response = requests.get(
    "https://smard.api.proxy.bund.dev/app/chart_data/4169/DE/index_hour.json"
)
timestamps = timestamp_response.json()

print(type(timestamps))

timeseries_response = requests.get(
    "https://smard.api.proxy.bund.dev/app/chart_data/4169/DE/4169_DE_hour_1736722800000.json"
)

df_timestamps = pd.DataFrame(timestamps["timestamps"], columns=["timestamps"])
df_timestamps["timestamps"] = pd.to_datetime(df_timestamps["timestamps"], unit="ms")
data = timeseries_response.json()

df = pd.DataFrame(data["series"], columns=["timestamp", "price"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
print(df_timestamps)

# print(response.status_code)
# print(response.json())
