"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc:数据表信息ORM实体，映射table_info表，记录业务库中所有数据表的名称、类型、业务说明等表级元数据
"""
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.mysql.base import Base


class TableInfoMySQL(Base):
    __tablename__ = "table_info"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        comment="表编号"
    )
    name: Mapped[str] = mapped_column(
        String(128),
        comment="表名称"
    )
    role: Mapped[str] = mapped_column(
        String(32),
        comment="表类型(fact/dim)"
    )
    description: Mapped[str] = mapped_column(
        Text,
        comment="表描述"
    )
