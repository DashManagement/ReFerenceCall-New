'''
Description: 
Author: fanshaoqiang
Date: 2016-08-04 18:57:57
LastEditTime: 2021-07-27 12:04:59
LastEditors: fanshaoqiang
'''
'''
Description: 
Author: fanshaoqiang
Date: 2016-08-04 18:57:57
LastEditTime: 2021-07-02 11:59:29
LastEditors: fanshaoqiang
'''




from views.ThirdParty.umessage.iosnotification import IOSNotification
from views.ThirdParty.umessage.umengnotification import MsgType
class IOSUnicast(IOSNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        IOSNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.uniCast)

    def setDeviceToken(self, token):
        self.setPredefinedKeyValue("device_tokens", token)


class IOSListcast(IOSNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        IOSNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.listCast)

    def setDeviceToken(self, token):
        self.setPredefinedKeyValue("device_tokens", token)


class IOSGroupcast(IOSNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        IOSNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.groupCast)

    def setFilter(self, filter):
        self.setPredefinedKeyValue("filter", filter)


class IOSFilecast(IOSNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        IOSNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.fileCast)

    def setFileId(self, fileId):
        self.setPredefinedKeyValue("file_id", fileId)


class IOSCustomizedcast(IOSNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        IOSNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.customizedCast)

    def setAlias(self, alias, aliasType):
        self.setPredefinedKeyValue("alias", alias)
        self.setPredefinedKeyValue("alias_type", aliasType)

    def setFileId(self, fileId, aliasType):
        self.setPredefinedKeyValue("file_id", fileId)
        self.setPredefinedKeyValue("alias_type", aliasType)


class IOSBroadcast(IOSNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        IOSNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.broadCast)
