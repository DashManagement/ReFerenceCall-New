'''
@Description:
@Author: michael
@Date: 2021-07-27 10:16:20
LastEditTime: 2021-07-27 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel
from typing import List


# 添加 reference call 公司模型验证
class AddCompanyModel(BaseModel):
    uid: str
    company_id: List[str]


# 删除 reference call 公司模型验证
class DeleteCompanyModel(BaseModel):
    id: str
    uid: str


# 志愿者已经添加的 reference call 公司列表模型验证
class CompanyListModel(BaseModel):
    uid: str


# 志愿者已经添加的 reference call 公司列表模型验证
class CompanyVolunteersListModel(BaseModel):
    id: str = '-'
    company_id: str


# 查看志愿者可预订时间的模型验证
class VolunteersTimeModel(BaseModel):
    id: str