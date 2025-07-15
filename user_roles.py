import streamlit as st

def check_user_role(role):
    if role == "Analyst":
        st.info("🔐 Analyst Mode: You can analyze encrypted data but cannot see or modify raw patient data.")
    elif role == "Admin":
        st.success("✅ Admin Mode: Full access to data and patient management.")
