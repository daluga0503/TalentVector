import streamlit as st
from login import show_login_page
from register import show_register_page
from jobs import show_job_page
# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="TalentVector", page_icon="💼", layout="centered")

# Inicializar el estado de la página si no existe
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --- LÓGICA DE ENRUTAMIENTO ---

if st.session_state['page'] == 'login':
    show_login_page()
elif st.session_state['page'] == 'register':
    show_register_page()
elif st.session_state['page'] == 'jobs':
    show_jobs_page()