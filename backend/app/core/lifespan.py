"""
  @Author:lining-lo
  @Time:2026/8/14
  @Desc:定义FastAPI生命周期事件
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import meta_mysql_client_manager, dw_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时，初始化客户端
    embedding_client_manager.init_client()
    es_client_manager.init_client()
    dw_mysql_client_manager.init_client()
    meta_mysql_client_manager.init_client()
    qdrant_client_manager.init_client()

    yield

    # 应用关闭前，释放资源
    await qdrant_client_manager.close()
    await es_client_manager.close()
    await meta_mysql_client_manager.close()
    await dw_mysql_client_manager.close()