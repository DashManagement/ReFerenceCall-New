'''
@Description:
@Author: michael
@Date: 2020-12-21 14:17:20
LastEditTime: 2020-12-21 20:00:00
LastEditors: michael
'''

# coding=utf-8

from pydantic import BaseModel

# 发送邮件或验证码请求方式
class VerifyModel(BaseModel):
    way: str
    verify_type: str
    email: str = None
    uid: str = None
    verify: str = None
