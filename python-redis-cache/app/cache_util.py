import json
import logging
import datetime
logger = logging.getLogger(__name__)

def existing_key(resource_url: str):
    """ Check if key exist in Cache"""
    from app import app_redis_handler
    if app_redis_handler.exists(resource_url):
        return True
    else:
        False

def get_from_memcache(resource_url: str):
    """ Get Resource from Cache specifying the exact key"""
    from app import app_redis_handler
    key = f'{resource_url}'
    if not existing_key(key):
        return None
    #if not app_redis_handler.exists(key):
    #    return None
    data_str = app_redis_handler.get(key)
    if data_str:
        try:
            return json.loads(data_str)
        except Exception as ex:
            logger.error(
                f"Could not resolve the data in redis cache, url={resource_url}, data_str={data_str}, exc={ex}")
            app_redis_handler.delete(key)
    return None


def get_data_from_cache(cache_key: str):
    cache_result = get_from_memcache(resource_url=cache_key)
    return cache_result.get("data", None) if cache_result else None


def get_cache_data_from_pattern(resource_url_pattern: str):
    from app import app_redis_handler
    keys = []
    for key in app_redis_handler.scan_iter(f'{resource_url_pattern}*'):
                keys.append(key)
    return keys


def put_to_memcache(resource_url: str, data: dict, retries=3, expiry=None):
    """ Put Resource into Cache specifying the exact key"""
    from app import app_redis_handler
    key = f'{resource_url}'
    try:
        app_redis_handler.set(key, json.dumps(data, default=stringify_date))
        if expiry is not None:
            app_redis_handler.expire(key, expiry)
        logger.info(f'Inserted {resource_url}')
    except Exception as ex:
        logger.error(f'Error during storage to redis cache url {resource_url} and exception is: {ex}')
        # Re-Try
        if retries <= 0:
            logger.error(f'Redis Insertion Failed for Key {resource_url}, Data: {data}')
            return
        logger.info(f'Re-Trying Inserting {resource_url}')
        return put_to_memcache(resource_url, data, retries=retries-1)
    return


def get_namespace_keys(namespace):
    """ Get Keys from Cache specifying the namespace"""
    from app import app_redis_handler
    return [key for key in app_redis_handler.scan_iter(f'{namespace}*')]


def invalidate_cache(resource_urls: list, wild_card=False):
    """ Delete Resource(s) from Cache"""
    from app import app_redis_handler
    keys = []
    for resource in resource_urls:
        if wild_card:
            for key in app_redis_handler.scan_iter(f'{resource}*'):
                keys.append(key)
        else:
            keys.append(resource)
    [app_redis_handler.delete(key) for key in keys]
    return keys


def stringify_date(o):
    """ Stringify Date"""

    if isinstance(o, datetime.date):
        return o.__str__()

