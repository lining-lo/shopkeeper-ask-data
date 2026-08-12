"""
  @Author:lining-lo
  @Time:2026/8/12
  @Desc:初始化全局LLM实例
"""
import os
from langchain.chat_models import init_chat_model
from app.conf.app_config import app_config

llm = init_chat_model(
    model=app_config.llm.model_name,
    api_key= os.getenv("DEEPSEEK_API_KEY"),
    # base_url="",
    temperature=0 # 让大型处理的结果稳定，不要创意
)

if __name__ == '__main__':
    for chunk in llm.stream("你是什么模型？"):
        print(chunk.text, end="", flush=True)