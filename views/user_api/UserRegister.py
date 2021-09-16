'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-08-08 00:22:05
LastEditors: fanshaoqiang
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
    userToken = ''
    platForm = ''
    localTimeZone = ''

    # 返回登陆后的首页信息 lp/gp

    async def returnUserRegister(self, account='', password='', email='', fund_type='', fund_name='',
                                 company_address='', user_name='', userToken='', platForm='', timeZone=''):

        self.account = account
        self.password = password
        self.email = account
        self.fund_type = fund_type
        self.fund_name = fund_name
        self.company_address = company_address
        self.user_name = user_name
        self.userToken = userToken
        self.platForm = platForm
        self.localTimeZone = timeZone

        return await self.resultData()

    # 返回注册响应数据
    async def resultData(self):

        # 判断用户是否存在
        result = await self.isUser()
        if result is not False:
            return {'code': 206, 'message': '用户已注册', 'data': result}

        # 添加用户
        adduser_result = await self.addUser()
        if adduser_result is False:
            return {'code': 203, 'message': '添加用户失败'}

        return {'code': 200, 'data': adduser_result}

    # 查找用户名称是否存在

    async def isUser(self):

        # 连接数据库
        dbo.resetInitConfig('test', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'account': self.account}
        field = {'_id': 0}
        result = await dbo.findOne(condition, field)

        # 用户存在的时候
        if result is not None:
            return result

        return False

    # 查找用户基金公司是否存在 - 不存在返回 false，存在返回公司 id，公司名称 fund_name， 管理员 id
    # async def isFund(self):

    #     # 连接数据库
    #     dbo.resetInitConfig('test', 'users')

    #     # 条件 - 查找 基金公司名称 fund_name 和 有管理权限 is_admin 的用户 - 返回字段 全部
    #     condition = {'fund_name': self.fund_name}
    #     field = {'_id': 0}
    #     result = await dbo.findOne(condition, field)

    #     if result is None:
    #         return False

    #     return result

    # 添加用户
    async def addUser(self):

        # 获取自增 ID
        get_id_result = await dbo.getNextIdtoUpdate('lp_gp', db='test')
        if get_id_result['action'] == False:
            logger.info('获取 id 自增失败')
            return False

        # 连接数据库集合
        dbo.resetInitConfig('test', 'users')

        document = {
            'id': get_id_result['update_id'],
            'is_reservation': 1,
            'userToken': self.userToken,
            'platForm': self.platForm,
            'localTimeZone': self.localTimeZone,
            'name': self.user_name,
            'alias': "-",
            'head_portrait': "-",
            'position': "-",
            'working_fixed_year': "-",
            'company_name': self.fund_name,
            'company_alias': "-",
            'company_icon': "-",
            'company_introduction': "-",
            'company_create_time': "-",
            'company_type': "-",
            'company_main_business': "-",
            'company_address': "-",
            'email': self.account,
            'account': self.account,
            'password': self.password,
            'is_email_verify': "0",
            'login_num': 0,
            'last_login_time': 0,
            "create_time": common.getTime(),
            "update_time": common.getTime()
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
