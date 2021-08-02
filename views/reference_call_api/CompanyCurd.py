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
            messages.append(await self.addCompany(uid, value))

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
            return {'code':200, 'message':'已经添加此公司', 'company_id':company_id}

        # 添加用户的 reference call 公司
        add_result = await self.addUserReferenceCall(data_result['user_info'], data_result['company_info'])
        if add_result is False:
            return {'code': 203, 'message': '添加 referencecall 失败'}

        return {'code': 200}


    # 添加用户的 reference call 公司
    async def addUserReferenceCall(self, user_info, company_info):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reference_call_company', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        # 连接数据库集合
        dbo.resetInitConfig('test', 'reference_call_company')

        document = {
            'id': get_id_result['update_id'],
            'uid': user_info['id'],
            'email': user_info['email'],
            'head_portrait': user_info['head_portrait'],
            'user_name': user_info['name'],
            'fund_name': user_info['company_name'],
            'company_icon': user_info['company_icon'],
            'company_introduction': user_info['company_introduction'],
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


    # 删除单个公司
    async def deleteCompany(self, id, uid):

        dbo.resetInitConfig('test', 'reference_call_company')

        # 删除一条数据
        condition = {'id':id, 'uid':uid}
        await dbo.deleteOne(condition)

        # 查询这条数据是否存在
        condition = {'id':id, 'uid':uid}
        field = {'_id':0}
        if await dbo.findOne(condition, field) is None:
            return {'code': 200}
        return {'code': 201, 'message': '删除失败'}


    # 志愿者已经添加的公司列表接口
    async def companyList(self, uid):
        
        dbo.resetInitConfig('test', 'reference_call_company')

        condition = {'uid':uid}
        field = {'rc_company_id':1, '_id':0}
        company_list = await dbo.getData(condition, field)

        if len(company_list) == 0:
            return {'code': 201, 'message':'此用户没有数据'}

        data = {}
        data['code'] = 200
        data['data'] = []

        for value in company_list:
            dbo.resetInitConfig('test','lp_gp')
            condition = {'id':str(value['rc_company_id']), 'company_id':str(value['rc_company_id'])}
            field = {'_id':0}
            result = await dbo.findOne(condition, field)
            data['data'].append(result)

        return data


    # 按公司查看 reference_call 的志愿者列表
    async def companyVolunteersList(self, id, company_id):

        data = {
            'company_info':{},
            'volunteers_list':[]
        }

        # 查询公司信息
        dbo.resetInitConfig('test', 'lp_gp')
        condition = {"id":str(company_id), "company_id":str(company_id), "describe":"0"}
        field = {"id":1, "fund_name":1, "company_info":1, '_id':0}
        company_info = await dbo.findOne(condition, field)

        if company_info is None:
            return {'code': 201, 'message': '不存在的公司'}
        else:
            data['company_info'] = company_info

        # 查询志愿者列表
        dbo.resetInitConfig('test', 'reference_call_company')
        condition = {'rc_company_id': company_id}
        field = {'uid':1, '_id':0}

        # field = {'uid':1, 'is_reservation':1, 'user_name':1, 'fund_name':1, 'company_icon':1, 'company_introduction':1, 'create_time':1, 'update_time':1, '_id':0}
        company_volunteers_list = await dbo.getData(condition, field)

        # 查询日愿者详细信息
        dbo.resetInitConfig('test', 'users')
        for value in company_volunteers_list:
            condition = {'id':int(value['uid'])}
            filed = {'id':1, 'is_reservation':1, 'name':1, 'company_name':1, 'company_icon':1, 'company_introduction':1, 'create_time':1, 'update_time':1, '_id':0}
            result = await dbo.findOne(condition, filed)
            data['volunteers_list'].append(result)

        return {'code':200, 'data':data}








companyCurd = CompanyCurd()