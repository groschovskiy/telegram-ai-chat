import os
import redis

r = redis.Redis(os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=2, ssl=True)


def get_ai_model(user_id):
    model = r.get('user:' + str(user_id) + ':model')
    return model.decode('utf-8') if model else "gemma-7b-it"


def set_ai_model(user_id, model_id):
    r.set('user:' + str(user_id) + ':model', str(model_id))

def download(url):
    