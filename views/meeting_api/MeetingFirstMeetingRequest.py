'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-02 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger

# meeting 第一次预约会议
class MeetingFirstMeetingRequest:


    # 第一次预约会议
    async def construct(self, id, volunteers_id, request_type, reservation_company_id, reservation_company_name):

        dbo.resetInitConfig('test','reservation_meeting')

        # 查找是否已经有未完成的预约会议
        condition = {'start_id': id, 'end_id': volunteers_id, 'is_create_meeting':0}
        field = {'_id':0}
        is_meeting_result = await dbo.findOne(condition, field)

        if is_meeting_result is None:
            '''如果没有未完成预约会议，则添加一条预约信息'''

            # 查询请求者和志愿者是否存在
            if await self.is_users(id, volunteers_id) is False:
                return {'code':201, 'message': '用户不存在'}

            # 查询预约沟通的公司是否存在
            # if await self.is_company(reservation_company_id) is False:
            #     return {'code':202, 'message': '被预约的公司不存在'}

            # 查询预约沟通的公司是否有此志愿者
            if await self.is_company_and_volunteer(volunteers_id, reservation_company_id) is False:
                return {'code':203, 'message': '被预约的公司不存在'}

            # 添加一条预约信息
            insert_result = await self.insertFirstMeetingRequest(id, volunteers_id, request_type, reservation_company_id, reservation_company_name)
            if insert_result is False:
                return {'code':204, 'message': '预约记录添加失败'}

            return {'code':200, 'message': '预约成功'}

        else:
            # 如果有未完成的预约会议，返回相应提示信息
            return {'code': 205, 'message': '请结束上一次预约会议'}


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
    # async def is_company(self, company_id):

    #     dbo.resetInitConfig('test','lp_gp')
    #     condition = {'company_id': company_id}
    #     field = {'id':1, '_id':0}
    #     result = await dbo.findOne(condition, field)

    #     if result is None:
    #         return False

    #     return True


    # 查询预约沟通的公司是否有此志愿者
    async def is_company_and_volunteer(self, volunteers_id, reservation_company_id):
        print(volunteers_id, reservation_company_id)
        dbo.resetInitConfig('test','reference_call_company')
        condition = {'uid':int(volunteers_id), 'rc_company_id': int(reservation_company_id)}
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
            'reservation_company_id': int(reservation_company_id),
            'reservation_company_name': reservation_company_name,
            'start_id': int(id),
            'end_id': int(volunteers_id),
            'session_id': get_session_id_result['update_id'],
            'current_id': int(id),
            'current_content': "-",
            'request_type': int(request_type),
            'volunteer_reply_time': "-",
            'requester_agree_time': "-",
            'national_area_code': "-",
            'national_area_name': "-",
            'request_num': 1,
            'is_create_meeting': 0,
            "create_time": common.getTime(),
            #此处需要一个预约过期时间，后面补上。也有可能不需要
            "update_time" : common.getTime()
        }

        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True











meetingFirstMeetingRequest = MeetingFirstMeetingRequest()