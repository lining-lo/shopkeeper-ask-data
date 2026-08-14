"""
  @Author:lining-lo
  @Time:2026/8/11
  @Desc:Qdrant向量库的列元数据Payload字典结构，做静态类型约束
"""
from typing import TypedDict

class ColumnInfoQdrant(TypedDict):
    id:str
    name:str
    type:str
    role:str
    examples:list
    description:str
    alias:list
    table_id:str