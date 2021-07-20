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

# 基金公司详情
class FundDetails:


    # 返回单个基金公司详情
    async def returnFundDetails(self, uid='', company_id=''):

        # 验证是否有此用户
        if await base.verifyUser(int(uid)) is False:
            return {'code': 201, 'message': '无效的用户 id'}

        # 验证是否有此公司
        company_info = await base.verifyFundCompany(company_id)
        if company_info is False:
            return {'code': 202, 'message': '无效的公司 id'}

        return company_info










fundDetails = FundDetails()