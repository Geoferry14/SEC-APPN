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

    result = authenticator.login(
        'main',
        fields={'Form name': 'My Login Form'},
        key='login-button'
    )

    # 🔐 Check if login returned None
    if result is None:
        return None, None, None

    name, auth_status, username = result
    return name, auth_status, username
    
    name, auth_status, username = authenticator.login('main', fields={'Form name': 'My Login Form'}, key='login-button')
   


    if auth_status:
        role = config["credentials"]["usernames"][username]["roles"][0]
        authenticator.logout("Logout", "sidebar")
        return name, auth_status, username, role
    elif auth_status is False:
        st.error("Incorrect username or password.")
    elif auth_status is None:
        st.warning("Please enter your username and password.")
    return None, auth_status, None, None
