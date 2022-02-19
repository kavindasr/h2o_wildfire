from h2o_wave import main, app, Q, ui
import os
from .ui_utils import make_markdown_table
from .plot import *
from .geo_api import get_address

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

    # Create columns for our issue table.
    columns = [
        ui.table_column(name='order', label='Order'),
        ui.table_column(name='location', label='Location', min_width="400px" ),
        ui.table_column(name='latitude', label='Latitude' ),
        ui.table_column(name='longitude', label='Longitude'),
        ui.table_column(name='confidence', label='Confidence', cell_type=ui.progress_table_cell_type()),
        ui.table_column(name='est_risk', label='Estimates Risk', cell_type=ui.progress_table_cell_type()),
    ]

    q.page['home'] = ui.form_card(box=ui.box('home'), items=[
        ui.text_l("### High Fire Alert Regions for Last 24 Hours"),
        ui.text_m("Considering most recent 24 hours data captured by VIIRS satellite following regions shows higher fire rates"),
        # ui.text(df_table),
        ui.table(
            name='issues',
            columns=columns,
            rows=[ui.table_row(
                name=f'{i}',
                cells=[str(i+1), get_address(df_values[i][0],df_values[i][1] ),str(df_values[i][0]), str(df_values[i][1]), str(df_values[i][4]/100), str(df_values[i][9])]
            ) for i in range(0,10)],
            downloadable=True,
            # width='1000px',
            )
    ])

    await q.page.save()

    # q.page['map'] = ui.wide_pie_stat_card(
    #     box=ui.box('map'),
    #     title='Wide Pie Stat',
    #     pies=[
    #         ui.pie(label='Category 1', value='35%', fraction=0.35, color='#2cd0f5', aux_value='$ 35'),
    #         ui.pie(label='Category 2', value='65%', fraction=0.65, color='$green', aux_value='$ 65'),
    #     ]
    # )

    # await q.page.save()

    # columns = 3
    # rows = 2

    # for column in range(1, columns + 1):
    #     for row in range(1, rows + 1):
    #         box = f'{column} {row} 1 1'
    #         q.page[f'card_{column}_{row}'] = ui.markdown_card(box=box, title=box, content='')

    # await q.page.save()

    # q.page['map'] = ui.meta_card(box=ui.box('map'), items=[
    #     ui.markdown_card(box='1 1 2 2', title="Hello", content="hhh")
    # ])

    q.page['topic'] = ui.form_card(box=ui.box('predict'), items=[
        ui.text_l("### High Fire Alert Regions for Last 24 Hours"),
    ])

    for i in range(0,5):
        q.page[f'card{i}'] = ui.form_card(box=ui.box('content1', width='250px', height='300px'),
                                        title='',
                                        items=[
                                            ui.text_m("### SYDNEY"),
                                            # ui.button(name='Sydney', label='SYDNEY', icon='Location', disabled=True),
                                            ui.separator(),
                                            # ui.button(name='standard_disabled_button', label='### Standard', disabled=True),
                                            ui.text_m("Tot Fire Count  : "),
                                            ui.text_m("Est Fire Area  :"),
                                            ui.text_m("Power(MegaWatt)  :"),
                                            ui.text_m("Brightness : "),
                                            ui.separator(),
                                            ui.slider(name='slider_disabled', label='Confidence', min=0, max=100, step=10, value=30,
                                            disabled=True),
                                        ],
                                        )

    # for i in range(5,10):
    #     q.page[f'card{i}'] = ui.form_card(box=ui.box('content2', width='250px', height='200px'), 
    #                                     title='',
    #                                     items=[
    #                                         ui.text_m("### High Fire Alert Regions for Last 24 Hours"),
    #                                     ])

    
    # q.page['card1'] = ui.tall_info_card(box=ui.box('content', width='200px', height='200px'), name='', 
    #                                     title='Card', caption='Lorem ipsum')
    # q.page['card2'] = ui.tall_info_card(box=ui.box('content', width='200px', height='200px'), name='',
    #                                     title='Card', caption='Lorem ipsum')
    # q.page['card3'] = ui.tall_info_card(box=ui.box('content', width='200px', height='200px'), name='',
    #                                     title='Card', caption='Lorem ipsum')
    # q.page['card4'] = ui.tall_info_card(box=ui.box('content', width='200px', height='200px'), name='',
    #                                     title='Card', caption='Lorem ipsum')
    # q.page['card5'] = ui.tall_info_card(box=ui.box('content', width='200px', height='200px'), name='',
    #                                     title='Card', caption='Lorem ipsum')
    # q.page['card6'] = ui.tall_info_card(box=ui.box('content', width='200px', height='200px'), name='',
    #                                     title='Card', caption='Lorem ipsum')                                    
                                        
    # q.page['quote'] = ui.markdown_card(
    #     box=ui.box('content'),
    #     title='Hello World',
    #     content='"The Internet? Is that thing still around?" - *Homer Simpson*',
    # )

    await q.page.save()
