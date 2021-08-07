'''
Description: 
Author: fanshaoqiang
Date: 2021-07-26 17:33:13
LastEditTime: 2021-08-05 18:34:18
LastEditors: fanshaoqiang
'''
from pydantic import BaseModel
import jwt
import requests
import json
from time import time
import chardet
from datetime import date, datetime
from config.log_config import logger


# Enter your API key and your API secret
API_KEY = 'g4tJbBqaT4mrAWtEoJaWlw'
API_SEC = 'lU4TtnLsqQx8rcOLijqhlMLZBFx00IK0ZA4A'
defaultDuration = "60"


class MeetingModel(BaseModel):
    fundName: str
    fromUserName: str
    toUserName: str
    fromEmail: str = None
    toEmail: str = None
    meetingTime: str = None
    meetingZone: str = None
    duration: str = None


class ZoomAPI:
    def __init__(self, apikey, apisec):
        self.apiKey = apikey
        self.apiSec = apisec

    # create a function to generate a token
    # using the pyjwt library
    def generateToken(self):
        token = jwt.encode(

            # Create a payload of the token containing
            # API Key & expiration time
            {'iss': API_KEY, 'exp': time() + 50000},

            # Secret used to generate token signature
            API_SEC,

            # Specify the hashing alg
            algorithm='HS256'
        )
        # print(chardet.detect(token))
        token = token.decode("utf-8")

        return token

    # create json data for post requests
    # 需要定义Topic
    # type 2是计划会议
    # pre_schedule 仅对type是2的有影响
    # duration 单位是分钟
    # settings就传个默认值
    # schedule_for
    # recurrence  只针对type 为8 的有作用
    def generateTopic(self, requestFundName, fromUser, toUser):
        topic = "About " + requestFundName + " from " + fromUser
        return topic

    def generateMeetingDetail(self, topic, start_time, timezone, duration=defaultDuration):
        meetingdetails = {
            "topic": topic,
            "type": 2,
            "start_time": start_time,
            "duration": duration,
            "timezone": timezone,
            "agenda": "Reference Call",

            "recurrence": {"type": 1,
                           "repeat_interval": 1
                           },
            "settings": {
                "host_video": "true",
                "participant_video": "true",
                "join_before_host": "False",
                "mute_upon_entry": "False",
                "watermark": "true",
                "audio": "voip",
                "auto_recording": "cloud"
            }
        }
        logger.info(meetingdetails)
        return meetingdetails

        # send a request with headers including
        # a token and meeting details

    # 返回参数里面有会议ID, 会议连接和会议密码
    def createMeeting(self,  meetingModel: MeetingModel):
        headers = {'authorization': 'Bearer %s' % self.generateToken(),
                   'content-type': 'application/json'}
        topic = self.generateTopic(
            meetingModel.fundName, meetingModel.fromUserName, meetingModel.toUserName)
        # timeNow = datetime.now()
        # timeNow = timeNow.strftime("%Y-%m-%dT%H:%M:%S")
        meetingdetails = self.generateMeetingDetail(
            topic, meetingModel.meetingTime, meetingModel.meetingZone, meetingModel.duration)

        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meetingdetails))

        print("\n creating zoom meeting ... \n")
        # print(r.text)
        # converting the output into json and extracting the details
        meetingInfo = json.loads(r.text)

        if meetingInfo.get("id") == None:
            return None
            # return {"Join_URL": None, "Meeting_ID": None, "Meeting_Pwd": None}
        join_URL = meetingInfo["join_url"]
        meeting_ID = meetingInfo.get("id")
        meetingPassword = meetingInfo.get("password")

        print(
            f'\n here is your zoom meeting link {join_URL} and your \
            password: "{meetingPassword}"\n')

        return {"Join_URL": join_URL, "Meeting_ID": meeting_ID, "Meeting_Pwd": meetingPassword}


# run the create meeting function
# testZoom = ZoomAPI(API_KEY, API_SEC)
# testZoom.createMeeting()
# generateToken()
zoomapi = ZoomAPI(API_KEY, API_SEC)
