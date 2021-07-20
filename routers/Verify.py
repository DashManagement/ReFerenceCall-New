'''
@Description:
@Author: michael
@Date: 2020-12-21 14:48:20
LastEditTime: 2021-05-19 15:35:51
LastEditors: fanshaoqiang
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.Verify import verify
from models.VerifyModel import VerifyModel


# 创建 APIRouter 实例
router = APIRouter()


# 发送邮件 或 邮件验证码验证
@router.post('/api/verify')
async def emailOrVerify(verify_params: VerifyModel):

    '''
    下面的为例子：非测试数据，
    uid 和 verify 两个字段为可选字段，验证码校验的时候才需要
    1. 发送邮件验证码的时候只需要填三个字段就可以
    1. {
        "way": "1",
        "verify_type": "1",
        "email": "26152462@qq.com"
    }
    1. 注册 - 验证码校验需要填满五个字段
    1. {
        "way": "2",
        "verify_type": "3",
        "email": "26152462@qq.com",
        "uid": "33",
        "verify": "9661"
    }
    1. 忘记密码 - 验证码校验的时候只需要填四个字段
    1. {
        "way": "2",
        "verify_type": "4",
        "email": "26152462@qq.com",
        "verify": "4252"
    }
    1. 其它参数发送请看文档
    '''
    
    return await verify.judgeRequest(verify_params.__dict__)
