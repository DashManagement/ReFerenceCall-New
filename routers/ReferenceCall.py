'''
@Description:
@Author: michael
@Date: 2020-07-27 10:48:20
LastEditTime: 2020-07-27 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.ReferenceCall import referenceCall
from models.ReferenceCallModel import AddCompanyModel
from models.ReferenceCallModel import DeleteCompanyModel
from models.ReferenceCallModel import CompanyListModel
from models.ReferenceCallModel import CompanyVolunteersListModel

# 创建 APIRouter 实例
router = APIRouter()


# 添加 referencecall 一个或多个公司，根据 company_id 参数的 列表长度是 1个或是 N个 为参考
@router.post('/api/referencecall/add_company')
async def addCompany(add_company: AddCompanyModel):
    ''' 
    非测试数据：
    {
        "uid": "20",
        "company_id": ["89"]
    }
    '''

    params = add_company.__dict__
    return await referenceCall.addCompany(params['uid'], params['company_id'])


# 删除 referencecall 单个公司接口
@router.post('/api/referencecall/delete_company')
async def deleteCompany(delete_company: DeleteCompanyModel):
    ''' 
    非测试数据：
    {
        "id": "30",
        "uid": "29"
    }
    '''

    params = delete_company.__dict__
    return await referenceCall.deleteCompany(int(params['id']), int(params['uid']))


# 志愿者 已经添加的 referencecall 公司列表接口
@router.post('/api/referencecall/company_list')
async def companyList(company_list: CompanyListModel):
    ''' 
    非测试数据：
    {
        "id": "29"
    }
    '''

    params = company_list.__dict__
    return await referenceCall.companyList(int(params['uid']))


# 按公司查看该公司的 referencecall 志愿者名单
@router.post('/api/referencecall/company_volunteers_list')
async def companyVolunteersList(company_volunteers_list: CompanyVolunteersListModel):
    ''' 
    非测试数据：
    {
        "id": 23
        "company_id": "29"
    }
    '''

    params = company_volunteers_list.__dict__
    return await referenceCall.companyVolunteersList(int(params['id']), int(params['company_id']))