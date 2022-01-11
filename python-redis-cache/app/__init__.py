# search_app/__init__.py
from flask import Flask
import redis
from flasgger import Swagger

from . import settings



app = Flask(__name__)
app.config.from_object(settings)

Swagger(app)

from . import routes  # noqa: F401 isort:skip


REDIS_BROKER = app.config['REDIS_BROKER']
REDIS_BROKER_PORT = app.config['REDIS_BROKER_PORT']
REDIS_DB = app.config['REDIS_DB']

app_redis_handler = redis.Redis(
    REDIS_BROKER,
    int(REDIS_BROKER_PORT),
    REDIS_DB,
    encoding='utf-8',
    decode_responses=True)

print(dir(redis.Redis))