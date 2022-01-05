'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel


# 设置 redis 缓存数据验证模型
class SetModel(BaseModel):
    key: str
    value: str


# 获取 redis 缓存数据验证模型
class GetModel(BaseModel):
    key: str = ''


# 获取 redis 已经缓存的所有 key 数据验证模型
class KeysModel(BaseModel):
    keys: str = '*'


