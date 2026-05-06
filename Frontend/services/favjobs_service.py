import requests
from ...utils import load_config

url_favjobs = load_config()['URL_FAVJOBS']

def get_fav_jobs(token):
    headers = {
        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"
    }

    response = requests.get(url=url_favjobs, headers=headers)
    return response.json() if response.status_code == 200 else []

def add_job_to_fav(token, job_id):
    headers = {
        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"
    }
    payload ={
        "job_id": job_id
    }
    response = requests.post(url=url_favjobs, headers=headers, json=payload)
    if response.status_code == 201:
        return True
    return False

def remove_job_from_fav(token, job_id):
    headers = {
        "Authorization" : f"Bearer {token}",
        "Content-Type" : "application/json"
    }

    payload = {
        "job_id": job_id
    }

    response = requests.delete(url=url_favjobs, headers=headers, json=payload)
    if response.status_code in [200, 204]:
        return True
    return False

