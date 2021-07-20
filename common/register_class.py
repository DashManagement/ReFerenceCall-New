'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''

# 导入第三方包中间件
from loguru import logger

# 自己创建的包
from common.Dbo import Dbo
from common.Common import Common





# 注册单例实例
dbo = Dbo()
common = Common()