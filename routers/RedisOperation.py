'''
@Description:
@Author: michael
@Date: 2020-07-13 10:50:20
LastEditTime: 2021-09-26 18:19:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from redis.Redis import RedisCache
from models.RedisModel import *

# 创建 APIRouter 实例
router = APIRouter()

# 创建 redis 实例
redis = RedisCache()



# 获取单个 key 的 value
@router.post('/api/redis/set')
async def set(set_params: SetModel):

    # 初始化 redis 连接
    await redis.init_cache()

    params = set_params.__dict__
    cache_result = await redis.set(params['key'], params['value'])

    # 判断设置值是否成功
    if cache_result is True:
        return {'code': 200}
    else:
        return {'code': 201}


# 获取单个 key 的 value
@router.post('/api/redis/get')
async def get(get_params: GetModel):

    # 初始化 redis 连接
    await redis.init_cache()

    params = get_params.__dict__
    return await redis.get(params['key'])


# 获取 redis 已经缓存的所有 key
@router.post('/api/redis/keys')
async def keys(keys_params: KeysModel):

    # 初始化 redis 连接
    await redis.init_cache()

    params = keys_params.__dict__
    return await redis.keys(params['keys'])
