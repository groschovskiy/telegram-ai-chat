import os
import redis
import requests

r = redis.Redis(os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=2, ssl=True)


def list_models():
    url = "https://api.groq.com/openai/v1/models"
    api_key = os.environ.get("GROQ_API_KEY")

    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    data = response.json()

    return [(model['id'], model['owned_by']) for model in data['data']]


def receive_model(user_id):
    model = r.get('user:' + str(user_id) + ':model')
    return model.decode('utf-8') if model else "gemma-7b-it"


def select_model(user_id, model_id):
    if not user_id:
        return None
    elif not model_id:
        return None
    else:
        r.set('user:' + str(user_id) + ':model', str(model_id))
