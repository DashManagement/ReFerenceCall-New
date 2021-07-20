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
from views.reference_call_api.CommonReferenceCall import commonReferenceCall

# reference call 对于 公司的 增/删/改/查/操作
class CompanyCurd:


    # 添加多个公司
    async def addManyCompany(self, uid='', company_id=''):

        messages = []
        for value in company_id:
            messages.push(self.addCompany(uid, value))

        return messages


    # 添加单个 公司
    async def addCompany(self, uid='', company_id=''):

        # 验证是否有此用户和需要添加的公司 - 返回用户和公司信息
        data_result = await commonReferenceCall.verifyUserAndCompany(uid, company_id)
        if data_result['action'] is False:
            return data_result['message']

        # 验证是否用户已经添加过此公司
        is_add = await commonReferenceCall.userIsAddCompany(uid, company_id)
        if is_add is True:
            return {'code':200, 'message':'已经添加此公司'}

        # 添加用户的 reference call 公司
        add_result = await self.addUserReferenceCall(data_result['user_info'], data_result['company_info'])
        if add_result is False:
            return {'code': 203, 'message': '添加 referencecall 失败'}

        return {'code': 200}


    # 添加用户的 reference call 公司
    async def addUserReferenceCall(self, user_info, company_info):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reference_call_company', db='referencecall')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False
        print(user_info)
        # 连接数据库集合
        dbo.resetInitConfig('referencecall', 'reference_call_company')

        document = {
            'id': get_id_result['update_id'],
            'uid': user_info['id'],
            'email': user_info['email'],
            'head_portrait': user_info['head_portrait'],
            'user_name': user_info['user_name'],
            'fund_name': user_info['fund_name'],
            'company_icon': user_info['company_icon'],
            'rc_company_id': int(company_info['id']),
            'rc_fund_name': company_info['fund_name'],
            'rc_company_icon': company_info['company_icon'],
            'create_time': common.getTime(),
            'update_time': 1,
            'delete_time': 1
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True
        









companyCurd = CompanyCurd()