"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:过滤表节点，调用LLM智能过滤数据表与字段，精简元数据
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime
from pydantic_settings.sources.providers.yaml import yaml

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "过滤表"})
    try:
        query = state["query"]
        table_infos = state["table_infos"]

        # 1. 调用模型，过滤掉不需要表和字段  --> {表名1：[字段名1， 字段名2]}
        prompt_template = PromptTemplate(
            template=load_prompt("filter_table_info"),
            input_variables=["query", "table_infos"],
        )
        output_parser = JsonOutputParser()
        chain = prompt_template | llm | output_parser
        result = await chain.ainvoke({
            "query": query,
            "table_infos": yaml.dump(
                table_infos,
                allow_unicode=True,  # 保留中文原文，不转换为unicode编码  ‘\u5317\u4eac’
                sort_keys=False,  # 不要对数据中的字典中的属性进行排序，保持原来的顺序
            )
        })

        # 2. 去对table_infos中的表和字段进行过滤
        for table_info in table_infos[:]:
            table_name = table_info["name"]
            if table_name not in result:
                table_infos.remove(table_info)
            else:
                columns = table_info["columns"]
                for column in columns[:]:
                    column_name = column["name"]
                    if column_name not in result[table_name]:
                        columns.remove(column)

        logger.info(f"过滤表完成：{table_infos}")

        return {"table_infos": table_infos}

    except Exception as e:
        logger.error(f"过滤表失败：{str(e)}")
        raise