'''
@Description:
@Author: michael
@Date: 2021-08-12 10:16:20
LastEditTime: 2021-09-26 18:19:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *


# 默认配置接口
class DefaultConfig:


    # app端 启动时的默认配置
    async def appStartConfig(self):

        dbo.resetInitConfig('test', 'default_config')

        condition = {'id': 1}
        field = {
            'company_volunteers_num': 1,
            'request_volunteers_num': 1,
            'volunteers_reply_time_num': 1, 
            '_id': 0
        }
        result = await dbo.findOne(condition, field)
        return {'code':200, 'data':result}


    # APP端 时区设置
    async def timeZone(self):

        dbo.resetInitConfig('test', 'default_config')

        condition = {'id': 2}
        field = {'time_zone':1, '_id': 0}
        result = await dbo.findOne(condition, field)
        return {'code':200, 'data':result['time_zone']}







defaultConfig = DefaultConfig()