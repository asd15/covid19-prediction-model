import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

st.cache()
def map_display():
    df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    df = df.set_index('State')
    df.drop(['Total', 'State Unassigned'], inplace=True)
    df.sort_values(by=['State'], inplace=True)
    df = df.reset_index()
    st.write("""
       # Covid19 Prediction App
       This page displays **active cases** in India on map!
       """)

    map_df = pd.DataFrame()

    map_df['State'] = df['State']
    map_df['Active'] = df['Confirmed'].map(int) - (df['Recovered'].map(int) + df['Deaths'].map(int))
    map_df['Active'] = map_df['Active'].map(int)

    map_data = gpd.read_file('Indian_States.shp')
    map_data.rename(columns={'st_nm': 'State'}, inplace = True)

    map_data['State'] = map_data['State'].str.replace('&', 'and')
    map_data['State'].replace('Arunanchal Pradesh', 'Arunachal Pradesh', inplace=True)
    map_data['State'].replace('NCT of Delhi', 'Delhi', inplace=True)
    map_data['State'].replace('Andaman and Nicobar Island', 'Andaman and Nicobar Islands', inplace=True)
    map_data['State'].replace('Dadara and Nagar Havelli', 'Dadra and Nagar Haveli and Daman and Diu', inplace=True)
    map_data['State'].drop(7, inplace=True)

    map_data.sort_values(by=['State'], inplace=True)

    merged_data = pd.merge(map_data, map_df, how='left', on='State')

    fig, ax = plt.subplots(1, figsize=(20, 15))
    ax.axis('off')

    ax.set_title('Covid 19 Statewise Data — Active Cases', fontdict={'fontsize': '60', 'fontweight': '9'})

    merged_data.plot(column='Active', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    plt.show()
    st.pyplot(fig)

    map_df = map_df.set_index('State')
    st.write(map_df)
