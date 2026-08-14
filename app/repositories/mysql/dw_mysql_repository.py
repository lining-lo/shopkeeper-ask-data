"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作mysql的持久层类
        专门处理dw库
"""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DWMysqlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_column_types(self, table_name: str) -> dict[str, str]:
        """获取当前表的所有字段的类型"""
        # 定义查询sql
        sql = f"show columns from {table_name}"
        # 执行sql
        result = await self.session.execute(text(sql))
        # 整理数据并返回
        return {row.Field: row.Type for row in result.all()}

    async def get_column_values(self, table_name: str, column_name: str, limit: int = 10) -> list:
        """查询指定字段的前limit个字段值"""
        # 定义查询sql
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        # 执行sql
        result = await self.session.execute(text(sql))
        # 整理数据并返回
        return result.scalars().all()

    async def get_db_infos(self):
        """查询数据库相关信息"""
        result = await self.session.execute(text("select version()"))
        version = result.scalar()
        dialect = self.session.bind.dialect.name
        return {"version": version, "dialect": dialect}
