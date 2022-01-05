'''
@Description:
@Author: michael
@Date: 2021-08-08 10:16:20
LastEditTime: 2021-08-08 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger

# meeting 我的 - 会议历史记录
class HistoryMeetingSchedule:


    id = ''

    # 返回我的/其它的 - 会议记录列表
    async def construct(self, id=''):

        self.id = int(id)

        # 查看请求者是否存在
        user_info = await base.verifyUserReturnInfo(self.id)
        if user_info is False:
            return {'code':201, 'message':'用户不存在'}

        # 查看用户列表信息
        result = await self.getMeetingScheduleList(user_info)
        return {'code':200, 'count':len(result), 'data':result}


    # 查询已经约定的会议日程接口
    async def getMeetingScheduleList(self, user_info):

        # 今日零点时间戳
        today_zero_stamp = common.getTimeStamp()
        '''后面会用今日零点的时间戳代替当前时间 common.getTime()，暂时只是测试用的'''

        dbo.resetInitConfig('test', 'meeting_list')
        condition = {'start_time':{'$lt' : str(today_zero_stamp)}, '$or':[
            {'start_id':self.id},
            {'end_id':self.id}  
        ]}
        field = {
            "id": 1,
            "reservation_company_id": 1,
            "reservation_company_name": 1,
            "start_id": 1,
            "start_user_name": 1,
            "start_head_portrait": 1,
            "start_company_name": 1,
            "start_company_icon": 1,
            "end_id": 1,
            "end_user_name": 1,
            "end_head_portrait": 1,
            "end_company_name": 1,
            "end_company_icon": 1,
            "session_id": 1,
            "start_time": 1,
            "meeting_id": 1,
            "meeting_pass": 1,
            "meeting_address": 1,
            "meeting_time": 1,
            "start_time": 1,
            "meeting_end_time": 1,
            'create_time':1,
            '_id':0
        }
        sort = [('create_time', -1)]
        result = await dbo.getDataSort(condition, field, sort)

        if len(result) > 0:
            for value in result:
                value['name'] = user_info['name']
                value['company_name'] = user_info['company_name']

        # 整理用户信息返回的字段
        return_list = await self.finishingReturnUserInfoField(result)

        return return_list


     # 整理用户信息字段
    async def finishingReturnUserInfoField(self, schedule_list):

        for value in schedule_list:
            # for meeting in value['meeting']['list']:
            if self.id == value['end_id']:
                value['name'] = value['start_user_name']
                value['head_portrait'] = value['start_head_portrait']
                value['company_name'] = value['start_company_name']
                value['company_icon'] = value['start_company_icon']
            if self.id == value['start_id']:
                value['name'] = value['end_user_name']
                value['head_portrait'] = value['end_head_portrait']
                value['company_name'] = value['end_company_name']
                value['company_icon'] = value['end_company_icon']

            del value['start_user_name'], value['start_head_portrait'], value['start_company_name'], value['start_company_icon']
            del value['end_user_name'], value['end_head_portrait'], value['end_company_name'], value['end_company_icon']

        return schedule_list










historyMeetingSchedule = HistoryMeetingSchedule()