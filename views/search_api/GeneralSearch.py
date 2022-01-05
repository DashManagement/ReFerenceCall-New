'''
@Description:
@Author: michael
@Date: 2021-07-30 10:16:20
LastEditTime: 2021-07-30 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *


# 一般搜索
class GeneralSearch:

    id = ''
    search_content = ''

    # 一般搜索流程
    async def construct(self, id='', search_content=''):

        self.id = id
        self.search_content = search_content

        # 添加搜索日志
        if await self.addSearchLog() is False:
            return {'code': 201, 'message': '添加搜索日志失败'}

        # 查看是否有搜索历史记录
        if await self.isSearchHistory() is False:
            # 如果没有搜索历史记录，就在搜索历史记录表里面新增一条搜索数据
            if await self.addSearchHistory() is False:
                return {'code': 202, 'message': '添加搜索历史记录失败'}
        else:
            # 如果有搜索历史记录，就在搜索历史记录表里面 - 搜索次数 +1 
            if await self.increaseSearchHistory() is False:
                return {'code': 203, 'message': '增加搜索历史记录次数失败'}

        # 获取基金名称和搜索内容匹配的基金列表
        return {'code':200, 'data': await self.getFundList()}


    # 添加搜索日志
    async def addSearchLog(self):

        # 获取搜索日志自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('search_log', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        # 添加一条搜索记录日志到搜索日志表里面
        dbo.resetInitConfig('test', 'search_log')
        document = {
            'id': get_id_result['update_id'],
            'search_user_id': self.id,
            'search_content': self.search_content,
            'create_time': common.getTime()
        }
        insert_result = await dbo.insert(document)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True


    # 查看是否有搜索历史记录
    async def isSearchHistory(self):

        dbo.resetInitConfig('test', 'search_history_number')
        condition = {'search_content':self.search_content}
        field = {'id':1, '_id':0}
        result = await dbo.findOne(condition, field)

        if result is None:
            return False

        return True


    # 查看是否有搜索历史记录
    async def addSearchHistory(self):
        
        # 获取搜索日志自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('search_history_number', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        # 添加一条搜索记录日志到搜索日志表里面
        dbo.resetInitConfig('test', 'search_history_number')
        document = {
            'id': get_id_result['update_id'],
            'search_content': self.search_content,
            'search_number': 1,
            'create_time': common.getTime(),
            'update_time': common.getTime()
        }
        insert_result = await dbo.insert(document)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        return True


    # 增加搜索历史记录
    async def increaseSearchHistory(self):

        dbo.resetInitConfig('test', 'search_history_number')
        condition = {'search_content': self.search_content}
        set_field = {'$set':{'update_time':common.getTime()}, '$inc':{'search_number':1}}
        updateOne = await dbo.updateOne(condition, set_field)

        if updateOne.modified_count != 1:
            return False

        return True


    # 获取基金列表
    async def getFundList(self):

        dbo.resetInitConfig('test', 'lp_gp')

        condition = {"$where": "this.id == this.company_id", "describe":"0", "fund_name":{"$regex": self.search_content}}
        field = {'id':1, 'company_id':1, 'fund_name':1, 'company_icon':1, 'base_info':1, 'company_info':1, '_id':0}
        result = await dbo.getData(condition, field)

        return result
        





generalSearch = GeneralSearch()