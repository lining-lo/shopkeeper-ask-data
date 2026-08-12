"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:召回字段节点，查询qdrant向量库
"""
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant


async def recall_column(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "召回字段"})
    try:
        keywords = state["keywords"]
        embedding_client = runtime.context["embedding_client"]
        column_qdrant_repository = runtime.context["column_qdrant_repo"]

        # 用来保存所有召回的字段信息对象，需要去重：key: column_id
        column_infos_dict: dict[str, ColumnInfoQdrant] = {}

        # 遍历各个分词去做召回
        for keyword in keywords:
            # 将keyword转换为向量
            vector = await embedding_client.aembed_query(keyword)
            # 去查询qdrant向量库, 得到字段信息列表： list[ColumnInfoQdrant]
            column_infos: list[ColumnInfoQdrant] = await column_qdrant_repository.search(vector)
            # 对查询得到的列表数据进行去重保存
            for column_info in column_infos:
                column_id = column_info["id"]
                if column_id not in column_infos_dict:
                    column_infos_dict[column_id] = column_info

        # 生成目标数据结构
        recall_columns: list[ColumnInfoQdrant] = list(column_infos_dict.values())
        logger.info(f"召回字段完成：{recall_columns}")

        # 返回字段信息列表： list[ColumnInfoQdrant]
        return {"recall_columns": recall_columns}

    except Exception as e:
        logger.error(f"召回字段失败：{str(e)}")
        raise
