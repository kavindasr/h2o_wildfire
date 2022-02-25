from h2o_wave import main, app, Q, ui
from .plot_v2 import *

BUSHFIRE_INFO = '''
### 2019–20 Australian bushfire season
From September 2019 until March 2020, when the final fire was extinguished, Australia had one of the worst bush fire seasons in its recorded history.
As it can be seen from the satellite dataset New South Wales and Victoria have been worst affected.
More than five million hectares, destroying more than 2,400 houses and forcing thousands to seek shelter elsewhere.
Source [wiki](https://en.wikipedia.org/wiki/2019%E2%80%9320_Australian_bushfire_season) [bbc](https://www.bbc.com/news/world-australia-50951043)
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