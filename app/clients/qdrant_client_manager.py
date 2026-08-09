"""
  @Author:lining-lo
  @Time:2026/8/9
  @Desc: Qdrant向量数据库客户端管理器
"""
import asyncio
import random
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import models
from app.conf.app_config import app_config, QdrantConfig


class QdrantClientManager:
    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client: Optional[AsyncQdrantClient] = None

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init_client(self):
        self.client = AsyncQdrantClient(self._get_url())

    async def close(self):
        await self.client.close()


# 创建向量数据库客户端管理器
qdrant_client_manager = QdrantClientManager(app_config.qdrant)

if __name__ == "__main__":
    async def test():
        collection_name = "test_collection"
        # 初始化客户端对象
        qdrant_client_manager.init_client()
        client = qdrant_client_manager.client

        # 创建集合, 如果集合已存在，先删除集合再创建
        if await client.collection_exists(collection_name):
            await client.delete_collection(collection_name)
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=10, distance=models.Distance.COSINE),
        )

        # 插入向量
        await client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=i,  # 标识id
                    payload={
                        "color": "red" if i % 2 == 0 else "blue",
                    },
                    # 生成10维随机向量
                    vector=[random.random() for _ in range(10)],
                )
                for i in range(100)  # 创建100个向量
            ],
        )

        # 搜索向量： 查找最相似的10个向量
        result = await client.query_points(
            collection_name=collection_name,
            query=[random.random() for _ in range(10)],  # 生成一个10维随机向量 用于查询
            limit=9,  # 返回的最相似的9个向量
            # query_filter=models.Filter(
            #     must=[models.FieldCondition(key="color", match=models.MatchValue(value="red"))]
            # ),
            score_threshold=0.9  # 向量相似度阈值，低于该阈值的向量将被忽略
        )

        print(result.points)
        print(len(result.points))

        for point in result.points:
            print(f"reload={point.payload}")

        # 释放资源
        await qdrant_client_manager.close()


    asyncio.run(test())
