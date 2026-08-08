"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc: SQLAlchemy异步MySQL客户端管理器，封装异步引擎创建与资源释放；
         根据DBConfig生成dw、meta两套全局异步mysql数据库客户端实例
"""
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.conf.app_config import DBConfig, app_config


class MysqlClientManager:
    def __init__(self, db_config: DBConfig):
        self.config = db_config
        self.client: Optional[AsyncEngine] = None

    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}/{self.config.database}?charset=utf8mb4"

    def init_client(self):
        return create_async_engine(self._get_url())

    async def close_client(self):
        if self.client is not None:
            await self.client.dispose()


# dw数仓数据库全局客户端
dw_mysql_client_manager = MysqlClientManager(app_config.db_dw)
# meta元数据数据库全局客户端
meta_mysql_client_manager = MysqlClientManager(app_config.db_meta)
