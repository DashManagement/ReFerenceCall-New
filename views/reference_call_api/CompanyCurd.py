'''
@Description:
@Author: michael
@Date: 2021-07-27 10:10:20
LastEditTime: 2021-09-26 18:19:00
LastEditors: michael
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
            'delete_time': 1,
            'status': 1
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True


    # 删除单个公司
    async def deleteCompany(self, id, uid):

        now_time = common.getTime()

        dbo.resetInitConfig('test', 'reference_call_company')
        condition = {'id': id, 'uid': uid, 'status': 1}
        set_field = {'$set':{'status': 0, 'update_time':now_time, 'delete_time':now_time}}
        update_result = await dbo.updateOne(condition, set_field)
        if update_result.modified_count != 1:
            logger.info('error: delete company failure')
            return {'code': 201, 'message': '删除失败'}

        return {'code': 200}


    # 志愿者已经添加的公司列表接口
    async def companyList(self, uid):

        dbo.resetInitConfig('test', 'reference_call_company')

        condition = {'uid': uid, 'status': 1}
        field = {'id': 1, 'rc_company_id': 1, '_id': 0}
        company_list = await dbo.getData(condition, field)

        if len(company_list) == 0:
            return {'code': 201, 'message': '此用户没有数据'}

        data = {'code':200, 'count':0, 'data':[]}
        tmp_data = []

        for value in company_list:
            dbo.resetInitConfig('test', 'lp_gp')
            condition = {'id': str(value['rc_company_id']), 'company_id': str(
                value['rc_company_id'])}
            field = {'_id': 0}
            result = await dbo.findOne(condition, field)

            # 有不存在的公司时，跳过本次循环
            if result is None:
                continue

            result['insert_id'] = value['id']
            tmp_data.append({
                'insert_id': value['id'],
                'company_id': result['company_id'],
                'company_name': result['fund_name'],
                'company_info': result['company_info'],
                'company_icon': result['company_icon'],
                'create_time': result['reg_time']
            })

        data['count'] = len(tmp_data)
        data['data'] = tmp_data
        return data


    # 按公司查看 reference_call 的志愿者列表
    async def companyVolunteersList(self, id, company_id):

        data = {
            'company_info': {},
            'volunteers_list': []
        }

        # 查询公司信息
        dbo.resetInitConfig('test', 'lp_gp')
        condition = {"id": str(company_id), "company_id": str(
            company_id), "describe": "0"}
        field = {"id": 1, "fund_name": 1, "company_info": 1, '_id': 0}
        company_info = await dbo.findOne(condition, field)

        if company_info is None:
            return {'code': 201, 'message': '公司不存在'}
        else:
            data['company_info'] = company_info

        # 查询志愿者 id 列表
        dbo.resetInitConfig('test', 'reference_call_company')
        condition = {'rc_company_id': company_id, 'status': 1}
        field = {'uid': 1, '_id': 0}

        company_volunteers_id_list = await dbo.getData(condition, field)

        # 查询志愿者详细信息
        data['volunteers_list'] = []
        for value in company_volunteers_id_list:

            dbo.resetInitConfig('test', 'users')
            '''根据 uid 查询公司匹配的志愿者信息（不包括当前用户id 的志愿者，也就是排除志愿者自己）'''
            condition = {'$and': [
                {'id': int(value['uid'])},
                {'id': {'$ne': int(id)}}
            ]}
            field = {'id': 1, 'is_reservation': 1, 'name': 1, 'company_name': 1, 'company_icon': 1,
                     'company_introduction': 1, 'create_time': 1, 'update_time': 1, '_id': 0}
            result = await dbo.findOne(condition, field)

            '''如果没有记录则跳过本次循环'''
            if result is None:
                continue

            '''查询志愿者是否有超过 5 次未完成的会议预约，如果有则代表志愿者不会再被预约会议'''
            if await self.is_reservation(result['id']) is False:
                result['is_reservation'] = 0
            else:
                result['is_reservation'] = 1

            '''添加一条志愿者信息到志愿者列表'''
            data['volunteers_list'].append(result)

        logger.info(f"data is {data}")
        return {'code': 200, 'data': data}


    # 查看志愿者是否有多余的时间来处理预约会议
    async def is_reservation(self, volunteers_id):

        dbo.resetInitConfig('test', 'meeting_list')
        condition = {
            '$or': [
                {'start_id': volunteers_id},
                {'end_id': volunteers_id}
            ],
            'status': 1
        }

        field = {'_id': 0}
        result = await dbo.getData(condition, field)

        new_result = await self.updateMeetingStatus(result)

        if len(new_result) > 5:
            return False

        return True


    # 过滤过期时间并更改数据库过期会议已失效
    async def updateMeetingStatus(self, result_list):

        # 数据为空则返回空
        if len(result_list) == 0:
            return []

        dbo.resetInitConfig('test', 'meeting_list')

        # 获取当前时间戳
        now_time = common.getTime()

        tmp_result_list = []
        # 循环查询会议是否过期 并 将过期会议状态更改为 0
        for value in result_list:

            if int(value['meeting_end_time']) < now_time:
                condition = {'id':value['id']}
                set_field = {'$set':{'status': 0}}
                update_result = await dbo.updateOne(condition, set_field)
                if update_result.modified_count != 1:
                    logger.info('error: update status failure')
            else:
                tmp_result_list.append(value)

        return tmp_result_list


    # 计算志愿者会议时间剩余可预约时间
    async def checkVolunteersTime(self, volunteers_id):

        # 查看志愿者是否存在
        user_info = await base.verifyUserReturnInfo(volunteers_id)
        if user_info is False:
            return {'code': 201, 'message': '用户不存在'}

        time_list = await timeOperation.timeList()
        volunteers_time = await self.volunteersTime(volunteers_id)
        # return time_list
        # return volunteers_time

        # 清除会议中已经被占用的时间
        for value in time_list:

            # 循环预约会议列表
            for meeting_list in volunteers_time['meeting_list']:

                ctmp_del = []
                # 循环一天当中9点到18点的时间戳
                for index, time_stamp in enumerate(value['time_stamp']):
                    # 判断如果预约会议时间和预约时间戳相等，则在一天当中的时间中移除这一个小时的时间
                    if int(meeting_list['requester_agree_time'][0]) == int(time_stamp[0]):
                        # 将需要删除的索引添加到列表中
                        ctmp_del.append(index)

                # return ctmp_del
                # 反转列表 - 不反转列表会删除错误的索引
                nctmp_del = list(reversed(ctmp_del))
                # 删除索引中的值
                for value_index in nctmp_del:
                    del value['time_stamp'][value_index], value['time_clock'][
                        value_index], value['time'][value_index], value['check_time'][value_index]

            # 循环正在进行预约的会议列表
            for booking_list in volunteers_time['booking_list']:

                tmp_del = []
                # 循环一天当中9点到18点的时间戳
                for index,time_stamp in enumerate(value['time_stamp']):
                    # 循环预约的三组时间
                    for reply_list in booking_list['time_stamp']:
                        # 判断如果预约会议时间和预约时间戳相等，则在一天当中的时间中移除这一个小时的时间
                        if int(reply_list[0]) == int(time_stamp[0]):
                            # 将需要删除的索引添加到列表中
                            tmp_del.append(index)

                # return tmp_del
                # 反转列表 - 不反转列表会删除错误的索引
                vtmp_del = list(reversed(tmp_del))
                # 删除索引中的值
                for value_index in vtmp_del:

                    del value['time_stamp'][value_index], value['time_clock'][
                        value_index], value['time'][value_index], value['check_time'][value_index]

        data = {
            'code': 200,
            'data': {
                'user_info': user_info,
                'volunteers': {
                    'count': len(time_list),
                    'volunteers_time_list': time_list
                }
            }
        }

        return data


    # 查看志愿者处理预约会议的时间
    async def volunteersTime(self, volunteers_id):

        # return await timeOperation.timeList()
        # 获取第一次发起请求的所有数据
        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'$or': [{'start_id': volunteers_id},
                             {'end_id': volunteers_id}], 'request_num': 1}
        field = {'session_id': 1, '_id': 0}
        result = await dbo.getData(condition, field)
        # print(result)

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
                "reservation_company_icon": 1,
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
        # 将已经预约的会议 和 正在进行预约当中的会议(并且志愿者已经回复的预约时间)分成两个列表
        meeting_list = []
        booking_list = []
        for value_two in session_id_record:
            value_two = value_two[0]

            '''添加已经预约的议列表'''
            if value_two['is_create_meeting'] == 1:
                meeting_list.append(value_two)

            '''添加正在进行中的预约，并且状态为有效，并且者愿者已经回复了时间可用时间'''
            if value_two['is_create_meeting'] == 0 and value_two['status'] == 1 and value_two['request_num'] == 2:
                
                # 增加一个临时字段 time_stamp, 将志愿者回复的预约时间 格式化为 [['123','123'],['321','321'],['111','111]]
                value_two['time_stamp'] = []
                for tmp_1 in value_two['volunteer_reply_time']:
                    value_1 = list(tmp_1.values())
                    for value_2 in value_1[0]:
                        value_two['time_stamp'].append(value_2)

                booking_list.append(value_two)

        return {'meeting_list': meeting_list, 'booking_list': booking_list}








companyCurd = CompanyCurd()
