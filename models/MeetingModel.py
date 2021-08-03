'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-02 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel


# 预约会议 - 预约者第一次发送请求的验证模型
class SendRequestModel(BaseModel):
    id: str
    volunteers_id: str
    request_type: str
    reservation_company_id: str
    reservation_company_name: str


# 预约会议 - 志愿者回复请求的验证模型
class VolunteerReplyRequestModel(BaseModel):
    id: str
    session_id: str
    request_type: str
    volunteer_reply_time: int = 0


# 预约会议 - 请求者回复请求的验证模型
class RequesterRequestModel(BaseModel):
    id: str
    session_id: str
    request_type: str
    requester_agree_time: int = 0


