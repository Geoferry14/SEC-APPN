# user_roles.py
import streamlit as st

def check_user_role(role):
    if role == "admin":
        st.sidebar.markdown("**Role:** Admin")
    elif role == "engineer":
        st.sidebar.markdown("**Role:** Engineer")
    elif role == "analyst":
        st.sidebar.markdown("**Role:** Analyst")
    else:
        st.warning("Unrecognized role. Access may be restricted.")
