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


# 创建 APIRouter 实例
router = APIRouter()


# 添加 referencecall 一个或多个公司，根据 company_id 参数的 列表长度是 1个或是 N个 为参考
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


