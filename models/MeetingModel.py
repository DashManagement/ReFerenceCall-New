'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-14 22:00:26
LastEditors: fanshaoqiang
'''

# coding=utf-8

from pydantic import BaseModel
from typing import List


# 预约会议 - 预约者第一次发送请求的验证模型
class SendRequestModel(BaseModel):
    id: str
    volunteers_id: list
    request_type: str
    reservation_company_id: str
    reservation_company_name: str


# 预约会议 - 志愿者回复请求的验证模型
class VolunteerReplyRequestModel(BaseModel):
    id: str
    session_id: str
    request_type: str
    time: list = []
    client_type: str = 'android'


# 预约会议 - 请求者回复请求的验证模型
class RequesterRequestModel(BaseModel):
    id: str
    session_id: str
    request_type: str
    time_info: dict = {}
    meeting_time: list = [0, 0]

# 正在进行中的预约列表相关操作验证模型


class CheckRequestModel(BaseModel):
    id: str
    request_type: str
    data_num: str


# 会议列表相关操作验证模型
class MeetingListModel(BaseModel):
    id: str
    request_type: str
    check_type: str
    data_num: str


# 已约定的会议日程验证模型
class BookingMeetingModel(BaseModel):
    id: str


# 已约定的会议日程验证模型
class LastCallModel(BaseModel):
    id: str


# 已约定的会议日程验证模型
class HistoryMeetingScheduleModel(BaseModel):
    id: str


# 按时间戳查看当天的会议日程验证模型
class CheckMeetingScheduleModel(BaseModel):
    id: str
    time_stamp: str
