from h2o_wave import main, app, Q, ui, data
import random
import os
from .ui_utils import make_markdown_table
from .plot import *
from .geo_api import get_address, get_res
from .utils.filter_location import main

# Functions for data tab.

async def home(q:Q):

    q.page['home'] = ui.form_card(box='home', items=[
        ui.progress(label='Loading dashboard data... ')
    ])
    await q.page.save()

    # Get existing datasets for the app.
    app_datasets = list(q.app.datasets.keys())
    # Select dataset from user input or the first dataset.
    val = app_datasets[0]
    if q.args.describe:
        val = q.args.datasets

    # Display the head of the dataframe as a ui markdown table.
    df = q.app.datasets[val]
    df_sort = df.sort_values(["ranking"],ascending = False)
    df_head = df_sort.head(10)
    df_values = df_head.values.tolist()

    # Retrive the location name using the geo API
    url_list = []

    for i in range(0,10):
        url = f"https://nominatim.openstreetmap.org/reverse?lat={df_values[i][0]}&lon={df_values[i][1]}&format=json"
        url_list.append(url)

    location_response = get_res(url_list)

    # Create columns for our issue table.
    columns = [
        ui.table_column(name='order', label='Order'),
        ui.table_column(name='location', label='Location', min_width="450px" ),
        ui.table_column(name='latitude', label='Latitude' ),
        ui.table_column(name='longitude', label='Longitude'),
        ui.table_column(name='est_burned', label='Est Burned Area(kha) '),
        ui.table_column(name='confidence', label='Confidence', cell_type=ui.progress_table_cell_type(color="#FFFF00"), sortable=True),
        ui.table_column(name='est_risk', label='Estimated Risk', cell_type=ui.progress_table_cell_type(color="#FF0000"), sortable=True),
    ]

    q.page['home'] = ui.form_card(box=ui.box('home'), items=[
        ui.text_l("### High Fire Alert Regions for Last 24 Hours"),
        ui.text_m("Considering most recent 24 hours data captured by VIIRS satellite following regions shows higher fire rates"),
        # ui.text(df_table),
        ui.table(
            name='stats',
            columns=columns,
            rows=[ui.table_row(
                name=f'{i}',
                cells=[str(i+1), location_response[i],str(df_values[i][0]), str(df_values[i][1]),str(round(df_values[i][7]/10,3)), str(df_values[i][4]/100), str(df_values[i][9])]
            ) for i in range(0,10)],
            downloadable=True,
            # width='1000px',
            )
    ])

    await q.page.save()

    #Get top 4 frequent fire regions
    df_freq = df.sort_values(["loc_count"],ascending = False)
    df_freq = df_freq.drop_duplicates(subset = ["latitude"])
    df_freq = df_freq.head(4).values.tolist()

    freq_url_list = []

    for i in range(0,4):
        frq_url = f"https://nominatim.openstreetmap.org/reverse?lat={df_freq[i][0]}&lon={df_freq[i][1]}&format=json"
        freq_url_list.append(frq_url)

    freq_location_response = get_res(freq_url_list)

    q.page['topic'] = ui.form_card(box=ui.box('predict'), items=[
        ui.text_l("### Frequent Fire Ocurring Regions"),
    ])

    for i in range(0,2):
        df_filter = main(df, df_freq[i][0],df_freq[i][1])
        df_filter['ds'] = df_filter['ds'].astype(str)

        q.page[f'card{i}'] = ui.form_card(box=ui.box('content1', width='600px'),
                                        title='',
                                        items=[
                                            ui.inline(items=[
                                                ui.button(name='button', icon='Location', caption='Tooltip on hover', disabled=True),
                                                ui.text_m(f'### {i+1}-{freq_location_response[i].split(",")[0]}'),
                                            ]),
                                            ui.separator(),
                                            ui.slider(name='slider_disabled', label='Estimated Risk', min=0, max=100, step=10, value=int(df_freq[i][9]*100),disabled=True, width='400px'),
                                            ui.inline(items=[
                                                ui.text_m('- Total Fire Count(since 2013)'),
                                                ui.text_l(f'{str(df_freq[i][3])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_m('- Total Burned Fire Area(kha)'),
                                                ui.text_l(f'{str(df_freq[i][7]/10)}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_m('- Total Radiative Power(MegaWatt)'),
                                                ui.text_l(f'{str(df_freq[i][6])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_m('- Mean Brightness'),
                                                ui.text_l(f'{str(df_freq[i][5])}'),
                                            ]),
                                            ui.separator(),
                                            ui.text_m('### Weekly Estimated Risk Chart since 2012'),
                                            ui.visualization(
                                                plot=ui.plot([
                                                    ui.mark(type='area', x_scale='time', x='=ds', y='=y',x_title='Weeks',y_title='Estimated Risk',curve='smooth', y_min=0),
                                                    ui.mark(type='line', x='=ds', y='=y', curve='smooth')
                                                ]),
                                                data=data(
                                                    fields=df_filter.columns.tolist(),
                                                    rows=df_filter.values.tolist(),
                                                    pack=True,
                                                ),
                                            ),
                                        ],
                                        )
    await q.page.save()

    for i in range(2,4):
        df_filter = main(df, df_freq[i][0],df_freq[i][1])
        df_filter['ds'] = df_filter['ds'].astype(str)

        q.page[f'card{i}'] = ui.form_card(box=ui.box('content2', width='600px'),
                                        title='',
                                        items=[
                                            ui.inline(items=[
                                                ui.button(name='button', icon='Location', caption='Tooltip on hover', disabled=True),
                                                ui.text_m(f'### {i+1}-{freq_location_response[i].split(",")[0]}'),
                                            ]),
                                            ui.separator(),
                                            ui.slider(name='slider_disabled', label='Estimated Risk', min=0, max=100, step=10, value=int(df_freq[i][9]*100),disabled=True, width='400px'),
                                            ui.inline(items=[
                                                ui.text_m('- Total Fire Count(since 2012)'),
                                                ui.text_l(f'{str(df_freq[i][3])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_m('- Total Burned Fire Area(kha)'),
                                                ui.text_l(f'{str(df_freq[i][7]/10)}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_m('- Total Radiative Power(MegaWatt)'),
                                                ui.text_l(f'{str(df_freq[i][6])}'),
                                            ]),
                                             ui.inline(items=[
                                                ui.text_m('- Mean Brightness'),
                                                ui.text_l(f'{str(df_freq[i][5])}'),
                                            ]),
                                            ui.separator(),
                                            ui.text_m('### Weekly Estimated Risk Chart since 2013'),
                                            ui.visualization(
                                                plot=ui.plot([
                                                    ui.mark(type='area', x_scale='time', x='=ds', y='=y', x_title='Weeks',y_title='Estimated Risk',curve='smooth', y_min=0),
                                                    ui.mark(type='line', x='=ds', y='=y', curve='smooth')
                                                ]),
                                                data=data(
                                                    fields=df_filter.columns.tolist(),
                                                    rows=df_filter.values.tolist(),
                                                    pack=True,
                                                ),
                                            ),
                                        ],
                                        )

    await q.page.save()