# -*- coding: utf-8 -*-

# Import necessary Libraries
import streamlit as st

import pandas as pd
import plotly.express as px

import pickle
from sklearn.ensemble import RandomForestRegressor

# Loading data and pickle file
df=pd.read_csv('Final_Emission_Data.csv')
model = pickle.load(open('model.pkl', 'rb'))

# To display the title
st.title("Car's Co2 Emission Predictor")


def set_bg_hack_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://www.springboard.com/blog/wp-content/uploads/2020/11/shutterstock_749427565-scaled.jpg");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


set_bg_hack_url()

#Building the Interface 

st.sidebar.header('Select your Features:')

vehicle_class = st.sidebar.selectbox('Vehicle Class', sorted(df['vehicle_class'].unique()))
engine_size = st.sidebar.number_input('Engine size', min_value=0.0, max_value=10.00, step=0.1, format='%f')
cylinders = st.sidebar.selectbox('Cylinders', sorted(df['cylinders'].unique()))
transmission = st.sidebar.selectbox('Transmission', sorted(df['transmission'].unique()))
fuel_type = st.sidebar.selectbox('Fuel Type', sorted(df['fuel_type'].unique()))
fuel_consumption_comb = st.sidebar.number_input('Combined Fuel Consumption Rating')

if st.sidebar.button("Predict"):
    val = pd.DataFrame({'vehicle_class':vehicle_class, 'engine_size':engine_size, 'cylinders':cylinders, 'transmission':transmission, 'fuel_type':fuel_type, 
                        'fuel_consumption_comb':fuel_consumption_comb},index=[1])

 
    val['vehicle_class']  =val['vehicle_class'].map({'compact':0.0,'full-size':1.0,'mid-size':2.0,'minicompact':3.0,'minivan':4.0,
                                                      'pickup truck - small':5.0,'pickup truck - standard':6.0,'special purpose vehicle':7.0,
                                                      'station wagon - mid-size':8.0,'station wagon - small':9.0,'subcompact':10.0,
                                                       'suv - small':11.0, 'suv - standard':12.0,'two-seater':13.0,'van - cargo':14.0,
                                                        'van - passenger':15.0})
    val['transmission']  =val['transmission'].map({'Automatic':0.0,'Automated manual':1.0,'Automatic with select shift':2.0,'Continuously variable':3.0,'Manual':4.0})
    val['fuel_type']  =val['fuel_type'].map({'Diesel':0.0,'Ethanol (E85)':1.0,'Natural gas':2.0,'Premium gasoline':3.0,'Regular gasoline':4.0})

    predicted = model.predict(val)
    predicted = round(predicted[0], 2)
    predicted_line = 'The co2 emission of the car with these features is {} grams per kilometer.'.format(predicted)

    
    fig = px.histogram(df['co2_emissions'],color_discrete_sequence=['lightsteelblue'], title='Graph of Co2 Emission')
    fig.update_layout(autosize=True,width=1000, xaxis_title='Co2 Emission', yaxis_title='Count', showlegend=False, font_size=18)
    fig.add_vline(x=predicted, line_dash='dash',line_color='red')
    st.plotly_chart(fig)
    st.subheader('Your Vehicle Emission:')
    st.success(predicted_line)

if st.sidebar.button('Clear'):
   st.empty()

