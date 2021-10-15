'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-10-08 80:00:00
LastEditors: michael
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
    client_type = ''
    time_zone = ''

    async def construct(self, id='', session_id='', request_type='', time='', client_type='', time_zone=''):

        self.id = int(id)
        self.session_id = int(session_id)
        self.request_type = int(request_type)
        self.time = time
        self.client_type = client_type
        self.time_zone = time_zone

        # 判断是安卓还是 ios 传入的时间戳 - 如果是 ios 传入的时间戳，则需要转换 time 的数据格式为通用格式
        if client_type == 'ios':
            await self.iosDataConversionJson()

        # 按时间戳大小重新排列时间
        self.time = self.sortTime()

        is_perform_step_two = await self.isPerformStepTwo()
        if is_perform_step_two['action'] is False:
            return is_perform_step_two['data']

        # 查询已经预约成功的会议中是否有未结束的会议 - 如果有则返回需要先完成已经预约成功的会议
        if await self.isUnexecutedMeeting() is False:
            return {'code': 202, 'message': '请先完成已经预约的会议'}

        first_request_result = await self.findFirstMeetingRequest()
        if first_request_result is False:
            return {'code': 203, 'message': '没有被请求记录'}

        # 查看是否已经有请求者或志愿者的回复信息
        volunteer_result = await self.checkVolunteerLastRecord()

        # 请求者或志愿者回复预约时间
        if self.request_type == 2:

            # 判断志愿者是否为第一次回复
            if len(volunteer_result) < 1:

                # 如果第一次回复的是第一次预约的发起人，将提示错误
                if first_request_result['start_id'] == self.id:
                    return {'code':301, 'message':'第一次回复的不能是预约发起的用户'}

                logger.info(f"first_request_result is {first_request_result}")
                logger.info(f" 志愿者{first_request_result['end_id']} 同意  用户{first_request_result['start_id']} 的 refCall")            
                await umengPushApi.sendUnicastByUserID(first_request_result['start_id'], first_request_result['end_id'], False)
                return await self.returnBookingTime(first_request_result, 1)

            else:

                '''关于传入 id 错误的判断'''
                if volunteer_result[0]['last_id'] == self.id:

                    if volunteer_result[0]['start_id'] == self.id:
                        return {'code':302, 'message':'请求者已经回复过志愿者预约时间'}

                    if volunteer_result[0]['end_id'] == self.id:
                        return {'code':303, 'message':'志愿者已经回复过请求者预约时间'}

                '''添加多次回复记录'''
                logger.info(f"first_request_result is {first_request_result}")
                logger.info(f" 志愿者{first_request_result['end_id']} 同意  用户{first_request_result['start_id']} 的 refCall")
                await umengPushApi.sendUnicastByUserID(first_request_result['start_id'], first_request_result['end_id'], False)
                return await self.returnBookingTime(first_request_result, volunteer_result[0]['discuss_number']+1 )

        # 请求者或者志愿者拒绝会议邀请
        if self.request_type == 4:

            # 判断是否为未曾回复过的预约
            if len(volunteer_result) < 1:
                return {'code':302, 'message': '错误，没有回复记录！'}

            # 如果拒绝的是最后一条记录是回复者发送，返回错误提示
            if volunteer_result[0]['last_id'] == self.id:
                return {'code':301, 'message':'拒绝的不能是最后一次回复的用户'}

            result = await self.returnRefused(first_request_result)
            if result['code'] == 200:
                # 志愿者已经 同意/拒绝 会议，将本次 session_id 相关的记录 status 都改为 0
                await self.updateSessionId()

            logger.info(f"请求者或志愿者{first_request_result['end_id']} 拒绝  用户{first_request_result['start_id']} 的 refCall")
            await umengPushApi.sendUnicastByUserID(first_request_result['start_id'], first_request_result['end_id'], False)

            return result


    # 查看是否已经有请求者或志愿者的回复信息
    async def checkVolunteerLastRecord(self):

        dbo.resetInitConfig('test','reservation_meeting')
        condition = {'session_id':self.session_id, 'request_type':2, 'request_num':2}
        field = {'_id':0}
        sort = [('create_time', -1)]
        skip = 0
        num = 1
        return await dbo.findSort(condition, field, sort, skip, num)


    # 按时间戳大小重新排列时间
    def sortTime(self):

        # return self.time

        time_key = []
        # 获取当日零时时间戳的 list 列表
        for value in self.time:
            for value_2 in value:
                time_key.append(value_2)
        # return time_key

        # 排序列表
        for j in range(len(time_key)-1,0,-1):
            for i in range(j):
                if time_key[i] > time_key[i+1]:
                    time_key[i], time_key[i+1] = time_key[i+1], time_key[i]
        # return time_key

        tmp_list = {}
        # 建立新的数据结构字典，以方便后面取wefhg
        for value_2 in self.time:
            for value_3 in value_2:
                # return value_2[value_3]
                tmp_list[str(value_3)] = value_2[value_3]
        # return tmp_list

        return_list = []
        # 按从小到大的时间顺序重新排列时间戳结构 - 生成字典
        for value in time_key:
            tmp_time_list = {}
            tmp_time_list[value] = tmp_list[value]
            return_list.append(tmp_time_list)

        return return_list


    # 志愿者回复 - 预约时间
    async def returnBookingTime(self, first_request_result, discuss_number):
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
            'reservation_company_icon': first_request_result['reservation_company_icon'],
            'session_id': self.session_id,
            'start_id': first_request_result['start_id'],
            'start_user_name': first_request_result['start_user_name'],
            'start_head_portrait': first_request_result['start_head_portrait'],
            'start_working_fixed_year': first_request_result['start_working_fixed_year'],
            'start_company_name': first_request_result['start_company_name'],
            'start_company_icon': first_request_result['start_company_icon'],
            'end_id': first_request_result['end_id'],
            'end_user_name': first_request_result['end_user_name'],
            'end_head_portrait': first_request_result['end_head_portrait'],
            'end_working_fixed_year': first_request_result['end_working_fixed_year'],
            'end_company_name': first_request_result['end_company_name'],
            'end_company_icon': first_request_result['end_company_icon'],
            'current_id': self.id,
            'current_content': "-",
            'request_type': self.request_type,
            'volunteer_reply_time': self.time,
            'requester_agree_time': [],
            'national_area_code': "-",
            'national_area_name': "-",
            'request_num': 2,
            'discuss_number': discuss_number,
            'last_id':self.id,
            'is_create_meeting': 0,
            'status': 1,
            'time_zone': self.time_zone,
            "create_time": common.getTime(),
            # 此处需要一个预约过期时间，后面补上。也有可能不需要
            "update_time": common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return {'code': 204, 'message': '志愿者回复请求失败'}

        return {'code': 200}


    # 请求者和志愿者多次修改回复预约时间 - 暂时未用
    # async def returnUpdateBookingTime(self):

    #     dbo.resetInitConfig('test', 'reservation_meeting')

    #     condition = {'session_id':self.session_id, 'request_type':self.request_type, 'request_num':2}
    #     set_fields = {'$set':{'last_id':self.id, 'update_time':common.getTime()}, '$inc':{'discuss_number':1}}

    #     update_result = await dbo.updateOne(condition, set_fields)

    #     if update_result.modified_count != 1:
    #         logger.info('error: update volunteer_reply_request failure')
    #         return {'code': 205, 'message': '多次回复请求失败'}

    #     return {'code': 200}


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
            'reservation_company_icon': first_request_result['reservation_company_icon'],
            'session_id': self.session_id,
            'start_id': first_request_result['start_id'],
            'start_user_name': first_request_result['start_user_name'],
            'start_head_portrait': first_request_result['start_head_portrait'],
            'start_working_fixed_year': first_request_result['start_working_fixed_year'],
            'start_company_name': first_request_result['start_company_name'],
            'start_company_icon': first_request_result['start_company_icon'],
            'end_id': first_request_result['end_id'],
            'end_user_name': first_request_result['end_user_name'],
            'end_head_portrait': first_request_result['end_head_portrait'],
            'end_working_fixed_year': first_request_result['end_working_fixed_year'],
            'end_company_name': first_request_result['end_company_name'],
            'end_company_icon': first_request_result['end_company_icon'],
            'current_id': self.id,
            'current_content': "-",
            'request_type': self.request_type,
            'volunteer_reply_time': [],
            'requester_agree_time': [],
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
            return {'code': 206, 'message': '志愿者拒绝请求失败'}

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
                data['data'] = {'code': 207,
                                'message': '已经成功创建会议，不能再次回复请求者预约时间'}
                return data

            if result[0]['is_create_meeting'] == 2:
                data['data'] = {'code': 208, 'message': '预约会议已经被拒绝，志愿者不能再次操作'}
                return data

        # 查看是否有志愿者回复记录
        # condition = {'end_id': self.id, 'session_id': self.session_id,
        #              'request_num': 2, 'is_create_meeting': 0}
        # field = {'_id': 0}
        # result = await dbo.findOne(condition, field)

        # if result is not None:
        #     data['action'] = False
        #     data['data'] = {'code': 202, 'message': '请先执行未完成的预约会议记录流程'}
        #     return data

        data['action'] = True
        return data


    # 查询 请求者第一次发送请求时的预议会议记录
    async def findFirstMeetingRequest(self):

        dbo.resetInitConfig('test', 'reservation_meeting')
        condition = {'$or':[
            {'start_id': self.id, 'session_id': self.session_id,'request_num': 1, 'is_create_meeting': 0, 'status': 1},
            {'end_id': self.id, 'session_id': self.session_id,'request_num': 1, 'is_create_meeting': 0, 'status': 1}
        ]}
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


    # 转换 ios 传入的时间戳结构
    async def iosDataConversionJson(self):

        time_list = []
        # str 转 json 格式转化
        for value in self.time:

            tmp_list = []
            for value_2 in value['timeList']:
                tmp_list.append(value_2)

            time_list.append({value['zero_stamp']:tmp_list})

        self.time = time_list










meetingVolunteerReplyRequest = MeetingVolunteerReplyRequest()
