'''
@Description:
@Author: michael
@Date: 2021-07-09 10:16:20
LastEditTime: 2021-07-09 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger

# 基金列表
class FundList:

    uid = ''

    async def returnFundList(self, uid=''):

        self.uid = uid

        # 验证是否有此用户
        if await base.verifyUser(int(uid)) is False:
            return {'code': 201, 'message': '无效的用户 id'}

        # 返回基金公司列表
        return await self.getFundList()


    # 返回基金公司列表
    async def getFundList(self):

        # 连接数据库 - 切换到 dash_test 数据库的 lp_gp 表
        dbo.resetInitConfig('test', 'lp_gp')

        condition = {"$where": "this.id == this.company_id", "describe":"0"}
        field = {'id':1, 'company_id':1, 'fund_name':1, 'company_icon':1, 'base_info':1, 'company_info':1, '_id':0}
        result = await dbo.getData(condition, field)

        return result










fundList = FundList()