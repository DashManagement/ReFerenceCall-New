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
from views.fund_api.FundList import fundList
from views.fund_api.FundDetails import fundDetails


# 基金接口类
class Fund:


    # 基金公司列表
    async def fundList(self, uid):
        return await fundList.returnFundList(uid)


    # 基金公司详情
    async def fundDetails(self, uid, company_id):
        return await fundDetails.returnFundDetails(uid, company_id)

    










fund = Fund()