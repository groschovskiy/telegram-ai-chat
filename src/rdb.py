import os
import redis

r = redis.Redis(os.environ.get("REDIS_URL"), port=os.environ.get("REDIS_PORT"), db=2, ssl=True)


def get_ai_model(user_id):
    resp = r.get('user:' + str(user_id) + ':model')
    if resp is None:
        return "gemma-7b-it"
    else:
        return r.get('user:' + str(user_id) + ':model')


def set_ai_model(user_id, model_id):
    r.set('user:' + str(user_id) + ':model', str(model_id))
