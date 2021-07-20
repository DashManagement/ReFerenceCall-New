'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''
# coding=utf-8

# 加载自己创建的包
import jwt
import json
import datetime
from starlette.responses import Response
from config.log_config import logger

# Jwt 认证类
class JwtOperation:


    # 生成 jwt
    async def generateJwt(self, uid, account):

        # 载荷
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=15),
            'uid': uid,
            'account': account,
        }

        # 签名
        return jwt.encode(payload=payload, key='miyao', algorithm='HS256')


    # 校验 jwt
    async def verifyJwt(self, request, call_next):

        # 初始化 response
        response = await call_next(request)

        # 处理 axios 两次请求中第一次测试通讯时的 OPTIONS 状态 - 暂时先这样处理，后面有更好的方案再另行解决
        if request.scope['method'] == 'OPTIONS':
            return response

        # 取 url 后缀
        url_suffix_name = str(request.url).rsplit("/",1)
        # 略过登陆页面的 token 验证 - 目前还未成立单独的白名单 - 后面有时间要单独增加白名单来管理 token 认证
        if url_suffix_name[1] == 'login' or url_suffix_name[1] == 'verify_callback':
            return response

        logger.info(request)
        # 查看 web_token 字段是否存在
        if 'web_token' not in request.headers.keys():
            data = {'message':'token 不存在', 'code':909}
            return await self.returnResponses(data)

        # 校验 jwt
        try: 
            logger.info(request.headers['web_token'])
            jwt.decode(request.headers['web_token'], key='miyao', algorithms=['HS256'])
        except Exception as e:
            logger.info(e)
            data = {'message':'无效的 token', 'code':909}
            return await self.returnResponses(data)

        return response


    # 返回 Responses
    async def returnResponses(self, data):

        # 返回值的跨域设置
        headers = {'access-control-allow-origin': '*'}
        return Response(content=json.dumps(data), headers=headers)








jwtOperation = JwtOperation()

