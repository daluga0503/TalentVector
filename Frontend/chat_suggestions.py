import streamlit as st
from chatbot.model import Model
from dotenv import load_dotenv
import os

load_dotenv()

@st.cache_resource
def get_model():
    return Model('it-recruiter', os.getenv('URL_OLLAMA'))

# Inicialización del estado de la sesión para almacenar la respuesta del modelo
if 'response' not in st.session_state:
    st.session_state.response = '¡Hola! Soy tu reclutador IT. ¿En qué puedo ayudarte?'

# Configuración de la página
st.set_page_config(page_title="IT Recruiter AI", page_icon="💼")

st.title('💼 IT Specialist Recruiter Chat')
st.markdown("Optimiza tu perfil técnico y prepárate para entrevistas con IA.")

# Formulario para enviar mensajes al chatbot
with st.form(key="chat_form"):
    st.markdown("#### Escribe tu mensaje")
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            label="Escribe tu mensaje",
            placeholder="¿Cómo optimizo mi CV para AI Engineer",
            icon="✍️",
            label_visibility="collapsed"
        )
    with col2:
        submit_button = st.form_submit_button("Enviar", use_container_width=True)

if submit_button:
    if user_input != "":
        with st.spinner("Generando respuesta..."):
            model = get_model()
            response = model.generate(prompt=user_input.strip())
            st.session_state.response = response
    else:
        st.error("Por favor, completa todos los campos antes de enviar el mensaje.")

formatted_response = st.session_state.response.replace('\n', '<br>')
st.markdown(
    f"""
    <div style="background-color:#f6f6f6; border-radius:10px; padding:20px; margin-top:20px; border:1px solid #e3e3e3;">
    <b>Chatbot:</b><br>
    {formatted_response}
    </div>
    """,
    unsafe_allow_html=True
)