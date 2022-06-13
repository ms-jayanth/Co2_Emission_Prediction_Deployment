import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport

df=pd.read_csv('co2_emissions (1).csv',sep=';')

profile=ProfileReport(df, title='Co2_emission Data')

st.title('EDA through Pandas Profiling')
st.write(df.head(11))

if st.button('EDA Report'):
   st_profile_report(profile)