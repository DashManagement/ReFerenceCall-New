'''
@Description:
@Author: michael
@Date: 2021-08-05 10:16:20
LastEditTime: 2021-08-05 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger

# meeting 我的/其它的 - 会议记录列表
class MeetingList:


    id = ''
    request_type= ''
    check_type = ''
    data_num = ''
    query_field = ''

    # 返回我的/其它的 - 会议记录列表
    async def construct(self, id='', request_type='', check_type='', data_num=''):

        if id == "refid":
            return {
                "code": 200,
                "data": [],
                "message": "no login"
            }

        self.id = int(id)
        self.request_type = int(request_type)
        self.check_type = int(check_type)
        self.data_num = int(data_num)

        # 查看请求者是否存在
        if await base.verifyUserReturnInfo(self.id) is False:
            return {'code':201, 'message':'用户不存在'}

        # 验证请求类型是否合法
        if self.request_type != 1 and self.request_type != 2:
            return {'code':202, 'message':'错误的请求类型'}

        # 验证查看类型是否合法
        if self.check_type != 0 and self.check_type != 1 and self.check_type != 2 and self.check_type != 3 and self.check_type != 4:
            return {'code':203, 'message':'错误的查看类型'}

        # 设置请求字段类型
        if self.request_type == 1:
            '''设置请求的字段类型为，查询我的'''
            self.query_field = 'start_id'
        else:
            '''设置请求的字段类型为，查询其它的'''
            self.query_field = 'end_id'

        # 判断查看类型
        #self.check_type == 0 '''未完成的会议列表'''
        #self.check_type == 1 '''已完成的会议列表'''
        #self.check_type == 2 '''已取消的会议列表'''
        #self.check_type == 3 '''已过期的会议记录'''
        #self.check_type == 4 '''全部会议列表'''

        # 查看用户列表信息
        return {'code':200, 'data':await self.getMeetingList()}


    # 查询会议列表
    async def getMeetingList(self):
        dbo.resetInitConfig('test', 'meeting_list')
        logger.info({'field':self.query_field, 'id':self.id, 'request_type':self.request_type, 'meeting_status':self.check_type})
        condition = {self.query_field:self.id, 'meeting_status':self.check_type}
        # field = {"id":1, "reservation_company_id":1, "reservation_company_name":1, "session_id":1, "name":1, "company_name":1, "_id":0}
        field = {
            "id": 1,
            "reservation_company_id": 1,
            "reservation_company_name": 1,
            "session_id": 1,
            "start_id": 1,
            "start_user_name": 1,
            "start_head_portrait": 1,
            "start_working_fixed_year": 1,
            "start_company_name": 1,
            "start_company_icon": 1,
            "end_id": 1,
            "end_user_name": 1,
            "end_head_portrait": 1,
            "end_working_fixed_year": 1,
            "end_company_name": 1,
            "end_company_icon": 1,
            "meeting_pass": 1,
            "national_area_code": 1,
            "national_area_name": 1,
            "meeting_time": 1,
            "meeting_status": 1,
            "create_time": 1,
            "_id":0
        }
        return await dbo.getData(condition, field)











meetingList = MeetingList()