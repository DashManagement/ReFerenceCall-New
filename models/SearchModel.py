'''
@Description:
@Author: michael
@Date: 2021-07-30 10:16:20
LastEditTime: 2021-07-30 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel


# 用户登陆验证模型
class GeneralSearchModel(BaseModel):
    id: str = '-'
    search_content: str


# 热门搜索列表
class HotSearchModel(BaseModel):
    id: str = '-'