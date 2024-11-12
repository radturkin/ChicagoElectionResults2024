# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xSS3OrAfa_5ixdipx_WvZjCHbuMsaK4W
"""



import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from shapely import wkt

st.title("Chicago Election Results 2024")

@st.cache_data
def load_data():
    df_merged = gpd.read_file("https://raw.githubusercontent.com/radturkin/ChicagoElectionResults2024/refs/heads/main/merged_chicago_elections_1.geojson")
    # df_merged['geometry'] = df_merged['geometry'].apply(wkt.loads)
    df_merged = gpd.GeoDataFrame(df_merged, geometry='geometry')
    df_merged.set_crs(epsg=4326, inplace=True)
    df_merged["geometry"] = (
        df_merged.to_crs(df_merged.estimate_utm_crs()).simplify(10).to_crs(df_merged.crs)
    )
    return df_merged

df_merged = load_data()

# Create the choropleth map
fig = px.choropleth_mapbox(df_merged,
                           geojson=df_merged.geometry,
                           locations=df_merged.index,
                           color='Kamala',
                           mapbox_style="carto-positron",
                           zoom=10,
                           center={"lat": 41.8781, "lon": -87.6298},
                           opacity=0.5,
                           hover_name="ward_precinct",
                           hover_data={'Kamala %': True, 'Trump %': True, 'Kamala': False},
                           color_continuous_scale='RdBu')

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig)