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


