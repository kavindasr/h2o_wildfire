import pandas as pd
import numpy as np
from datetime import datetime

from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

def filterLocation(aus_fires,latitude,longitude):
    ## aus_fires = DataFrame
    filtered = aus_fires[(aus_fires.latitude == latitude)&(aus_fires.longitude == longitude)]
    return filtered

def predict_rank(filtered):
	df = filtered.filter(['time','ranking'])
	df.rename({'time': 'ds'}, axis=1, inplace=True)
	df.rename({'ranking': 'y'}, axis=1, inplace=True)

	# RESAMPLE DATA FROM DAILY TO MONTHLY
	df_m = df.copy()
	df_m.set_index('ds', inplace=True)
	df_m.index = pd.to_datetime(df_m.index)
	df_m = df_m.resample('1M').mean()

	df_m['y'] = df_m['y'].fillna(0)
	df_m.reset_index('ds', inplace=True)

	m = Prophet(yearly_seasonality=5,seasonality_mode='multiplicative')
	m.fit(df_m)

	future = m.make_future_dataframe(periods=6,freq = "m")
	forecast = m.predict(future)

	fig1 = plot_plotly(m, forecast)
	fig2 = plot_components_plotly(m, forecast)

	return fig1,fig2

def predict_area(filtered):
	df = filtered.filter(['time','est_fire_area'])
	df.rename({'time': 'ds'}, axis=1, inplace=True)
	df.rename({'est_fire_area': 'y'}, axis=1, inplace=True)

	# RESAMPLE DATA FROM DAILY TO MONTHLY
	df_m = df.copy()
	df_m.set_index('ds', inplace=True)
	df_m.index = pd.to_datetime(df_m.index)
	df_m = df_m.resample('1M').mean()

	df_m['y'] = df_m['y'].fillna(0)
	df_m.reset_index('ds', inplace=True)

	m = Prophet(yearly_seasonality=5,seasonality_mode='multiplicative')
	m.fit(df_m)

	future = m.make_future_dataframe(periods=6,freq = "m")
	forecast = m.predict(future)

	fig1 = plot_plotly(m, forecast)
	fig2 = plot_components_plotly(m, forecast)

	return fig1,fig2

def predict(aus_fires,lat,lng):
    filtered = filterLocation(aus_fires,lat,lng)
    
    if len(filtered.index)>= 10 :
    	fig1,fig2 = predict_rank(filtered)
    	fig3,fig4 = predict_area(filtered)

    	response = {
    	data: [fig1,fig2,fig3,fig4],
    	message: "Success"
    	}

    else:
    	response = {
    	data: filtered,
    	message: "No Enough Data to Predict the Future"
    	}

    return response
