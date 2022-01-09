import streamlit as st
import pandas as pd

from constants import states


def format_func(option):
    return states[option]


def compare_display():
    st.write("""
      # Covid19 Prediction App
      This page **compares** the **New cases** between each state suffering from the virus in India!
      """)
    df = pd.read_csv('https://data.covid19bharat.org/csv/latest/state_wise_daily.csv')
    df['Date'] = df['Date'].replace('Sept', 'Sep', regex=True)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%b-%y")
    df = df.set_index('Status')
    df.drop(['Recovered', 'Deceased'], inplace=True)
    df = df.reset_index()
    og_df = df
    og_df = og_df.set_index('Date')

    comp_states = st.multiselect('Select states to compare', options=list(states.keys()), format_func=format_func)

    og_df[comp_states] = og_df[comp_states].astype(float)
    comp_state_df = og_df[comp_states]
    st.line_chart(comp_state_df, width=600, height=500)
