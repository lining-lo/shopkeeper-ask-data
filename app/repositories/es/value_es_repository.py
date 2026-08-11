"""
  @Author:lining-lo
  @Time:2026/8/10
  @Desc:操作ES全文索引库的持久层类
"""
from app.clients.es_client_manager import ESClientManager
from app.models.es.value_info_es import ValueInfoES


class ValueESRepository:
    index_name = "data-agent-value_index"

    def __init__(self, client: ESClientManager):
        self.client = client

    async def _ensure_index(self):
        """确保索引存在"""
        index_name = self.index_name
        client = self.client

        if await client.indices.exists(index=index_name):
            await client.indices.delete(index=index_name)
        await client.indices.create(
            index=index_name,
            mappings={
                "dynamic": False,
                "properties": {
                    "id": {"type": "keyword"},
                    "value": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"},
                    "type": {"type": "keyword"},
                    "column_id": {"type": "keyword"},
                    "column_name": {"type": "keyword"},
                    "table_id": {"type": "keyword"},
                    "table_name": {"type": "keyword"},
                }
            }
        )

    async def insert_values(self, values: list[ValueInfoES]):
        """批量插入多个字段值信息数据"""
        index_name = self.index_name
        client = self.client

        # 确保索引存在
        await self._ensure_index()

        index_dict = {
            "index": {
                "_index": self.index_name
            }
        }

        # 将要保存的数据全部收集到operations中
        operations = []
        for value in values:
            operations.append(index_dict)
            operations.append(value)

        # 批量插入多个字段值信息数据
        batch_size = 10
        for i in range(0, len(operations), batch_size):
            # 得到当前批次的operations
            batch_operations = operations[i:i + batch_size]
            # 批量插入当前批次的数据
            await self.client.bulk(operations=batch_operations)
