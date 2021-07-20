'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载第三方包
from bson.objectid import ObjectId
'''
查询 _id 字段必须导入 from bson.objectid import ObjectId
'''
import sys
'''
用于主动退出 python 程序，sys.exit()，1个参数，默认为0，表示正常退出，也可以为1，表示异常退出。
'''

# 加载自己创建的包
from common.read_db_config import *
from config.log_config import logger


# 数据库操作类 - 全名 Database operation 缩写
class Dbo:
    '''
    :param prefix 数据库前缀 (string)
    :param client 数据库客户端连接 (string)
    :param dbname 数据库名称 (string)
    :param collection 当前连接的集合 (string)
    :param tmp_collection 当前连接的集合名称 (string)
    '''
    prefix = prefix 
    client = client
    dbname = ''
    collection = ''
    tmp_collection = ''

    # 构造
    def __init__(self, dbname=db, collection=collection_name):
        self.resetInitConfig(dbname, collection)

    # 重新初始化数据库配置
    def resetInitConfig(self, dbname, collection):
        if dbname is None: dbname = db
        if collection is None: collection = collection_name
        self.dbname = self.combinationPrefix(dbname)
        self.tmp_collection = self.combinationPrefix(collection)
        self.db = self.configDataLink()
        self.collection = self.configCollectionLink()

    # 组合前缀
    def combinationPrefix(self, param):
        return self.prefix + param

    # 连接指定数据库
    def configDataLink(self):
        return self.client[self.dbname]

    # 连接指定集合
    def configCollectionLink(self):
        return self.db[self.tmp_collection]

    # 插入单条数据
    def insert(self, document):
        return self.collection.insert_one(document)

    # 插入或更新单条数据
    def save(self, document):
        return self.collection.save(document)

    # 更新一条数据
    async def updateOne(self, condition, set_field):
        '''
        :param condition = {'id':self.user_id}
        :param set_field = {'$set':{'is_admin':'0'}}
        '''
        return await self.collection.update_one(condition, set_field)

    # 批量更新数据
    async def updateAll(self, condition, set_fields):
        '''
        :param condition = {'id':self.user_id}
        :param set_field = {'$set':{'is_admin':'0'}}
        '''
        return await self.collection.update_many(condition, set_fields)

    # 查找一条数据
    async def findOne(self, condition={}, field={'_id':0}):
        return await self.collection.find_one(condition, field)

    async def del_one(self, condition={}):
        return await self.collection.delete_one(condition)

    # 查询一条数据，一参
    async def find_one(self, condition={}):
        return await self.collection.find_one(condition)

    # 查找指定条件排序的 N 条数据 - 分页用的较多
    async def findSort(self, condition={}, field={'_id':0}, sort=[('id',1)], skip=0, num=1, length=None):
        '''
        :param condition = {'id':self.user_id}
        :param field = {'_id':0} 获取指定字段
        :param sort = [('id',1)] 正序或倒序的排列，1 正序，-1 倒序
        :param num = 1 读取的条数
        :param length 指定获取数据的条数，默认 None 获取全部数据
        '''
        result = self.collection.find(condition, field).sort(sort).skip(skip).limit(num)
        return await result.to_list(length=length)


    # 查询指定条件数据并排序
    async def getDataSort(self, condition={}, field={}, sort={}, length=None):
        '''
        :param sort 排序字段 
        :param length 指定获取数据的条数，默认 None 获取全部数据
        '''
        result = self.collection.find(condition, field).sort(sort)
        return await result.to_list(length=length)


    # 获取指定条件数据
    async def getData(self, condition={}, field={}, length=None):
        '''
        :param length 指定获取数据的条数，默认 None 获取全部数据
        '''
        result = self.collection.find(condition, field)
        return await result.to_list(length=length)


    # 获取指定条件数据集合的总数
    async def getCountCollection(self, condition={}):
        return await self.collection.count_documents(condition)


    # 获取指定条件数据集合的总数 - 测试用的 - 主要是用来测试那个 GP 列表 集合带 WHERE 条件的 company 查询
    async def getCountCollectionTest(self, condition={}, field={}):
        result = self.collection.find(condition, field)
        return await result.to_list(length=None)


    # 获取当前实例属性信息 - 暂未使用
    def getAttribute(self):
        return {
            'perfix': self.prefix, 
            'client': self.client, 
            'dbname': self.dbname, 
            'collection': self.collection
        }


    # 获取 id自增表 下个 ID 的方法
    async def getNextIdtoUpdate(self, field_name, db='test'):
        """
        获取当前集合id的最新编号
        :param field_name 字段名称 - 需要获取的表名称 string
        :return:None
        """
        # 记录原来的数据库连接点，后面操作完用来还原到原来的数据库连接 - 暂时废弃
        # tmp_dbname = self.dbname
        # tmp_collection = self.tmp_collection

        # 重置数据库集合连接
        self.resetInitConfig(db, 'pk_increment')

        # 组织查询参数 - 暂时没用，为了方便换机器的时候数据库 ObjectId 不一样也可以使用，暂时不设置条件，默认第一条数据
        condition = {'_id': ObjectId('5fd344556cd96f634ca57b57')}
        field = {field_name: 1, '_id': 0}

        # 查询
        find_result = await self.findOne({}, field)

        # 将返回字段的数据转换为数值类型以做比较
        id = int(find_result[field_name])
        # logger.info(id)

        # 判断返回 id 是否存在并大于等于 1 - 返回相应结果
        if id >= 0:
            insert_id = id + 1
        else:
            logger.info('获取ID失败，返回错误，不能自增！')
            sys.exit(0)
            '''这块如果不使用 exit 退出全部程序，容易造成用户或其它集合 ID 的重复，会出现大问题的，所以在没有事务处理之这前，宁可让它出现错误时崩溃'''

        # 组织更新参数
        # update_id = {field_name: str(insert_id)}

        # 更新
        # updateResult = await self.updateOne(condition, {'$set': update_id})
        updateResult = await self.updateOne(condition, {'$inc':{field_name:1}})
                                                        
        result = {}
        if updateResult.modified_count == 1:
            result['action'] = True
            result['update_id'] = insert_id
            result['table_name'] = field_name
        else:
            result['action'] = False
            result['old_id'] = id
            result['field_name'] = field_name

        # 重置数据库集合连接到原来的连接 - 暂时废弃
        # self.resetInitConfig(tmp_dbname, tmp_collection)

        return result
        '''
        result 这个返回值的数据结构，目前这样定义是考虑手写事务，后面可能会用副本集来考虑事务的问题。
        '''

