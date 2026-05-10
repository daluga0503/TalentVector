import streamlit as st
from groq import Groq
from utils import load_config

client = Groq(api_key=load_config()['GROQ_API_KEY'])

st.session_state.messages = [
    {"role": "system", "content": "Eres un reclutador IT especializado en optimizar perfiles técnicos y preparar a candidatos para entrevistas. Proporciona consejos prácticos, sugerencias de habilidades y estrategias para destacar en el mercado laboral tecnológico."}
]

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
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages + [{"role": "user", "content": user_input}]],
            )

            answer = completion.choices[0].message.content
            st.session_state.response = answer
            st.session_state.messages.append({"role": "assistant", "content": answer})
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