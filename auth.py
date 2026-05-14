import streamlit as st
from supabase_client import supabase


def login():

    st.subheader("🔐 Vendor Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        try:

            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            st.session_state["user"] = response.user

            st.success("Login Successful!")

            st.rerun()

        except Exception as e:

            st.error(str(e))


def signup():

    st.subheader("📝 Create Account")

    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")

    if st.button("Sign Up"):

        try:

            supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            st.success("Account Created! Please Login.")

        except Exception as e:

            st.error(str(e))


def logout():

    if st.sidebar.button("Logout"):

        supabase.auth.sign_out()

        st.session_state.clear()

        st.rerun()
     
