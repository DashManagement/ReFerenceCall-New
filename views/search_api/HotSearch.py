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


# 热门搜索
class HotSearch:


    # id = ''

    # 返回热门搜索列表
    async def returnHotSearchList(self, id=''):

        # self.id = id

        return await self.hotSearchList()


    # 获取热门搜索列表 - 此处暂时未限制返回条数
    async def hotSearchList(self):

        dbo.resetInitConfig('test', 'search_history_number')

        condition = {}
        field = {'_id':0}
        sort=[('search_number',-1)]   # 排序字段
        result = await dbo.getDataSort(condition, field, sort)

        data = {}
        data['code'] = 200
        data['data'] = result

        return data
        





hotSearch = HotSearch()