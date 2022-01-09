import streamlit as st
import pandas as pd
import statsmodels.api as sm
import datetime
import matplotlib.pyplot as plt

from constants import states


def format_func(option):
    return states[option]


st.cache()


def positive_display():
    st.write("""
    # Covid19 Prediction App
    This page predicts the **New cases** suffering from the virus in India!
    """)
    df = pd.read_csv('https://data.covid19bharat.org/csv/latest/state_wise_daily.csv')
    df['Date'] = df['Date'].replace('Sept', 'Sep', regex=True)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%b-%y")
    df = df.set_index('Status')
    df.drop(['Recovered', 'Deceased'], inplace=True)
    df = df.reset_index()
    og_df = df
    og_df = og_df.set_index('Date')
    state = st.sidebar.selectbox('State', options=list(states.keys()), format_func=format_func)
    date_sel = st.sidebar.slider('Number of Days to Predict', 1, 60, 15)
    sel_state = format_func(state)
    st.write(f"You selected {sel_state}")
    og_df[state] = og_df[state].astype(float)
    pre_df = og_df
    sel_state_df = og_df[state]
    st.line_chart(sel_state_df)

    non_sel_states = og_df[state]

    sarimax_mod = sm.tsa.statespace.SARIMAX(non_sel_states, trend='n', order=(14, 1, 0)).fit()

    #predict

    future_predict = sarimax_mod.predict(start=datetime.date.today(), end=datetime.date.today()+datetime.timedelta(days=date_sel), dynamic= True,)

    f_temp = pd.DataFrame()
    f_temp['Date'] = future_predict.index
    f_temp['Values'] = future_predict.values

    f_temp.loc[-1] = [pre_df.index[-1], pre_df[state][-1]]

    f_temp.index = f_temp.index + 1
    f_temp = f_temp.sort_index()

    f_temp['Date'] = pd.to_datetime(f_temp['Date'], format='%d-%b-%y')
    f_temp = f_temp.set_index('Date')

    figg = plt.figure(num=1, figsize=(12, 8), dpi=100)
    orig = plt.plot(og_df[state], color='blue', label='Original')
    fore = plt.plot(f_temp['Values'], color='red', label='Forecast')
    plt.legend(loc='best')
    plt.xticks(rotation=60)
    plt.tight_layout()
    st.write(f'**Forecast of upcoming {date_sel} days Covid-19 Cases in {sel_state}**')
    plt.show()
    st.pyplot(figg)

    data = {'state': state,
            'date_sel': date_sel}
    features = pd.DataFrame(data, index=[0])
    return features


