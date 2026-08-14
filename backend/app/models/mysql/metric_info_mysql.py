"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc:业务指标信息ORM实体，映射metric_info表，统一管理系统所有统计指标的配置与描述信息
"""
from sqlalchemy import String, Text
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.mysql.base import Base


class MetricInfoMySQL(Base):
    __tablename__ = "metric_info"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        comment="指标编码"
    )
    name: Mapped[str | None] = mapped_column(
        String(128),
        comment="指标名称"
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        comment="指标描述"
    )
    relevant_columns: Mapped[dict | list | None] = mapped_column(
        JSON,
        comment="关联字段"
    )
    alias: Mapped[dict | list | None] = mapped_column(
        JSON,
        comment="指标别名"
    )
