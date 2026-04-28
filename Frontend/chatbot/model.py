import ollama
import requests

# Clase para interactuar con el modelo LLM de ollama
class Model:
    # Inicialización del modelo con el nombre, la URL del endpoint y el cliente de ollama
    # El cliente se usa para enviar solicitudes al modelo y obtener respuestas
    def __init__(self, model_name, url):
        self.model_name = model_name
        self.client = ollama.Client()
        self.url = url

    # Método para generar una respuesta del modelo dado un prompt
    # Envía el prompt al modelo y devuelve la respuesta generada
    # Utiliza la URL del endpoint y el nombre del modelo para hacer la solicitud
    def generate(self, prompt):
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": 1.0,
            "max_tokens": 1000,
            "stream": False
        }
        # Realiza una solicitud POST al endpoint del modelo con el payload
        response = requests.post(self.url, json=payload)
        # Si la respuesta es exitosa, devuelve el texto generado
        # Si hay un error, lanza una excepción con el mensaje de error
        if response.status_code == 200:
            return response.json()["response"]
        else:
            raise Exception(f"Error generating text: {response.status_code} - {response.text}")