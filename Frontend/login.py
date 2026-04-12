import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
url_login= os.getenv('URL_LOGIN')



def show_login_page():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #007bff;
            color: white;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            color: white;
        }
        .login-header {
            text-align: center;
            color: #1E3A8A;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)


    # Contenedor principal centrado
    st.markdown("<h1 class='login-header'>🚀 TalentVector</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):
            st.subheader("Iniciar Sesión")
            
            email = st.text_input("Correo electrónico", placeholder="ejemplo@correo.com")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            
            st.markdown("---")
            
            if st.button("Login"):
                if email and password:
                    
                    try:
                        with st.spinner('Autenticando...'):
                            response = requests.post(url_login, json={
                                "email": email,
                                "password": password
                            })
                        
                        if response.status_code == 200:
                            data = response.json()
                            # Guardamos los tokens en la sesión de Streamlit
                            st.session_state['access'] = data['access']
                            st.session_state['logged_in'] = True
                            
                            st.success("¡Bienvenido!")
                            # Aquí podrías usar st.rerun() para ir a la página principal
                            st.session_state['page'] = 'jobs'
                            st.rerun()
                        else:
                            st.toast("Credenciales incorrectas. Inténtalo de nuevo.")
                            
                    except Exception as e:
                        st.error(f"Error de conexión con el servidor: {e}")
                else:
                    st.toast("Por favor, rellena todos los campos.")

            st.write("")
            if st.button("¿No tienes cuenta? Regístrate", key="btn_reg"):
                st.session_state['page'] = 'register'
                st.rerun()