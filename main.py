'''
@Description:
@Author: michael
@Date: 2021-07-08 10:16:20
LastEditTime: 2021-07-08 20:00:00
LastEditors: michael
'''

# coding=utf-8
# import sys
# import time

# import uvicorn
from fastapi import FastAPI
from routers import User
from routers import Fund
from routers import ReferenceCall

from starlette.middleware.cors import CORSMiddleware

# from views.JwtOperation import jwtOperation

app = FastAPI()

# 设置允许的origins来源
origins = [
    "http://localhost:8080",
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的origins来源
    # allow_origins=origins,  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"],
    expose_headers=["*"]
)

# True 开启 Jwt 验证，False 关闭 Jwt 认证
# is_verify_jwt = True

# if is_verify_jwt:

#     # 全局校验token中间件
#     @app.middleware("http")
#     async def add_process_token_header(request: Request, call_next):
#         print('中间件------------')
#         tmp_result = await jwtOperation.verifyJwt(request, call_next)
#         print(tmp_result.__dict__)
#         return tmp_result



# 用户路由
app.include_router(User.router)

# 基金路由
app.include_router(Fund.router)

# Reference Call 路由
app.include_router(ReferenceCall.router)
