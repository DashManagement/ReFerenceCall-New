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
        user_info = await base.verifyUserReturnInfo(self.id)
        if user_info is False:
            return {'code':201, 'message':'用户不存在'}

        # 查看用户列表信息
        result = await self.getLastCall(user_info)
        return {'code':200, 'data':result}


    # 查询已经约定的会议日程接口
    async def getLastCall(self, user_info):

        dbo.resetInitConfig('test', 'meeting_list')
        condition = {'$or':[
            {'start_id':self.id},
            {'end_id':self.id}  
        ]}
        field = {
            "id": 1,
            "reservation_company_id": 1,
            "reservation_company_name": 1,
            "start_id": 1,
            "end_id": 1,
            "session_id": 1,
            "start_time": 1,
            "meeting_end_time": 1,
            "meeting_id": 1,
            "meeting_pass": 1,
            "meeting_address": 1,
            'create_time':1,
            '_id':0
        }
        sort = [('id', -1)]
        num = 0
        result = await dbo.findSort(condition, field, sort, num)

        # 没有记录则返回空
        if len(result) == 0:
            return []

        # 判断是会议请求者，还是会议的志愿者
        if self.id == result[0]['start_id']:
            condition = {'id':int(result[0]['end_id'])}
        else:
            condition = {'id':int(result[0]['start_id'])}
        field = {'_id':0}

        dbo.resetInitConfig('test', 'users')
        user_result = await dbo.findOne(condition, field)

        if user_result is None:
            return {'code':205, 'message':'获取会议请求者或志愿者信息失败'}

        result[0]['name'] = user_result['name']
        result[0]['head_portrait'] = user_result['head_portrait']
        result[0]['company_name'] = user_result['company_name']
        result[0]['company_icon'] = user_result['company_icon']

        return result












lastCall = LastCall()