'''
@Description:
@Author: michael
@Date: 2021-07-27 10:16:20
LastEditTime: 2021-07-27 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包


from views.reference_call_api.CompanyCurd import companyCurd
from views.ThirdParty.ZoomAPI import zoomapi, MeetingModel
import views.ThirdParty.UMengPushAPI


# ReferenceCall 接口类 - 公司信息服务志愿者接口
class ReferenceCall:

    # 添加公司
    async def addManyCompany(self, uid, company_id):
        return await companyCurd.addManyCompany(uid, company_id)


    # 添加单个公司
    async def addCompany(self, uid, company_id):
        return await companyCurd.addCompany(uid, company_id[0])


    # 删除单个公司
    async def deleteCompany(self):
        pass


    # 删除多个公司
    async def deleteManyCompany(self):
        pass


    def testCreateZoomMeeting(self):
        meetingTest = MeetingModel(
            fundName="123", fromUserName="fanshaoqiang", toUserName="123")
        zoomapi.createMeeting(meetingTest)


referenceCall = ReferenceCall()
