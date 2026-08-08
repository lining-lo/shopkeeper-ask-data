"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc: SQLAlchemy异步MySQL客户端管理器，封装异步引擎创建与资源释放；
         根据DBConfig生成dw、meta两套全局异步mysql数据库客户端实例
"""
import asyncio
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from app.conf.app_config import DBConfig, app_config


class MysqlClientManager:
    def __init__(self, config: DBConfig):
        self.config = config
        self.client: Optional[AsyncEngine] = None  # AsyncEngine|None

    # 获取连接字符串
    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}/{self.config.database}?charset=utf8mb4"

    # 初始化
    def init(self):
        # 创建一个异步引擎
        self.client = create_async_engine(
            self._get_url()
        )

    # 释放资源
    async def close(self):
        await self.client.dispose()


# 创建操作dw库的客户端管理器
dw_mysql_client_manager = MysqlClientManager(app_config.db_dw)
# 创建操作meta库的客户端管理器
meta_mysql_client_manager = MysqlClientManager(app_config.db_meta)

if __name__  == "__main__":
    async def test():
        # 初始化dw客户端对象
        dw_mysql_client_manager.init()

        # 创建异步会话
        async with AsyncSession(dw_mysql_client_manager.client) as session:
            # 执行查询sql
            sql = "select * from dim_customer limit 2"
            result = await session.execute(text(sql))

            # 读取数据
            """
            result.all()    返回 [row, row, row]  row是可迭代的对象
            result.mappings().all() 返回 [rowMapping, rowMapping, rowMapping]  rowMapping是包含一行数据的字段名和字段值的对象
            result.scalars().all() 所回 [val, val, val]  val是第一列值
            """

            # rows = result.all()  # 返回 [row, row, row]   row是可迭代的对象
            # for row in rows:
            #     for val in row:
            #         print(val)

            # rows = result.mappings().all() # 返回 [rowMapping, rowMapping, rowMapping]  rowMapping是包含一行数据的字段名和字段值的对象
            # for row in rows:
            #     for key, val in row.items():
            #         print(key, val)

            rows = result.scalars().all()  # 所回 [val, val, val]  val是第一列值
            for row in rows:
                print(row)

        # 释放资源
        await dw_mysql_client_manager.close()

    asyncio.run(test())