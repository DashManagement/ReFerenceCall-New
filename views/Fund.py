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

        # 加入 redis 列表缓存
        await redis.init_cache()
        fund_data = await redis.get('fund_data')

        # 判断是否有缓存基金列表，如果没有则获取数据库数据并缓存基金列表
        if fund_data is None:
            '''将基金列表加入 redis 缓存(转换成字符串 str)，将返回数据'''
            fund_data = await fundList.returnFundList(uid)
            await redis.set('fund_data',str(fund_data))
            return fund_data
        else:
            '''将缓存中的基金列表字符串 str 转换为 dict 数据类型'''
            return eval(fund_data)


    # 基金公司详情
    async def fundDetails(self, uid, company_id):
        return await fundDetails.returnFundDetails(uid, company_id)

    










fund = Fund()