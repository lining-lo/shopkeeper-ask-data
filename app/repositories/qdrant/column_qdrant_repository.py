"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作Qdrant向量索引库的持久层类
        专门处理字段信息数据
"""
from qdrant_client import AsyncQdrantClient


class ColumnQdrantRepository:
    collection_name = "data-agent_column_collection"

    def __init__(self, client: AsyncQdrantClient):
        self.client = client
