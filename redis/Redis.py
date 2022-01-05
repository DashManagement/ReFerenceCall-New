'''
@Description:
@Author: michael
@Date: 2021-09-25 10:16:20
LastEditTime: 2021-09-29 20:00:00
LastEditors: michael
'''

# coding=utf-8


from typing import Optional
from aioredis import Redis, create_redis_pool



class RedisCache:




    def __init__(self):
        self.redis_cache: Optional[Redis] = None
        # self.redis_cache = Redis


    async def init_cache(self, db_connection="redis://localhost:6379/0?encoding=utf-8"):

        self.redis_cache = await create_redis_pool(db_connection)
        # self.redis_cache = await create_redis_pool(('127.0.0.1', 6379), db=7, encoding='utf-8')


    async def keys(self, pattern):
        return await self.redis_cache.keys(pattern)


    async def set(self, key, value):
        return await self.redis_cache.set(key, value)


    async def get(self, key):
        return await self.redis_cache.get(key)


    async def close(self):
        self.redis_cache.close()
        await self.redis_cache.wait_closed()





# redisCache = RedisCache()