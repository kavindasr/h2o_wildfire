from h2o_wave import main, app, Q, ui
import os
from .ui_utils import make_markdown_table
import pandas as pd
from .utils.predict import predict
from plotly import io as pio


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
        ui.button(name='predict1', label='Predict', primary=True),
    ])

    q.page['card2'] = ui.form_card(box=ui.box('content1'), items=[
        # ui.text_l("### Prediction"),
        ui.text_m("#### Predict by Latitude and Longitude"),
        ui.text_s("Enter the city and state of Australia"),
        ui.inline(items=[
            ui.textbox(name='latitude', label='Latitude', required=True),
            ui.textbox(name='longitude', label='Longitude', required=True),
        ]),
        ui.button(name='predict2', label='Predict', primary=True),
    ])
    await q.page.save() 

    if q.args.predict1:
        print("button 1 clocked")

    if q.args.predict2:
        await predict_results(q, val)

async def predict_results(q:Q, val:str):
    df = q.app.datasets[val]
    print(q.args.latitude)
    data_latitude = q.args.latitude
    data_longitude = q.args.longitude
    print(data_longitude)
    
    # Update map card to notify that predictions are being made.
    q.page['search'] = ui.form_card(box='predict_res', items=[
        ui.progress(label=f'Making predictions for')
    ])
    await q.page.save()
    output = predict(df, -32.4,123.5)
    print(output["message"])
    if output["message"] == "Success":
        print("This is a success")
        html = pio.to_html(output["data"][0])

        q.page['search'] = ui.form_card(box='predict_res', items=[
            ui.frame(content=html, height='500px')
        ])
        await q.page.save()

    else:
        print("No data")

    

