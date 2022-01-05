'''
@Description:
@Author: michael
@Date: 2020-07-08 10:10:20
LastEditTime: 2021-09-28 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.User import user
from models.UserModel import UserRegisterModel
from models.UserModel import UserLoginModel
from models.UserModel import UpdateUserTokenModel
from models.UserModel import IsAnonymousModel

# 创建 APIRouter 实例
router = APIRouter()

# 注册


@router.post('/api/user/register')
async def userRegister(register_params: UserRegisterModel):
    ''' 
    账号只可以用邮箱来注册 - email 是添加 account 后自动同步的字段 
    测试数据：
    {
        "account": "1132v@qq.com",
        "password": "123123a",
        "fund_name": "test+me",
        "user_name": "孙某某"
    }
    '''

    params = register_params.__dict__
    return await user.userRegister(params)


# 用户登陆后的首个返回信息
@router.post('/api/user/login')
async def loginFirstInfo(login_params: UserLoginModel):
    ''' 测试数据
    {
        "account":"232312131@qq.com",
        "password":"123123a"
    }
    '''

    params = login_params.__dict__
    return await user.loginInfo(params['account'], params['password'])


# 更新用户机器的 userToken
@router.post('/api/user/update_user_token')
async def updateUserToken(update_user_token: UpdateUserTokenModel):
    ''' 测试数据
    {
        "uid":"153",
        "user_token":"E3F273426BF8170065D8C384C7C2FB6552F19EF495EDF7B11792718B746DA475"
        "plat_form":"1"
    }
    '''

    params = update_user_token.__dict__
    return await user.updateUserToken(params['uid'], params['user_token'], params['plat_form'])


# 设置用户是否匿名
@router.post('/api/user/is_anonymous')
async def isAnonymous(is_anonymous: IsAnonymousModel):
    ''' 测试数据
    {
        "id": 454,              # 用户 id
        "is_anonymous": "1"     # 是否匿名：1 是，0 否
    }
    '''

    params = is_anonymous.__dict__
    return await user.isAnonymous(params['id'], params['is_anonymous'])