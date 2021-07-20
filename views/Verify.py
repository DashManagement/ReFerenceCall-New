'''
@Description:
@Author: michael
@Date: 2020-12-21 16:22:20
LastEditTime: 2021-05-19 16:26:55
LastEditors: fanshaoqiang
'''
# coding=utf-8

# 加载自己创建的包
from views.verify_api.SendEmailVerify import sendEmailVerify
from views.verify_api.EmailCaptchaVerify import emailCaptchaVerify


from config.log_config import logger
# 邮件和验证类
class Verify:
    

    # 用户身份验证 - 后面做 jwt 验证的时候再调用
    async def userVerify(self):
        pass

    # 判断请求方式
    async def judgeRequest(self, verify_params):

        logger.info(verify_params)
        # logger.info(type(verify_params))
        # logger.info(verify_params['way'])
        # return 666
        # 判断请求方式是否正确
        if verify_params['way'] != '1' and verify_params['way'] != '2':
            return '条件错误：请发送正确的验证方式'

        return await self.getWay(
            verify_params['way'],
            verify_params['verify_type'],
            verify_params['email'],
            verify_params['uid'],
            verify_params['verify']
        )
        

    # 获取请求方式：1注册发送邮件-2注册码验证-3找回密码验证码验证
    async def getWay(self, way, verify_type, email, uid, verify):

        if way == '1':
            '''请求类型1：发送邮件验证码'''
            return await sendEmailVerify.returnSendEmail(way, verify_type, email)
        elif way == '2':
            '''请求类型2：验证码校验'''
            return await emailCaptchaVerify.returnCaptchaVerify(way, verify_type, email, uid, verify)








verify = Verify()