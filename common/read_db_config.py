'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''
# coding=utf-8


from configparser import ConfigParser
import motor.motor_asyncio
import pymongo

readConfig = ConfigParser()


# 加载远程数据库配置变量
# readConfig.read('./config/database.ini')
# host = readConfig.get('remote_config', 'host')
# port = readConfig.getint('remote_config', 'port')
# user = readConfig.get('remote_config', 'user')
# password = readConfig.get('remote_config', 'password')
# db = readConfig.get('remote_config', 'db')
# prefix = readConfig.get('remote_config', 'prefix')
# collection_name = readConfig.get('remote_config', 'collection')

# 组合远程数据库地址
# mongo_url = f"mongodb://{user}:{password}@{host}:{port}/{db}"

# 加载 本地 localhost 数据库配置变量
readConfig.read('./config/database.ini')
host = readConfig.get('localhost_config', 'host')
port = readConfig.getint('localhost_config', 'port')
user = readConfig.get('localhost_config', 'user')
password = readConfig.get('localhost_config', 'password')
db = readConfig.get('localhost_config', 'db')
prefix = readConfig.get('localhost_config', 'prefix')
collection_name = readConfig.get('localhost_config', 'collection')

# 加载 服务器 server 数据库配置变量
# readConfig.read('./config/database.ini')
# host = readConfig.get('remote_config', 'host')
# port = readConfig.getint('remote_config', 'port')
# user = readConfig.get('remote_config', 'user')
# password = readConfig.get('remote_config', 'password')
# db = readConfig.get('remote_config', 'db')
# prefix = readConfig.get('remote_config', 'prefix')
# collection_name = readConfig.get('remote_config', 'collection')

# 组合本地数据库地址
mongo_url = f"mongodb://{host}:{port}"

# 组合远程数据库地址
# mongo_url = f"mongodb://{user}:{password}@{host}:{port}"

# 远程数据库地址 mongoClient 示例
# emote_client = MongoClient('mongodb://dash:dashmima!@118.193.47.247:8088/dash')

# 连接数据库服务器
client = motor.motor_asyncio.AsyncIOMotorClient(
    mongo_url, retryWrites="false", uuidRepresentation="standard"
)
