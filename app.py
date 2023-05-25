"""Creates an interactive website displaying characteristics of electric vehicles"""

# Import Libraries
import pandas as pd 
import numpy as np
import streamlit as st
import plotly_express as px

# Set Application Name
st.set_page_config(page_title='Electric Vehicle Data Visualizations')

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


# Centered Title
st.markdown('<div style="text-align: center:">Price, Efficiency, and Range of EVs by Brand and Body Style</div>', unsafe_allow_html=True)


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


# Create bar chart of average efficiency by brand 
eff_bar = px.histogram(top_brands, x='brand', y='efficiency_whkm', histfunc='avg', 
                          title='Average Efficiency by Brand of EVs', text_auto='.2s',
                          labels={'efficiency_whkm':'Efficiency (WhKm)', 'brand':'Brand Name'},
                          color_discrete_sequence=[px.colors.qualitative.Plotly[7]],
                          width=800, height=500)

eff_bar.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
}) 

eff_bar.update_traces(textfont_size=11, textposition='outside')

eff_bar.update_layout(xaxis={'categoryorder':'array', 'categoryarray':
    ['Porsche ', 'Audi ', 'Tesla ', 'Mercedes ', 'Byton ', 'Ford ', 'BMW ',
     'Nissan ', 'Skoda ', 'Hyundai ', 'Kia ', 'Opel ', 'Volkswagen ', 'Renault ', 'Smart ']}) 

eff_bar.update_xaxes(showgrid=False)
eff_bar.update_yaxes(range=[0,250], showgrid=False) # Set y axis range


# Create a bar chart of average range by brand
range_bar = px.histogram(top_brands, x='brand', y='range_km', histfunc='avg', 
                          title='Average Range by Brand of EVs', text_auto='.2s',
                          labels={'range_km':'Range (Km)', 'brand':'Brand Name'},
                          color_discrete_sequence=[px.colors.qualitative.Plotly[7]],
                          width=800, height=500)

range_bar.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
})

range_bar.update_traces(textfont_size=11, textposition='outside')

range_bar.update_layout(xaxis={'categoryorder':'array', 'categoryarray':
    ['Porsche ', 'Audi ', 'Tesla ', 'Mercedes ', 'Byton ', 'Ford ', 'BMW ',
     'Nissan ', 'Skoda ', 'Hyundai ', 'Kia ', 'Opel ', 'Volkswagen ', 'Renault ', 'Smart ']})

range_bar.update_xaxes(showgrid=False)
range_bar.update_yaxes(showgrid=False)

# Drop down menu
# option = st.selectbox('Choose characteristic:', ('Price', 'Efficiency', 'Range'))

# Create Header 
st.header('By Brand')

# Radio Buttons
option = st.radio(label='Choose characteristic:', options=['Price', 'Efficiency', 'Range'])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

if option == 'Price':
    st.subheader('Average Price by Brand') # Create header
    st.plotly_chart(price_bar)
elif option == 'Efficiency':
    st.subheader('Average Efficiency by Brand') # Create header
    st.plotly_chart(eff_bar)
elif option == 'Range':
    st.subheader('Average Range by Brand') # Create header
    st.plotly_chart(range_bar)

# Header for scatter plot 
st.header('Efficiency by Price')

# Create a scatter plot of efficiency by price
price_efficiency = px.scatter(data_frame=ev, title='Efficiency vs Price for EVs', x='price_euro', y='efficiency_whkm', 
           labels={'price_euro':'Price Euro', 'efficiency_whkm':'Efficiency WhKm'},
           color='brand', width=900, height=500)

price_efficiency.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
})

price_efficiency.update_xaxes(range=[0, 250000], showgrid=False)
price_efficiency.update_yaxes(range=[125, 280], showgrid=False)

# Display scatter plot on website
st.plotly_chart(price_efficiency)