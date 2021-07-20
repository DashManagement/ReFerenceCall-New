'''
@Description:
@Author: michael
@Date: 2021-07-27 10:10:20
LastEditTime: 2021-07-27 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger


# ReferenceCall 公共类
class CommonReferenceCall:


    # 验证是否有此用户和需要添加的公司 - 返回用户和公司信息
    async def verifyUserAndCompany(self, uid='', company_id=''):

        data = {'action': True}

        # 验证是否有此用户 - 并返回相应用户信息
        user_info = await base.verifyUserReturnInfo(int(uid))
        if user_info is False:
            data['action'] = False
            data['message'] = {'code': 201, 'message': '无效的用户 id'}
            return data

        # 验证是否有此公司
        company_info = await base.verifyFundCompany(company_id)
        if company_info is False:
            data['action'] = False
            data['message'] = {'code': 202, 'message': '无效的公司 id'}
            return data

        data['user_info'] = user_info
        data['company_info'] = company_info

        return data


    # 验证用户是否已经添加过此公司
    async def userIsAddCompany(self, uid='', company_id=''):

        dbo.resetInitConfig('referencecall', 'reference_call_company')
        condition= {'uid':int(uid), 'rc_company_id':int(company_id)}
        field = {'_id':0}
        if await dbo.findOne(condition, field) is None:
            return False
        return True








commonReferenceCall = CommonReferenceCall()