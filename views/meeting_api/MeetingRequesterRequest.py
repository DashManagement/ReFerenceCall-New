'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-08 20:19:34
LastEditors: fanshaoqiang

'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from views.ThirdParty.UMengPushAPI import umengPushApi
from views.ThirdParty.ZoomAPI import *
import time
from config.log_config import logger

# meeting 预约会议 - 请求者回复请求


class MeetingRequesterRequest:

    '''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-02 20:00:00
LastEditors: michael
'''

# coding=utf-8


# 加载自己创建的包

# meeting 预约会议 - 志愿者回复请求

class MeetingRequesterRequest:

    id = ''
    session_id = ''
    request_type = ''
    time_info = ''
    time = ''

    async def construct(self, id='', session_id='', request_type='', time_info='', selectTime=''):

        self.id = int(id)
        self.session_id = int(session_id)
        self.request_type = int(request_type)
        self.time_info = time_info
        logger.info(f"MeetingRequesterRequest time is {selectTime}")

        if await self.isUnexecutedMeeting() is False:
            return {'code': 202, 'message': '请先完成已经预约的会议'}

        is_perform_step_two = await self.isPerformStepTwo()
        if is_perform_step_two['action'] is False:
            return is_perform_step_two['data']

        two_request_result = await self.volunteersRequestTwo()
        # logger
        if two_request_result is False:
            return {'code': 203, 'message': '没有志愿者回复记录'}

        if self.request_type == 3:
            self.time = selectTime
            
            # 添加请求者同意记录
            if await self.acceptBookingTime(two_request_result) is False:
                return {'code': 204, 'message': '请求者接受志愿者预约时间失败'}

            # 在会议列表中添加一条待处理的会议记录
            if await self.addMeetingRecord(two_request_result, selectTime) is False:
                return {'code': 205, 'message': '在会议列表中添加会议记录失败'}

            # 请求者已经 同意/拒绝 会议，将本次 session_id 相关的记录 status 都改为 0
            await self.updateSessionId()
            logger.info(
                f" 用户{self.id} 同意 志愿者{two_request_result['end_id']} 给的时间里面的一个")
            await umengPushApi.sendUnicastByUserID(
                self.id, two_request_result['end_id'], True)
            return {'code': 200}

        if self.request_type == 5:

            # 添加请求者拒绝记录
            result = await self.returnRefused(two_request_result)
            if result['code'] == 200:
                # 请求者已经 同意/拒绝 会议，将本次 session_id 相关的记录 status 都改为 0
                await self.updateSessionId()
            logger.info(
                f"  用户{self.id} 拒绝  志愿者{two_request_result['end_id']} 的时间")
            await umengPushApi.sendUnicastByUserID(
                self.id, two_request_result['end_id'], True)
            return result

    # 请求者回复 - 接受志愿者预约时间

    async def acceptBookingTime(self, two_request_result):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reservation_meeting', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return {'code': 209, 'message': '获取 id 自增失败'}
        logger.info(two_request_result['volunteer_reply_time'])
        dbo.resetInitConfig('test', 'reservation_meeting')
        document = {
            'id': get_id_result['update_id'],
            'reservation_company_id': two_request_result['reservation_company_id'],
            'reservation_company_name': two_request_result['reservation_company_name'],
            'session_id': self.session_id,
            'start_id': self.id,
            'start_user_name': two_request_result['start_user_name'],
            'start_head_portrait': two_request_result['start_head_portrait'],
            'start_working_fixed_year': two_request_result['start_working_fixed_year'],
            'start_company_name': two_request_result['start_company_name'],
            'start_company_icon': two_request_result['start_company_icon'],
            'end_id': two_request_result['end_id'],
            'end_user_name': two_request_result['end_user_name'],
            'end_head_portrait': two_request_result['end_head_portrait'],
            'end_working_fixed_year': two_request_result['end_working_fixed_year'],
            'end_company_name': two_request_result['end_company_name'],
            'end_company_icon': two_request_result['end_company_icon'],
            'current_id': self.id,
            'current_content': "-",
            'request_type': self.request_type,
            'volunteer_reply_time': [],
            'agree_time_info': self.time_info,
            'requester_agree_time': self.time,
            'national_area_code': "-",
            'national_area_name': "-",
            'request_num': 3,
            'is_create_meeting': 1,
            'status': 0,
            "create_time": common.getTime(),
            # 此处需要一个预约过期时间，后面补上。也有可能不需要
            "update_time": common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True

    # 请求者回复 - 拒绝

    async def returnRefused(self, two_request_result):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reservation_meeting', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return {'code': 209, 'message': '获取 id 自增失败'}

        dbo.resetInitConfig('test', 'reservation_meeting')
        document = {
            'id': get_id_result['update_id'],
            'reservation_company_id': two_request_result['reservation_company_id'],
            'reservation_company_name': two_request_result['reservation_company_name'],
            'session_id': self.session_id,
            'start_id': self.id,
            'start_user_name': two_request_result['start_user_name'],
            'start_head_portrait': two_request_result['start_head_portrait'],
            'start_working_fixed_year': two_request_result['start_working_fixed_year'],
            'start_company_name': two_request_result['start_company_name'],
            'start_company_icon': two_request_result['start_company_icon'],
            'end_id': two_request_result['end_id'],
            'end_user_name': two_request_result['end_user_name'],
            'end_head_portrait': two_request_result['end_head_portrait'],
            'end_working_fixed_year': two_request_result['end_working_fixed_year'],
            'end_company_name': two_request_result['end_company_name'],
            'end_company_icon': two_request_result['end_company_icon'],
            'current_id': self.id,
            'current_content': "-",
            'request_type': self.request_type,
            'volunteer_reply_time': [],
            'requester_agree_time': [],
            'national_area_code': "-",
            'national_area_name': "-",
            'request_num': 3,
            'is_create_meeting': 2,
            'status': 0,
            "create_time": common.getTime(),
            # 此处需要一个预约过期时间，后面补上。也有可能不需要
            "update_time": common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return {'code': 206, 'message': '请求者拒绝请求失败'}
        return {'code': 200}

    # 查询 预约会议过程中的 - 会话id记录 session_id 和志愿者id 是否存在，并且已经执行到第三步 - 请求者同意或者拒绝

    async def isPerformStepTwo(self):

        data = {'action': '', 'data': ''}

        dbo.resetInitConfig('test', 'reservation_meeting')

        # 查看是否已经成功创建会议 或者 拒绝了创建会议
        condition = {'session_id': self.session_id, 'status': 1}
        field = {'_id': 0}
        sort = [('id', -1)]
        num = 0
        result = await dbo.findSort(condition, field, sort, num)

        if len(result) == 1:

            data['action'] = False
            if result[0]['is_create_meeting'] == 1:
                data['data'] = {'code': 207,
                                'message': '已经成功创建会议，不能再次回复请求者预约时间'}
                return data

            if result[0]['is_create_meeting'] == 2:
                data['data'] = {'code': 208, 'message': '预约会议已经被拒绝，请求者不能再次操作'}
                return data

        # 查看是否有请求者回复记录
        condition = {'start_id': self.id, 'session_id': self.session_id,
                     'request_num': 3, 'is_create_meeting': 0, 'status': 1}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        if result is not None:
            data['action'] = False
            data['data'] = {'code': 301, 'message': '请先执行未完成的预约会议记录流程'}
            return data

        data['action'] = True
        return data

    # 查询 志愿者是否有回复预约会议时间的记录

    async def volunteersRequestTwo(self):

        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'start_id': self.id, 'session_id': self.session_id,
                     'request_num': 2, 'is_create_meeting': 0, 'status': 1}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)
        logger.info(f"condition is {condition}")

        if result is None:
            return False

        return result

    # 查询已经预约成功的会议中是否有未结束的会议 - 如果有则返回需要先完成已经预约成功的会议

    async def isUnexecutedMeeting(self):

        # await dbo.insert(document)
        dbo.resetInitConfig('test', 'meeting_list')
        condition = {'start_id': self.id,
                     'session_id': self.session_id, 'status': 1}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        if result is not None:
            return False

        return True

    # 在会议列表中 - 添加一条会议记录

    async def addMeetingRecord(self, two_request_result, selectTime):

        logger.info(f"in add MeetingRecord the selectTime is {selectTime}")
        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('meeting_list', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return {'code': 209, 'message': '获取 id 自增失败'}
        meetingModel = await self.getMeetingModelFromTwoResult(two_request_result, selectTime)
        meetingInfo = zoomapi.createMeeting(meetingModel)
        if meetingInfo == None:
            logger.info('Zoom创建会议失败')
            return {'code': 210, 'message': 'Zoom创建会议失败'}
        logger.info(f"zoom 创建成功 {meetingInfo.get('Meeting_ID')}")
        dbo.resetInitConfig('test', 'meeting_list')
        logger.info(f"meetingInfo is {meetingInfo.get('Meeting_Pwd')}")
        document = {

            'id': get_id_result['update_id'],
            'reservation_company_id': two_request_result['reservation_company_id'],
            'reservation_company_name': two_request_result['reservation_company_name'],
            'session_id': self.session_id,
            'start_id': self.id,
            'start_user_name': two_request_result['start_user_name'],
            'start_head_portrait': two_request_result['start_head_portrait'],
            'start_working_fixed_year': two_request_result['start_working_fixed_year'],
            'start_company_name': two_request_result['start_company_name'],
            'start_company_icon': two_request_result['start_company_icon'],
            'end_id': two_request_result['end_id'],
            'end_user_name': two_request_result['end_user_name'],
            'end_head_portrait': two_request_result['end_head_portrait'],
            'end_working_fixed_year': two_request_result['end_working_fixed_year'],
            'end_company_name': two_request_result['end_company_name'],
            'end_company_icon': two_request_result['end_company_icon'],
            'meeting_pass': meetingInfo.get('Meeting_Pwd'),
            'meeting_address': meetingInfo.get('Join_URL'),
            'meeting_id': meetingInfo.get('Meeting_ID'),
            'national_area_code': "-",
            'national_area_name': "-",
            'meeting_time': self.time,
            'meeting_status': 0,
            'agree_time_info':self.time_info,
            'start_time': str(selectTime[0]),
            'meeting_end_time': str(selectTime[1]),
            'cancel_time': 0,
            'overdue_time': 0,
            'status': 1,
            'create_time': common.getTime(),
            'update_time': common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False
            logger.info(
                f"  会议创建成功 给用户{self.id} 和 志愿者{two_request_result['end_id']} 发push")
        await umengPushApi.sendUnicastByUserID(
            two_request_result['end_id'], self.id, False)
        await umengPushApi.sendUnicastByUserID(
            self.id, two_request_result['end_id'], False)
        return True

    # 请求者已经 同意/拒绝 会议，将本次 session_id 相关的记录 status 都改为 0

    async def updateSessionId(self):

        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'session_id': self.session_id}
        set_fields = {'$set': {'status': 0}}
        result = await dbo.updateAll(condition, set_fields)
        '''此条记录记入日志 - 不作其它处理'''
        logger.info('update all meeting status = 0')

    async def getMeetingModelFromTwoResult(self, two_request_result, selectTime):

        fundName = two_request_result['reservation_company_name']
        sendUserInfo = await base.getUserPushInfo(
            self.id)
        toUserInfo = await base.getUserPushInfo(
            two_request_result['end_id'])
        fromUserName = sendUserInfo.get("userName")
        fromEmail = sendUserInfo.get("userEmail")
        toUserName = toUserInfo.get("userName")
        toEmail = toUserInfo.get("userEmail")
        meetingZone = sendUserInfo.get("localTimeZone")

        startTime = int(selectTime[0][0:10])
        endTime = int(selectTime[1][0:10])
        duration = int((endTime-startTime)/60)
        startTime = datetime.fromtimestamp(
            startTime).strftime("%Y-%m-%dT%H:%M:%S")
        endTime = datetime.fromtimestamp(
            endTime).strftime("%Y-%m-%dT%H:%M:%S")
        logger.info(f"startTime is {startTime}, endTime is {endTime}")
        meetingTime = startTime

        meetingModel = MeetingModel(
            fundName=fundName, fromUserName=fromUserName, toEmail=toEmail, toUserName=toUserName,
            fromEmail=fromEmail, meetingZone=meetingZone, meetingTime=meetingTime, duration=duration)
        return meetingModel






meetingRequesterRequest = MeetingRequesterRequest()
