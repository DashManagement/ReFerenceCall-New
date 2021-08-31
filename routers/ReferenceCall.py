'''
@Description:
@Author: michael
@Date: 2020-07-27 10:48:20
LastEditTime: 2021-08-08 12:08:45
LastEditors: fanshaoqiang
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
from models.ReferenceCallModel import VolunteersTimeModel

from config.log_config import logger
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
    logger.info(f"params is {params}")
    result = await referenceCall.addManyCompany(params['uid'], params['company_id'])
    logger.info(f"result is {result}")
    return result

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
    logger.info(params)
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
    logger.info(f"params is {params}")
    if params['id'] == 'refid':
        userID = 0
    else:
        userID = int(params['id'])
    return await referenceCall.companyVolunteersList(userID, int(params['company_id']))


# 查看志愿者可预约的时间
@router.post('/api/referencecall/volunteers_time')
async def volunteersTime(volunteers_time: VolunteersTimeModel):
    '''
    非测试数据：{"id": 23} 
    '''
    params = volunteers_time.__dict__
    return await referenceCall.volunteersTime(int(params['id']))