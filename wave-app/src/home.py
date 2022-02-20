from h2o_wave import main, app, Q, ui
import os
from .ui_utils import make_markdown_table
from .plot import *
from .geo_api import get_address, get_res
from .utils.filter_location import filter_data

# Functions for data tab.

async def home(q:Q):
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
    df_table = await make_markdown_table(
        fields=df_head.columns.tolist(),
        rows=df_head.values.tolist()
    )

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
                cells=[str(i+1), location_response[i],str(df_values[i][0]), str(df_values[i][1]), str(df_values[i][4]/100), str(df_values[i][9])]
            ) for i in range(0,10)],
            downloadable=True,
            # width='1000px',
            )
    ])

    await q.page.save()

    q.page['topic'] = ui.form_card(box=ui.box('predict'), items=[
        ui.text_l("### More on High Fire Alert Regions"),
    ])

    for i in range(0,5):
        q.page[f'card{i}'] = ui.form_card(box=ui.box('content1', width='250px', height='350px'),
                                        title='',
                                        items=[
                                            ui.inline(items=[
                                                ui.button(name='button', icon='Location', caption='Tooltip on hover', disabled=True),
                                                ui.text_m(f'### {i+1}-{location_response[i].split(",")[0]}'),
                                            ]),
                                            ui.separator(),
                                            ui.inline(items=[
                                                ui.text_s('Total Fire Count'),
                                                ui.text_l(f'{str(df_values[i][3])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_s('Estimated Fire Area'),
                                                ui.text_l(f'{str(df_values[i][7])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_s('Power(MegaWatt)'),
                                                ui.text_l(f'{str(df_values[i][6])}'),
                                            ]),
                                             ui.inline(items=[
                                                ui.text_s('Brightness'),
                                                ui.text_l(f'{str(df_values[i][5])}'),
                                            ]),
                                            ui.separator(),
                                            ui.slider(name='slider_disabled', label='Confidence', min=0, max=100, step=10, value=df_values[i][4],
                                            disabled=True),
                                        ],
                                        )

    for i in range(5,10):
        q.page[f'card{i}'] = ui.form_card(box=ui.box('content2', width='250px', height='350px'),
                                        title='',
                                        items=[
                                            ui.inline(items=[
                                                ui.button(name='button', icon='Location', caption='Tooltip on hover', disabled=True),
                                                ui.text_m(f'### {i+1}-{location_response[i].split(",")[0]}'),
                                            ]),
                                            ui.separator(),
                                            ui.inline(items=[
                                                ui.text_s('Total Fire Count'),
                                                ui.text_l(f'{str(df_values[i][3])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_s('Estimated Fire Area'),
                                                ui.text_l(f'{str(df_values[i][7])}'),
                                            ]),
                                            ui.inline(items=[
                                                ui.text_s('Power(MegaWatt)'),
                                                ui.text_l(f'{str(df_values[i][6])}'),
                                            ]),
                                             ui.inline(items=[
                                                ui.text_s('Brightness'),
                                                ui.text_l(f'{str(df_values[i][5])}'),
                                            ]),
                                            ui.separator(),
                                            ui.slider(name='slider_disabled', label='Confidence', min=0, max=100, step=10, value=df_values[i][4],
                                            disabled=True),
                                        ],
                                        )

    await q.page.save()

    print(filter_data(df, -29.5, 123.9))
