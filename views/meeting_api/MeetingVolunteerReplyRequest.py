'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20

LastEditTime: 2021-08-05 19:37:13
LastEditors: fanshaoqiang
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from views.ThirdParty.UMengPushAPI import umengPushApi
from config.log_config import logger

# meeting 预约会议 - 志愿者回复请求


class MeetingVolunteerReplyRequest:

    id = ''
    session_id = ''
    request_type = ''
    time = ''

    async def construct(self, id='', session_id='', request_type='', time=''):

        self.id = int(id)
        self.session_id = int(session_id)
        self.request_type = int(request_type)
        self.time = time

        is_perform_step_two = await self.isPerformStepTwo()
        if is_perform_step_two['action'] is False:
            return is_perform_step_two['data']

        if await self.isUnexecutedMeeting() is False:
            return {'code': 202, 'message': '请先完成已经预约的会议'}

        first_request_result = await self.findFirstMeetingRequest()
        if first_request_result is False:
            return {'code': 202, 'message': '没有被请求记录'}

        if self.request_type == 2:
            logger.info(f"first_request_result is {first_request_result}")
            logger.info(
                f" 志愿者{first_request_result['end_id']} 同意  用户{first_request_result['start_id']} 的 refCall")
            await umengPushApi.sendUnicastByUserID(
                first_request_result['start_id'], first_request_result['end_id'], False)
            return await self.returnBookingTime(first_request_result)

        if self.request_type == 4:

            result = await self.returnRefused(first_request_result)
            if result['code'] == 200:
                # 志愿者已经 同意/拒绝 会议，将本次 session_id 相关的记录 status 都改为 0
                await self.updateSessionId()
            logger.info(
                f" 志愿者{first_request_result['end_id']} 拒绝  用户{first_request_result['start_id']} 的 refCall")
            await umengPushApi.sendUnicastByUserID(
                first_request_result['start_id'], first_request_result['end_id'], False)
            return result

    # 志愿者回复 - 预约时间

    async def returnBookingTime(self, first_request_result):
        print(first_request_result)
        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reservation_meeting', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return {'code': 209, 'message': '获取 id 自增失败'}

        dbo.resetInitConfig('test', 'reservation_meeting')
        document = {
            'id': get_id_result['update_id'],
            'reservation_company_id': first_request_result['reservation_company_id'],
            'reservation_company_name': first_request_result['reservation_company_name'],
            'session_id': self.session_id,
            'start_id': first_request_result['start_id'],
            'start_user_name': first_request_result['start_user_name'],
            'start_head_portrait': first_request_result['start_head_portrait'],
            'start_working_fixed_year': first_request_result['start_working_fixed_year'],
            'start_company_name': first_request_result['start_company_name'],
            'start_company_icon': first_request_result['start_company_icon'],
            'end_id': self.id,
            'end_user_name': first_request_result['end_user_name'],
            'end_head_portrait': first_request_result['end_head_portrait'],
            'end_working_fixed_year': first_request_result['end_working_fixed_year'],
            'end_company_name': first_request_result['end_company_name'],
            'end_company_icon': first_request_result['end_company_icon'],
            'current_id': self.id,
            'current_content': "-",
            'request_type': self.request_type,
            'volunteer_reply_time': self.time,
            'requester_agree_time': "-",
            'national_area_code': "-",
            'national_area_name': "-",
            'request_num': 2,
            'is_create_meeting': 0,
            'status': 1,
            "create_time": common.getTime(),
            # 此处需要一个预约过期时间，后面补上。也有可能不需要
            "update_time": common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return {'code': 202, 'message': '志愿者回复请求失败'}

        return {'code': 200}

    # 志愿者回复 - 拒绝

    async def returnRefused(self, first_request_result):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reservation_meeting', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return {'code': 209, 'message': '获取 id 自增失败'}

        dbo.resetInitConfig('test', 'reservation_meeting')
        document = {
            'id': get_id_result['update_id'],
            'reservation_company_id': first_request_result['reservation_company_id'],
            'reservation_company_name': first_request_result['reservation_company_name'],
            'start_id': first_request_result['start_id'],
            'end_id': self.id,
            'session_id': self.session_id,
            'current_id': self.id,
            'current_content': "-",
            'request_type': self.request_type,
            'volunteer_reply_time': "-",
            'requester_agree_time': "-",
            'national_area_code': "-",
            'national_area_name': "-",
            'request_num': 2,
            'is_create_meeting': 2,
            'status': 1,
            "create_time": common.getTime(),
            # 此处需要一个预约过期时间，后面补上。也有可能不需要
            "update_time": common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return {'code': 203, 'message': '志愿者拒绝请求失败'}

        return {'code': 200}

    # 查询 预约会议过程中的 - 会话id记录 session_id 和志愿者id 是否存在，并且已经执行到第二步 - 等待志愿者回复

    async def isPerformStepTwo(self):

        data = {'action': '', 'data': ''}

        dbo.resetInitConfig('test', 'reservation_meeting')

        # 查看是否已经成功创建会议 或者 拒绝了创建会议
        condition = {'session_id': self.session_id}
        field = {'_id': 0}
        sort = [('id', -1)]
        num = 0
        length = 1
        result = await dbo.findSort(condition, field, sort, num, length)

        if len(result) == 1:

            data['action'] = False
            if result[0]['is_create_meeting'] == 1:
                data['data'] = {'code': 201,
                                'message': '已经成功创建会议，不能再次回复请求者预约时间'}
                return data

            if result[0]['is_create_meeting'] == 2:
                data['data'] = {'code': 204, 'message': '预约会议已经被拒绝，志愿者不能再次操作'}
                return data

        # 查看是否有志愿者回复记录
        condition = {'end_id': self.id, 'session_id': self.session_id,
                     'request_num': 2, 'is_create_meeting': 0}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        if result is not None:
            data['action'] = False
            data['data'] = {'code': 202, 'message': '请先执行未完成的预约会议记录流程'}
            return data

        data['action'] = True
        return data

    # 查询 请求者第一次发送请求时的预议会议记录

    async def findFirstMeetingRequest(self):

        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'end_id': self.id, 'session_id': self.session_id,
                     'request_num': 1, 'is_create_meeting': 0, 'status': 1}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        if result is None:
            return False

        return result

    # 查询已经预约成功的会议中是否有未结束的会议 - 如果有则返回需要先完成已经预约成功的会议

    async def isUnexecutedMeeting(self):

        dbo.resetInitConfig('test', 'meeting_list')
        condition = {'end_id': self.id,
                     'session_id': self.session_id, 'status': 1}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        if result is not None:
            return False

        return True

    # 志愿者已经 同意/拒绝 会议，将本次 session_id 相关的记录 status 都改为 0

    async def updateSessionId(self):

        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'session_id': self.session_id}
        set_fields = {'$set': {'status': 0}}
        result = await dbo.updateAll(condition, set_fields)
        '''此条记录记入日志 - 不作其它处理'''
        logger.info('update all meeting status = 0')


meetingVolunteerReplyRequest = MeetingVolunteerReplyRequest()
