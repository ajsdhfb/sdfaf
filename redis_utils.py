import redis
import config

pool = redis.ConnectionPool(host=config.REDIS_HOSTNAME, port=config.REDIS_PORT, encoding='utf8', decode_responses=True)


def get_connection():
    return redis.StrictRedis(connection_pool=pool)


def check_key_existence(key_name):
    return get_connection().exists(key_name)


def get_key(key_name):
    return get_connection().get(key_name)


def set_key_value(key, value):
    get_connection().set(key, value)
