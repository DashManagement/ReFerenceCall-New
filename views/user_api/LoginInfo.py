'''
@Description:
@Author: michael
@Date: 2021-07-09 10:16:20
LastEditTime: 2021-07-09 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from views.JwtOperation import jwtOperation
from views.Fund import fund
from config.log_config import logger

# 用户登陆后的返回信息类 - 返回登陆后的首页信息 lp/gp
class LoginInfo:

    # 测试使用的用户名称和密码 - 
    account = ''    '''后面可能用 id 来替代 account'''
    password = ''   '''后面可能去掉 password 这个字段'''

    # 返回登陆后的首页信息 lp/gp
    async def returnLoginInfo(self, account='', password=''):

        self.account = account
        self.password = password

        return await self.resultData()


    # 返回 用户 的登陆信息列表
    async def resultData(self):

        user_info = await self.findUserBaseInfo()
        
        # 判断用户是否存在
        if user_info is None:
            return {'code':201, 'message':'错误的账号'}

        logger.info(self.password, user_info['password'])

        # 判断密码是否正确
        if self.password != user_info['password']:
            return {'code':203, 'message':'登陆密码错误'}

        # 判断更新次数 - 这一条可以抹掉或者不提示
        if await self.updateLoginNum() is False:
            return {'code':206, 'message':'更新登陆次数失败'}

        user_info = await self.returnUserInfo(user_info)
        fund_list = await fund.fundList(user_info['uid'])
        data = {
            'code': 200,
            'data': {
                'uses_info': user_info,
                'fund_list': fund_list
            }
        }

        return data


    # 查找用户的基本信息 
    async def findUserBaseInfo(self):
        # 连接数据库
        dbo.resetInitConfig('referencecall', 'users')

        # 条件 - 用户名 - 返回字段 全部
        condition = {'account': self.account}
        field = {'_id': 0}
        data = await dbo.findOne(condition, field)
        # logger.info(data)
        return data


    # 组织返回用户信息数据结构 - S
    async def returnUserInfo(self, user_info):

        num = int(user_info['login_num']) + 1

        # 生成 jwt 
        web_token = await jwtOperation.generateJwt(user_info['id'], user_info['account'])

        data = {
            "uid": user_info['id'],
            "web_token": web_token,
            "account": user_info['account'],
            "head_portrait": user_info['head_portrait'],
            "company_icon": user_info['company_icon'],
            "fund_type": user_info['fund_type'],
            "fund_name": user_info['fund_name'],
            "company_address": user_info['company_address'],
            "username": user_info['user_name'],
            "login_num": num,
            "last_login_time": user_info['last_login_time']
        }

        return data


    # 更新用户登陆次数 + 1， 默认 0， 当为 1 的时候为首次登陆
    async def updateLoginNum(self):
        dbo.resetInitConfig('referencecall', 'users')
        condition = {'account': self.account}
        set_field = {'$set':{'last_login_time':common.getTime()}, '$inc':{'login_num':1}}
        updateOne = await dbo.updateOne(condition, set_field)

        if updateOne.modified_count != 1:
            return False

        return True


    # 获取 gp 信息列表
    # async def getGpInfoList(self, user_id):
    #     return await commonPage.CommonPageInit(current_page='1', init_data=user_id, dataClass=gpList)
















loginInfo = LoginInfo()