import streamlit as st
import json
import requests
from streamlit_extras.switch_page_button import switch_page
import pandas as pd



def single_line_prediction():
    st.subheader("Single user check")
    if 'token' in st.session_state:
        st.info("Input data below")
        # Based on our optimal features selection
        st.subheader("Identifier")
        customerID = st.text_input('Customer identifier')

        st.subheader("Demographic data")
        seniorcitizen = st.selectbox('Senior Citizen:', ('Yes', 'No'))
        dependents = st.selectbox('Dependent:', ('Yes', 'No'))
        partner = st.selectbox('Partner:', ('Yes', 'No'))
        gender = st.selectbox('Gender:', ('Male', 'Female'))

        st.subheader("Payment data")
        tenure = st.number_input('Number of months the customer has stayed with the company', min_value=0,
                                 max_value=200,
                                 value=0)
        contract = st.selectbox('Contract',
                                ('Month-to-month', 'One year', 'Two year')
                                )
        paperlessbilling = st.selectbox('Paperless Billing', ('Yes', 'No'))
        PaymentMethod = st.selectbox('PaymentMethod',
                                     ('Electronic check', 'Mailed check', 'Bank transfer (automatic)',
                                      'Credit card (automatic)')
                                     )
        monthlycharges = st.number_input('The amount charged to the customer monthly', min_value=0, max_value=150,
                                         value=0)
        totalCharges = st.number_input('The amount charged to the customer yearly', min_value=0, max_value=150, value=0)

        st.subheader("Services signed up for")
        mutliplelines = st.selectbox("Does the customer have multiple lines", ('Yes', 'No', 'No phone service'))
        phoneservice = st.selectbox('Phone Service:', ('Yes', 'No'))
        internetservice = st.selectbox("Does the customer have internet service", ('DSL', 'Fiber optic', 'No'))
        onlinesecurity = st.selectbox("Does the customer have online security", ('Yes', 'No', 'No internet service'))
        onlinebackup = st.selectbox("Does the customer have online backup", ('Yes', 'No', 'No internet service'))
        techsupport = st.selectbox("Does the customer have technology support", ('Yes', 'No', 'No internet service'))
        deviceProtection = st.selectbox("Does the customer have device protection", ('Yes', 'No'))
        streamingtv = st.selectbox("Does the customer stream TV", ('Yes', 'No', 'No internet service'))
        streamingmovies = st.selectbox("Does the customer stream movies", ('Yes', 'No', 'No internet service'))

        data = {
            'customerID': customerID,
            'SeniorCitizen': seniorcitizen,
            'Dependents': dependents,
            'Partner': partner,
            'gender': gender,
            'tenure': tenure,
            'PhoneService': phoneservice,
            'MultipleLines': mutliplelines,
            'InternetService': internetservice,
            'OnlineSecurity': onlinesecurity,
            'OnlineBackup': onlinebackup,
            'DeviceProtection': deviceProtection,
            'TechSupport': techsupport,
            'StreamingTV': streamingtv,
            'StreamingMovies': streamingmovies,
            'Contract': contract,
            'PaperlessBilling': paperlessbilling,
            'PaymentMethod': PaymentMethod,
            'MonthlyCharges': monthlycharges,
            'TotalCharges': totalCharges
        }

        features_df = pd.DataFrame.from_dict([data])
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.write('Overview of input is shown below')
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.dataframe(features_df)

        token = 'anc'
        url = 'http://127.0.0.1:8000/predict_churn'
        # Create a dictionary to hold all the data
        data_dict = {'token': token, 'featureDict': data, 'inputType': 'single'}

        if st.button('Predict'):
            response = requests.post(url, json=data_dict)
            print(response.json())
            print(type(response.json()["response"]))
            results_df = pd.DataFrame(response.json()["response"])
            print(results_df)
            st.dataframe(results_df)
            prediction = results_df.iloc[0, 1]
            print(prediction)
            if prediction == 1:
                st.warning("This customer is a potential churner")
            if prediction == 0:
                st.success("This customer is not a potential churner")
    else:
        st.warning("Please login to access the contents of this page")





if __name__ == '__main__':
    single_line_prediction()