import logging

from abc import ABC, abstractmethod
from redis.asyncio import Redis
from orjson import orjson


class Cache(ABC):
    @abstractmethod
    async def get(self, key):
        pass


class RedisCache(Redis, Cache):

    async def get(self, key):
        logging.debug("getting objects from cache by key {0}".format(key))
        cache_data = await super().get(key)
        if not cache_data:
            logging.debug("Cache empty")
            return None

        objects_data = orjson.loads(cache_data)

        return objects_data


cache: RedisCache = None


async def get_cache() -> RedisCache:
    return cache
