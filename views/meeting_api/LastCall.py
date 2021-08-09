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

# meeting 最后一个已完成的会议信息接口
class LastCall:


    id = ''

    # 返回我的/其它的 - 会议记录列表
    async def construct(self, id=''):

        self.id = int(id)

        # 查看请求者是否存在
        user_info = await self.getUserInfo()
        if user_info is False:
            return {'code':201, 'message':'无效的用户id'}

        # 查看用户列表信息
        result = await self.getLastCall(user_info)
        return {'code':200, 'data':result}


    # 查询已经约定的会议日程接口
    async def getLastCall(self, user_info):

        dbo.resetInitConfig('test', 'meeting_list')
        condition = {'status':0, 'meeting_status':1, '$or':[
            {'start_id':self.id},
            {'end_id':self.id}  
        ]}
        field = {
            "id": 1,
            "reservation_company_id": 1,
            "reservation_company_name": 1,
            "session_id": 1,
            "start_time": 1,
            "meeting_id": 1,
            "meeting_pass": 1,
            "meeting_address": 1,
            'create_time':1,
            '_id':0
        }
        sort = [('id', -1)]
        num = 0
        result = await dbo.findSort(condition, field, sort, num)

        for value in result:
            value['name'] = user_info['name']
            value['company_name'] = user_info['company_name']

        return result


    # 获取用户信息
    async def getUserInfo(self):

        dbo.resetInitConfig('test','users')
        condition = {'id':self.id}
        field = {'_id':0}
        result = await dbo.findOne(condition, field)
        logger.info(result)
        if result is None:
            return False

        return result









lastCall = LastCall()