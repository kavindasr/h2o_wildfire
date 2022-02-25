import pandas as pd
import numpy as np
from datetime import date

from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly


def filterLocation(aus_fires, latitude, longitude):
    ## aus_fires = DataFrame
    filtered = aus_fires[(aus_fires.latitude == latitude)
                         & (aus_fires.longitude == longitude)]
    return filtered


def predict_rank(filtered):
    df = filtered.filter(['time', 'ranking'])
    df.rename({'time': 'ds'}, axis=1, inplace=True)
    df.rename({'ranking': 'y'}, axis=1, inplace=True)

    fig1, fig2 = predict(df)

    return fig1, fig2


def predict_area(filtered):
    df = filtered.filter(['time', 'est_fire_area'])
    df.rename({'time': 'ds'}, axis=1, inplace=True)
    df.rename({'est_fire_area': 'y'}, axis=1, inplace=True)

    fig1, fig2 = predict(df)
    return fig1, fig2


def predict(df):
    # RESAMPLE DATA FROM DAILY TO MONTHLY
    df_m = df.copy()
    df_m.set_index('ds', inplace=True)
    df_m.index = pd.to_datetime(df_m.index)
    df_m = df_m.resample('1M').mean()
    df_m['y'] = df_m['y'].fillna(0)

    # Add missing months
    max_date = df.ds.max()
    end = date.today()
    if (max_date < end):
        r = pd.date_range(start=df.ds.min(), end=end, freq='M')
        df_m = df_m.reindex(r).fillna(0.0).rename_axis('ds').reset_index()
    else:
        df_m.reset_index('ds', inplace=True)

    m = Prophet(weekly_seasonality=False,daily_seasonality = False)
    m.add_seasonality(name='yearly', period=356, fourier_order=30)
    m.fit(df_m)

    future = m.make_future_dataframe(periods=12, freq="m")
    forecast = m.predict(future)
    table = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)

    fig1 = plot_plotly(m, forecast)
    fig2 = plot_components_plotly(m, forecast)

    return fig1, fig2, table


def main(aus_fires, lat, lng):
    filtered = filterLocation(aus_fires, lat, lng)

    if len(filtered.index) >= 10:
        fig1, fig2, table1 = predict_rank(filtered)
        fig3, fig4, table2 = predict_area(filtered)

        response = {
            "data": [fig1, fig2, fig3, fig4],
            "table": [table1,table2]
            "message": "Success"
        }

    else:
        response = {
            "data": filtered,
            "message": "No Enough Data to Predict the Future"
        }

    return response
