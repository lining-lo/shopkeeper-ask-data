"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作mysql的持久层类
        专门处理meta库
"""
from sqlalchemy.ext.asyncio import AsyncSession


class MetaMysqlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
