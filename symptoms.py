import streamlit as st
import pandas as pd

st.cache()
def symptoms_display():
    st.write("""
               # Covid19 Prediction App
               This page checks the **probability** of covid by taking **symptoms** as user input.
               """)
    fever = st.sidebar.slider('How much is your body temperature?', 90, 105, 95)
    bodyPain = st.sidebar.selectbox('BodyPain', ('YES', 'NO'))
    age = st.sidebar.slider('Enter age', 1, 100, 50)
    runnyNose = st.sidebar.selectbox('RunnyNose', ('YES', 'NO'))
    diffBreath = st.sidebar.selectbox('Difficulty Breathing', ('YES', 'NO'))

    data = {'fever': fever,
            'bodyPain': bodyPain,
            'age':  age,
            'runnyNose': runnyNose,
            'diffBreath': diffBreath,
            }
    features = pd.DataFrame(data, index=[0])
    return features
