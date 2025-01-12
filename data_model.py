import pandas as pd
import numpy as np

df = pd.read_csv("data/da_prices.csv", delimiter=";")
df.drop(
    columns=[
        "∅ Anrainer DE/LU [€/MWh] Originalauflösungen",
        "Belgien [€/MWh] Originalauflösungen",
        "Dänemark 1 [€/MWh] Originalauflösungen",
        "Dänemark 2 [€/MWh] Originalauflösungen",
        "Frankreich [€/MWh] Originalauflösungen",
        "Niederlande [€/MWh] Originalauflösungen",
        "Norwegen 2 [€/MWh] Originalauflösungen",
        "Österreich [€/MWh] Originalauflösungen",
        "Polen [€/MWh] Originalauflösungen",
        "Schweden 4 [€/MWh] Originalauflösungen",
        "Schweiz [€/MWh] Originalauflösungen",
        "Tschechien [€/MWh] Originalauflösungen",
        "DE/AT/LU [€/MWh] Originalauflösungen",
        "Italien (Nord) [€/MWh] Originalauflösungen",
        "Slowenien [€/MWh] Originalauflösungen",
        "Ungarn [€/MWh] Originalauflösungen",
    ],
    inplace=True,
)

df.rename(
    columns={
        "Deutschland/Luxemburg [€/MWh] Originalauflösungen": "price [€/MWh]",
        "Datum von": "Date_from",
        "Datum bis": "Date_to",
    },
    inplace=True,
)

df[["Date_from", "Date_to"]] = df[["Date_from", "Date_to"]].apply(
    pd.to_datetime, format="%d.%m.%Y %H:%M"
)

print(df.columns)
