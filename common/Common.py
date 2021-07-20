'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 第三方的包
from datetime import datetime, timedelta
import datetime
import time
import random
import socket
import base64
from config.log_config import logger

# 公共类
class Common:
    
    # 清除返回数据 _id 类型，因为该字段通常为 object 类型 - 现在不需要了，已经没有类调用它 - 随时可以删除
    def clear_id(self, data):
        del data['_id']
        return data

    # 创建 DB 操作类 - 已被新的方式替代 - 取消此模块
    # def createDb(dbname=None, collection=None):
    #     return Curd(dbname, collection)


    # 获取时间戳
    def getTime(self):

        '''注释掉的代码为 - 时间戳转换为 - 年-月-日 时:分:秒'''
        # last_hour = datetime.fromtimestamp(self.getTime()+10*60)
        # logger.info('last_hour = ',last_hour)

        da_1 = datetime.datetime.now()
        da_2 = datetime.datetime.timetuple(da_1)
        return int(time.mktime(da_2))
        

    # 今天开始时间戳
    def getTimeStamp(self):
        today = datetime.date.today()
        yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
        today_start_time = yesterday_end_time + 1
        return today_start_time


    # 转换时间戳为日期
    def getTimeData(self, timeStamp):
        timeArray = time.localtime(timeStamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


    # 转换时间戳为时分秒
    def getTimeDataHMS(self, timeStamp):
        timeArray = time.localtime(timeStamp)
        return time.strftime("%H:%M:%S", timeArray)


    # 生成随机数字验证码
    def myRandVerify(self, num):
        '''
        :param num integer 随机验证码的位数
        '''
        checkcode = ''
        for i in range(num):
            current = random.randrange(0,num)
            # if current == i:
                # tep = chr(random.randint(65,97))
            # else:
            tep = random.randint(0,9)
            checkcode+=str(tep)
            
        return checkcode


    # 生成随机数字+英文验证码
    def myRandVerifyStr(self, num):
        '''
        :param num integer 随机验证码的位数
        '''
        checkcode = ''
        for i in range(num):
            current = random.randrange(0,num)
            if current != i:     #!=  不等于 - 比较两个对象是否不相等
                temp = chr(random.randint(65,90))
            else:
                temp = random.randint(0,9)
            checkcode += str(temp)
            
        return checkcode


    # 获取当前服务器 ip 地址 - 目前没有调用本页方法的类
    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
            return ip

        if __name__ == '__main__':
            logger.info(get_host_ip())


    # 判断是否为字典 - 暂时未用上
    async def is_dict(self, uid):
        return isinstance(uid, dict)
        

    # 判断变量是否存在
    async def isset(v): 
        try:
            type (eval(v))
        except:
            return False
        else:
            return True

    # base64encode 加密
    async def encryption(self, ostr):
        
        #接收bytes入参，返回bytes加密结果
        base_result = base64.b64encode(ostr.encode())

        #返回的bytes数据通过decode()转换为字符串
        new_mstr = base_result.decode()

        # + 改成 *， / 改成 -
        good_str = new_mstr.replace('/', '-').replace('+', '*')

        # logger.info(new_mstr)
        return good_str


    # base64decode 解密
    async def decryption(self, mstr):

        ''': mstr 加密后的字符串'''
        base_result = base64.b64decode(mstr)
        ostr = base_result.decode()

        # - 改成 /， * 改成 +
        good_str = ostr.replace('-', '/').replace('*', '+')        

        # logger.info(good_str)
        return good_str


    # 字符串反转
    async def reversedString(self, a_string):
        return a_string[::-1]




common = Common()