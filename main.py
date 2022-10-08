import streamlit as st
import pandas as pd

df_flood = pd.read_csv(r'sf_flood.csv')
df_census = pd.read_csv(r'sf_census.csv')
df_census_i = df_census.set_index('GEOID')
df_flood_i = df_flood.set_index('Census Blockgroup')

df_flood.shape
df_census.shape

df_main = df_flood.merge(df_census, left_on='Census Blockgroup', right_on='GEOID')
df_main = df_main.drop(["data_as_of","data_loaded_at", "multipolygon"], axis = 1)
st.dataframe(df_main)
df_main = df_main[['Census Blockgroup', 'INTPTLAT', 'INTPTLON', 'Children', 'Elderly', 'NonWhite', 'Poverty', 'Education', 'English', 'Elevation', 'SeaLevelRise', 'Precipitation', 'Diabetes', 'MentalHealth', 'Asthma', 'Disability', 'HousingQuality', 'Homeless', 'LivAlone', 'FloodHealthIndex', 'FloodHealthIndex_Quintiles']]
st.dataframe(df_main)

df_map = df_main[['INTPTLAT', 'INTPTLON']]
df_map.rename(columns={'INTPTLAT': 'lat', 'INTPTLON': 'lon'}, inplace=True)
st.map(df_map)

@st.cache
def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

st.download_button(
  label="Download data as CSV",
  data=convert_df_to_csv(df_main),
  file_name='sf_main.csv',
  mime='text/csv',
)