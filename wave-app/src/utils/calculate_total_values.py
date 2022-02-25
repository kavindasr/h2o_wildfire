import pandas as pd
import numpy as np

# get total count
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