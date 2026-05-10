import os
from dotenv import load_dotenv
import streamlit as st

def load_config():
    load_dotenv()
    config = {
        'URL_AUTH': os.getenv('URL_AUTH'),
        'URL_JOBS': os.getenv('URL_JOBS'),
        'URL_SCRAP_JOBS': os.getenv('URL_SCRAP_JOBS'),
        'URL_FAVJOBS': os.getenv('URL_FAVJOBS'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY')
    }
    return config

def get_token():
    return st.session_state.get('access')