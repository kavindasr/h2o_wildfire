from h2o_wave import main, app, Q, ui
from sklearn.linear_model import HuberRegressor
import asyncio

from .ui_utils import *
from .initializers import *
from . import data, home, predict, search, about
from .nasa_api import cronjob

task = asyncio.create_task(cronjob())

@app('/')
async def serve(q: Q):
    # Initialize app and client if not already initialized.
    if not q.app.initialized:
        await init_app(q)

    if not q.client.initialized:
        await init_client(q)

    # Attach a flex layout for the cards.
    await layouts(q)

    # Check which tab is active and invoke the corresponding handler.
    await handler(q)

# A FLEX LAYOUT FOR AN ADAPTIVE UI
async def layouts(q:Q):
    q.page['meta'] = ui.meta_card(box='', theme='h2o-dark', title = 'Australia WildFire Predictor | Team DeepMind', layouts=[
        # Apply layout to all viewport widths.
        ui.layout(breakpoint='xs', zones=[
            # Predefine app's wrapper height to 100% viewpoer height.
            ui.zone(name='main', size='100vh', zones=[
                # Zone for the header.
                ui.zone(name='header', size='80px'),
                # Zone for navigation menu.
                ui.zone('tabs'),
                # Zone for the actual content and data.
                ui.zone(name='body', size='1', zones=[
                    ui.zone(name='home'),
                    ui.zone('predict', align='center'),
                    ui.zone(name='map'),
                    ui.zone(
                        name='content1',
                        direction=ui.ZoneDirection.ROW,
                        # Specify a zone size, otherwise will be adapted to the biggest card in the zone.
                        #size='500px', 
                        # Align cards on the cross-axis (vertical direction for ROW and horizontal for COLUMN).
                        align='center', 
                        # Align cards on the main-axis (vertical direction for COLUMN and horizontal for ROW).
                        justify='around' 
                    ),
                    ui.zone(
                        name='content2',
                        direction=ui.ZoneDirection.ROW,
                        # Specify a zone size, otherwise will be adapted to the biggest card in the zone.
                        #size='500px', 
                        # Align cards on the cross-axis (vertical direction for ROW and horizontal for COLUMN).
                        align='center', 
                        # Align cards on the main-axis (vertical direction for COLUMN and horizontal for ROW).
                        justify='around' 
                    ),
                    ui.zone(name='predict_res1'),
                    ui.zone(name='predict_res2'),
                ]),
                # App footer of fixed sized, aligned in the center.
                ui.zone(name='footer', size='120px', align='center')
            ])
        ])
    ])

# Handler for tab content.
async def handler(q: Q):
    # Clear ui, delete pages/cards of other tabs.
    await reset_pages(q)

    # Set the current tab to the user-selected tab, otherwise stay on the same tab.
    q.client.tabs = q.args.tabs or q.client.tabs

    # Display the menu bar with different tabs.
    await render_menu(q)

    # Handler for each tab / menu option.
    if q.client.tabs == "home":
        await home.home(q)

    elif q.client.tabs == "search":
        await search.search(q)

    elif q.client.tabs == "predict":
        await predict.predict(q)

    elif q.client.tabs == "model":
        await about.about(q)
