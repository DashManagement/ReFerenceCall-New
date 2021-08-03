'''
@Description:
@Author: michael
@Date: 2020-08-02 10:48:20
LastEditTime: 2020-08-02 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.Meeting import meeting
from models.MeetingModel import SendRequestModel
from models.MeetingModel import VolunteerReplyRequestModel
from models.MeetingModel import RequesterRequestModel

# 创建 APIRouter 实例
router = APIRouter()


# 预约会议 - 预约者第一次发送请求
@router.post('/api/meeting/send_request')
async def sendRequest(send_request: SendRequestModel):
    ''' 
    id	是	string	请求者 id
    volunteers_id	是	list	志愿者 id
    request_type	是	string	请求类型：1 请求者发送预约请求
    reservation_company_id	是	string	预约沟通的公司id
    reservation_company_name	是	string	预约沟通的公司名称
    非测试数据：
    {
        "id": 1,
        "volunteers_id": 2,
        "request_type": 1,
        "reservation_company_id": 2323,
        "reservation_company_name": "AA公司"
    }
    '''

    params = send_request.__dict__
    return await meeting.sendRequest(
        params['id'], 
        params['volunteers_id'], 
        params['request_type'], 
        params['reservation_company_id'], 
        params['reservation_company_name']
    )


# 预约会议 - 志愿者回复请求
@router.post('/api/meeting/volunteer_reply_request')
async def volunteerReplyRequest(volunteer_reply_request: VolunteerReplyRequestModel):
    return 123