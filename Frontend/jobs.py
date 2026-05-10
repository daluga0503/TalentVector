import streamlit as st
from services.jobs_service import get_jobs
from services.favjobs_service import get_fav_jobs, add_job_to_fav, remove_job_from_fav
from utils import load_config, get_token

URL_JOBS = load_config()['URL_JOBS']


def handle_fav_toggle(job_id, token):
    """
    Esta función se ejecuta cuando el usuario toca el toggle.
    Gestiona la API y actualiza el estado sin necesidad de rerun manual.
    """
    # El valor actual del toggle se recupera del session_state usando su key
    is_now_fav = st.session_state[f"fav_{job_id}"]
    
    if is_now_fav:
        if add_job_to_fav(token, job_id):
            st.session_state['fav_ids'].append(job_id)
            st.toast(f"Añadido a favoritos ❤️")
        else:
            st.error("Error al añadir a favoritos")
    else:
        if remove_job_from_fav(token, job_id):
            if job_id in st.session_state['fav_ids']:
                st.session_state['fav_ids'].remove(job_id)
            st.toast(f"Eliminado de favoritos 🗑️")
        else:
            st.error("Error al eliminar de favoritos")

def card_job(job):
    job_id = str(job.get('id', ''))
    img = job.get('image', '')
    title = job.get('title', '')
    company = job.get('company', '')
    location = job.get('location', '')
    movility = job.get('movility', '')

    st.markdown(
    f"""
        <div style="
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
            font-family: 'Open Sans', sans-serif;
            margin-bottom: 12px;
            max-width: 725px;
            position: relative;
        ">
            <div style="display: flex; align-items: flex-start; margin-bottom: 10px;">
                <div style="
                    min-width: 80px;
                    height: 80px;
                    border: 1px solid #f0f0f0;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 16px;
                ">
                    <img src="{img}" style="max-width: 70px; max-height: 70px;">
                </div>
                <div style="flex-grow: 1;">
                    <h3 style="margin: 0; font-size: 20px; color: #111; font-weight: 700;">
                        {title}
                    </h3>
                    <p style="margin: 2px 0 0; color: #0056b3; font-size: 17px;">
                        {company}
                    </p>
                </div>
            </div>
            <div style="display: flex; align-items: center; font-size: 15px; color: #666; margin-left: 96px;">
                <span>{location}</span>
                <span style="margin: 0 8px; color: #ccc;">|</span>
                <span>{movility}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    ya_es_fav = job_id in st.session_state.get('fav_ids', [])
    
    col1, col2, col3, col4 = st.columns([0.35, 1, 1, 0.25])
    
    with col2:
        # Usamos on_change para ejecutar la lógica de la API
        st.toggle(
            "¿Favorito?", 
            key=f"fav_{job_id}", 
            value=ya_es_fav,
            on_change=handle_fav_toggle,
            args=(job_id, st.session_state.get('access'))
        )

    with col3:
        if st.button("Ver detalles", key=f"btn_{job_id}"):
            show_full_details(job)

@st.dialog("Detalle de la oferta")
def show_full_details(job):
    st.markdown(f"### {job.get('title', '')}")
    st.markdown(f"**Empresa:** {job.get('company', '')}")
    st.markdown(f"**Ubicación:** {job.get('location', '')}")
    st.markdown(f"**Movilidad:** {job.get('movility', '')}")
    st.markdown(f"**Salario:** {job.get('salary', '')}")
    st.markdown("---")
    st.markdown(f"**Descripción:**\n\n{job.get('description', 'No hay descripción disponible.')}")
    st.markdown("---")
    st.markdown(f"**Requisitos:**\n\n{job.get('skills', 'No hay skills especificados.')}")
    st.markdown("---")
    st.markdown(f"**Experiencia Requerida:**\n\n{job.get('experience_required', 'N/A')}")
    st.markdown("---")
    st.markdown(f"**Perfil:**\n\n{job.get('seniority', 'N/A').capitalize()}")
    st.markdown("---")
    st.markdown(f"**Tipo de Contrato:**\n\n{job.get('type_contract', 'N/A')}")
    st.markdown("---")
    st.markdown(f"**Enlace oferta:**\n\n{job.get('url', 'N/A')}")

    if st.button("Cerrar"):
        st.rerun()


def container_jobs(jobs):
    if not jobs:
        st.info("No se encontraron ofertas.")
        return

    with st.container():
        for i in range(0, len(jobs), 2):
            cols = st.columns(2)
            
            # Tarjeta izquierda
            with cols[0]:
                card_job(jobs[i])
            
            # Tarjeta derecha (si existe)
            if i + 1 < len(jobs):
                with cols[1]:
                    card_job(jobs[i+1])

def show_jobs_page():
    token = get_token()
    
    # 1. Cargar favoritos una sola vez (Estado Inicial)
    if 'fav_ids' not in st.session_state:
        with st.spinner("Sincronizando favoritos..."):
            st.session_state['fav_ids'] = get_fav_jobs(token)
    
    # --- FILTROS ---
    st.markdown("### 🔍 Filtrar ofertas")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

    with col1:
        location = st.text_input('Ubicación', placeholder="Ej: Madrid")
    with col2:
        skill = st.text_input('Habilidades', placeholder="Ej: Python")
    with col3:
        company = st.text_input('Empresa', placeholder="Ej: Sopra")
    with col4:
        seniority = st.selectbox('Experiencia', ['Cualquiera', 'Junior', 'Mid', 'Senior', 'Architecture'])
    
    with col5:
        st.write(" ")
        st.write(" ") 
        btn_filter = st.button('Filtrar', use_container_width=True)

    # Lógica de ruta para filtros
    params = []
    if location: params.append(f"location={location}")
    if skill: params.append(f"skills={skill}")
    if company: params.append(f"company={company}")
    if seniority != 'Cualquiera': params.append(f"seniority={seniority}")
    
    ruta = f"{URL_JOBS}?{'&'.join(params)}" if params and btn_filter else URL_JOBS

    st.markdown("---") 
    
    with st.spinner('Cargando ofertas...'):
        jobs = get_jobs(token, ruta)
    
    if jobs is None:
        st.error("Hubo un problema de conexión con el servidor. Inténtalo de nuevo más tarde.")
    elif len(jobs) > 0:
        st.write(f"Se han encontrado **{len(jobs)}** ofertas.")
        container_jobs(jobs)
    else:
        st.info("No hay ofertas disponibles.")