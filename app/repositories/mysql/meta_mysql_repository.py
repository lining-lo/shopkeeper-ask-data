"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作mysql的持久层类
        专门处理meta库
"""
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
