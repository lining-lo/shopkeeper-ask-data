"""
  @Author:lining-lo
  @Time:2026/8/9
  @Desc: 协程上下文RequestID工具类，基于contextvars实现异步请求链路ID透传，
在FastAPI等异步框架中间件中设置全局追踪ID，全链路任意位置获取，请求结束重置上下文防止污染。
"""
import asyncio
from contextvars import ContextVar, Token

# 定义协程上下文变量，默认值为空字符串
_req_context_var = ContextVar("req_id", default="")


def set_request_id(request_id: str) -> Token:
    """设置当前协程请求追踪ID，返回重置用的Token令牌"""
    return _req_context_var.set(request_id)


def get_request_id() -> str:
    """获取当前协程绑定的请求ID"""
    return _req_context_var.get()


def reset_request_id(token: Token) -> None:
    """使用令牌重置协程上下文，释放当前请求数据"""
    _req_context_var.reset(token)

if __name__ == "__main__":
    async def test_req1():
        print(f"before req1 req_id={get_request_id()}")
        token = set_request_id("1111")
        await asyncio.sleep(1)
        print(f"after req1 req_id={get_request_id()}")
        await asyncio.sleep(1)
        reset_request_id(token)
        print(f"after reset req1 req_id={get_request_id()}")


    async def test_req2():
        print(f"before req2 req_id={get_request_id()}")
        token = set_request_id("2222")
        await asyncio.sleep(1)
        print(f"after req2 req_id={get_request_id()}")
        await asyncio.sleep(1)
        reset_request_id(token)
        print(f"after reset req2 req_id={get_request_id()}")


    async def test():
        await asyncio.gather(test_req1(), test_req2())

    asyncio.run(test())