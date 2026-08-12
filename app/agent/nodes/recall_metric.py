"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:
"""
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def recall_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "召回指标"})
    try:
        return {}
    except Exception as e:
        logger.error(f"召回指标失败：{str(e)}")
        raise