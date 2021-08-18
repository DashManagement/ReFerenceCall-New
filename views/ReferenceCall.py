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
        
        if len(company_id) > 1 :
            return await companyCurd.addManyCompany(uid, company_id)
        else:
            return await companyCurd.addCompany(uid, company_id[0])


    # 删除单个公司
    async def deleteCompany(self, id, uid):
        return await companyCurd.deleteCompany(id, uid)


    # 删除多个公司
    async def deleteManyCompany(self):
        pass


    # 志愿者已经添加的公司列表接口
    async def companyList(self, uid):
        return await companyCurd.companyList(uid)


    # 按公司查看 reference_call 的志愿者列表
    async def companyVolunteersList(self, id, company_id):
        return await companyCurd.companyVolunteersList(id, company_id)


    # 志愿者会议时间剩余可预约时间
    async def volunteersTime(self, id):
        return await companyCurd.checkVolunteersTime(id)


    def testCreateZoomMeeting(self):
        meetingTest = MeetingModel(
            fundName="123", fromUserName="fanshaoqiang", toUserName="123")
        zoomapi.createMeeting(meetingTest)






referenceCall = ReferenceCall()
