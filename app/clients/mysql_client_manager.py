"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc: SQLAlchemy异步MySQL客户端管理器，封装异步引擎创建与资源释放；
         根据DBConfig生成dw、meta两套全局异步mysql数据库客户端实例
"""
import asyncio
from typing import Optional

from sqlalchemy import text, Select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from app.conf.app_config import DBConfig, app_config
from app.models.mysql.table_info_mysql import TableInfoMySQL


class MysqlClientManager:
    def __init__(self, config: DBConfig):
        self.config = config
        self.client: Optional[AsyncEngine] = None  # AsyncEngine|None
        self.session_factory: Optional[async_sessionmaker] = None

    # 获取连接字符串
    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}/{self.config.database}?charset=utf8mb4"

    # 初始化
    def init(self):
        # 创建一个异步引擎
        self.client = create_async_engine(
            self._get_url(),
            pool_size=10,  # 内部连接池中缓存的长久连接数   默认是5
            max_overflow=5,  # 最大临时连接数， 默认是10
        )
        # 创建一个异步会话工厂
        self.session_factory = async_sessionmaker(
            self.client,
            autoflush=False,  # 查询看不到前面未提交的修改
            autobegin=True,  # 自动开启事务
        )

    # 释放资源
    async def close(self):
        await self.client.dispose()


# 创建操作dw库的客户端管理器
dw_mysql_client_manager = MysqlClientManager(app_config.db_dw)
# 创建操作meta库的客户端管理器
meta_mysql_client_manager = MysqlClientManager(app_config.db_meta)

if __name__ == "__main__":
    async def test():
        # 初始化dw客户端对象
        dw_mysql_client_manager.init()

        # 创建异步会话
        async with dw_mysql_client_manager.session_factory() as session:
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


    # 测试orm的添加和查询
    async def test_orm():
        # 初始化meta客户端对象
        meta_mysql_client_manager.init()

        # 创建异步会话
        async with meta_mysql_client_manager.session_factory() as session:
            # 添加一条数据
            info1 = TableInfoMySQL(
                id="dim_customer1",
                name="dim_customer1",
                role="dim",
                description="客户信息维度表1"
            )
            session.add(info1)
            # 再添加一条数据
            info2 = TableInfoMySQL(
                id="dim_customer2",
                name="dim_customer2",
                role="dim",
                description="客户信息维度表2"
            )
            session.add(info2)

            # 提交事务
            await session.commit()

            # 查询一条数据
            table_info = await session.get(TableInfoMySQL, "dim_customer1")
            print(table_info.description)

            # 查询多条数据
            # result = await session.execute(Select(TableInfoMySQL).limit(2))
            result = await session.execute(
                Select(TableInfoMySQL).from_statement(text("select * from table_info limit 2")))
            rows: list[TableInfoMySQL] = result.scalars().all()
            print(rows)
            print(rows[0].description)

            # 看是否可以在提交事务后读取ORM对象的属性
            # print(info1.name)

        # 释放资源
        await meta_mysql_client_manager.close()


    # 测试ORM的更新和删除
    async def test_orm2():
        # 初始化meta客户端对象
        meta_mysql_client_manager.init()

        # 创建异步会话
        async with meta_mysql_client_manager.session_factory() as session:
            # 查询一条数据
            table_info = await session.get(TableInfoMySQL, "dim_customer1")
            print(table_info.description)

            # 修改一条数据
            table_info.description = "xxxx"

            # 删除一条数据
            await session.delete(table_info)

            # 提交事务
            await session.commit()

        # 释放资源
        await meta_mysql_client_manager.close()


    # asyncio.run(test())
    # asyncio.run(test_orm())
    asyncio.run(test_orm2())
