'''
@Description:
@Author: michael
@Date: 2021-08-05 10:16:20
LastEditTime: 2021-09-02 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from views.meeting_api.BookingMeetingList import BookingMeetingList
from config.log_config import logger

# meeting 我的/其它的 - 预约会议流程列表


class IsBookingMeeting:

    id = ''
    request_type = ''
    check_type = ''
    
    def construct(self, id='', request_type='', data_num=''):

        if id == "refid":
            return {
                "code": 200,
                "unread_count": 0,
                "my_unread_count": 0,
                "other_unread_count": 0,
                "message": "no login"
            }

        self.id = int(id)
        self.request_type = int(request_type)
        self.data_num = int(data_num)

        if self.request_type != 1 and self.request_type != 2 and self.request_type != 3:
            return {'code':201, 'message':'错误的请求方式'}
    
        return self.returnMeetingCount()

    
    def returnMeetingCount(self):

        data = {'code':200, 'unread_count':0}

        if self.request_type == 3:

            self.request_type = 1
            my_result = self.getResult()

            self.request_type = 2
            other_result = self.getResult()

            if my_result['code'] != 200:
                return my_result
            if other_result['code'] != 200:
                return other_result

            data['my_unread_count'] = 0
            data['other_unread_count'] = 0

            data['my_unread_count'] = self.getMyResultCount(my_result)
            data['other_unread_count'] = self.getOtherResultCount(other_result)

            data['unread_count'] = data['my_unread_count'] + data['other_unread_count']

            return data

        result = self.getResult()
        if result['code'] != 200:
            return result
        
        if self.request_type == 1:
            data['unread_count'] = self.getMyResultCount(result)
            return data

        if self.request_type == 2:
            data['unread_count'] = self.getOtherResultCount(result)
            return data


    def getResult(self):
        newBookingMeeting = BookingMeetingList()
        return newBookingMeeting.construct(self.id, self.request_type, self.data_num)


    def getOtherResultCount(self, data):

        count = 0
        if data['code'] == 200 and data['count'] != 0:

            for value in data['data']:

                if value['request_num'] == 1 and value['status'] == 1 and value['is_create_meeting'] == 0:

                    logger.info(value)
                    count = count + 1

        return count


    def getMyResultCount(self, data):

        count = 0
        if data['code'] == 200 and data['count'] != 0:

            for value in data['data']:

                if value['request_num'] == 2 and value['status'] == 1 and value['is_create_meeting'] == 0:

                    logger.info(value)
                    count = count + 1

        return count