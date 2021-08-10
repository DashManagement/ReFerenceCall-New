'''
@Description:
@Author: michael
@Date: 2021-07-27 10:10:20
LastEditTime: 2021-08-08 12:05:51
LastEditors: fanshaoqiang
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger
from views.reference_call_api.CommonReferenceCall import commonReferenceCall
from views.reference_call_api.TimeOperation import timeOperation

# reference call 对于 公司的 增/删/改/查/操作


class CompanyCurd:

    # 添加多个公司
    async def addManyCompany(self, uid='', company_id=''):

        messages = []
        for value in company_id:
            messages.append(await self.addCompany(uid, value))

        isAllSuccess = True
        for item in messages:
            if item.get("code") != 200:
                isAllSuccess = False

        if isAllSuccess == False:
            return {"code": 203, "message": "批量添加失败", "detail": messages}

        ret = {"code": 200, "message": "批量添加成功", "detail": messages}

        return ret

    # 添加单个 公司

    async def addCompany(self, uid='', company_id=''):

        # 验证是否有此用户和需要添加的公司 - 返回用户和公司信息
        data_result = await commonReferenceCall.verifyUserAndCompany(uid, company_id)
        if data_result['action'] is False:
            return data_result['message']

        # 验证是否用户已经添加过此公司
        is_add = await commonReferenceCall.userIsAddCompany(uid, company_id)
        if is_add is True:
            return {'code': 200, 'message': '已经添加此公司', 'company_id': company_id}

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
        condition = {'id': id, 'uid': uid}
        await dbo.deleteOne(condition)

        # 查询这条数据是否存在
        condition = {'id': id, 'uid': uid}
        field = {'_id': 0}
        if await dbo.findOne(condition, field) is None:
            return {'code': 200}
        return {'code': 201, 'message': '删除失败'}

    # 志愿者已经添加的公司列表接口

    async def companyList(self, uid):

        dbo.resetInitConfig('test', 'reference_call_company')

        condition = {'uid': uid}
        field = {'id': 1, 'rc_company_id': 1, '_id': 0}
        company_list = await dbo.getData(condition, field)

        if len(company_list) == 0:
            return {'code': 201, 'message': '此用户没有数据'}

        data = {}
        data['code'] = 200
        data['data'] = []

        for value in company_list:
            dbo.resetInitConfig('test', 'lp_gp')
            condition = {'id': str(value['rc_company_id']), 'company_id': str(
                value['rc_company_id'])}
            field = {'_id': 0}
            result = await dbo.findOne(condition, field)
            result['insert_id'] = value['id']
            data['data'].append({
                'insert_id': value['id'],
                'company_id': result['company_id'],
                'company_name': result['fund_name'],
                'company_info': result['company_info'],
                'company_icon': result['company_icon'],
                'create_time': result['reg_time']
            })

        return data

    # 按公司查看 reference_call 的志愿者列表

    async def companyVolunteersList(self, id, company_id):

        data = {
            'company_info': {},
            'volunteers_list': []
        }

        # 查询公司信息
        dbo.resetInitConfig('test', 'lp_gp')
        condition = {"id": str(company_id), "company_id": str(company_id), "describe": "0"}
        field = {"id": 1, "fund_name": 1, "company_info": 1, '_id': 0}
        company_info = await dbo.findOne(condition, field)

        if company_info is None:
            return {'code': 201, 'message': '不存在的公司'}
        else:
            data['company_info'] = company_info

        # 查询志愿者 id 列表
        dbo.resetInitConfig('test', 'reference_call_company')
        condition = {'rc_company_id': company_id}
        field = {'uid': 1, '_id': 0}

        company_volunteers_id_list = await dbo.getData(condition, field)
        
        # 查看志愿者是否有多余的时间来处理预约会议
        check_volunteers_time = await self.checkVolunteersTime(company_volunteers_id_list)
        return check_volunteers_time
        # 查询志愿者详细信息
        data['volunteers_list'] = []
        dbo.resetInitConfig('test', 'users')
        for value in company_volunteers_id_list:
            '''根据 uid 查询公司匹配的志愿者信息（不包括当前用户id 的志愿者，也就是排除志愿者自己）'''
            condition = {'$and': [
                {'id': int(value['uid'])},
                {'id': {'$ne': int(id)}}
            ]}
            filed = {'id': 1, 'is_reservation': 1, 'name': 1, 'company_name': 1, 'company_icon': 1,
                     'company_introduction': 1, 'create_time': 1, 'update_time': 1, '_id': 0}
            result = await dbo.findOne(condition, filed)

            '''如果没有记录则跳过本次循环'''
            if result is None:
                continue
            '''添加一条志愿者信息到志愿者列表'''
            data['volunteers_list'].append(result)

        logger.info(f"data is {data}")
        return {'code': 200, 'data': data}


    # 查看志愿者是否有多余的时间来处理预约会议
    # async def checkVolunteersTime(self, id, company_volunteers_id_list):
    #     print(company_volunteers_id_list)


    # 查看志愿者是否有多余的时间来处理预约会议
    async def checkVolunteersTime(self, company_volunteers_id_list):
        # print(type(id))
        # return id
        # 获取第一次发起请求的所有数据
        # condition = {self.query_field: self.id, 'request_num': 1}
        # field = {'session_id': 1, '_id': 0}
        # result = await dbo.getData(condition, field)

        # 获取第一次发起请求的所有数据
        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'request_num': 1}
        field = {'session_id': 1, '_id': 0}
        result = await dbo.getData(condition, field)
        print(result)

         # 如果没有记录则直接返回空的 list 列表
        if len(result) == 0:
            return []

        # 获取单个 session_id 的所有预约记录的最后一条
        session_id_record = []
        for value in result:
            condition = {'session_id': value['session_id']}
            field = {
                "id": 1,
                "reservation_company_id": 1,
                "reservation_company_name": 1,
                "session_id": 1,
                "start_id": 1,
                "start_user_name": 1,
                "start_head_portrait": 1,
                # "start_working_fixed_year": 1,
                "start_company_name": 1,
                "start_company_icon": 1,
                "end_id": 1,
                "end_user_name": 1,
                "end_head_portrait": 1,
                # "end_working_fixed_year": 1,
                "end_company_name": 1,
                "end_company_icon": 1,
                # "meeting_pass": 1,
                # "national_area_code": 1,
                # "national_area_name": 1,
                # "meeting_time": 1,
                # "meeting_status": 1,
                "volunteer_reply_time": 1,
                "volunteer_reply_time": 1,
                "requester_agree_time": 1,
                "request_num": 1,
                "current_id": 1,
                "is_create_meeting": 1,
                "status": 1,
                "create_time": 1,
                "_id": 0
            }
            sort = [('id', -1)]
            num = 0
            session_id_record.append(await dbo.findSort(condition, field, sort, num))

        # return session_id_record

        meeting_list = []
        booking_list = []
        for value_two in session_id_record:
            value_two = value_two[0]

            '''添加已经预约的议列表'''
            if value_two['is_create_meeting'] == 1:
                meeting_list.append(value_two)

            '''添加正在进行中的预约，并且状态为有效，并且者愿者已经回复了时间可用时间'''
            if value_two['is_create_meeting'] == 0 and value_two['status'] == 1 and value_two['request_num'] == 2:
                booking_list.append(value_two)

        return {'meeting_list':meeting_list, 'booking_list':booking_list}






companyCurd = CompanyCurd()
