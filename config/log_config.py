'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''
from loguru import logger

logger.add('./log/server_logging_{time}.log', rotation='00:00')