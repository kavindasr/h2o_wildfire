import pandas as pd

def filterLocation(aus_fires,latitude,longitude):
    ## aus_fires = DataFrame
    filtered = aus_fires[(aus_fires.latitude == latitude)&(aus_fires.longitude == longitude)]
    return filtered


def filter_data(aus_fires,lat,lng):
    filtered = filterLocation(aus_fires,lat,lng)

    df = filtered.filter(['time','ranking'])
    df.rename({'time': 'ds'}, axis=1, inplace=True)
    df.rename({'ranking': 'y'}, axis=1, inplace=True)

    # RESAMPLE DATA FROM DAILY TO WEEKLY
    df_w = df.copy()
    df_w.set_index('ds', inplace=True)
    df_w.index = pd.to_datetime(df_w.index)
    df_w = df_w.resample('1W').mean()

    df_w['y'] = df_w['y'].fillna(0)

    df_w.reset_index('ds', inplace=True)

    return df_w