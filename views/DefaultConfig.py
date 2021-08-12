'''
@Description:
@Author: michael
@Date: 2021-08-12 10:16:20
LastEditTime: 2021-08-12 20:00:00
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
        return await dbo.findOne({},{'_id':0})











defaultConfig = DefaultConfig()