import streamlit as st
from datetime import datetime
from services.auth_service import logout, get_user_profile
from utils import get_token, load_config
from services.jobs_service import scrap_jobs

URL_SCRAP_JOBS = load_config()['URL_SCRAP_JOBS']

def show_profile_page():
    st.subheader("Información Personal")
    st.divider()

    token = get_token()
    if not token:
        st.error("No se ha encontrado una sesión activa. Pro favor, inicie sesión.")
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.rerun()

    try:
        response = get_user_profile(token)

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
                if user_data.get('is_staff', False):
                    scrap_btn = st.button('Scrapear ofertas de Infojobs', type='tertiary')
                    if scrap_btn:
                        with st.spinner("Scrapeando InfoJobs..."):
                            resultado = scrap_jobs(token, URL_SCRAP_JOBS)
                            
                        if resultado:
                            total = resultado.get('total_scrapped', 0)
                            guardados = resultado.get('saved', 0)
                            repetidos = resultado.get('skipped', 0)

                            if guardados > 0:
                                st.success(f"✅ ¡Éxito! Se encontraron {total} ofertas y se guardaron {guardados} nuevas.")
                            elif repetidos > 0:
                                st.warning(f"ℹ️ Scraping finalizado. Se encontraron {total} ofertas, pero todas ya estaban en la base de datos.")
                            else:
                                st.info("No se encontraron ofertas nuevas en esta búsqueda.")
                        else:
                            st.error("Ocurrió un error al conectar con el servidor de scraping.")
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
