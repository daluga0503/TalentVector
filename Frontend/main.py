import streamlit as st
from login import show_login_page
from register import show_register_page
from jobs import show_jobs_page

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="TalentVector", page_icon="💼", layout="centered")

# 2. Inicializar estado
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "login"

# 3. Navegación dinámica
if not st.session_state["logged_in"]:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)
    # Si no está logueado, mostrar login o registro
    if st.session_state["page"] == "login":
        show_login_page()
    else:
        show_register_page()
else:
    pages = {
        "Trabajos": [
            st.Page(show_jobs_page, title="Ofertas de trabajo", icon="💼")       
        ],
        "Búsqueda Asistida":[
            st.Page("rag_jobs.py", title="Búsqueda Vectorial", icon="🔍"),
            st.Page("chat_suggestions.py", title="ChatBot de Sugerencias", icon="💬")
        ],
        "Dashboard":[
            st.Page("dashboard.py", title="Dashboard", icon="📊")
        ],
        "Perfil": [
            st.Page("profile.py", title="Mi perfil", icon="👤")
        ]
    }

    pg = st.navigation(pages)
    pg.run()