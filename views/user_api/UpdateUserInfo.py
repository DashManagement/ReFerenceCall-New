'''
@Description:
@Author: michael
@Date: 2021-07-09 10:16:20
LastEditTime: 2021-08-04 17:03:50
LastEditors: fanshaoqiang
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from views.reference_call_api.CompanyCurd import companyCurd
from config.log_config import logger


# 用户登陆后的返回信息类 - 返回登陆后的首页信息 lp/gp
class UpdateUserInfo:

    uid = ''
    user_token = ''
    plat_form = ''


    # 返回登陆后的首页信息 lp/gp
    async def updateUserToken(self, uid='', user_token='', plat_form=''):

        self.uid = int(uid)
        self.user_token = user_token
        self.plat_form = plat_form

        logger.info(f"params is uid: {uid}, user_token: {user_token}, plat_form: {plat_form}")
        return await self.resultData()


    # 返回 用户 的登陆信息列表
    async def resultData(self):

        user_info = await base.verifyUserReturnInfo(self.uid)

        # 判断用户是否存在
        if user_info is False:
            return {'code': 201, 'message': '用户不存在'}

        # 判断更新是否成功
        if await self.exceUpdate() is False:
            return {'code': 202, 'message': '用户 userToken 更新失败'}

        return {'code': 200}


    # 更新用户的 userToken
    async def exceUpdate(self):

        dbo.resetInitConfig('test', 'users')
        condition = {'id': self.uid}
        set_field = {'$set': {'userToken': self.user_token, 'platForm': self.plat_form}}

        updateOne = await dbo.updateOne(condition, set_field)

        if updateOne.modified_count != 1:
            return False

        return True





updateUserInfo = UpdateUserInfo()
