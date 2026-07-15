import pandas as pd
import numpy as np

def clean_and_aggregate(raw_csv_path):
    """
    Performs production-grade cleaning and monthly aggregation.
    """
    df = pd.read_csv(raw_csv_path, sep=None, engine='python', na_values=['?'])
    df.columns = df.columns.str.strip()
    
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['DateTime'])
    df.set_index('DateTime', inplace=True)
    df.drop(columns=['Date', 'Time'], errors='ignore', inplace=True)
    
    df['Global_active_power'] = pd.to_numeric(df['Global_active_power'], errors='coerce')
    df['Global_active_power'] = df['Global_active_power'].ffill()
    df = df[~df.index.duplicated(keep='first')]
    
    clean_monthly = (df['Global_active_power'].resample('ME').sum() / 60.0).to_frame(name='predicted_units')
    return clean_monthly.dropna()
