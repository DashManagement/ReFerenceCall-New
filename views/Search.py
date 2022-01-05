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
from views.search_api.GeneralSearch import generalSearch
from views.search_api.HotSearch import hotSearch


# 搜索接口类
class Search:


    # 一般搜索
    async def generalSearch(self, id, search_content):
        return await generalSearch.construct(id, search_content)


    # 热门搜索
    async def hotSearch(self, id):
        return await hotSearch.returnHotSearchList(id)













search = Search()