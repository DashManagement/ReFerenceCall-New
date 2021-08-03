'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-02 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from pydantic.tools import T
from views.Base import *
from config.log_config import logger

# meeting 会议操作类
class MeetingOperation:


    # 第一次预约会议
    async def firstMeetingRequest(self, id, volunteers_id, request_type, reservation_company_id, reservation_company_name):
        
        dbo.resetInitConfig('test','reservation_meeting')

        # 查找是否已经有未完成的预约会议
        condition = {'start_id': id, 'end_id': volunteers_id, 'is_create_meeting':0}
        field = {'_id':0}
        is_meeting_result = await dbo.findOne(condition, field)
        print(is_meeting_result)
        if is_meeting_result is None:
            '''如果没有未完成预约会议，则添加一条预约信息'''

            # 查询请求者和志愿者是否存在
            if await self.is_users(id, volunteers_id) is False:
                return {'code':201, 'message': '用户不存在'}

            # 查询预约沟通的公司是否存在
            if await self.is_company(reservation_company_id) is False:
                return {'code':202, 'message': '被预约的公司不存在'}

            # 添加一条预约信息
            insert_result = await self.insertFirstMeetingRequest(id, volunteers_id, request_type, reservation_company_id, reservation_company_name)
            if insert_result is False:
                return {'code':203, 'message': '预约记录添加失败'}

            return {'code':200, 'message': '预约成功'}

        else:
            # 如果有未完成的预约会议，返回相应提示信息
            return {'code': 201, 'message': '请结束上一次预约会议'}


        # 给志愿者推送信息
        # push 信息


    # 查询请求者和志愿者是否存在
    async def is_users(self, id, volunteers_id):

        dbo.resetInitConfig('test','users')
        condition = {'$or':[{'id':int(id)}, {'id':int(volunteers_id)}]}
        field = {'id':1, '_id':0}
        result = await dbo.getData(condition, field)

        if int(len(result)) == 2:
            return True

        return False


    # 查询预约沟通的公司是否存在
    async def is_company(self, company_id):

        dbo.resetInitConfig('test','lp_gp')
        condition = {'company_id': company_id}
        field = {'id':1, '_id':0}
        result = await dbo.findOne(condition, field)

        if result is None:
            return False

        return True


    # 添加第一次预约会议的请求记录
    async def insertFirstMeetingRequest(self, id, volunteers_id, request_type, reservation_company_id, reservation_company_name):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('reservation_meeting', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        # 获取 session_id 自增 ID
        get_session_id_result = await dbo.getNextIdtoUpdate('session_id', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        dbo.resetInitConfig('test','reservation_meeting')

        document = {
            'id': get_id_result['update_id'],
            'reservation_company_id': reservation_company_id,
            'reservation_company_name': reservation_company_name,
            'start_id': id,
            'end_id': volunteers_id,
            'session_id': get_session_id_result['update_id'],
            'current_id': id,
            'current_content': "-",
            'request_type': request_type,
            'volunteer_reply_time': "-",
            'requester_agree_time': "-",
            'national_area_code': "-",
            'national_area_name': "-",
            'is_create_meeting': 0,
            "create_time": common.getTime(),
            "update_time" : common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True











meetingOperation = MeetingOperation()