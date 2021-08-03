'''
@Description:
@Author: michael
@Date: 2021-07-30 10:16:20
LastEditTime: 2021-07-30 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.Search import search
from models.SearchModel import GeneralSearchModel
from models.SearchModel import HotSearchModel

# 创建 APIRouter 实例
router = APIRouter()

# 一般搜索内容
@router.post('/api/search/general_search')
async def generalSearch(search_params:GeneralSearchModel):
    ''' 
    非测试数据 - 目前是只是示例：
    {
        "id": "123",                    # 这里如果用户已经登陆，那么就使用用户的id, 如果没登陆，就用 - 来表示未登陆搜索。
        "search_content": "某某基金公司"  # 这里只搜基金公司的名称
    }
    '''
    
    params = search_params.__dict__
    return await search.generalSearch(params['id'], params['search_content'])


# 热门搜索列表
@router.post('/api/search/hot_search')
async def hotSearch(hot_search_params:HotSearchModel):
    ''' 
    非测试数据 - 目前是只是示例：
    {
        "id": "123",                    # 这里如果用户已经登陆，那么就使用用户的id, 如果没登陆，就用 - 来表示未登陆搜索。
    }
    '''

    params = hot_search_params.__dict__
    return await search.hotSearch(params['id'])