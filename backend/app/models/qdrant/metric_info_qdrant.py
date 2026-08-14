"""
  @Author:lining-lo
  @Time:2026/8/11
  @Desc:Qdrant向量库的列元数据Payload字典结构，做静态类型约束
"""
from typing import TypedDict

class MetricInfoQdrant(TypedDict):
    id:str
    name:str
    description:str
    relevant_columns:list
    alias:list
