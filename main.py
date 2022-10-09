import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np

df_flood = pd.read_csv(r'sf_flood.csv')       #this is the dataset we got from CDC
df_census = pd.read_csv(r'sf_census.csv')     #this is the dataset we found that has lat and long
df_census_i = df_census.set_index('GEOID')
df_flood_i = df_flood.set_index('Census Blockgroup')

#df_flood.shape
#df_census.shape
col1, col2 = st.columns(2)


df_main = df_flood.merge(df_census, left_on='Census Blockgroup', right_on='GEOID')    #merging datasets and dropping unneeded features
df_main = df_main.drop(["data_as_of", "data_loaded_at", "multipolygon"], axis=1)
# df_main = df_main[['Census Blockgroup', 'INTPTLAT', 'INTPTLON', 'Children', 'Elderly', 'NonWhite', 'Poverty', 'Education', 'English', 'Elevation', 'SeaLevelRise', 'Precipitation', 'Diabetes', 'MentalHealth', 'Asthma', 'Disability', 'HousingQuality', 'Homeless', 'LivAlone', 'FloodHealthIndex', 'FloodHealthIndex_Quintiles']]
df_button = df_main[['Children', 'Elderly', 'NonWhite', 'Poverty', 'Education', 'English', 'SeaLevelRise', 'Precipitation', 'Diabetes', 'MentalHealth', 'Asthma', 'Disability', 'HousingQuality', 'Homeless', 'LivAlone', 'FloodHealthIndex']]
button_options = ['Children', 'Elderly', 'NonWhite', 'Poverty', 'Education', 'English', 'SeaLevelRise', 'Precipitation', 'Diabetes', 'MentalHealth', 'Asthma', 'Disability', 'HousingQuality', 'Homeless', 'LivAlone', 'FloodHealthIndex']
option = st.selectbox(
    label="map display",
    options=button_options
)
'''
The column labels are not great as button labels, as they are not very descriptive and 
also don't have spaces between the words. I can change the button labels later I am just
dropping this here to remind myself.
'''

df_main = df_main[['INTPTLAT', 'INTPTLON', option]]
df_main.rename(columns={'INTPTLAT': 'lat', 'INTPTLON': 'lon'}, inplace=True)

df_main['coordinates'] = df_main.apply(lambda x: (x.lon, x.lat), axis=1) #idk what this line does lol
with col1:
    st.dataframe(df_main)

midpoint = (np.average(df_main["lat"]), np.average(df_main["lon"]))
match option:
    case 'Children':
        df_main['circle_radius'] = df_main[option] * 100
    case "Elderly":
        df_main['circle_radius'] = df_main[option] * 100
    case "NonWhite":
        df_main['circle_radius'] = df_main[option] * 100
    case "Poverty":
        df_main['circle_radius'] = df_main[option] * 100
    case "Education":
        df_main['circle_radius'] = df_main[option] * 100
    case "English":
        df_main['circle_radius'] = df_main[option] * 100
    case "SeaLevelRise":
        df_main['circle_radius'] = df_main[option] * 100
    case "Precipitation":
        df_main['circle_radius'] = df_main[option] * 100
    case "Diabetes":
        df_main['circle_radius'] = df_main[option]
    case "MentalHealth":
        df_main['circle_radius'] = df_main[option]
    case "Asthma":
        df_main['circle_radius'] = df_main[option]
    case "Disability":
        df_main['circle_radius'] = df_main[option] * 100
    case "HousingQuality":
        df_main['circle_radius'] = df_main[option]
    case "Homeless":
        df_main['circle_radius'] = df_main[option]
    case "LivAlone":
        df_main['circle_radius'] = df_main[option] * 100
    case "FloodHealthIndex":
        df_main['circle_radius'] = df_main[option] * .75

with col2:
    st.write(
      pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
          pdk.Layer(
            "ScatterplotLayer",
            df_main,
            pickable=True,
            opacity=1.0,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=3,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="coordinates",
            get_radius= "circle_radius",
            get_fill_color=[255, 0, 0],
            get_line_color=[0, 0, 0],
          ),
          pdk.Layer(
            "HexagonLayer",
            #df_zone1,
            get_position=["lon", "lat"],
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=False,
            coverage=1,
            radius = 70,
            opacity = 0.5,
          )

        ],
    ))

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

