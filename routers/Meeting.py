'''
@Description:
@Author: michael
@Date: 2020-08-02 10:48:20
LastEditTime: 2021-08-08 20:26:21
LastEditors: fanshaoqiang
'''
# coding=utf-8

# 第三方包
from multiprocessing import Queue
# from aioredis import create_redis_pool, Redis
import asyncio
from time import sleep
from fastapi import APIRouter
from config.log_config import logger

# 自己创建的包
from views.Meeting import meeting
from views.Meeting import Meeting
from models.MeetingModel import SendRequestModel
from models.MeetingModel import VolunteerReplyRequestModel
from models.MeetingModel import RequesterRequestModel
from models.MeetingModel import CheckRequestModel
from models.MeetingModel import MeetingListModel
from models.MeetingModel import BookingMeetingModel
from models.MeetingModel import LastCallModel
from models.MeetingModel import HistoryMeetingScheduleModel
from models.MeetingModel import CheckMeetingScheduleModel


# 创建 APIRouter 实例
router = APIRouter()


# 预约会议 - 预约者第一次发送请求
@router.post('/api/meeting/send_request')
async def sendRequest(send_request: SendRequestModel):
    ''' 
    id	                        是	string	请求者 id
    volunteers_id	            是	list	志愿者 id 列表
    request_type	            是	string	请求类型：1 请求者发送预约请求
    reservation_company_id	    是	string	预约沟通的公司id
    reservation_company_name	是	string	预约沟通的公司名称
    非测试数据：
    {
        "id": 1,
        "volunteers_id": [11, 12],
        "request_type": 1,
        "reservation_company_id": 2323,
        "reservation_company_name": "AA公司"
    }
    '''

    params = send_request.__dict__
    logger.info(f"params is {params}")
    result = await meeting.sendRequest(
        params['id'],
        params['volunteers_id'],
        params['request_type'],
        params['reservation_company_id'],
        params['reservation_company_name']
    )
    logger.info(f"result is {result}")
    return result


# 预约会议 - 志愿者回复请求
@router.post('/api/meeting/volunteer_reply_request')
async def volunteerReplyRequest(volunteer_reply_request: VolunteerReplyRequestModel):
    ''' 
    id	            是	string	        志愿者 id
    session_id	    是	list	        会话 id
    request_type	是	string	        请求类型：2 志愿者回复请求时间，4 志愿者拒绝，没有预约时间
    time	        否	string	        志愿者回复预订的时间 例：[[13213565461, 12474672392],[13213565461, 12474672392],[13213565461, 12474672392]]
    time 为ios传入时 否	string	        ios 传入的 志愿者回复预订的时间 例：[{"timeList": [[1629334800, 1629338400],[1629334800, 1629338400]], "zero_stamp": "1629302400"}, {"timeList": [[1629601200, 1629604800]], "zero_stamp": "1629561600"}, {"timeList": [[1629511200, 1629514800]], "zero_stamp": "1629475200"}]
    非测试数据：
    {
        "id": 1,
        "session_id": 2,
        "request_type": 1,
        "time": [
            [13213565461, 12474672392],
            [13213565461, 12474672392],
            [13213565461, 12474672392]
        ]
    }
    client_type     否  string          判断是 android 还是 ios 传进来的值
    '''

    params = volunteer_reply_request.__dict__
    logger.info(params)
    return await meeting.volunteerReplyRequest(
        params['id'],
        params['session_id'],
        params['request_type'],
        params['time'],
        params['client_type']
    )


# 预约会议 - 请求者回复志愿者
@router.post('/api/meeting/requester_request')
async def requesterRequest(requester_request: RequesterRequestModel):
    ''' 
    id	            是	string	        志愿者 id
    session_id	    是	list	        会话 id
    request_type	是	string	        请求类型：2 志愿者回复请求时间，4 志愿者拒绝，没有预约时间
    time_info	    否	dict	        创建会议的时间信息 例：{
                                                                "date": "2021-08-13",
                                                                "year": 2021,
                                                                "month": 8,
                                                                "month_english": "Aug",
                                                                "day": 13,
                                                                "week": 5,"week_english": "Fri" 
                                                            }
    meeting_time	否	list	        请求者回复志愿者预订的时间 例：[13213565461, 12474672392]
    非测试数据：
    {
        "id": 1,
        "session_id": 2,
        "request_type": 1,
        "time_info": {
            "date": "2021-08-13",
            "year": 2021,
            "month": 8,
            "month_english": "Aug",
            "day": 13,
            "week": 5,"week_english": "Fri" 
        }
        "meeting_time": [13213565461, 12474672392]
    }
    '''

    params = requester_request.__dict__
    logger.info(params)
    logger.info("in requesterRequest the params is ")
    logger.info(f"params is {params}")
    return await meeting.requesterRequest(
        params['id'],
        params['session_id'],
        params['request_type'],
        params['time_info'],
        params['meeting_time']
    )


# 预约会议 - 查看请求 - 我发送的预约请求 my request /被邀请的预约请求 other
@router.post('/api/meeting/check_request')
def checkRequest(check_request: CheckRequestModel):
    ''' 
    id	            是	string  	    请求者 id
    request_type	是	string	        请求类型：1 我的 my request，2 其它的 other request
    data_num	    是	string	        数据类型：1 显示 3条，2 显示 30条
    非测试数据：
    {
        "id": 1,
        "request_type": 2,
        "data_num": 1
    }
    '''
    params = check_request.__dict__
    logger.info(params)
    # sleep(0.5)
    test_meeting = Meeting()
    result = test_meeting.checkRequest(params['id'], params['request_type'], params['data_num'])
    # sleep(0.5)
    # asyncio.sleep(0.3)
    return result


# 预约会议 - 查看是否有未处理的请求
@router.post('/api/meeting/is_request')
async def checkRequest(is_request: CheckRequestModel):
    '''
    id	            是	string  	    请求者 id
    request_type	是	string	        请求类型：1 我的 my request，2 其它的 other request
    data_num	    是	string	        数据类型：1 显示 3条，2 显示 30条
    非测试数据：
    {
        "id": 1,
        "request_type": 2,
        "data_num": 1
    }
    '''

    params = is_request.__dict__
    logger.info(params)
    test_meeting = Meeting()
    result = test_meeting.isRequest(params['id'], params['request_type'], params['data_num'])
    return result

    return data


# 会议列表相关操作 - 暂时被取消 - 没有用到
@router.post('/api/meeting/meeting_list')
async def meetingList(meeting_list: MeetingListModel):
    ''' 
    id	            是	string  	    请求者 id
    request_type	是	string	        请求类型：1 我的 my request，2 其它的 other request
    data_num	    是	string	        数据类型：1 显示 3条，2 显示 30条
    非测试数据：
    {
        "id": 1,
        "request_type": 2,
        "data_num": 1
    }
    '''

    params = meeting_list.__dict__
    logger.info(params)
    return await meeting.getMeetingList(params['id'], params['request_type'], params['check_type'], params['data_num'])


# 已经约定的会议日程接口
@router.post('/api/meeting/meeting_schedule')
async def meetingSchedule(meeting_schedule: BookingMeetingModel):
    ''' 非测试数据：{ "id": 23 } '''
    params = meeting_schedule.__dict__

    '''判断是否为未注册的用户'''
    if params['id'] == 'refid':
        return {'code':200, 'data':{'count':0, 'schedule_list':[]}}

    '''非法的字符串用户'''
    if params['id'].isdigit() is False:
        return {'code':302, 'message':'非法用户'}

    return await meeting.meetingSchedule(int(params['id']))


# 最后一个已完成的会议信息接口
@router.post('/api/meeting/last_call')
async def lastCall(last_call: LastCallModel):
    ''' 非测试数据：{ "id": 23 } '''
    params = last_call.__dict__
    return await meeting.lastCall(int(params['id']))


# 查看今日和今日之前已约定的历史会议日程接口
@router.post('/api/meeting/history_meeting_schedule')
async def historyMeetingSchedule(history_meeting_schedule: HistoryMeetingScheduleModel):
    ''' 非测试数据：{ "id": 23 } '''
    params = history_meeting_schedule.__dict__
    return await meeting.historyMeetingSchedule(int(params['id']))


# 按时间戳查看当天的会议日程
@router.post('/api/meeting/check_meeting_schedule')
async def checkMeetingSchedule(check_meeting_schedule: CheckMeetingScheduleModel):
    ''' 非测试数据：{ "id": 23, "time_stamp": "1629093600" } '''
    params = check_meeting_schedule.__dict__
    return await meeting.checkMeetingSchedule(int(params['id']), int(params['time_stamp']))


# 志愿者回复时间数据结构 - IOS 测试
@router.post('/api/meeting/volunteer_reply_request_test')
async def volunteerReplyRequest(volunteer_reply_request: VolunteerReplyRequestModel):

    time = [
        {"timeList": [[1629334800, 1629338400],[1629334800, 1629338400]], "zero_stamp": "1629302400"}, 
        {"timeList": [[1629601200, 1629604800]], "zero_stamp": "1629561600"}, 
        {"timeList": [[1629511200, 1629514800]], "zero_stamp": "1629475200"}
    ]

    time_list = []
    # str 转 json 格式转化
    for value in time['time']:

        tmp_list = []

        for value_2 in value['timeList']:
            tmp_list.append(value_2)

        time_list.append({value['zero_stamp']:tmp_list})
    
    return time_list

    # params = volunteer_reply_request.__dict__
    # logger.info(params)
    # return await meeting.volunteerReplyRequest(
    #     params['id'],
    #     params['session_id'],
    #     params['request_type'],
    #     params['time']
    # )


async def que():
    return 123

# async def log_to_data_base():
#     await asyncio.sleep(3)
#     print("log in database")