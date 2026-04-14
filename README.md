# TalentVector 🚀
**Optimización de Búsqueda Laboral mediante Inteligencia Artificial y Web Scraping**

TalentVector no es solo un agregador de empleos; es un ecosistema inteligente diseñado para cerrar la brecha entre los candidatos y las ofertas de trabajo ideales. Utilizando técnicas avanzadas de **RAG (Retrieval-Augmented Generation)** y **Web Scraping**, la aplicación permite a los usuarios gestionar su carrera profesional de forma proactiva.

---

## 🌟 Características Principales

### 🔍 Búsqueda Inteligente (RAG)
Olvida los filtros por palabras clave tradicionales. TalentVector utiliza la arquitectura **RAG**:
- **Análisis de CV:** Sube tu currículum en PDF.
- **Búsqueda Semántica:** El sistema vectoriza tu perfil y lo compara con miles de ofertas de Infojobs, devolviendo las posiciones que mejor encajan con tu experiencia real y habilidades, no solo con títulos de cargo.

### 🤖 Chatbot de Asesoramiento
Un asistente virtual especializado disponible 24/7 para:
- Optimizar los puntos clave de tu CV.
- Simular entrevistas técnicas o de comportamiento.
- Resolver dudas sobre el mercado laboral actual.

### 🕷️ Scraping Avanzado de Infojobs
Motor de extracción de datos robusto que recopila ofertas en tiempo real:
- **Exclusivo para Administradores:** Control total sobre la actualización de la base de datos para evitar redundancias y garantizar la calidad de la información.
- Tecnologías: Extracción dinámica para superar retos de carga de contenido.

### 📊 Dashboard
Visualiza tu progreso mediante paneles interactivos:
- Estado de tus candidaturas (Postulado, En proceso, Finalizado).
- Estadísticas sobre las ofertas que más se ajustan a tu perfil.
- Gestión de favoritos.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Lenguaje Core** | Python 3.x |
| **Backend / API** | Django |
| **Frontend / Interfaz** | Streamlit |
| **Scraping** | BeautifulSoup & Playwright (para contenido dinámico) |
| **Base de Datos Relacional** | SQLite (Gestión de usuarios y estados) |
| **Base de Datos NoSQL** | MongoDB (Almacenamiento de ofertas y vectores) |
| **IA / LLM** | LangChain / OpenAI (Implementación RAG) |

---

## 🏗️ Arquitectura del Sistema

1.  **Capa de Datos:** Los scrapers (Playwright) obtienen datos de Infojobs y los limpian. Las ofertas se almacenan en MongoDB.
2.  **Capa de IA:** Al subir un CV, se generan embeddings que se comparan con los documentos en el almacén de vectores.
3.  **Capa de Usuario:** Una interfaz en Streamlit que se comunica con el backend de Django para gestionar la lógica de negocio y la persistencia de datos de usuario.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para poner en marcha TalentVector en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/TalentVector.git](https://github.com/tu-usuario/TalentVector.git)
cd TalentVector

