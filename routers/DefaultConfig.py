'''
@Description:
@Author: michael
@Date: 2020-08-12 10:10:20
LastEditTime: 2021-09-26 18:19:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.DefaultConfig import defaultConfig

# 创建 APIRouter 实例
router = APIRouter()

# APP端 默认配置
@router.get('/api/default_config')
async def appStartConfig():
    return await defaultConfig.appStartConfig()


# APP端 时区设置
@router.get('/api/time_zone')
async def timeZone():
    return await defaultConfig.timeZone()


