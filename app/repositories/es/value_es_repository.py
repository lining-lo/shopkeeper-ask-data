"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作ES全文索引库的持久层类
"""
from app.clients.es_client_manager import ESClientManager


class ValueESRepository:
    def __init__(self, client: ESClientManager):
        self.client = client
