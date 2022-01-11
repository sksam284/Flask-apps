import logging
from flask import request
from flasgger.utils import swag_from
from flask_restful import Resource
import os
from . import app
from app import constants as const
from app.cache_util import get_from_memcache, put_to_memcache, get_namespace_keys, existing_key, invalidate_cache

# get logger
logger = logging.getLogger(__name__)

class MasterDataApi(Resource):

    docs = {
        "GET": os.path.join(app.config['SWAGGER_DOCS_DIR'], 'master_data_get.yml'),
        "PATCH": os.path.join(app.config['SWAGGER_DOCS_DIR'], 'master_data_patch.yml'),
        "DELETE": os.path.join(app.config['SWAGGER_DOCS_DIR'], 'master_data_delete.yml')
    }

    @swag_from(docs['GET'])
    def get(self, data_key):
        cache_key = const.CACHE_DATA_KEY.format(data_key)
        data = get_from_memcache(cache_key)
        if not data:
            return {"Message": "Key Doesn't exist in Cache"}, 404
        return data

    @swag_from(docs['PATCH'])
    def patch(self, data_key):
        data = request.get_json(force=True)
        cache_key = const.CACHE_DATA_KEY.format(data_key)
        existing = existing_key(cache_key)
        if not existing:
            return {
                       "Updated": False,
                       "Message": "Key Does not exist."
                   }, 404
        put_to_memcache(cache_key, data=data)
        return {"Updated": True}

    @swag_from(docs['DELETE'])
    def delete(self, data_key):
        cache_key = const.CACHE_DATA_KEY.format(data_key)
        keys = invalidate_cache(cache_key)
        if not keys:
            return {"Message": "Keys Not found in Cache"}, 404

        return {
            "keys": keys,
            "Message": "Deleted"
        }

class MasterDataCreateApi(Resource):
    docs = {
        "GET": os.path.join(app.config['SWAGGER_DOCS_DIR'], 'master_data_all_get.yml'),
        "POST": os.path.join(app.config['SWAGGER_DOCS_DIR'], 'master_data_post.yml')
    }

    @swag_from(docs['GET'])
    def get(self):
        """
        Get all cache keys from Redis
        :return: List of cache keys
        """
        cache_key = const.CACHE_DATA_KEY.format('')
        data = get_namespace_keys(cache_key)
        return data

    @swag_from(docs['POST'])
    def post(self):
        data = request.get_json(force=True)
        data_key = data['data_key']
        cache_key = const.CACHE_DATA_KEY.format(data_key)
        existing = existing_key(cache_key)
        if existing:
            return {
                "Created": False,
                "Message": "Key Already exist."
            }, 422
        put_to_memcache(cache_key, data=data['data'])
        return {"Created": True}

