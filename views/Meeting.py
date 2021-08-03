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


# Meeting 会议接口类
class Meeting:


    # 第一次预约会议
    async def sendRequest(self, id, volunteers_id, request_type, reservation_company_id, reservation_company_name):
        return await meetingFirstMeetingRequest.construct(id, volunteers_id, request_type, reservation_company_id, reservation_company_name)








meeting = Meeting()
