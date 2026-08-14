"""
  @Author:lining-lo
  @Time:2026/8/14
  @Desc:负责定义查询接口请求体结构
"""
from pydantic import BaseModel


class QuerySchema(BaseModel):
    query: str


