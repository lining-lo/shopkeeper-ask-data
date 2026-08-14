"""
  @Author:lining-lo
  @Time:2026/8/8
  @Desc:SQLAlchemy ORM 模型基础父类，所有MySQL数据表实体类的统一基类
"""
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass