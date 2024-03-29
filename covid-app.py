import streamlit as st
import pandas as pd
import numpy as np
import pickle

from covid_map import map_display
from positve import positive_display
from recovered import recovered_display
from deaths import deaths_display
from symptoms import symptoms_display
from compare import compare_display

page = {'Map', 'Recovered', 'Deaths', 'Positive Cases', 'Symptoms', 'Compare States', 'Thank you!'}

st.sidebar.header('Select Input')

sel_page = st.sidebar.selectbox('Select Page to Display', options=list(page))


if sel_page == 'Positive Cases':
    input_df = positive_display()
elif sel_page == 'Map':
    map_display()
elif sel_page == 'Recovered':
    recovered_display()
elif sel_page == 'Deaths':
    deaths_display()
elif sel_page == 'Compare States':
    compare_display()
elif sel_page == 'Thank you!':
    st.balloons()
    st.balloons()
    st.header('Thank you for watching!')
    st.subheader('Code available on my github ac: github.com/asd15')

elif sel_page == 'Symptoms':
    input_df = symptoms_display()
    symptoms_raw = pd.read_csv('symptoms_dataset.csv')
    symptoms = symptoms_raw.drop(columns=['infectionProb'])
    df = pd.concat([input_df, symptoms], axis=0)

    encode = ['bodyPain', 'runnyNose', 'diffBreath']

    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummy], axis=1)
        del df[col]
    df = df[:1] # Selects only the first row (the user input data)

    # Displays the user input features
    st.subheader('User Input')
    st.write(df)

    load_clf = pickle.load(open('symptoms_clf.pkl', 'rb'))

    prediction = load_clf.predict(df)
    prediction_prob = load_clf.predict_proba(df)

    st.header('Prediction')
    virus_symptoms = np.array(['NO', 'YES'])
    yes_no = ''.join(virus_symptoms[prediction])
    if yes_no == "YES":
        st.subheader('NO probably you are not suffering from covid.')
    elif yes_no == "NO":
        st.subheader('YES probably you are suffering from covid.')

    st.header('Prediction Probability')
    st.subheader('Probability of YES is: ')
    st.subheader(prediction_prob[0][0])
    st.subheader('Probability of NO is: ')
    st.subheader(prediction_prob[0][1])
