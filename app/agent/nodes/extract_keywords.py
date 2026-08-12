"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:
"""
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


def extract_keywords(state: DataAgentState, runtime: Runtime[DataAgentContext]) -> dict:
    runtime.stream_writer({"stage": "提取关键字"})
    try:
        return {}
    except Exception as e:
        logger.error(f"提取关键字失败：{str(e)}")
        raise
