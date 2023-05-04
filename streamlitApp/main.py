import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
import requests


def main():
    st.title("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    inputs = {"username": username, "password":password}
    if st.button("Log In"):
        res = requests.post(url = "http://127.0.0.1:8000/api/v1/login", data=json.dumps(inputs))
        print(res.json())
        st.session_state.token = res.json()["access_token"]
        if st.session_state.token:
            switch_page("home")
        else:
            st.warning("Login failed")
    elif st.button("Sign up"):
        switch_page("register")


if __name__ == '__main__':
    main()