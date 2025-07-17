# auth.py
import streamlit as st
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

# Load config.yaml safely
def load_config():
    try:
        with open("config.yaml") as file:
            config = yaml.load(file, Loader=SafeLoader)
            if config is None:
                st.error("config.yaml loaded empty or improperly formatted.")
                return None
            return config
    except Exception as e:
        st.error(f"Error loading config.yaml: {e}")
        return None

# Login handler
def login():
    config = load_config()
    if config is None:
       return None, None, None
    authenticator = stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        cookie_key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"]
    )

    name, auth_status, username = authenticator.login(
        "main",
        fields={"Form name": "My Login Form"},
        key="login-button",
    )

    if name is None and auth_status is None and username is None:
        return None, None, None

    if auth_status:
        roles = config["credentials"]["usernames"][username]["roles"]
        st.session_state["roles"] = roles
        authenticator.logout("Logout", "sidebar")
    elif auth_status is False:
        st.error("Incorrect username or password.")
    else:
        st.warning("Please enter your username and password.")

    return name, auth_status, username
