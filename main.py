"""
  @Author:lining-lo
  @Time:2026/8/14
  @Desc:程序入口
"""
import uuid
import uvicorn
from fastapi import FastAPI,Request
from app.api.routers.query_router import query_router
from app.core.context import set_request_id
from app.core.lifespan import lifespan

# 创建API应用，并绑定生命周期函数
app = FastAPI(lifespan=lifespan)

# 添加路由器
app.include_router(query_router)


# 添加中间件，在每个请求中生成唯一的request_id
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # 调用路径函数之前，创建reqeust_id并保存
    set_request_id(uuid.uuid4())
    # 调用路由函数
    response = await call_next(request)
    # 调用路由函数之后
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
