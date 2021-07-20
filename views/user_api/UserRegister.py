'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger


# 用户登陆后的返回信息类 - 返回登陆后的首页信息 lp/gp
class UserRegister:

    account = ''
    password = ''
    email = ''
    fund_type = ''
    fund_name = ''
    company_address = ''
    user_name = ''

    # 返回登陆后的首页信息 lp/gp
    async def returnUserRegister(self, account='', password='', email='', fund_type='', fund_name='', company_address='', user_name=''):

        self.account = account
        self.password = password
        self.email = email
        self.fund_type = fund_type
        self.fund_name = fund_name
        self.company_address = company_address
        self.user_name = user_name
        
        return await self.resultData()


    # 返回注册响应数据
    async def resultData(self):

        # 判断用户是否存在
        if await self.isUser() is True:
            return {'code':206, 'message':'用户已注册'}

        # 添加用户
        adduser_result = await self.addUser()
        if adduser_result is False:
            return {'code':203, 'message':'添加用户失败'}

        return {'code':200, 'data':adduser_result}


    # 查找用户名称是否存在
    async def isUser(self):

        # 连接数据库
        dbo.resetInitConfig('referencecall', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'account': self.account}
        field = {'is_email_verify':1, 'is_admim':1, 'is_auditing':1, '_id': 0}
        result = await dbo.findOne(condition, field)

        # 用户存在的时候
        if result is not None:
            return True

        return False


    # 查找用户基金公司是否存在 - 不存在返回 false，存在返回公司 id，公司名称 fund_name， 管理员 id
    async def isFund(self):

        # 连接数据库
        dbo.resetInitConfig('referencecall', 'users')

        # 条件 - 查找 基金公司名称 fund_name 和 有管理权限 is_admin 的用户 - 返回字段 全部
        condition = {'fund_name': self.fund_name}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        if result is None:
            return False
        
        return result


    # 添加用户
    async def addUser(self):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('users', db='referencecall')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        # 连接数据库集合
        dbo.resetInitConfig('referencecall', 'users')

        document = {
            'id': get_id_result['update_id'],
            'email': self.email,
            'account': self.account,
            'password': self.password,
            'fund_name': self.fund_name,
            'fund_type': 1,
            'company_address': self.company_address,
            'user_name': self.user_name,
            'head_portrait': 1,
            'company_icon': 1,
            'company_info': 1,
            'login_num': 0,
            'reg_time': common.getTime(),
            'last_login_time': 0,
            "update_time" : 1
        }
        
        insert_result = await dbo.insert(document)
        logger.info(insert_result.inserted_id)

        # 判断添加记录是否成功
        if insert_result.inserted_id is None:
            return False

        # 组织返回注册成功后的数据结构
        data = {
            'id': get_id_result['update_id'],
            'account': self.account,
            'user_name': self.user_name,
            'fund_name': self.fund_name
        }

        return data
        







userRegister = UserRegister()