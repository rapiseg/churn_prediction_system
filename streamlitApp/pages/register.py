import streamlit as st
import pymongo
from streamlit_extras.switch_page_button import switch_page

#
# async def register():
#
        # Register the user
        # await User().register(username, password)
        # st.write("Account created")
        #
        # # Generate a JWT token
        # token = jwt.encode({'username': username}, 'secret_key', algorithm='HS256')
        #
        # # Store the token in a cookie
        # st.session_state.token = token
        #
        # # Redirect to the home page
        # st.experimental_rerun()


def main():
    st.title("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        switch_page("home.py")


if __name__ == '__main__':
    main()