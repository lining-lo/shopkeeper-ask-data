"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作Qdrant向量索引库的持久层类
        专门处理字段信息数据
"""
from typing import List

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import models
from app.conf.app_config import app_config
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant


class ColumnQdrantRepository:
    collection_name = "data-agent_column_collection"

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def _ensure_collection(self):
        """确保集合存在：如果存在，先删除，后面创建"""
        client = self.client
        collection_name = self.collection_name

        if await client.collection_exists(collection_name=collection_name):
            await client.delete_collection(collection_name=collection_name)

        await client.create_collection(
            collection_name=collection_name,  # 集合名称
            vectors_config=models.VectorParams(
                size=app_config.qdrant.embedding_size,  # 向量的维度
                distance=models.Distance.COSINE  # 余弦相似匹配
            ),
        )

    async def upsert_column_vectors(self, vectors: list[list[float]],
                                    payloads: list[ColumnInfoQdrant], ids: list[str]):
        """
        批量新增/更新字段向量数据到Qdrant向量库
        多个向量的数组：vectors: list[list[float]]
        多个payload的数组：payloads: list[包含字段信息的dict]
        多个向量对应的id: ids: list[str]
        """
        client = self.client
        collection_name = self.collection_name

        # 创建集合, 如果集合已存在，先删除集合再创建
        await self._ensure_collection()

        # 分批次插入向量
        batch_size = 10
        for i in range(0, len(vectors), batch_size):
            # 得到当前批次的数据
            batch_vectors = vectors[i:i + batch_size]
            batch_payloads = payloads[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            # 批量插入当前批次的向量数据
            await client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=batch_ids[j],
                        payload=batch_payloads[j],
                        vector=batch_vectors[j],
                    )
                    for j in range(len(batch_ids))
                ],
            )

    async def search(self, keyword_vector: List[float]) -> list[ColumnInfoQdrant]:
        client = self.client

        # 搜索向量
        result = await client.query_points(
            collection_name=self.collection_name,
            query=keyword_vector,
            score_threshold=0.6  # 向量相似度阈值，低于该阈值的向量将被忽略
        )

        return [ColumnInfoQdrant(**point.payload) for point in result.points]
