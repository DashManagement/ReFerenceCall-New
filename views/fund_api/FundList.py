'''
@Description:
@Author: michael
@Date: 2021-07-09 10:16:20
LastEditTime: 2021-08-08 16:51:32
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger


# 基金列表
class FundList:


    async def returnFundList(self, uid=''):

        # 判断如果是游戏客而直接返回 fund_list 基金印象上表
        if uid == "refid":
            return await self.getFundList()

        # 验证是否有此用户
        if await base.verifyUser(int(uid)) is False:
            return {'code': 201, 'message': '用户不存在'}

        return await self.getFundList()


    # 返回基金公司列表
    async def getFundList(self):

        dbo.resetInitConfig('test', 'lp_gp')

        condition = {"$where": "this.id == this.company_id", "describe": "0"}
        field = {'id': 1, 'company_id': 1, 'fund_name': 1, 'company_icon': 1, 'base_info': 1, 'company_info': 1, '_id': 0}
        # 按公司名称 1-10，a-z 排序
        sort = [('fund_name',1)]

        result = await dbo.getDataSort(condition, field, sort)

        if len(result) == 0:
            '''如果不存在记录则返回总数为0的，空列表'''
            return {'code': 200, 'count':0, 'data': []}
        else:
            return {'code': 200, 'count':len(result), 'data': result}








fundList = FundList()
