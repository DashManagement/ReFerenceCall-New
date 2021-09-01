'''
Description: 
Author: fanshaoqiang
Date: 2021-07-27 11:52:52
LastEditTime: 2021-09-01 11:28:13
LastEditors: fanshaoqiang
'''
'''
Description: 
Author: fanshaoqiang
Date: 2021-07-27 11:52:52
LastEditTime: 2021-07-27 11:52:52
LastEditors: fanshaoqiang
'''
# coding=utf-8


# 注意andorid和ios是不同的appkey和appMasterSecret。 在不同需求下换成各自的appkey。
# 注意andorid和ios是不同的appkey和appMasterSecret。 在不同需求下换成各自的appkey。
import json
from views.ThirdParty.umessage.pushclient import PushClient
from views.ThirdParty.umessage.iospush import *
from views.ThirdParty.umessage.androidpush import *
from views.ThirdParty.umessage.errorcodes import UMPushError, APIServerErrorCode
from enum import Enum, unique
from views.Base import base
from config.log_config import logger
appKey = '60dd7be426a57f1018425555'
androidKey = '60fa83e0999517176d7a95c6'
appMasterSecret = 'ei0ycynmvzhqybdxcgwa5zbmrxuwingo'
deviceToken = 'DEC3C97AB50F958395E0F799037C1FAF5F71CCE0869307F57785FC6C7BC78DD2'
androidMasterSecret = 'rzggvkq7bhwhahetw8mweaxnc7d8mjyx'


@unique
class PlatForm(Enum):
    platform_IOS = 0
    platform_Android = 1


# @unique
class UMengPushAPI():
    def __init__(self):

        self.pushClient = PushClient()

    def generatePushContent(self, isReplay):
        if isReplay:
            return "You got a replay."
        else:
            return "You got a request."

    # 通过发送者的ID和志愿者的ID和是否是请求来发送Push
    # 如果isRequest为真，那应该寻找volunteerID相关的信息
    async def sendUnicastByUserID(self, fromUserID, volunteerID, isRequest):
        # logger.info(f"send bu id 11111 {fromUserID}, {volunteerID}")
        sendUid = fromUserID
        if isRequest:
            sendUid = volunteerID
        basicUserInfo = await base.getUserPushInfo(sendUid)
        # logger.info(f"send bu id 2222 {basicUserInfo}")
        if basicUserInfo != None:
            title = "New request." if isRequest else "New replay."
            content = "You got a new request." if isRequest else "You got a new replay."
            platForm = PlatForm.platform_IOS if basicUserInfo.get(
                "platForm") == "1" else PlatForm.platform_Android
            deviceToken = basicUserInfo.get("userToken", None)
            # logger.info(f"send bu id 3333 {deviceToken}")
            if deviceToken:
                self.sendUnicast(title, content, platForm, deviceToken)

    def sendUnicast(self, title, content, platForm, deviceToken):
        logger.info(f"params is {title}, {content}, {platForm},{deviceToken}")
        if platForm == PlatForm.platform_IOS:
            self.iosUnicast = IOSUnicast(appKey, appMasterSecret)
            self.iosUnicast.setAppKey(appKey)
            self.iosUnicast.setDeviceToken(deviceToken)
            self.iosUnicast.setAlert(title)
            self.iosUnicast.setBadge(1)
            self.iosUnicast.setCustomizedField(title, content)
            # unicast.setProductionMode()
            self.iosUnicast.setTestMode()
            # pushClient = PushClient()
            ret = self.pushClient.send(self.iosUnicast)
            logger.info(f"ret is {ret}")
            return ret.status_code
        elif platForm == PlatForm.platform_Android:
            logger.info("begin send Android push ")
            self.androidUnicast = AndroidUnicast(
                androidKey, androidMasterSecret)
            self.androidUnicast.setAppKey(androidKey)
            self.androidUnicast.setDeviceToken(deviceToken)
            self.androidUnicast.setTicker("Android unicast ticker")
            self.androidUnicast.setTitle(title)
            self.androidUnicast.setText(content)
            self.androidUnicast.goAppAfterOpen()
            self.androidUnicast.setDisplayType(
                AndroidNotification.DisplayType.notification)
            self.androidUnicast.setTestMode()
            logger.info(f"self.appKey is {self.androidUnicast.appKey}")
            logger.info(self.androidUnicast.getPostBody())
            # pushClient = PushClient()
            ret = self.pushClient.send(self.androidUnicast)
            # retJson = json.JSONDecoder(ret)
            logger.info(f"ret is {ret.text},{ret.status_code}")
            return ret.status_code
        # print(2)
        # self.androidUnicast

        # return 1
        # android


# def sendAndroidUnicast():
#     unicast = AndroidUnicast(appKey, appMasterSecret)
#     unicast.setDeviceToken(deviceToken)
#     unicast.setTicker("Android unicast ticker")
#     unicast.setTitle("中文的title")
#     unicast.setText("Android unicast text")
#     unicast.goAppAfterOpen()
#     unicast.setDisplayType(AndroidNotification.DisplayType.notification)
#     unicast.setTestMode()
#     pushClient = PushClient()
#     pushClient.send(unicast)


# def sendAndroidBroadcast():
#     broadcast = AndroidBroadcast(appKey, appMasterSecret)
#     broadcast.setTicker("Android broadcast ticker")
#     broadcast.setTitle("中文的title")
#     broadcast.setText("Android broadcast text")
#     broadcast.goAppAfterOpen()
#     broadcast.setDisplayType(AndroidNotification.DisplayType.notification)
#     broadcast.setTestMode()
#     # Set customized fields
#     broadcast.setExtraField("test", "helloworld")
#     pushClient = PushClient()
#     pushClient.send(broadcast)

# # ios


# def sendIOSUnicast():
#     unicast = IOSUnicast(appKey, appMasterSecret)
#     unicast.setDeviceToken(deviceToken)
#     unicast.setAlert("这个是一个iOS单播测试")
#     unicast.setBadge(1234)
#     unicast.setCustomizedField("test", "helloworld")
#     # unicast.setProductionMode()
#     unicast.setTestMode()
#     pushClient = PushClient()
#     ret = pushClient.send(unicast)
#     unicast.statuCode = ret.status_code
#     printResult(ret)


# def sendIOSBroadcast():
#     broadcast = IOSBroadcast(appKey, appMasterSecret)
#     broadcast.setAlert("这个是一个iOS广播测试")
#     broadcast.setBadge(1234)
#     broadcast.setTestMode()
#     pushClient = PushClient()
#     pushClient.send(broadcast)


# def sendIOSCustomizedcast():
#     customizedcast = IOSCustomizedcast(appKey, appMasterSecret)
#     customizedcast.setAlias("alias", "alias_type")
#     customizedcast.setAlert("这个是一个iOS个性化测试")
#     customizedcast.setBadge(1234)
#     customizedcast.setTestMode()
#     pushClient = PushClient()
#     pushClient.send(customizedcast)


# def sendIOSFilecast():
#     #fileId = client.uploadContents(appkey, appMasterSecret, "aa" + "\n" + "bb");
#     fileId = "fileid1"
#     filecast = IOSFilecast(appKey, appMasterSecret)
#     filecast.setFileId(fileId)
#     filecast.setAlert("这个是一个iOS组播测试")
#     filecast.setBadge(1234)
#     filecast.setTestMode()
#     pushClient = PushClient()
#     pushClient.send(filecast)


# def sendIOSListcast():
#     listcast = IOSListcast(appKey, appMasterSecret)
#     listcast.setDeviceToken("xxx,yyy,zzz")
#     listcast.setAlert("这个是一个iOS列播测试")
#     listcast.setBadge(1234)
#     listcast.setTestMode()
#     pushClient = PushClient()
#     pushClient.send(listcast)


# def sendIOSGroupcast():
#     # condition:
#     # "where":
#     # {
#     #  	"and":
#     #		[
#     #			{"tag" :"iostest"}
#     #		]
#     #	} /

#     groupcast = IOSGroupcast(appKey, appMasterSecret)

#     filterJson = json.loads('{}')
#     whereJson = json.loads('{}')
#     testTag = json.loads('{}')
#     testTag['tag'] = "iostest"
#     tagArray = [testTag]
#     whereJson['and'] = tagArray
#     filterJson['where'] = whereJson
#     groupcast.setFilter(filterJson)
#     groupcast.setAlert("IOS 组播测试")
#     groupcast.setBadge(1)
#     groupcast.setSound("default")
#     groupcast.setTestMode()
#     pushClient = PushClient()
#     ret = pushClient.send(groupcast)
#     printResult(ret)


# def printResult(ret):
#     print("http status code: %s" % ret.status_code)

#     if ret.text != "":
#         ret_json = json.loads(ret.text)
#         if ret_json["ret"] == IOSNotification.CONSTR_STATUS_SUCCESS:
#             if 'msg_id' in ret_json['data']:
#                 print("msgId: %s" % ret_json['data']['msg_id'])
#             if 'task_id' in ret_json['data']:
#                 print("task_id: %s" % ret_json['data']['task_id'])
#         elif ret_json["ret"] == IOSNotification.CONSTR_STATUS_FAIL:
#             errorcode = int(ret_json["data"]["error_code"])
#             print("error Code: %s, detail: %s" %
#                   (errorcode, APIServerErrorCode.errorMessage(errorcode)))


umengPushApi = UMengPushAPI()

# umengPushApi.sendUnicast(
#     "title", "123", PlatForm.platform_Android, "AjzbDEhet8jsUe9FaQNyzPQaHZgLgpRpHdtLx8hxTJVx")
# testUmengapi.sendUnicast("ios title", "123", PlatForm.platform_IOS,
#                          "DEC3C97AB50F958395E0F799037C1FAF5F71CCE0869307F57785FC6C7BC78DD2")
