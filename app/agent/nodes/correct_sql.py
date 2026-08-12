"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:
"""
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def correct_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "校正sql"})
    try:
        return {}
    except Exception as e:
        logger.error(f"校验SQL失败：{str(e)}")
        raise
