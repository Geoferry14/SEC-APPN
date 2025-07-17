# app.py
import streamlit as st
import pandas as pd
import numpy as np
from phe import paillier
from yaml import safe_load
import streamlit_authenticator as stauth
from encryption_utils import encrypt_column, decrypt_column, public_key
from model_utils import load_data, train_model, predict_encrypted
from user_roles import check_user_role
from auth import login

# ----------------------------
# 🔐 Authentication
name, auth_status, username = login()

if None in (name, auth_status, username):
    st.warning("Login failed or config issue.")
    st.stop()

# 🧑‍💼 Get role from session_state (new API)
role_list = st.session_state.get("roles", [])
role = role_list[0] if role_list else "unknown"

st.sidebar.success(f"Logged in as {name} ({role})")
check_user_role(role)

# ----------------------------
# 📁 Navigation
page = st.sidebar.selectbox("Page", [
    "Home Dashboard",
    "Engineer Panel",
    "Admin Panel",
    "Analyst Workspace",
    "Anomaly Logs"
])

# ----------------------------
# 📊 Pages based on Role

if page == "Home Dashboard":
    st.title("🏥 Secure Healthcare Analytics Dashboard")
    st.info("Welcome to the secure healthcare analytics platform.")

elif page == "Engineer Panel" and role == "engineer":
    st.title("🔧 Engineer Panel - Upload Patient Data")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        st.success("Data uploaded successfully.")

elif page == "Admin Panel" and role == "admin":
    st.title("🔐 Admin Panel")
    st.write("View and manage data, logs, and system settings.")
    df = load_data()
    st.subheader("Full Patient Dataset")
    st.dataframe(df)

elif page == "Analyst Workspace" and role == "analyst":
    st.title("📊 Analyst Workspace")
    st.write("Perform secure analysis on encrypted data.")
    df = load_data()
    model = train_model(df)
    X = df.iloc[:, :-1].values
    new_patient = X[1]
    encrypted_input = encrypt_column(new_patient)
    encrypted_result = predict_encrypted(encrypted_input, model, public_key)
    prediction = decrypt_column([encrypted_result])[0]
    st.success(f"Encrypted prediction: {prediction:.2f}")

elif page == "Anomaly Logs" and role == "admin":
    st.title("🚨 Anomaly Logs")
    st.write("View system-detected anomalies.")
    try:
        log_df = pd.read_json("audit_log.json", lines=True)
        st.dataframe(log_df[log_df["action"] == "ANOMALY"])
    except Exception:
        st.warning("No anomaly logs found.")
