import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
import requests


def login_form():
    st.subheader("Log In")
    form = st.form(key="login_form")
    form.username = form.text_input("Username")
    form.password = form.text_input("Password", type="password")
    inputs = {"username": form.username, "password": form.password}
    if form.form_submit_button("Login"):
        res = requests.post(url = "http://127.0.0.1:8000/api/v1/login", data=json.dumps(inputs))
        print(res.json())
        st.session_state.token = res.json()["access_token"]
        st.experimental_rerun()
        # switch_page("main")
        # if st.session_state.token:
        #     st.success("Successfully logged in")
        #     # switch_page("home")
        # else:
        #     st.warning("Login failed")
    if form.form_submit_button("Sign up"):
        registration_form()

def registration_form():
    st.subheader("Create an account")
    form = st.form(key="registration_form")
    form.username = form.text_input("Username")
    form.password = form.text_input("Password", type="password")
    inputs = {"username": form.username, "password": form.password}
    if form.form_submit_button("Register"):
        res = requests.post(url="http://127.0.0.1:8000/api/v1/register", data=json.dumps(inputs))
        print(res.json())
        st.session_state.token = res.json()["access_token"]
        main()

def main():
    # st.title("Log In")
    # username = st.text_input("Username")
    # password = st.text_input("Password", type="password")
    # inputs = {"username": username, "password":password}
    # if st.button("Log In"):
    #     res = requests.post(url = "http://127.0.0.1:8000/api/v1/login", data=json.dumps(inputs))
    #     print(res.json())
    #     st.session_state.token = res.json()["access_token"]
    #     if st.session_state.token:
    #         switch_page("home")
    #     else:
    #         st.warning("Login failed")
    # elif st.button("Sign up"):
    #     switch_page("register")
    st.subheader("welcome to main page")

    # if 'token' in st.session_state:
    #     st.subheader("welcome to main page")
    # else:
    #     login_form()


if __name__ == '__main__':
    if 'token' in st.session_state:
        main()
    else:
        login_form()