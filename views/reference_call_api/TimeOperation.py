'''
@Description:
@Author: michael
@Date: 2021-07-27 10:10:20
LastEditTime: 2021-07-27 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
from views.Base import *
from datetime import date, datetime, timedelta
import time
from config.log_config import logger


# reference all 时 计算时间的操作
class TimeOperation:


    # 计算一段时间的时间戳列表，默认从今天开始向后五天
    async def timeList(self, number_day=6):
        time_list = []
        for i in range(number_day):
            result = await self.calculatedTimeCycle(i)
            # time_list[result['time_info']['date']] = result
            time_list.append(result)
        return time_list


    # 计算当天 早9点 到 晚6点 的时间段列表
    async def calculatedTimeCycle(self, number_day=0):
        '''
        :param number_day integer 指定从今天开始向后计算的天数，例：number_day=1，向后一天，number_day=2，向后二天，默认0，计算当天
        '''

        # 今日零点时间戳
        today_zero_stamp = common.getTimeStamp()

        # 上午 9点整 时间戳
        nine_clock_stamp = today_zero_stamp + (3600*9) + (number_day*86400)
        # 上午 9点整 时间戳转换为 - 年-月-日 时:分:秒
        nine_clock = datetime.fromtimestamp(nine_clock_stamp)

        # 下午 6点整
        six_clock_stamp = today_zero_stamp + 3600*18 + (number_day*86400)
        # 下午 6点整 时间戳转换为 - 年-月-日 时:分:秒
        # six_clock = datetime.fromtimestamp(six_clock_stamp)

        time_list = []
        host_time_list = []
        tmp_time = []
        start_time = 9
        # 建立早上9点到晚上6点的时间戳列表
        for i in range(11):
            if i != 0 and len(host_time_list) == 2:
                time_list.append(host_time_list)
                host_time_list = [tmp_time]

            new_time = nine_clock_stamp + 3600 * i
            host_time_list.append(new_time)
            tmp_time = new_time

        # 计算时间为星期几
        date_week_result = await self.weekWhatDay(nine_clock_stamp, number_day)

        # 建立早上9点到晚上6点的时间戳转换为 - 年-月-日 时:分:秒, 和 时:分:秒 两组数据
        good_time_list = []
        new_time_list = []
        check_list = []
        for value in time_list:

            # 转换并添加时间格式为  ["2021-08-10T09:00:00","2021-08-10T10:00:00"]
            good_time_list.append([datetime.fromtimestamp(value[0]), datetime.fromtimestamp(value[1])])

            # 转换并添加时间格式为 ["09:00:00","10:00:00"],
            tmp_1 = datetime.time(datetime.fromtimestamp(value[0]))
            new_time_1 = tmp_1.strftime('%H:%M')
            tmp_2 = datetime.time(datetime.fromtimestamp(value[1]))
            new_time_2 = tmp_2.strftime('%H:%M')
            new_time_list.append([new_time_1, new_time_2])

            # 组合查看时间段 - 以小时为区间 如：9点到10点查示方式为 "09:00-10:00",
            tmp_str = str(new_time_1) + '-' + str(new_time_2)
            check_list.append(tmp_str)

        data = {
            'time_info':date_week_result,
            'time_stamp':time_list,
            'time_clock':good_time_list,
            'time':new_time_list,
            'check_time':check_list
        }
        return data


    # 计算时间戳为星期几
    async def weekWhatDay(self, date, number_day=0):

        # date = '1573401600'
        ltime = time.localtime(int(date))
        dateymd = time.strftime("%Y-%m-%d", ltime)
        # print(ltime)
        # print(dateymd)
        # 数字年月日 转换为 英语年月日
        month_english = time.strftime('%b', ltime)

        # print(dateymd)
        # 转换为星期几 星期表示 0-6，所以2019-11-11实际为周一，打印结果为0
        week = datetime.strptime(dateymd, "%Y-%m-%d").weekday()

        today_time = datetime.today()
        # # 获取当前年份
        # year = today_time.year
        # # 获取当前月份
        # month = today_time.month
        # # 获取当前日历
        # day = today_time.day

        # 获取当前年份
        year = time.strftime("%Y", ltime)

        # 获取当前月份
        month = time.strftime("%m", ltime)

        # 获取当前日历
        day = time.strftime("%d", ltime)

        # 将星期 + 1，改为 星期表示 1-7，实际周一的打印结果为 1
        new_week = week + 1

        # 今日零点时间戳
        today_zero_stamp = common.getTimeStamp()
        if number_day != 0:
            zero_stamp = today_zero_stamp + (3600*24)*number_day
        else:
            zero_stamp = today_zero_stamp

        data = {'date':dateymd, 'today_zero_stamp':zero_stamp, 'year':year, 'month':month, 'month_english':month_english, 'day':day, 'week':new_week, 'week_english':await self.digitalConversionEnglish(new_week)}

        return data


    # 将以星期几为数学的代表转化为英语的星期几 - 星期表示 1-7，实际周一的打印结果为 1
    async def digitalConversionEnglish(self, num):

        if num == 1:
            # Monday
            return 'Mon'
        elif num == 2:
            # Tuesday
            return 'Tue'
        elif num == 3:
            # Wednesday
            return 'Wed'
        elif num == 4:
            # Thursday
            return 'Thur'
        elif num == 5:
            # Friday
            return 'Fri'
        elif num == 6:
            # Saturday
            return 'Sat'
        elif num == 7:
            # Sunday
            return 'Sun'
        else:
            logger.info('error digitalConversionEnglish')
            return 'error digitalConversionEnglish'
            
            
    # 返回未来 N 天的 早9点 到晚 6点的时间戳
    async def returnTimeStamp(self, number_day=2):
    
        time_list = []
        for i in range(number_day):
            result = await self.returnNumberDayTimeStamp(i)
            time_list.append(result)

        return time_list


    # 返回 传入未来天数的 早9点 到晚 6点的时间戳
    async def returnNumberDayTimeStamp(self, number_day=0):

        # 今日零点时间戳
        today_zero_stamp = common.getTimeStamp()
        
        # 上午 8点整 时间戳
        nine_clock_stamp = today_zero_stamp + (3600*9) + (number_day*86400)
        # 上午 9点整 时间戳转换为 - 年-月-日 时:分:秒
        nine_clock = datetime.fromtimestamp(nine_clock_stamp)

        # 下午 6点整
        six_clock_stamp = today_zero_stamp + 3600*18 + (number_day*86400)
        # 下午 6点整 时间戳转换为 - 年-月-日 时:分:秒
        six_clock = datetime.fromtimestamp(six_clock_stamp)

        # 获取当前年份
        year = nine_clock.year
        # 获取当前月份
        month = nine_clock.month
        # 获取当前日期天数
        day = nine_clock.day

        time_info = {
            'time_stamp':[nine_clock_stamp, six_clock_stamp],
            'time_clock':[nine_clock, six_clock],
            'time_info':{
                'number_day':number_day,
                'year':year,
                'month':month,
                'day':day
            }
        }

        return time_info








timeOperation = TimeOperation()