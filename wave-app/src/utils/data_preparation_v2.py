import pandas as pd
import numpy as np
from sklearn import preprocessing

def handle_type(df):
    try:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['bright_ti4'] = pd.to_numeric(df['bright_ti4'], errors='coerce')
        df['acq_date'] = pd.to_datetime(df['acq_date'], errors='coerce')
        df['scan'] = pd.to_numeric(df['scan'], errors='coerce')
        df['track'] = pd.to_numeric(df['track'], errors='coerce')
        df['bright_ti5'] = pd.to_numeric(df['bright_ti5'], errors='coerce')
        df['frp'] = pd.to_numeric(df['frp'], errors='coerce')
        return df
    except Exception as e:
        raise e


def feature_engineering(df):
    try:
        df.rename({'acq_date': 'time'}, axis=1, inplace=True)
        df.confidence = df.confidence.replace({'l': 20, 'n': 60, 'h': 100, 'low': 20, 'nominal': 60, 'high': 100})
        df['est_fire_area'] = df['scan'] * df['track']
        df['est_brightness'] = (df['bright_ti4'] + df['bright_ti5'])/2
        df.latitude = df.latitude.round(1)
        df.longitude = df.longitude.round(1)
        if('type' in df.columns):
            df = df[df.type==0]
        return df
    except Exception as e:
        raise e


def add_counts(df):
    try:
        df_copy = df[['latitude', 'longitude', 'time','confidence',
                        'est_fire_area','est_brightness','frp']].copy()

        ## Add fire_count column
        count = df_copy.groupby(['latitude', 'longitude', 'time']).size().reset_index().rename(columns={0:'fire_count'})
        df_copy = df_copy.merge(count,how='outer', on=['latitude', 'longitude', 'time'])

        df_copy2 = df_copy.groupby(['latitude', 'longitude', 'time'])[['fire_count','confidence','est_brightness']].mean().reset_index()
        df_copy3 = df_copy.groupby(['latitude', 'longitude', 'time'])[['frp','est_fire_area']].sum().reset_index()

        df_copy = df_copy2.merge(df_copy3,how='outer', on=['latitude', 'longitude', 'time'])

        ## Add location count column
        count = df_copy.groupby(['latitude', 'longitude']).size().reset_index().rename(columns={0:'loc_count'})
        df_copy = df_copy.merge(count,how='outer', on=['latitude', 'longitude'])

        ## round values
        df_copy.est_fire_area = df_copy.est_fire_area.round(1)
        df_copy.est_brightness = df_copy.est_brightness.round(1)
        df_copy.confidence = df_copy.confidence.round().astype(int)
        df_copy.frp = df_copy.frp.round(1)
        df_copy.fire_count = df_copy.fire_count.round().astype(int)

        df = df_copy

        return df
    except Exception as e:
        raise e


def normalization(df):
    try:
        confidence_norm = preprocessing.normalize([df['confidence']], norm='max')
        frp_norm = preprocessing.normalize([df['frp']], norm='max')
        area_norm = preprocessing.normalize([df['est_fire_area']], norm='max')
        count_norm = preprocessing.normalize([df['fire_count']], norm='max')

        df['ranking'] = confidence_norm[0]*0.4 + frp_norm[0]*0.2 + area_norm[0]*0.2 + count_norm[0]*0.2

        df = df.sort_values(by=['ranking'], ascending=False)
        return df
    except Exception as e:
        raise e


def import_data(file):
    try:
        df = pd.read_csv(file, parse_dates=['acq_date'])
        return df
    except Exception as e:
        raise e


def save_data(df, path):
    try:
        df.to_csv(path, index=False, compression='gzip')
        df.to_csv(path, index=False)
    except Exception as e:
        raise e


def concat_df(df1, df2):
    try:
        df = pd.concat([df1, df2])
        return df
    except Exception as e:
        raise e


def run_preprocessor(file):
    df = import_data(file)
    df = handle_type(df)
    df = feature_engineering(df)
    df = add_counts(df)
    df = normalization(df)
    return df


def update_csv(file):
    output_path = "../../data/australia_viirs_prepared.csv.gz"
    df_old = import_data(output_path)
    df_new = run_preprocessor(file)
    df = concat_df(df_old, df_new)
    save_data(df, output_path)

