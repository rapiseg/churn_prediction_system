import streamlit as st
import json
import requests
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


def upload():
    st.subheader("Dataset upload")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        # Get overview of data
        st.dataframe(data)
        # st.write(data.head())
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        # Preprocess inputs
        # preprocess_df = preprocess(data, "Batch")
        token = "ad"
        url = 'http://127.0.0.1:8000/predict_churn'
        data_dict = {'token': token, 'featureDict': data.to_dict(), 'inputType': 'multi'}
        st.button("Save")
        if st.button('Predict'):
            response = requests.post(url, json=data_dict)
            print(response.json())
            print(type(response.json()["response"]))
            results_df = pd.DataFrame(response.json()["response"])
            print(results_df)
            st.dataframe(results_df)
            # st.write(results_df.head())

            if results_df is not None:
                st.button("Download Results")
            # Get batch prediction
            # prediction = model.predict(preprocess_df)
            # prediction_df = pd.DataFrame(prediction, columns=["Predictions"])
            # prediction_df = prediction_df.replace({1:'Yes, the customer will terminate the service.',
            #                                     0:'No, the customer is happy with Telco Services.'})

            st.markdown("<h3></h3>", unsafe_allow_html=True)
            st.subheader('Prediction')


if __name__ == '__main__':
    upload()