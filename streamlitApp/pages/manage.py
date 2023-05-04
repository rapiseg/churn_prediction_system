import streamlit as st
import json
import requests
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


def manage_datasets():
    st.info("Manage datasets below")
    st.subheader("Select datasets")
    #     res = requests.get(url=" http://127.0.0.1:8000/api/v1/filenames",
    #                        data=json.dumps(
    #                            {
    #                                "token": st.session_state.token
    #                            }
    #                        ))
    #     print(res.json())
    #     filenames = res.json()["filenames"]
    code = 400
    if code==200:
        st.selectbox()
    elif code == 400:
        st.text("No Files")
    filename = ""
    st.button("Predict")
    st.button("Delete")



if __name__ == '__main__':
    manage_datasets()