'''
@Description:
@Author: michael
@Date: 2020-12-22 22:49:20
LastEditTime: 2021-05-19 16:11:33
LastEditors: fanshaoqiang
'''
# coding=utf-8


# 加载自己创建的包
from views.Base import *
from common.tools.Email import email
from config.log_config import logger

# 邮件验证
class EmailCaptchaVerify():

    way = ''
    verify_type = ''
    email = ''
    uid = ''
    verify = ''

    company_id = ''

    data = {
        'code':200
    }

    # 返回发送邮件的信息
    async def returnCaptchaVerify(self, way, verify_type, email_str, uid, verify):
        
        self.way = way
        self.verify_type = verify_type
        self.email = email_str
        self.uid = uid
        self.verify = verify
        self.company_id = ''


        logger.info(verify_type)
        # 清除垃圾 数据
        self.data.pop('message', 404)
        self.data.pop('data', 405)
        self.data.pop('is_admin', 405)
        self.data['code'] = 200

        if self.verify_type != '3' and self.verify_type != '4':
            self.data['code'] = 301
            self.data['message'] = '参数错误'
            return self.data

        # 判断验证类型
        if self.verify_type == '3':
            '''注册码验证'''
            return await self.registerVerify()
        elif self.verify_type == '4':
            '''修改新密码验证'''
            return await self.UpdatePassVerify()

        # return '???'


    # 注册码 - 验证
    async def registerVerify(self):


        # 判断用户 ID 和验证码 是否都存在 - 验证这块暂时先做个简单的验证 - 后面有时间再做更详细的验证
        if self.uid == 'None' or self.verify == 'None':
            self.data['code'] = 302
            self.data['message'] = '参数不正确'
            return self.data

        # logger.info(123123)
        user_result = await self.isUserInfo()
        if self.data['code'] != 200:
            return user_result

        # logger.info(123123)
        verify_result = await self.findUserForVerify()
        if self.data['code'] != 200:
            return verify_result

        # logger.info(123123)
        update_verify = await self.updateEmailVerifyStatus()
        if self.data['code'] != 200:
            return update_verify

        # logger.info(123123)
        update_user = await self.updateUserEmailVerifyStatus()
        if self.data['code'] != 200:
            return update_user

        update_admin_user = await self.updateUserIsAdminStatus()
        if self.data['code'] != 200:
            return update_admin_user    
        
        # logger.info(123123)
        return self.data


    # 修改新密码验证码 - 验证
    async def UpdatePassVerify(self):

        # 判断 email 和 验证码 是否都存在 - 验证这块暂时先做个简单的验证 - 后面有时间再做更详细的验证
        if self.email == 'None' or self.verify == 'None':
            self.data['code'] = 302
            self.data['message'] = '参数不正确'
            return self.data


        user_result = await self.isUserEmailInfo()
        if self.data['code'] != 200:
            return self.data


        verify_result = await self.findUserForVerify()
        if self.data['code'] != 200:
            return verify_result


        update_verify = await self.updateEmailVerifyStatus()
        if self.data['code'] != 200:
            return update_verify


        self.data['data'] = {}
        self.data['data']['uid'] = self.uid

        return self.data


    # 注册码验证 - 判断用户是否存在
    async def isUserInfo(self):

        dbo.resetInitConfig('test', 'lp_gp')
        condition = {'id':self.uid, 'is_email_verify':'0'}
        field = {'id':1, 'email':1, 'company_id':1, '_id':0}
        user_result = await dbo.findOne(condition, field)
        logger.info(user_result)
        # 判断用户是否存在
        if user_result is None:
            self.data['code'] = 201
            self.data['message'] = '不存在的用户 或 已经注册验证过'
            return self.data

        self.company_id = user_result['company_id']

        return self.data


    # 修改密码验证 - 判断用户是否存在 并设置 self.uid 为当前用户根据 email 查询到的 id
    async def isUserEmailInfo(self):

        dbo.resetInitConfig('test', 'lp_gp')
        condition = {'email':self.email}
        field = {'id':1, 'email':1, '_id':0}
        user_result = await dbo.findOne(condition, field)
        
        # 判断用户是否存在
        if user_result is None:
            self.data['code'] = 201
            self.data['message'] = '不存在的用户'
    
        # 判断验证方式如果为 4， 修改密码的验证方式：则赋值全局 uid，为返回值
        if self.verify_type == '4':
            self.uid = user_result['id']

        return self.data


    # 查找邮件验证码集合此用户的验证记录是否存在
    async def findUserForVerify(self):

        dbo.resetInitConfig('test', 'email_verify')
        condition = {'receive_id':self.uid, 'is_verify':'0', 'status':'0'}
        field = {'verify':1, 'over_time':1, '_id':0}
        verify_result = await dbo.findOne(condition, field)        

        # condition = condition = {'receive_id':self.uid, 'is_verify':'0', 'status':'0'}
        # field = {'verify':1, 'over_time':1, '_id':0}
        # sort = {'id':-1}
        # limit = 1
        # user_result = await dbo.findSort(condition, field, sort, limit)

        # logger.info(user_result)
        # self.data['code'] = 303
        # return self.data

        # 判断验证记录是否存在
        if verify_result is None:
            self.data['code'] = 202
            self.data['message'] = '不存在的 验证记录'
            return self.data
        elif verify_result['verify'] != self.verify:
            self.data['code'] = 203
            self.data['message'] = '验证码不正确'
            return self.data
        elif verify_result['over_time'] < common.getTime():
            self.data['code'] = 204
            logger.info(verify_result['over_time'])
            logger.info(common.getTime())
            self.data['message'] = '验证邮件已过期 请重新发送'
            return self.data
    
        return self.data


    # 更改本行验证记录状态
    async def updateEmailVerifyStatus(self):

        dbo.resetInitConfig('test', 'email_verify')
        condition = {'receive_id':self.uid, 'status':'0'}
        set_field = {'$set':{'is_verify':'1', 'verify_type':self.verify_type, 'verify_time':common.getTime(), 'status':'1'}}
        update_result = await dbo.updateOne(condition, set_field)
        logger.info(update_result.matched_count)
        logger.info(update_result.modified_count)
        
        # 判断验证记录是状态是否更改成功
        if update_result.modified_count != 1:
            self.data['code'] = 205
            self.data['message'] = '更新验证记录失败'

        return self.data


    # 更改用户表 注册邮箱是否已经验证
    async def updateUserEmailVerifyStatus(self):

        dbo.resetInitConfig('test', 'lp_gp')
        condition = {'id':self.uid, 'is_email_verify':'0'}
        set_field = {'$set':{'is_email_verify':'1'}}
        user_update_result = await dbo.updateOne(condition, set_field)

        # 判断用户注册是否已经通过验证码验证过
        if user_update_result.modified_count != 1:
            self.data['code'] = 205
            self.data['message'] = '更新用户注册验证失败'

        return self.data


    # 更改用户表 验证人身份是否为公司第一个注册的人
    async def updateUserIsAdminStatus(self):

        dbo.resetInitConfig('test', 'lp_gp')

        # 查找公司是否已经存在管理员
        condition = {'company_id':self.company_id, 'is_admin':'1'}
        field = {'id':1, '_id':0}
        admin_result = await dbo.findOne(condition, field)

        if admin_result is None:
            '''不存在改为管理员身份'''
            is_admin = '1'

            condition = {'id':self.uid}
            set_field = {'$set':{'is_admin':is_admin, 'is_auditing':'1'}}
            user_update_result = await dbo.updateOne(condition, set_field)

            # 判断用户注册验证后是否已经更新身份成功
            if user_update_result.modified_count != 1:
                self.data['code'] = 205
                self.data['message'] = '更新用户注册验证失败'
                logger.info(self.data)

            '''将注册用户绑定 云信 accid '''
            dbo.resetInitConfig('test', 'third_party')
            condition = {'is_bind':'0', 'status':'1'}
            field = {'_id':0}
            thirdParty_user = await dbo.findOne(condition, field)
            logger.info(thirdParty_user)
            # 获取 云信 accid 失败 或者已经没有用户
            if thirdParty_user is None:
                self.data['code'] = 206
                self.data['message'] = '获取第三方信息失败'
                return self.data

            '''更新用户第三方ID信息'''
            dbo.resetInitConfig('test', 'lp_gp')
            condition = {'id':self.uid}
            set_field = {'$set':{
                'w_account':thirdParty_user['accid'], 
                'w_password':thirdParty_user['token'], 
                'meeting_accountId':thirdParty_user['meeting_accountId'],
                'meeting_accountToken':thirdParty_user['meeting_accountToken']
            }}
            user_update_thirdParty = await dbo.updateOne(condition, set_field)

            # 判断用户注册验证后是否已经更新身份成功
            if user_update_thirdParty.modified_count != 1:
                self.data['code'] = 207
                self.data['message'] = '更新用户第三方信息失败'
                logger.info(self.data)
            logger.info(user_update_thirdParty)
            '''更新第三方账号使用状态为 已被绑定 is_bind:1 '''
            dbo.resetInitConfig('test', 'third_party')
            condition = {'id':thirdParty_user['id']}
            set_field = {'$set':{'uid':self.uid, 'is_bind':'1'}}
            update_thirdParty = await dbo.updateOne(condition, set_field)

            # 判断状态是否更新成功
            if update_thirdParty.modified_count != 1:
                self.data['code'] = 208
                self.data['message'] = '更新第三方绑定状态失败'
                return self.data


        else:
            '''存在给管理员发送消息，和未审核信息 - 现在还不知道用什么方式发送消息'''
            is_admin = '0'
            is_auditing = '0'


        self.data['is_admin'] = is_admin
        return self.data









emailCaptchaVerify = EmailCaptchaVerify()