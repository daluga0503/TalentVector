import requests
import streamlit as st

def get_jobs(token, ruta):
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(ruta, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else []
        else:
            return []
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
    
def scrap_jobs(token, ruta):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ruta, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
