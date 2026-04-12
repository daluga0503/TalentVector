import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
url_get_user_profile= os.getenv('URL_GET_USER_PROFILE')

def logout():
    st.session_state["access"] = None
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"
    st.rerun()



def show_profile_page():
    st.subheader("Información Personal")
    st.divider()

    token = st.session_state.get("access")
    if not token:
        st.error("No se ha encontrado una sesión activa. Pro favor, inicie sesión.")
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.rerun()

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url_get_user_profile, headers=headers)

        if response.status_code == 200:
            user_data = response.json()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; align-items: center; 
                                background-color: #007bff; color: white; border-radius: 50%; 
                                width: 150px; height: 150px; font-size: 60px; font-weight: bold;">
                        {user_data.get('name', '').upper()[0]}{user_data.get('surname', '').upper()[0]}
                    </div>
                """, unsafe_allow_html=True)
                st.write("")
                if st.button('Cerrar Sesión', type='primary'):
                    logout()
            with col2:
                with st.container(border=True):
                    st.markdown("### Información Personal")

                    c1, c2 = st.columns(2)
                    c1.markdown(f"**Nombre:**\n\n{user_data.get('name', 'N/A')}")
                    c2.markdown(f"**Apellidos:**\n\n{user_data.get('surname', 'N/A')}")
                    st.markdown(f"**Nombre de usuario (Username):**\n\n{user_data.get('username', 'N/A')}")
                    st.markdown(f"**Correo electrónico:**\n\n{user_data.get('email', 'N/A')}")

                    st.divider()
                    fecha_creacion = user_data.get('date_joined', None)
                    if fecha_creacion:
                        fecha_formateada = datetime.strptime(fecha_creacion, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")
                    st.info(f"**¿Es Admin?:** {user_data.get('is_staff', False)}")
                    st.info(f"📅 **Miembro desde:** {fecha_formateada}")
        else:
            st.error("Error al obtener los datos del perfil. Por favor, inténtelo de nuevo.")
    except Exception as e:
        st.error(f"Ha ocurrido un error: {str(e)}")

show_profile_page()
