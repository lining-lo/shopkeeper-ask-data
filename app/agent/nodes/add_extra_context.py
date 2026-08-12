"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:
"""
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def add_extra_context(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "添加额外信息"})
    try:
        return {}
    except Exception as e:
        logger.error(f"添加额外信息失败：{str(e)}")
        raise