"""Creates an interactive website displaying characteristics of electric vehicles"""

# Import Libraries
import pandas as pd 
import numpy as np
import streamlit as st
import plotly_express as px

## READ AND CLEAN DATA
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

# Create top brands data frame 
top_brands = ev[(ev['brand']=='Tesla ') | (ev['brand']=='Audi ') | (ev['brand']=='Nissan ') 
                | (ev['brand']=='Volkswagen ') | (ev['brand']=='Skoda ') | (ev['brand']=='Renault ') 
                | (ev['brand']=='Porsche ') | (ev['brand']=='BMW ') | (ev['brand']=='Ford ')
                | (ev['brand']=='Kia ') | (ev['brand']=='Smart ') | (ev['brand']=='Byton ')
                | (ev['brand']=='Mercedes ') | (ev['brand']=='Hyundai ') | (ev['brand']=='Opel ')] 


## CREATE HEADER
st.header('Price, Efficiency, and Range of Electric Vehicles')

# Create Text
st.markdown('Welcome to the electric vehicle data visualization page! Click the buttons \nand toggle the colors to see how electric vehicles compare across the market.')

## CREATE BAR CHARTS 
# Create a bar chart of average price by brand
price_bar = px.histogram(top_brands, x='brand', y='price_euro', histfunc='avg', 
                          title='Average Price by Brand', text_auto='.2s',
                          labels={'price_euro':'Price (Euros)', 'brand':'Brand Name'},
                          color_discrete_sequence=[px.colors.qualitative.Plotly[7]],
                          width=800, height=500)

price_bar.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
}) 

price_bar.update_traces(textfont_size=11, textposition='outside') # Add labels above bars

price_bar.update_layout(xaxis={'categoryorder':'total descending'}) # Arrange in order from expensive to inexpensive

price_bar.update_xaxes(showgrid=False) # Turn off x grid
price_bar.update_yaxes(showgrid=False) # Turn off y grid

# Create bar chart of average efficiency by brand 
eff_bar = px.histogram(top_brands, x='brand', y='efficiency_whkm', histfunc='avg', 
                          title='Average efficiency by Brand', text_auto='.2s',
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

# Create bar chart of average range by brand
range_bar = px.histogram(top_brands, x='brand', y='range_km', histfunc='avg', 
                         title='Average Range by Brand', text_auto='.2s',
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

# Create Header 
st.subheader('By Brand')

# Radio Buttons
option = st.radio(label='Choose characteristic:', options=['Price', 'Efficiency', 'Range'])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) # Make buttons horizontal

# Displays for radio button options
if option == 'Price':
    st.plotly_chart(price_bar)
elif option == 'Efficiency':
    st.plotly_chart(eff_bar)
elif option == 'Range':
    st.plotly_chart(range_bar)
    
st.markdown('Porsche has the highest average price. Byton has the highest average efficiency, \nand Tesla has the highest average range.')
    

# CREATE HISTOGRAMS
# Header for body style
st.subheader('By Body Style')

# Create data frame with only top 3 body styles
suv_hatch_sed = ev[(ev['body_style']=='SUV') | (ev['body_style']=='Hatchback') | (ev['body_style']=='Sedan')]

# Drop down menu 
option_2 = st.selectbox('Choose characteristic:', ('Price', 'Efficiency', 'Range'))

x_value_hist = (option_2=='Price' and 'price_euro') or (option_2=='Efficiency' and 'efficiency_whkm') or (option_2=='Range' and 'range_km')
x_label_hist = (option_2=='Price' and 'Price (Euros)') or (option_2=='Efficiency' and 'Efficiency (WhKm)') or (option_2=='Range' and 'Range (Km)')

# Create histograms by drop down selection
body_hist = px.histogram(suv_hatch_sed, title=f'{option_2} by Body Style', x=x_value_hist, color='body_style', 
                          nbins=25, labels={x_value_hist:x_label_hist},
                          color_discrete_sequence=[px.colors.qualitative.Plotly[0],
                                                   px.colors.qualitative.Plotly[7],
                                                   px.colors.qualitative.Plotly[9]],
                          width=800, height=500)
                                                   

body_hist.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
})

body_hist.update_layout(barmode='overlay')
body_hist.update_traces(opacity=0.7)

body_hist.update_xaxes(showgrid=False)
body_hist.update_yaxes(showgrid=False)

st.plotly_chart(body_hist)

# CREATE SCATTER PLOTS
# Header for scatter plot 
st.subheader('By Price')

# Drop down nenu for scatter plot
y_axis = st.selectbox('Y Axis:', ('Efficiency', 'Range'))

# Create scatter plot from drop down selection
y_value_scat = (y_axis=='Efficiency' and 'efficiency_whkm') or (y_axis=='Range' and 'range_km')

y_label_scat = (y_axis=='Price' and 'Price (Euros)') or (y_axis=='Efficiency' and 'Efficiency (WhKm)') or (y_axis=='Range' and 'Range (Km)')

price_efficiency = px.scatter(data_frame=ev, title=f'{y_axis} vs Price', x='price_euro', y=y_value_scat, 
           labels={'price_euros':'Price (Euros)', y_value_scat:y_label_scat},
           color='brand', width=900, height=500, hover_data=['model'])

price_efficiency.update_layout({
    'plot_bgcolor':'rgba(0, 0, 0, 0)',
    'paper_bgcolor':'rgba(0, 0, 0, 0)'
})

price_efficiency.update_xaxes(showgrid=False)
price_efficiency.update_yaxes(showgrid=False)

# Display scatter plot on website
st.plotly_chart(price_efficiency)

st.markdown('Graphics on this site were created from data on the 103 top electric vehicles on the market today.')