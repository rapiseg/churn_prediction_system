import streamlit as st
import json
import requests
from streamlit_extras.switch_page_button import switch_page



def home():
    st.title("Welcome")
    st.markdown("Please select your preferred input type")
    st.button("Single Line")
    st.button("Batch")
    st.button("Manage Datasets")
    # if st.button("View Datasets"):
    #     res = requests.get(url=" http://127.0.0.1:8000/api/v1/filenames",
    #                        data=json.dumps(
    #                            {
    #                                "token": st.session_state.token
    #                            }
    #                        ))
    #     print(res.json())
    #     filenames = res.json()["filenames"]
    #     selected_file = st.selectbox("Select a file to view", filenames)
    #     st.text(selected_file)
    # else:
    #     pass


if __name__ == '__main__':
    home()