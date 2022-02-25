from h2o_wave import main, app, Q, ui
import os
from .ui_utils import make_markdown_table
import pandas as pd
from .utils.predict import main
from plotly import io as pio
from .geo_api import get_location


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
   
    q.page['card1'] = ui.form_card(box=ui.box('content1'), items=[
        # ui.text_l("### Prediction"),
        ui.text_m("#### Predict by City and State"),
        ui.text_s("Enter the city and state of Australia"),
        ui.inline(justify='center',items=[
            ui.textbox(name='city', label='City', required=True),
            ui.textbox(name='state', label='State', required=True),
        ]),
        ui.inline(justify='center', items=[
            ui.button(name='predict1', label='Predict', primary=True),
        ])
    ])

    q.page['card2'] = ui.form_card(box=ui.box('content1'), items=[
        # ui.text_l("### Prediction"),
        ui.text_m("#### Predict by Latitude and Longitude"),
        ui.text_s("Enter the Latitude and Longitude within Autralia"),
        ui.inline(justify='center', items=[
            ui.textbox(name='latitude', label='Latitude', required=True, placeholder="Enter a value in range (-40, -9)", width="250px"),
            ui.textbox(name='longitude', label='Longitude', required=True, placeholder="Enter a value in range (112, 155)", width="250px"),
        ]),
        ui.inline(justify='center', items=[
            ui.button(name='predict2', label='Predict', primary=True),
        ]) 
    ])
    await q.page.save() 

    if q.args.predict1:
        await predict_results_by_loc(q,val)

    if q.args.predict2:
        await predict_results_by_cor(q,val)

async def predict_results_by_loc(q:Q, val:str):
    df = q.app.datasets[val]
    data_city = q.args.city
    data_state = q.args.state
    
    q.page['search'] = ui.form_card(box='predict_res1', items=[
        ui.progress(label=f'Making predictions for Location ({data_city},{data_state})')
    ])
    await q.page.save()

    loc_res = get_location(data_city, data_state)
    print(loc_res)

    if (loc_res == "NotFound"):
        q.page['search'] = ui.form_card(box='predict_res1', items=[
            ui.message_bar(type='warning', text="This location is not found. Please Try Again"),
        ])
        await q.page.save()
    else:
        latitu = round(float(loc_res[0]),1)
        longi = round(float(loc_res[1]),1)
        print(latitu)
        print(longi)

    output = main(df, latitu,longi)

    if output["message"] == "Success":
        html_fig1 = pio.to_html(output["data"][0])
        html_fig3 = pio.to_html(output["data"][2])

        q.page['search'] = ui.form_card(box='predict_res1', items=[
            ui.text(f'## Prediction of the Location ({latitu},{longi}) for next 12 months'),
            ui.text("## Predicted Estimated Risk"),
            ui.inline(justify='center', items=[
                ui.frame(content=html_fig1, width='1000px', height="600px"),
            ])        
        ])
        await q.page.save()

        q.page['home'] = ui.form_card(box='predict_res2', items=[
            ui.text("## Predicted Burned Fire Area"),
            ui.inline(justify='center', items=[
                ui.frame(content=html_fig3, width='1000px', height="600px")
            ])
        ])
        await q.page.save()

    else:
        q.page['search'] = ui.form_card(box='predict_res1', items=[
             ui.message_bar(type='warning', text=output["message"]),
        ])
        await q.page.save()

async def predict_results_by_cor(q:Q, val:str):
    df = q.app.datasets[val]
    data_latitude = round(float(q.args.latitude.strip()),1)
    data_longitude = round(float(q.args.longitude.strip()),1)
    
    q.page['search'] = ui.form_card(box='predict_res1', items=[
        ui.progress(label=f'Making predictions for Location ({data_latitude},{data_longitude})')
    ])
    await q.page.save()

    output = main(df, data_latitude,data_longitude)

    if output["message"] == "Success":
        html_fig1 = pio.to_html(output["data"][0])
        html_fig3 = pio.to_html(output["data"][2])

        q.page['search'] = ui.form_card(box='predict_res1', items=[
            ui.text(f'## Prediction of the Location ({data_latitude},{data_longitude}) for next 12 months'),
            ui.text("## Predicted Estimated Risk"),
            ui.inline(justify='center', items=[
                ui.frame(content=html_fig1, width='1000px', height="630px"),
            ])
            
        ])
        await q.page.save()

        q.page['home'] = ui.form_card(box='predict_res2', items=[
            ui.text("## Predicted Burned Fire Area"),
            ui.inline(justify='center', items=[
                ui.frame(content=html_fig3, width='1000px', height="630px")
            ])
            
        ])
        await q.page.save()

    else:
        q.page['search'] = ui.form_card(box='predict_res1', items=[
             ui.message_bar(type='warning', text=output["message"]),
        ])
        await q.page.save()


    

