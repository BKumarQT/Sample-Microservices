import aioredis
from decouple import config

from app import logger

log = logger.get_logger()


async def connect_to_redis():
    # Replace the following values with our Redis server information
    redis_host = config("redis_host")  # e.g., 'localhost'
    redis_port = config("redis_port")  # Default Redis port is 6379

    log.info(f"redis host -> {redis_host}")
    # Create a connection to the Redis server
    redis = await aioredis.Redis(host=redis_host, port=redis_port, db=0)
    log.info(f"redis connection object --> {redis}")
    return redis


class RedisConnection:

    @staticmethod
    async def set_key(key, value, ex=None):
        """
        Set the value in redis
        :param ex:
        :param key: key to -> name of the data
        :param value: information to be stored
        :return: str
        """
        log.info(f"key, value and ex sent to set in the redis {key} {value} and {ex} respectively")
        redis = await connect_to_redis()
        # SET operation to set a key-value pair in Redis
        await redis.set(key, value, ex)
        await redis.close()

    @staticmethod
    async def get_key(key):
        """
        Get the data from redis
        :param key: -key-set while storing
        :return: str
        """
        redis = await connect_to_redis()
        # GET operation to retrieve the value associated with the given key from Redis
        value = await redis.get(key)
        await redis.close()
        return value


redis_obj = RedisConnection()
