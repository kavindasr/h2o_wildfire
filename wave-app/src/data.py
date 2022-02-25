from h2o_wave import main, app, Q, ui
import os
from .ui_utils import make_markdown_table
import pandas as pd
from .nasa_api import last_24h_data
# from .model import *


# Functions for data tab.

async def data(q:Q):
    # Get existing datasets for the app.
    app_datasets = list(q.app.datasets.keys())
    # Select dataset from user input or the first dataset.
    val = app_datasets[0]
    if q.args.describe:
        val = q.args.datasets

    # Display the head of the dataframe as a ui markdown table.
    df = q.app.datasets[val]
    df_head = df.sample(6)
    df_table = await make_markdown_table(
        fields=df_head.columns.tolist(),
        rows=df_head.values.tolist()
    )
    q.page['df'] = ui.form_card(box=ui.box('home'), items=[
        ui.combobox(name='datasets', label='Datasets', choices=app_datasets, value=val),
        ui.buttons(justify='center', items=[
            ui.button(name='describe', label='Describe', primary=True),
        ]),
        ui.text(open('markdowns/firms_info.md').read()),
        ui.separator(),
        ui.text(df_table),
    ])
    await q.page.save() 


# Init existing datasets for the app.
async def load_datasets(q: Q):
    q.app. datasets = {}
    data_dir = 'data'

    # For each csv.gz file in the data dir, make a dataframe and save it.
    for dataset_file in os.listdir(data_dir):
        # Read csv and make dataframe.
        path = f'{data_dir}/{dataset_file}'
        df = pd.read_csv(path, parse_dates=['time'])
        # Add this dataset to the list of app's datasets.
        q.app.datasets[path] = df

    q.app.datasets['last24h'] = last_24h_data()
