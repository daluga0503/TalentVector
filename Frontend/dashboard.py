import streamlit as st
import pandas as pd
import plotly.express as px
from services.jobs_service import get_jobs
from utils import load_config

token = st.session_state.get('access')
ruta = load_config()['URL_JOBS']
jobs = get_jobs(token, ruta)
df = pd.DataFrame(jobs)

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
    seniority = st.multiselect("Selecciona la seniority", ["Junior", "Mid", "Senior", "Architecture"])
with col2:
    movility = st.multiselect("Selecciona la movilidad", ["Remoto", "Presencial", "Híbrido"])
with col3:
    skills = st.multiselect("Selecciona las skills", ["Python", "Java", "Spring", "Spring Boot", "Angular", "JavaScript", 
                                                    "TypeScript", "PHP", "Laravel","AWS", "Docker", "Frontend", "Backend", 
                                                    "React", "Node.js", "SQL", "NoSQL", "DevOps", "Data Science", "Machine Learning", 
                                                    "IA", "Cloud", "Microservices", "Agile", "Scrum", "Kanban", "CI/CD", "Testing", 
                                                    "Security", "UI/UX"])
    

df_filtrado = df.copy()
if seniority:
    seniority = [s.lower() for s in seniority]
    df_filtrado = df_filtrado[df_filtrado['seniority'].isin(seniority)]
if movility:
    movility = [m.lower() for m in movility]
    df_filtrado = df_filtrado[df_filtrado['movility'].isin(movility)]
if skills:
    df_filtrado = df_filtrado[df_filtrado['skills'].apply(lambda x: any(skill in x for skill in skills))]

st.markdown("## Resultados de ofertas laborales")
st.markdown("Aquí se mostrarán las ofertas laborales filtradas según los criterios seleccionados.")
col1, col2, col3, col4 = st.columns(4)
with col1:
    ofertas_totales = df_filtrado.shape[0]
    st.metric("Ofertas Totales", ofertas_totales)
with col2:
    ciudades_ofertas = df_filtrado['location'].nunique()
    st.metric("Nº Ciudades", ciudades_ofertas)
with col3:
    empresas_ofertas = df_filtrado['company'].nunique()
    st.metric("Nº Empresas", empresas_ofertas)
with col4:
    salario_medio = df_filtrado['salary'].mean()
    st.metric("Salario Medio", f"{salario_medio:.2f} €")



# Gráficos de análisis
st.markdown("## Análisis de datos")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Distribución de Ofertas por Seniority")
    # 1. Convertimos la Serie en un DataFrame con columnas claras
    seniority_counts = df_filtrado['seniority'].value_counts().reset_index()
    seniority_counts.columns = ['level', 'total']

    # 2. Ahora pasamos los nombres de las columnas como strings
    fig1 = px.bar(
        seniority_counts, 
        x='level', 
        y='total', 
        labels={'level': 'Seniority', 'total': 'Número de Ofertas'}, 
        title="Ofertas por Seniority",
        color='level' # Opcional: añade colores por categoría
    )
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.markdown("### Distribución de Ofertas por Movilidad")
    movility_counts = df_filtrado['movility'].value_counts()
    fig2 = px.bar(movility_counts, x=movility_counts.index, y=movility_counts.values, labels={'x': 'Movilidad', 'y': 'Número de Ofertas'}, title="Ofertas por Movilidad")
    st.plotly_chart(fig2, use_container_width=True)

# Mapa de calor geográfico
st.markdown("### Top 10 Provincias con más Ofertas")
city_counts = df_filtrado['location'].value_counts().reset_index()
city_counts.columns = ['city', 'count']
fig3 = px.bar(
    city_counts.head(10), 
    x='count', 
    y='city', 
    orientation='h',
    color='count',
    color_continuous_scale='Viridis'
)
# Esto hace que la barra más alta esté arriba
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

# Gráfico de barras de habilidades más demandadas
st.markdown("### Habilidades Más Demandadas")
skills_counts = df_filtrado['skills'].explode().value_counts().reset_index()
skills_counts.columns = ['skill', 'count']
fig4 = px.bar(skills_counts.head(20), x='skill', y='count', labels={'skill': 'Habilidad', 'count': 'Número de Ofertas'})
st.plotly_chart(fig4, use_container_width=True)



