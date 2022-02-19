import asyncio
import pandas as pd

from .utils.data_preparation_v2 import update_csv

url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Australia_NewZealand_24h.csv"
file_path = "../data/australia_viirs_prepared.csv.gz"


async def cronjob():
    while True:
        update_csv(url)
        print("Data updated")
        await asyncio.sleep(86400)

