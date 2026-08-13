"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作mysql的持久层类
        专门处理meta库
"""
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mysql.column_info_mysql import ColumnInfoMySQL
from app.models.mysql.column_metric_mysql import ColumnMetricMySQL
from app.models.mysql.metric_info_mysql import MetricInfoMySQL
from app.models.mysql.table_info_mysql import TableInfoMySQL


class MetaMysqlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def save_table_infos(self, table_infos: list[TableInfoMySQL]):
        """向table_info表中插入多条数据"""
        self.session.add_all(table_infos)

    def save_column_infos(self, column_infos: list[ColumnInfoMySQL]):
        """向column_info表中插入多条数据"""
        self.session.add_all(column_infos)

    def save_metric_infos(self, metric_infos: list[MetricInfoMySQL]):
        """向metric_info表中插入多条数据"""
        self.session.add_all(metric_infos)

    def save_column_metrics(self, column_metrics: list[ColumnMetricMySQL]):
        """向column_metric表中插入多条数据"""
        self.session.add_all(column_metrics)

    async def get_column_info_by_id(self, column_id: str) -> ColumnInfoMySQL:
        """根据column_id查询colun_info表"""
        return await self.session.get(ColumnInfoMySQL, column_id)

    async def get_key_column_infos_by_table_id(self, table_id: str) -> list[ColumnInfoMySQL]:
        """根据key和table_id查询colun_info表"""
        result = await self.session.execute(
            Select(ColumnInfoMySQL)
            .where(ColumnInfoMySQL.table_id == table_id)
            .where(ColumnInfoMySQL.role.in_(["primary_key", "foreign_key"]))
        )
        return result.scalars().all()

    async def get_table_info_by_table_id(self, table_id: str) -> TableInfoMySQL:
        """根据table_id查询table_info表"""
        return await self.session.get(TableInfoMySQL, table_id)
