'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel


# 基金列表验证模型
class FundListModel(BaseModel):
    uid: str


# 基金列表验证模型
class FundDetailsModel(BaseModel):
    uid: str
    company_id: str


