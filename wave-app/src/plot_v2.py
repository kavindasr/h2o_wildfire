import plotly
import plotly.express as px
from plotly.missing_ipywidgets import FigureWidget
import pandas as pd

token = "pk.eyJ1Ijoia3NycmFqIiwiYSI6ImNrenV6NTVvdDB1OXIyb21oemNtZWh1azcifQ._qZ-A6I3O8ky7XlABxUCNQ"

def show_bush_fires(df: pd.DataFrame):
    aus_fires = df.copy()
    
    sample = aus_fires[(aus_fires.time >= '2020-03-30') & (aus_fires.time <= '2020-03-31')]
    px.set_mapbox_access_token(token)
    fig = px.scatter_mapbox(sample, lat='latitude', lon='longitude', color='ranking', title="Wildfires in past 24 hours", size='est_fire_area', color_continuous_scale=px.colors.sequential.matter, size_max=15, zoom=3)
    return fig


# Convert plotly figure to html.
def to_html(fig: FigureWidget):
    #config = {'scrollZoom': False, 'showLink': False, 'displayModeBar': False}
    return plotly.io.to_html(fig, validate=False, include_plotlyjs='cdn')#, config=config)


