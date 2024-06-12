import os
import requests

def list_models():
    url = "https://api.groq.com/openai/v1/models"
    api_key = os.environ.get("GROQ_API_KEY")

    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    data = response.json()

    return [(model['id'], model['owned_by']) for model in data['data']]
