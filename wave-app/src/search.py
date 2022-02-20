from h2o_wave import main, app, Q, ui
import os
from .ui_utils import make_markdown_table
import pandas as pd
# from .model import *


# Functions for data tab.

async def search(q:Q):
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
