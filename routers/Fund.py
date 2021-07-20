'''
@Description:
@Author: michael
@Date: 2020-07-13 10:50:20
LastEditTime: 2020-07-13 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 第三方包
from fastapi import APIRouter

# 自己创建的包
from views.Fund import fund
from models.FundModel import FundListModel
from models.FundModel import FundDetailsModel

# 创建 APIRouter 实例
router = APIRouter()


# 基金公司列表
@router.post('/api/fund/fund_list')
async def fundList(fund_list: FundListModel):
    ''' 
    测试数据：
    {
        "uid": "20"
    }
    '''

    params = fund_list.__dict__
    return await fund.fundList(params['uid'])


# 基金公司详情
@router.post('/api/fund/fund_details')
async def fundDetails(fund_details: FundDetailsModel):
    ''' 
    测试数据：
    {
        "uid": "1",
        "company_id": "1"
    }
    '''

    params = fund_details.__dict__
    return await fund.fundDetails(params['uid'], params['company_id'])