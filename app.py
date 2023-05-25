"""Creates an interactive website displaying characteristics of electric vehicles"""

# Import Libraries
import pandas as pd 
import numpy as np
import streamlit as st
import plotly_express as px


# Read in dataset
url = 'https://raw.githubusercontent.com/kellyshreeve/Web-App-Project/main/ElectricCarData_Clean.csv'
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

st.header('Price, Efficiency, and Range of EVs by Brand') # Create header

# Create top brands data frame 
top_brands = ev[(ev['brand']=='Tesla ') | (ev['brand']=='Audi ') | (ev['brand']=='Nissan ') 
                | (ev['brand']=='Volkswagen ') | (ev['brand']=='Skoda ') | (ev['brand']=='Renault ') 
                | (ev['brand']=='Porsche ') | (ev['brand']=='BMW ') | (ev['brand']=='Ford ')
                | (ev['brand']=='Kia ') | (ev['brand']=='Smart ') | (ev['brand']=='Byton ')
                | (ev['brand']=='Mercedes ') | (ev['brand']=='Hyundai ') | (ev['brand']=='Opel ')] 

# Create a bar chart of average price by brand
price_bar = px.histogram(top_brands, x='brand', y='price_euro', histfunc='avg', 
                          title='Average Price by Brand of EVs', text_auto='.2s',
                          labels={'price_euro':'Price (Euros)', 'brand':'Brand Name'},
                          color_discrete_sequence=[px.colors.qualitative.Plotly[7]],
                          width=800, height=500)

price_bar.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
}) # Turn off background color

price_bar.update_traces(textfont_size=11, textposition='outside') # Add labels above bars

price_bar.update_layout(xaxis={'categoryorder':'total descending'}) # Arrange in order from expensive to inexpensive

price_bar.update_xaxes(showgrid=False) # Turn off x grid
price_bar.update_yaxes(showgrid=False) # Turn off y grid

st.plotly_chart(price_bar)


