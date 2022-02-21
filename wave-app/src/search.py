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
    q.page['card1'] = ui.form_card(box=ui.box('content1'), items=[
        # ui.text_l("### Prediction"),
        ui.text_m("#### Predict by City and State"),
        ui.text_s("Enter the city and state of Australia"),
        ui.inline(items=[
            ui.textbox(name='textbox_required', label='City', required=True),
            ui.textbox(name='textbox_required', label='State', required=True),
        ]),
        ui.button(name='button', label='Predict', primary=True),
        # ui.text_m("#### Predict by Latitude and Longitude"),
        # ui.text_s("Enter a region within the range"),
        # ui.inline(items=[
        #     ui.textbox(name='textbox_required', label='Latitude', required=True),
        #     ui.textbox(name='textbox_required', label='Longitude', required=True),
        #     ui.button(name='button', label='')
        # ]),
    ])
    q.page['card2'] = ui.form_card(box=ui.box('content1'), items=[
        # ui.text_l("### Prediction"),
        ui.text_m("#### Predict by Latitude and Longitude"),
        ui.text_s("Enter the city and state of Australia"),
        ui.inline(items=[
            ui.textbox(name='textbox_required', label='Latitude', required=True),
            ui.textbox(name='textbox_required', label='Longitude', required=True),
        ]),
        ui.button(name='button', label='Predict', primary=True),
        # ui.text_m("#### Predict by Latitude and Longitude"),
        # ui.text_s("Enter a region within the range"),
        # ui.inline(items=[
        #     ui.textbox(name='textbox_required', label='Latitude', required=True),
        #     ui.textbox(name='textbox_required', label='Longitude', required=True),
        #     ui.button(name='button', label='')
        # ]),
    ])
    await q.page.save() 
