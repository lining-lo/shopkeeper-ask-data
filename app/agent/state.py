"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:
"""
from typing import TypedDict

# Agent总结状态封装实体
class DataAgentState(TypedDict):
    query: str # 用户的查询
    keywords: list[str] # 提取关键字列表
    sql: str # 生成的SQL
    error: str # 错误信息,根据state中是否存在错误信息，可以进行流程执行