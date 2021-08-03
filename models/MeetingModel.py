'''
@Description:
@Author: michael
@Date: 2021-08-02 10:16:20
LastEditTime: 2021-08-02 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel


# 用户登陆验证模型
class SendRequestModel(BaseModel):
    id: str
    volunteers_id: str
    request_type: str
    reservation_company_id: str
    reservation_company_name: str

