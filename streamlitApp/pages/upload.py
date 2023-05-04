import streamlit as st
import json
import requests
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder

def upload():
    st.subheader("Dataset upload")
    if 'token' in st.session_state:
        token = st.session_state.token
        uploaded_file = st.file_uploader("Choose a file", type="csv")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            # # Get overview of data
            st.dataframe(data)
            # # st.write(data.head())
            st.markdown("<h3></h3>", unsafe_allow_html=True)

            if st.button("Save"):
                url = 'http://127.0.0.1:8000/api/v1/upload_file'
                response = upload_file(uploaded_file, token, url)
                if response["status_code"] == 200:
                    st.success(response["message"])
                else:
                    st.warning(response["message"])
                print(response)

            if st.button('Predict'):
                url = 'http://127.0.0.1:8000/predict_churn'
                data_dict = {'token': token, 'featureDict': data.to_dict(), 'inputType': 'multi'}
                response = requests.post(url, json=data_dict)
                print(response.json())
                print(type(response.json()["response"]))
                results_df = pd.DataFrame(response.json()["response"])
                print(results_df)
                st.dataframe(results_df)
                # st.write(results_df.head())

                if results_df is not None:
                    st.download_button("Download Results",
                                       data=convert_df(results_df),
                                       file_name="results.csv",
                                       mime="text/csv",
                                       )



                st.markdown("<h3></h3>", unsafe_allow_html=True)
                st.subheader('Prediction')
    else:
        st.warning("Please login to access the contents of this page")

def upload_file(file, token, url):
    # Create a MultipartEncoder object
    encoder = MultipartEncoder(fields={
        "file": file,
        "filename": file.name,
        "session_token": token
    })
    # Set the content type header to 'multipart/form-data'
    headers = {"Content-Type": encoder.content_type}
    # Send the request to the backend API endpoint
    response = requests.post(url, data=encoder, headers=headers)

    return response.json()


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


if __name__ == '__main__':
    upload()