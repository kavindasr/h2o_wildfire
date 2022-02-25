import pandas as pd
from datetime import date

def total_values(df):
    total_fire_count = df['fire_count'].sum()
    total_frp = df['frp'].sum().round(2)
    total_est_fire_area = df['est_fire_area'].sum().round(2)

    response = {
        'total_fire_count': total_fire_count,
        'total_frp': total_frp,
        'total_est_fire_area': total_est_fire_area
    }
    return response

def filterLocation(aus_fires,latitude,longitude):
    ## aus_fires = DataFrame
    filtered = aus_fires[(aus_fires.latitude == latitude)&(aus_fires.longitude == longitude)]
    return filtered


def main(aus_fires,lat,lng):
    filtered = filterLocation(aus_fires,lat,lng)
    tot_val = total_values(filtered)

    df = filtered.filter(['time','ranking'])
    df.rename({'time': 'ds'}, axis=1, inplace=True)
    df.rename({'ranking': 'y'}, axis=1, inplace=True)

    # RESAMPLE DATA FROM DAILY TO WEEKLY
    df_w = df.copy()
    df_w.set_index('ds', inplace=True)
    df_w.index = pd.to_datetime(df_w.index)
    df_w = df_w.resample('1W').mean()
    df_w['y'] = df_w['y'].fillna(0)

    # Add missing weeks
    max_date = df.ds.max()
    end = date.today()
    if (max_date<end):
        print('hiiiiii')
        r = pd.date_range(start=df.ds.min(), end=end,freq='W')
        df_w = df_w.reindex(r).fillna(0.0).rename_axis('ds').reset_index()
        print(df_w)
        print(type(df_w))
    else:
        df_w.reset_index('ds', inplace=True)

    response = {'df':df_w, 'tot_val':tot_val}
    print(type(response['df']))
    return response