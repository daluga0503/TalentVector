import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
URL_JOBS = os.getenv('URL_JOBS')



def get_jobs(token, ruta):
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(ruta, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list):
                return data
            else:
                st.error("Error: La respuesta no es una lista de trabajos.")
                return []
        except ValueError:
            st.error("Error: No se pudo parsear la respuesta JSON.")
            return []
    else:
        st.error(f"Error al obtener trabajos: {response.status_code}")
        return []
