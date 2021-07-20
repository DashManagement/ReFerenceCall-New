'''
@Description:
@Author: michael
@Date: 2020-12-21 12:48:20
LastEditTime: 2021-05-19 16:11:22
LastEditors: fanshaoqiang
'''
# coding=utf-8


# 加载自己创建的包
from views.Base import *
from common.tools.Email import email
from config.log_config import logger

# 发送邮件
class SendEmilVerify():

    way = ''
    verify_type = ''
    email_str = ''

    rand_verify = ''
    data = {
        'code':200
    }

    # 返回发送邮件的信息
    async def returnSendEmail(self, way, verify_type, email_str):
        
        self.way = way
        self.verify_type = verify_type
        self.email_str = email_str
        self.rand_verify = ''

        return await self.registerOrFindPassSendEmail()


    # 注册码 或 找回密码验证码 - 发送邮件
    async def registerOrFindPassSendEmail(self):

        self.data['code'] = 200
        self.data.pop('message', 404)

        if self.verify_type != '1' and self.verify_type != '2':
            self.data['code'] = 301
            self.data['message'] = '参数错误'
            return self.data


        user_result = await self.isUserEmail()
        if user_result == 201:
            self.data['code'] = 201
            self.data['message'] = '不存在的用户'
            return self.data


        if user_result == 206:
            self.data['code'] = 206
            self.data['message'] = '邮箱已验证'
            self.data['is_email_verify'] = '1'
            return self.data


        email_result = await self.isSendEmail()
        if email_result == 202:
            self.data['code'] = 202
            self.data['message'] = '邮件 验证码 发送失败'
            '''
            注：邮件发送失败多数是因为邮件SMTP服务代理会检测自家是否有该账号
            例：用腾讯SMTP发送邮件给腾讯用户的时候，腾讯会检测该QQ号是否存在，然后选择是否发送，用其它STMP中转服务就可以解决该问题。
            '''
            return self.data


        insert_email_result = await self.insertEmaiVerifyInfo(user_result['id'])
        if insert_email_result == 203:
            self.data['code'] = 203
            self.data['message'] = '邮件发送成功，但插入数据集合失败，写入log日志里面'

        self.data['is_email_verify'] = '0'
        return self.data


    # 判断 email 是否存在
    async def isUserEmail(self):

        dbo.resetInitConfig('test', 'lp_gp')

        # 判断是 - 注册发送验证码，还是 - 修改密码发送验证码    1 注册， 2 修改密码
        # if self.verify_type == '1':
            # condition = {'email':self.email_str, 'is_email_verify':'0'}
        # elif self.verify_type == '2':
        condition = {'account':self.email_str}
        logger.info(self.email_str)
        field = {'id':1, 'is_email_verify':1, '_id':0}
        result = await dbo.findOne(condition, field)
        # logger.info(result)
        # return 123123123
        # 判断用户是否存在
        if result is None:
            return 201

        # 判断是否已注册
        if self.verify_type == '1' and result['is_email_verify'] == '1':
            return 206


        return result


    # 发送邮件
    async def isSendEmail(self):

        self.rand_verify = common.myRandVerify(num=4)

        if self.verify_type == '1':
            send_name = '达世科技'
            header_name = send_name +' | 注册码'
            email_address = self.email_str
            content = 'Dash项目 注册码 邮件发送测试... ｜' + self.rand_verify 
        else:
            send_name = '达世科技'
            header_name = send_name + ' | 找回密码'
            email_address = self.email_str
            content = 'Dash项目 找回密码 邮件发送测试... ｜' + self.rand_verify 

        result = await email.sendEmail(send_name, header_name, email_address, content)

        # 判断邮件是否发送成功
        if result == 0:
            return 202


    # 向邮件验证集合里面添加一条信息 并将该用户其它未验证的信息关闭
    async def insertEmaiVerifyInfo(self, user_id):

        create_time = common.getTime()
        over_time = create_time + 10*60

        dbo.resetInitConfig('test', 'email_verify')

        # 关闭该用户以前发送验证码但并没有验证的记录 状态
        condition = {'receive_id':user_id, 'verify_type':self.verify_type, 'status':'0'}
        set_fields = {'$set':{'status':'1'}}
        update_result = await dbo.updateAll(condition, set_fields)
        '''此条记录记入日志 - 不作其它处理'''

        # 插入验证记录信息
        '''下面的ID应该用自增的ID - 暂时还没获取它'''
        # 获取 id 自增记录
        get_id_result = await dbo.getNextIdtoUpdate('friend_verify_log')
        if get_id_result['action'] == False:
            return '获取 id 自增值失败'
        # logger.info(123123123)
        # logger.info(get_id_result)
        # logger.info(123123123)

        dbo.resetInitConfig('test', 'email_verify')

        document = {
            'id':str(get_id_result['update_id']),
            'send_way':self.way, 
            'receive_id':user_id, 
            'receive_email':self.email_str, 
            'is_verify':'0', 
            'verify_type':self.verify_type, 
            'verify':self.rand_verify,
            'status':'0',
            'create_time':create_time,
            'over_time':over_time
        }
        result = await dbo.insert(document)
        logger.info(result.inserted_id)

        # 判断信息是否添加成功
        if result.inserted_id is None:
            return 203

        

    








sendEmailVerify = SendEmilVerify()