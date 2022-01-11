"""
application common setting value
"""
import os

from os.path import dirname
import logging

BASE_DIR = dirname(dirname(__file__))

DEBUG = True
ENABLE_LOGGING = True
LOG_LEVEL = logging.DEBUG
ENV = os.getenv('ENVIRONMENT')

SWAGGER_DOCS_DIR = os.path.join(BASE_DIR, "docs")

REDIS_BROKER = "localhost"
REDIS_BROKER_PORT = 6379
REDIS_DB = '0'