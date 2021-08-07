'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-02 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.meeting_api.MeetingFirstMeetingRequest import meetingFirstMeetingRequest
from views.meeting_api.MeetingVolunteerReplyRequest import meetingVolunteerReplyRequest
from views.meeting_api.MeetingRequesterRequest import meetingRequesterRequest
from views.meeting_api.MeetingList import meetingList
from views.meeting_api.BookingMeetingList import bookingMeetingList

# Meeting 会议接口类
class Meeting:


    # 第一次预约会议
    async def sendRequest(self, id, volunteers_id, request_type, reservation_company_id, reservation_company_name):

        if len(volunteers_id) < 1:
            return {'code':207, 'message':'预约会议列表不合法'}

        data = []
        for value in volunteers_id:
            result = await meetingFirstMeetingRequest.construct(id, value, request_type, reservation_company_id, reservation_company_name)
            result['send_request_info'] = {'id':id, 'volunteers_id':value}
            data.append(result)

        return {'coce':200, 'data':data}


    # 志愿者回复预约时间或者拒绝
    async def volunteerReplyRequest(self, id, session_id, request_type, volunteer_reply_time):
        return await meetingVolunteerReplyRequest.construct(id, session_id, request_type, volunteer_reply_time)


    # 请求者同意预约时间或者拒绝
    async def requesterRequest(self, id, session_id, request_type, requester_agree_time):
        return await meetingRequesterRequest.construct(id, session_id, request_type, requester_agree_time)


    # 查看预约会议请求
    async def checkRequest(self, id, request_type, data_num):
        return await bookingMeetingList.construct(id, request_type, data_num)


    # 获取会议列表相关操作
    async def getMeetingList(self, id, request_type, check_type, data_num):
        return await meetingList.construct(id, request_type, check_type, data_num)




meeting = Meeting()
