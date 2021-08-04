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

# Meeting 会议接口类
class Meeting:


    # 第一次预约会议
    async def sendRequest(self, id, volunteers_id, request_type, reservation_company_id, reservation_company_name):
        return await meetingFirstMeetingRequest.construct(id, volunteers_id, request_type, reservation_company_id, reservation_company_name)


    # 志愿者回复预约时间或者拒绝
    async def volunteerReplyRequest(self, id, session_id, request_type, volunteer_reply_time):
        return await meetingVolunteerReplyRequest.construct(id, session_id, request_type, volunteer_reply_time)


    # 请求者同意预约时间或者拒绝
    async def requesterRequest(self, id, session_id, request_type, requester_agree_time):
        return await meetingRequesterRequest.construct(id, session_id, request_type, requester_agree_time)





meeting = Meeting()
