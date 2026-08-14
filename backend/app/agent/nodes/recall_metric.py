"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:召回指标节点，查询qdrant向量库
"""
from app.prompt.prompt_loader import load_prompt
from app.agent.llm import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger
from app.models.qdrant.metric_info_qdrant import MetricInfoQdrant


async def recall_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "召回指标"})
    try:
        query = state["query"]
        keywords = state["keywords"]
        embedding_client = runtime.context["embedding_client"]
        metric_qdrant_repo = runtime.context["metric_qdrant_repo"]

        # 对query进行大模型语义化的分词，并与jiaba分词合并
        prompt_template = PromptTemplate(
            template=load_prompt("extend_keywords_for_metric_recall"),
            input_variables=["query"],
        )
        output_parser = JsonOutputParser()
        chain = prompt_template | llm | output_parser
        result = await chain.ainvoke({"query": query})
        logger.info(f"recall_metric llm keywords: {result}")
        keywords = list(set(keywords + result))

        # 用来保存所有召回的指标信息对象，需要去重：key: column_id
        metric_infos_dict: dict[str, MetricInfoQdrant] = {}

        # 遍历各个分词去做召回
        for keyword in keywords:
            # 将keyword转换为向量
            vector = await embedding_client.aembed_query(keyword)
            # 去查询qdrant向量库, 得到字段信息列表： list[MetricInfoQdrant]
            metric_infos: list[MetricInfoQdrant] = await metric_qdrant_repo.search(vector)
            # 对查询得到的列表数据进行去重保存
            for metric_info in metric_infos:
                metric_id = metric_info["id"]
                if metric_id not in metric_infos_dict:
                    metric_infos_dict[metric_id] = metric_info

        # 生成目标数据结构
        recall_metrics: list[MetricInfoQdrant] = list(metric_infos_dict.values())
        logger.info(f"召回指标完成：{recall_metrics}")

        # 返回字段信息列表： list[MetricInfoQdrant]
        return {"recall_metrics": recall_metrics}
    except Exception as e:
        logger.error(f"召回指标失败：{str(e)}")
        raise