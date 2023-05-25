# Import Libraries
import pandas as pd 
import numpy as np
import plotly.express as px

# Read in dataset
url = 'https://raw.githubusercontent.com/kellyshreeve/Web-App-Project/main/ElectricCarData_Clean.csv?token=GHSAT0AAAAAACC2O2SU3UV3WOYKFXLLDT4KZDPW2XA'
ev = pd.read_csv(url)

# Rename columns with snake case
ev = ev.rename(
    columns={'Brand':'brand',
             'Model':'model',
             'AccelSec':'accel_sec',
             'TopSpeed_KmH':'top_speed_kmh',
             'Range_Km':'range_km',
             'Efficiency_WhKm':'efficiency_whkm',
             'FastCharge_KmH':'fast_charge_kmh',
             'RapidCharge':'rapid_charge',
             'PowerTrain':'power_train',
             'PlugType':'plug_type',
             'BodyStyle':'body_style',
             'Segment':'segment',
             'Seats':'seats',
             'PriceEuro':'price_euro'
             }
)

# Clean duplicates and missing values
ev['fast_charge_kmh'] = ev['fast_charge_kmh'].replace('-', np.NaN) # Change '-' to NaN

ev['fast_charge_kmh'] = pd.to_numeric(ev['fast_charge_kmh']) # Change fast_charge_kmh to int type data

ev = ev.drop_duplicates(subset=['brand', 'model']).reset_index(drop=True)

