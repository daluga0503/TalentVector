import streamlit as st
from .services.jobs_service import get_jobs, URL_JOBS

token = st.session_state.get('access')

def save_to_favorites(job_id):
    st.toast("Guardando en favoritos...")


def card_job(job):
    job_id = job.get('id', '')
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
            postion: relative;
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
    container = st.container()
    col1, col2, col3, col4 = container.columns([0.35, 1, 1, 0.25])
    with col2:
        es_fav = st.toggle(f"¿Favorito?", key=f"fav_{job_id}", value=False)
        if es_fav:
            save_to_favorites(job_id)
    with col3:
        if st.button("Ver detalles", key=f"btn_{job_id}"):
            show_full_details(job)
        else:
            st.write("")

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
    ruta = URL_JOBS
    
    st.markdown("### 🔍 Filtrar ofertas")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1]) # Ajustamos anchos

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

    params = []
    if location: params.append(f"location={location}")
    if skill: params.append(f"skills={skill}")
    if company: params.append(f"company={company}")
    if seniority != 'Cualquiera': params.append(f"seniority={seniority}")
    
    if params and btn_filter:
        ruta = f"{URL_JOBS}?{'&'.join(params)}"
    else:
        ruta = URL_JOBS

    st.markdown("---") # Línea divisoria
    
    with st.spinner('Cargando ofertas...'):
        jobs = get_jobs(token, ruta)
        
    if jobs:
        st.write(f"Se han encontrado **{len(jobs)}** ofertas.")
        container_jobs(jobs)
    else:
        st.info("No hay ofertas disponibles para estos criterios.")

    