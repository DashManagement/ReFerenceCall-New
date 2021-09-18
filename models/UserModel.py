'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-08-08 12:54:55
LastEditors: fanshaoqiang
'''

# coding=utf-8

from pydantic import BaseModel, EmailStr


# 用户注册验证模型
class UserRegisterModel(BaseModel):
    account: EmailStr
    password: str
    email: EmailStr = 1
    company_name: str
    fund_type: str = 1
    company_address: str = 1
    user_name: str
    userToken: str
    platForm: str
    localTimeZone: str


# 用户登陆验证模型
class UserLoginModel(BaseModel):
    account: EmailStr
    password: str


# 更新用户机器的 userToken
class UpdateUserTokenModel(BaseModel):
    uid: str
    user_token: str
    plat_form: str