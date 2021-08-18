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
from views.meeting_api.HistoryMeetingSchedule import historyMeetingSchedule
import datetime
import time
from config.log_config import logger

# meeting 按时间戳查看当天的会议日程
class CheckMeetingSchedule:


    id = ''
    time_stamp = ''

    # 按时间戳查看当天的会议列表
    async def construct(self, id='', time_stamp=''):

        self.id = id
        self.time_stamp = time_stamp
        logger.info(f"check_meeting_schedule is id:{id},time_stamp:{time_stamp}")

        # 获取所有 self.id 用户的历史记录
        result = await historyMeetingSchedule.construct(self.id)

        if result['count'] == 0: 
            return result

        # 转换传入时间戳为 time 类型
        tmp_time = common.getTimeDataYmd(self.time_stamp)
        
        # 初始化返回会议值列表
        tmp_result_list = []

        # 过滤历史记录，寻找 self.time_stamp 时间戳当天的会议记录
        for value in result['data']:
            if common.getTimeDataYmd(int(value['start_time'])) == tmp_time:
                # logger.info(common.getTimeDataYmd(int(value['start_time'])))
                tmp_result_list.append(value)

        # 定义返回数据结构
        data = {
            'code': 200,
            'count': len(tmp_result_list),
            'data': tmp_result_list
        }

        return data









checkMeetingSchedule = CheckMeetingSchedule()