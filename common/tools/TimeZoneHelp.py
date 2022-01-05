'''
Description:
Author: fanshaoqiang
Date: 2021-07-30 17:56:39
LastEditTime: 2021-07-30 23:09:52
LastEditors: fanshaoqiang
'''
import pytz
# from datetime import timezone
import datetime
from datetime import date
from datetime import timedelta


localFormat = "%Y-%m-%dT%H:%M:%S"

# timezones = ['America/Los_Angeles', 'Europe/Madrid', 'America/Puerto_Rico']

# for tz in timezones:
#     localDatetime = utcmoment.astimezone(pytz.timezone(tz))
#     print(localDatetime.strftime(localFormat))


def createLocalTime(year, month, day, hour, localTimeZone):
    localTime = datetime.datetime(int(year), int(month), int(
        day), int(hour), tzinfo=pytz.timezone(localTimeZone))
    # datetime(2021,)
    return localTime


def convertTimeTo(localTime, distTimeZone):
    localDatetime = localTime.astimezone(pytz.timezone(distTimeZone))
    distDatetime = localDatetime.strftime(localFormat)
    return distDatetime


tempLT = datetime.datetime(2021, 8, 1, 20, 0, 0, 0)
print(tempLT)
td = timedelta(hours=8)  # timedelta 对象
tz = datetime.timezone(td)  # 时区对象
tmpLocalTime = datetime.datetime(2021, 8, 1, 20, tzinfo=tz)
print(tmpLocalTime)
tmpLocalTime = createLocalTime(2021, 8, 1, 20, "Asia/Hong_Kong")
print(tmpLocalTime)
print(tmpLocalTime.strftime(localFormat))
convertTime = convertTimeTo(tmpLocalTime, "America/Los_Angeles")
print(convertTime)

# utcmoment_naive = datetime.now(tz=timezone('Australia/Sydney'))
# utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
# utcmoment = datetime(2021, 7, 30, 13, 0, 0, 000, timezone("Asia/Shanghai"))
# # print"utcmoment_naive: {0}".format(utcmoment_naive) # python 2
# print("utcmoment_naive: {0}".format(utcmoment_naive))
# print("utcmoment:       {0}".format(utcmoment))
