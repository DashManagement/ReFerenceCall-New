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

# 创建 APIRouter 实例
router = APIRouter()


# 添加 referencecall 一个或多个公司，根据 company_id 参数的 列表长度是 1个或是 N个 为参考
@router.post('/api/referencecall/add_company')
async def addCompany(add_company: AddCompanyModel):
    ''' 
    测试数据：
    {
        "uid": "20",
        "company_id": ["89"]
    }
    '''

    params = add_company.__dict__
    return await referenceCall.addCompany(params['uid'], params['company_id'])
