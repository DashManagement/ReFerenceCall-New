'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-08-08 01:01:41
LastEditors: fanshaoqiang
'''
# coding=utf-8

# 加载第三方包
# from bson.objectid import ObjectId

# 加载自己创建的包
from common.register_class import *
from config.log_config import logger


class Base:

    # 根据 id 验证是否有此用户
    async def verifyUser(self, uid=''):

        # 连接数据库
        dbo.resetInitConfig('test', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'id': uid}
        field = {'id': 1, '_id': 0}
        user_info = await dbo.findOne(condition, field)

        if user_info is None:
            return False

        return True

    # 根据 id 验证是否有此用户 - 并返回用户信息

    async def verifyUserReturnInfo(self, uid=''):

        # 连接数据库
        dbo.resetInitConfig('test', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'id': uid}
        field = {'_id': 0}
        user_info = await dbo.findOne(condition, field)

        if user_info is None:
            return False

        return user_info

    # 非异步的 - 根据 id 验证是否有此用户 - 并返回用户信息
    def awaitVerifyUserReturnInfo(self, uid=''):

        # 连接数据库
        dbo.resetInitConfig('test', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'id': uid}
        field = {'_id': 0}
        user_info = dbo.findOne(condition, field)

        if user_info is None:
            return False

        return user_info


    # 根据 id 验证是否有此公司 - 并返回公司信息

    async def verifyFundCompany(self, company_id=''):

        # 连接数据库
        dbo.resetInitConfig('test', 'lp_gp')

        # 条件 - 用户名 - 返回字段 全部
        # condition = {"$where": "this.id == this.company_id", "describe":"0", "company_id":company_id}
        condition = {"id": company_id,
                     "company_id": company_id, "describe": "0"}
        field = {'id': 1, 'company_id': 1, 'fund_name': 1,
                 'company_icon': 1, 'base_info': 1, 'company_info': 1, '_id': 0}
        company_info = await dbo.findOne(condition, field)

        if company_info is None:
            return False

        return company_info

    # 返回用户Push相关的参数

    async def getUserPushInfo(self, uid):
        # 连接数据库
        dbo.resetInitConfig('test', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'id': int(uid)}
        field = {'_id': 0}
        user_info = await dbo.findOne(condition, field)

        if user_info is None:
            return None

        return {"userName": user_info.get("name"), "userEmail": user_info.get("email"),
                "userToken": user_info.get("userToken"), "localTimeZone": user_info.get("localTimeZone"), "platForm": user_info.get("platForm")}






base = Base()
