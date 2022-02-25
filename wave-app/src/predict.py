from h2o_wave import main, app, Q, ui
from .plot_v2 import *

BUSHFIRE_INFO = '''
## Wildfire Map of Last 24 Hours

- #### In Australia the peak fire season typically begins in early August and lasts around 27 weeks.
- #### There were 66,510 VIIRS fire alerts reported between 1st of March 2021 and 21st of February 2022 considering high confidence alerts only.
- #### In Australia, 600kha of land has burned so far in 2021.

'''

async def predict(q: Q):
     # Get existing datasets for the app.
    app_datasets = list(q.app.datasets.keys())
    # Select dataset from user input or the first dataset.
    val = app_datasets[1]
    if q.args.describe:
        val = q.args.datasets

    # Display the head of the dataframe as a ui markdown table.
    df = q.app.datasets[val]
    # Update map card to notify scatter plot is being made.
    q.page['map'] = ui.form_card(box='map', items=[
        ui.progress(label='Making a Scatter Plot...')
    ])
    await q.page.save()

    # Make scatter plot for the 2019-2020 bushfire season.
    fig = await q.run(show_bush_fires, df)
    # Convert plotly figure to html.
    html = await q.run(to_html, fig)
    # Render figure's html on on the form card.
    q.page['map'] = ui.form_card(box=ui.box('map', order=2), items=[
        ui.text(BUSHFIRE_INFO),
        ui.frame(content=html, height='600px'),
        ui.message_bar(type='info', text=open('markdowns/acknowledgement.md').read()),
    ])
    await q.page.save() 