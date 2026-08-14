"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc:column与metric多对多关联中间表ORM实体，映射column_metric表，存储字段和指标的绑定关系
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.mysql.base import Base


class ColumnMetricMySQL(Base):
    __tablename__ = "column_metric"

    column_id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        comment="列编号"
    )
    metric_id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        comment="指标编号"
    )
