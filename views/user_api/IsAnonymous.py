'''
@Description:
@Author: michael
@Date: 2021-09-28 10:00:00
LastEditTime: 2021-09-28 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *
from config.log_config import logger


# 设置用户是否匿名类
class IsAnonymous:

    id = ''                 # 用户 id
    is_anonymous = ''       # 是否匿名：1 是，0 否

    # 返回登陆后的首页信息 lp/gp
    async def construct(self, id='', is_anonymous=''):

        self.id = int(id)
        self.is_anonymous = int(is_anonymous)

        # 检测传入的匿名状态是否有效
        if self.is_anonymous != 1 and self.is_anonymous != 0:
            return {'code':201, 'message':'匿名参数错误'}

        # 检测 id 用户是否存在
        user_info = await base.verifyUserReturnInfo(self.id)
        if user_info is False:
            return {'code':202, 'message':'用户不存在'}

        # 更改用户的匿名状态
        return await self.updateIsAnonymous()


    # 返回注册响应数据
    async def updateIsAnonymous(self):

        dbo.resetInitConfig('test', 'users')

        condition = {'id': self.id}
        set_field = {'$set':{'is_anonymous': self.is_anonymous, 'update_time': common.getTime()}}

        update_result = await dbo.updateOne(condition, set_field)
        if update_result.modified_count != 1:
            logger.info('error: delete company failure')
            return {'code': 201, 'message': '更新匿名状态失败！'}

        return {'code': 200}







isAnonymous = IsAnonymous()




