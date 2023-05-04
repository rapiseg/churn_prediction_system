import io

import streamlit as st
import json
import requests
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


def manage_datasets():
    if 'token' in st.session_state:

        st.info("Manage datasets below")
        st.subheader("Select datasets")
        res = requests.get(url="http://127.0.0.1:8000/api/v1/filenames",
                               data=json.dumps(
                                   {
                                       "token": st.session_state.token
                                   }
                               ))
        print(res.json())
        filenames = res.json()["filenames"]
        if res.json()["status_code"] == 200:
            filename = st.selectbox("Select a file to view", filenames)
            file_res = requests.get(url="http://127.0.0.1:8000/api/v1/dataset",
                                    data=json.dumps(
                                        {
                                            "token": st.session_state.token,
                                            "filename":filename
                                        }
                                    ))
            if file_res.json()["status_code"] == 200:
                # st.success("Retrieved dataset successfully")
                pass
            else:
                st.warning("Failed to retrieve dataset")
            dataset = file_res.json()["dataset"]
            print(type(dataset))
            print(dataset)
            dataframe = pd.read_csv(io.StringIO(dataset))

            st.dataframe(dataframe)
            st.button("Predict")
            delete = st.button("Delete")
            if delete:
                url = "http://127.0.0.1:8000/api/v1/delete"
                delete_response = requests.delete(url,
                                            data=json.dumps(
                                       {
                                           "token": st.session_state.token,
                                           "filename": filename
                                       }
                               ))
                if delete_response.json()["status_code"] == 200:
                    st.success("Successfully deleted the dataset")
                    st.experimental_rerun()
                else:
                    st.warning("Failed to delete dataset.")
        elif res.json()["status_code"] == 400:
            st.text("No Files")


    else:
        st.warning("Please login to access the contents of this page")



if __name__ == '__main__':
    manage_datasets()