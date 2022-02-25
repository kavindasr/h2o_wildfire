import asyncio
import pandas as pd

from .utils.data_preparation_v2 import update_csv, run_preprocessor

url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Australia_NewZealand_24h.csv"


async def cronjob():
    while True:
        print("started")
        update_csv(url)
        print("Data updated")
        await asyncio.sleep(86400)


def last_24h_data():
    df = run_preprocessor(url)
    return df
