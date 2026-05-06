import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    config = {
        'URL_AUTH': os.getenv('URL_AUTH'),
        'URL_JOBS': os.getenv('URL_JOBS'),
        'URL_FAVJOBS': os.getenv('URL_FAVJOBS'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY')
    }
    return config