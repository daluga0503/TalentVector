import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@st.cache_data
def get_data():
    response = requests.get(os.getenv('URL_JOBS'))
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Error al cargar los datos de las ofertas laborales.")
        return pd.DataFrame()
    
df = get_data()

st.set_page_config(
    page_title="TalentVector Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título del dashboard
st.markdown("# 📊 TalentVector Dashboard")

# Sistema de filtros

col1, col2, col3 = st.columns(3)
with col1:
    seniority = st.selectbox("Selecciona la seniority", ["Junior", "Mid", "Senior", "Architecture"])
with col2:
    movility = st.selectbox("Selecciona la movilidad", ["Remoto", "Presencial", "Híbrido"])
with col3:
    skills = st.multiselect("Selecciona las skills", ["Python", "Java", "Spring", "Spring Boot", "Angular", "JavaScript", 
                                                    "TypeScript", "PHP", "Laravel","AWS", "Docker", "Frontend", "Backend", 
                                                    "React", "Node.js", "SQL", "NoSQL", "DevOps", "Data Science", "Machine Learning", 
                                                    "IA", "Cloud", "Microservices", "Agile", "Scrum", "Kanban", "CI/CD", "Testing", 
                                                    "Security", "UI/UX"])

st.markdown("## Resultados de ofertas laborales")
st.markdown("Aquí se mostrarán las ofertas laborales filtradas según los criterios seleccionados.")
col1, col2, col3, col4 = st.columns(4)
with col1:
    ofertas_totales = df.shape[0]
    st.metric("Ofertas Totales", ofertas_totales)
with col2:
    ciudades_ofertas = df['location'].value_counts()
    st.metric("Nº Ciudades", ciudades_ofertas)
with col3:
    empresas_ofertas = df['company'].value_counts()
    st.metric("Nº Empresas", empresas_ofertas)
with col4:
    salario_medio = df['salary'].mean()
    st.metric("Salario Medio", f"{salario_medio:.2f} €")

df_filtrado = df.copy()
if seniority:
    df_filtrado = df_filtrado[df_filtrado['seniority'] == seniority]
if movility:
    df_filtrado = df_filtrado[df_filtrado['movility'] == movility]
if skills:
    df_filtrado = df_filtrado[df_filtrado['skills'].apply(lambda x: all(skill in x for skill in skills))]

# Gráficos de análisis
st.markdown("## Análisis de datos")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Distribución de Ofertas por Seniority")
    seniority_counts = df_filtrado['seniority'].value_counts()
    fig1 = px.bar(seniority_counts, x=seniority_counts.index, y=seniority_counts.values, labels={'x': 'Seniority', 'y': 'Número de Ofertas'}, title="Ofertas por Seniority")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.markdown("### Distribución de Ofertas por Movilidad")
    movility_counts = df_filtrado['movility'].value_counts()
    fig2 = px.bar(movility_counts, x=movility_counts.index, y=movility_counts.values, labels={'x': 'Movilidad', 'y': 'Número de Ofertas'}, title="Ofertas por Movilidad")
    st.plotly_chart(fig2, use_container_width=True)

# Mapa de calor geográfico
st.markdown("### Mapa de Calor de Ofertas por Ciudad")
city_counts = df_filtrado['location'].value_counts().reset_index()
city_counts.columns = ['city', 'count']
fig3 = px.choropleth(city_counts, locations='city', locationmode='country names', color='count', color_continuous_scale='Viridis', title="Mapa de Calor de Ofertas por Ciudad")
st.plotly_chart(fig3, use_container_width=True)

# Gráfico de barras de habilidades más demandadas
st.markdown("### Habilidades Más Demandadas")
skills_counts = df_filtrado['skills'].explode().value_counts().reset_index()
skills_counts.columns = ['skill', 'count']
fig4 = px.bar(skills_counts.head(20), x='skill', y='count', labels={'skill': 'Habilidad', 'count': 'Número de Ofertas'}, title="Habilidades Más Demandadas")
st.plotly_chart(fig4, use_container_width=True)



