# API接口

## 1. FastAPI 相关技术点

```
技术点1: 处理不同类型的请求
技术点2：获取不同类型的参数
技术点3：使用路由器
技术点4：SSE流式响应
技术点5：生命周期 
技术点6：中间件
技术点7：依赖注入
```

### 1.1. 处理不同类型的请求

- 常见的请求类型：GET，POST，PUT，DELETE
- 通过FastAPI的注解来定义处理不同请求类型的路由接口
  - @app.get()：定义GET类型接口
  - @app.post(): 定义POST类型接口
  - @app.put()：定义PUT类型接口
  - @app.delete(): 定义DELETE类型接口
- 区别REST API与非REST API
  - REST API：
    - 一个接口路径对应多种请求方式，不同请求方式对应的后台操作不同
      - GET：获取数据
      - DELETE：删除数据
      - POST/PUT: 添加或更新数据
    - 请求路径上不带操作名称
  - 非REST API
    - 一个接口路径只有一种请求方式，也就是只能对应一个后台操作，
    - 请求路径上一般带操作名称

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()

"""测试1: 测试不同类型的请求"""
# 注册路由接口
# 当这个路由路径被请求时，会自动调用路由函数
@app.get("/xxx")
async def test_get():
    print("处理 /xxx get的请求。。。")
    return {"get message": "Hello World2222333"}  # response：服务器端给浏览器端的响应数据

@app.post("/xxx")
async def test_post():
    print("处理 /xxx post 的请求。。。")
    return {"post message": "Hello World2222333"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

测试：

> - GET请求：http://localhost:8001/xxx
> - POST请求：http://localhost:8001/xxx

### 1.2. 获取不同类型的参数

- 3种携带文本参数的方式
  - query参数：请求路径？后面的参数，如：/xxx?name=tom&age=12
  - path参数：看似像路径，与路由路径占位对应的部分，如：路由路径：/xxx/{id}，请求：/xxx/2
  - body参数：请求体参数，一般是json格式，如：{"name": "tom", "age": 12}
- 路由函数接收3种不同的参数
  - 接收 body参数：BaseModel子类型的形参
  - 接收path参数：与路由路径中占位同名的形参
  - 接收query参数：其它形参

```python
from pydantic import BaseModel

"""
测试2：获取不同类型的参数
1. query参数: 请求路径中？后面的参数
2. param参数：路径中可变的的部分
3. body参数：json格式
"""
class MyBody(BaseModel):
    age: int
    sex: str

@app.post("/api/user/{id}")
def test_three_params(body: MyBody, id: int, name: str):
    print(f"处理多种参数的路由函数 body={body}, id={id}, name={name}")
    return {"id":id, "name":name, "age": body.age, "sex": body.sex}
```

测试：

> - POST请求：
>   - url: http://localhost:8001/api/user/12?name=tom
>   - 请求体：{"age": 12, "sex": "男"}

### 1.3. 使用路由器

- 当项目中的接口数量过多时，会根据不同的功能模块对接口进行分组管理
- 一个路由器就是一个包含多个接口的一个分组
- 在路由器中注册当前分组中的所有路由
- 将所有路由器注册到应用中

`app/api/test/main.py`

```python
from app.api.test.order_router import order_router
from app.api.test.product_router import product_router

"""
测试3：使用路由器
  操作order的有3个接口  order_router
  操作product的有4个接口  product_router
"""
# 注册路由器
app.include_router(product_router, prefix="/v1")
app.include_router(order_router, prefix="/v2")

```

`app/api/test/product_router.py`

```python
from fastapi import APIRouter

# 管理product相关路由的路由器
product_router = APIRouter()

@product_router.get("/product/{id}")
def test(id: int):
    return {"id": id, "name": "prductt abc"}
```



`app/api/test/order_router.py`

```python
from fastapi import APIRouter

# 管理order相关路由的路由器
order_router = APIRouter()

@order_router.get("/order/{id}")
def test(id: int):
    return {"id": id, "name": "order cba"}
```

测试：

> - GET请求：http://localhost:8001/v1//product/2
> - GET请求：http://localhost:8001/v2/order/3



### 1.4. SSE流式响应

- 需求：服务器端不断推送数据到浏览器端实时显示
- 技术：SSE或WebSocket，当前项目使用SSE
- 路由函数返回响应流：接受一个异步生成器，并指定媒体类型为text/event-stream
- 异步生成器函数中通过yield来指定推送给客户端的数据，数据格式：`data: 数据 \n\n`

```python
import asyncio
from starlette.responses import StreamingResponse

"""
测试4：流式响应与SSE
"""
async def fake_video_streamer():
    for i in range(10):
        yield 'data: {"name": f"Tom{i}", "age": 18} \n\n'
        await asyncio.sleep(1)

async def call_async():
    async for chunk in fake_video_streamer():
        print(chunk)

@app.get("/api/stream")
async def test_stream():
    return StreamingResponse(fake_video_streamer(), media_type="text/event-stream")

```

测试：

> - GET请求：http://localhost:8001/api/stream      看页面上是否能流式显示内容

### 1.5. 应用生命周期

- FastAPI支持在应用启动时和应用结束前执行一次特定逻辑代码
- 应用：可以在应用启动时初始化客户端管理器，在应用结束前关闭所有管理器

```python
"""
测试5：生命周期
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("应用初始时执行一次, 做一次的初始化工作")
    yield
    print("应用停止前执行一次， 做一次的收尾工作")

# 创建FastAPI的应用对象
app = FastAPI(lifespan=lifespan)

```



### 1.6. 请求中间件

- FastAPI支持在每次处理请求前和处理请求后统一插入特定逻辑代码
- 应用：可以在处理请求前保存一个唯一的请求id

```python
"""
测试6：中间件
"""
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 处理请求前执行
    print("处理请求前执行....")
    # 调用下一个中间件或目标路由，返回值是目标路由返回的响应
    response = await call_next(request)
    # 处理请求后执行
    print("处理请求后执行....")
    return response
```



### 1.7. 依赖注入

在 FastAPI 中，[依赖项](https://fastapi.org.cn/tutorial/dependencies/)（Dependencies） 是框架核心的「模块化逻辑复用机制」，本质是**可被注入、可复用、可组合的通用逻辑单元**—— 它允许你将接口中重复的非业务逻辑（如鉴权、参数校验、资源初始化）抽离成独立组件，在需要的地方通过 `Depends()` 注入使用，既避免代码冗余，又保证逻辑的一致性和可维护性

```python
"""
测试7：依赖注入(DI  Depend Inject)
"""
def get_value_es_repo():
    print("get_value_es_repo()")
    es_client_manager.init()
    return ValueESRepository(es_client_manager.client)


@app.get("/di/{id}")
def test_di(id: int, value_es_repo: ValueESRepository=Depends(get_value_es_repo)):
    print(f"处理 /di/{id} 的请求 value_es_repo={value_es_repo}")
    return {"id": id, "name": "abc"}
```

## 2. 代码组织规划

```bash
data-agent/
├─ main.py # FastAPI入口脚本
└─ app/
   ├─ api/
   │  ├─ routers/
   │  │  └─ query_router.py # 负责定义查询接口
   │  ├─ schemas/ # 请求参数和返回值结果
   │  │  └─ query_schema.py # 负责定义查询接口请求体结构
   │  └─ dependencies.py # 负责定义查询接口依赖项
   │
   ├─ services/
   │  └─ query_service.py # 负责定义查询接口核心业务逻辑
   │
   └─ core/
      ├─ lifespan.py # 负责定义FastAPI生命周期事件
```



## 3. 具体实现

### 3.1. 整和依赖项组件

**1）QueryService 实现业务**

在`data-agent/app/services/query_service.py`中编写如下代码：

```python
import json

from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.agent.context import DataAgentContext
from app.agent.graph import compiled_graph
from app.agent.state import DataAgentState
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw_mysql_repository import DWMysqlRepository
from app.repositories.mysql.meta_mysql_repository import MetaMysqlRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository


class QueryService:
    def __init__(self,
                 dw_mysql_repo: DWMysqlRepository,
                 meta_mysql_repo: MetaMysqlRepository,
                 value_es_repo: ValueESRepository,
                 column_qdrant_repo: ColumnQdrantRepository,
                 metric_qdrant_repo: MetricQdrantRepository,
                 embedding_client: HuggingFaceEndpointEmbeddings):
        self.dw_mysql_repo = dw_mysql_repo
        self.meta_mysql_repo = meta_mysql_repo
        self.value_es_repo = value_es_repo
        self.column_qdrant_repo = column_qdrant_repo
        self.metric_qdrant_repo = metric_qdrant_repo
        self.embedding_client = embedding_client

    async def search(self, query: str):
        try:
            # 创建state对象
            state = DataAgentState(query=query)
            # 创建context对象
            context = DataAgentContext(
                dw_mysql_repo=self.dw_mysql_repo,
                meta_mysql_repo=self.meta_mysql_repo,
                value_es_repo=self.value_es_repo,
                column_qdrant_repo=self.column_qdrant_repo,
                metric_qdrant_repo=self.metric_qdrant_repo,
                embedding_client=self.embedding_client
            )

            # 异步流式执行图
            async for chunk in compiled_graph.astream(
                    input=state,
                    context=context,
                    stream_mode="custom"
            ):
                """
                chunk: {"stage": "xxx"}   {"result": [{}, {}]}
                """
                # 返回给浏览器端
                yield f"data: {json.dumps(chunk, ensure_ascii=False, default=str)} \n\n"
        except Exception as e:
            # 返回错误给浏览器
            yield f"data: {json.dumps({"error": str(e)}, ensure_ascii=False, default=str)} \n\n"
```

**json.dumps**：作用是将 Python 对象（如字典、列表）转换为 JSON 格式的字符串（序列化）

参数ensure_ascii=False：保留中文、表情等非 ASCII 字符的原始形态，不转义

参数default=str：如果 `chunk` 中包含 JSON 不支持的类型（如 datetime 时间对象、自定义类实例），会自动调用 `str()` 把该对象转为字符串，避免抛出序列化异常

**2）整合依赖项**

在`data-agent/app/api/dependencies.py`中编写如下内容：

```python
from fastapi import Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw_mysql_repository import DWMysqlRepository
from app.repositories.mysql.meta_mysql_repository import MetaMysqlRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.query_service import QueryService


async def get_dw_session():
    """
        请求进来 → 进入 async with（创建 session）→ yield 暂停，把 session 交给路由函数
                                                          ↓
                                              路由函数使用 session 执行业务逻辑
                                                          ↓
        路由函数返回 → 回到 yield 后面的位置 → 退出 async with（自动关闭/归还 session）→ 请求结束
    """
    async with dw_mysql_client_manager.session_factory() as session:
        yield session # 返回session给调用，当前暂停，当 调用者执行完成回到当前yield后面执行，退出async with, 关闭session
        # return session  # 立即返回，退出async with 自动关闭session =》路由中调用的业务对象不再使用使用session了

def get_dw_mysql_repo(session: AsyncSession=Depends(get_dw_session)):
    return DWMysqlRepository(session)


async def get_meta_session():
    async with meta_mysql_client_manager.session_factory() as session:
        yield session


def get_meta_mysql_repo(session: AsyncSession = Depends(get_meta_session)):
    return MetaMysqlRepository(session)

def get_value_es_repo():
    return ValueESRepository(es_client_manager.client)

def get_column_qdrant_repo():
    return ColumnQdrantRepository(qdrant_client_manager.client)

def get_metric_qdrant_repo():
    return MetricQdrantRepository(qdrant_client_manager.client)

def get_embedding_client():
    return embedding_client_manager.client

def get_query_service(
    dw_mysql_repo: DWMysqlRepository = Depends(get_dw_mysql_repo),
    meta_mysql_repo: MetaMysqlRepository = Depends(get_meta_mysql_repo),
    value_es_repo: ValueESRepository =  Depends(get_value_es_repo),
    column_qdrant_repo: ColumnQdrantRepository =  Depends(get_column_qdrant_repo),
    metric_qdrant_repo: MetricQdrantRepository =  Depends(get_metric_qdrant_repo),
    embedding_client: HuggingFaceEndpointEmbeddings = Depends(get_embedding_client)
):
    return QueryService(
        dw_mysql_repo=dw_mysql_repo,
        meta_mysql_repo=meta_mysql_repo,
        value_es_repo=value_es_repo,
        column_qdrant_repo=column_qdrant_repo,
        metric_qdrant_repo=metric_qdrant_repo,
        embedding_client=embedding_client
    )
```



**3）接口中整合**

`data-agent/app/api/schemas/query_schema.py` 

~~~python
# 负责定义查询接口请求体结构
from pydantic import BaseModel

class QuerySchema(BaseModel):
    query: str

~~~



`data-agent/app/api/routers/query_router.py` 

~~~python
from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.api.dependencies import get_query_service
from app.api.schemas.query_schema import QuerySchema
from app.services.query_service import QueryService

# 创建查询的路由器
query_router = APIRouter()

# 注册搜索的路由
@query_router.post("/api/query")
async def search(query_schema: QuerySchema, service: QueryService=Depends(get_query_service)):

    return StreamingResponse(service.search(query_schema.query), media_type="text/event-stream")
~~~

### 3.2. 整合生命周期组件

场景： 使用[生命周期组件](https://fastapi.org.cn/advanced/events/)，应用启动前对依赖项进行初始化

`data-agent/app/core/lifespan`   

~~~python
# 负责定义FastAPI生命周期事件
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import meta_mysql_client_manager, dw_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时，初始化客户端
    embedding_client_manager.init()
    qdrant_client_manager.init()
    es_client_manager.init()
    meta_mysql_client_manager.init()
    dw_mysql_client_manager.init()

    yield

    # 应用关闭前，释放资源
    await qdrant_client_manager.close()
    await es_client_manager.close()
    await meta_mysql_client_manager.close()
    await dw_mysql_client_manager.close()
~~~

在`main.py`中编写如下内容：

```python
import uuid
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from app.api.routers.query_router import query_router
from app.core.context import set_req_id
from app.core.lifespan import lifespan


# 创建API应用，并绑定生命周期函数
app = FastAPI(lifespan=lifespan)

```

后续可在终端的main.py所在的目录直接执行`fastapi dev`命令来启动测试服务器。

### 3.3. 整合中间件组件

实现：[中间件组件](https://fastapi.org.cn/tutorial/middleware/#create-a-middleware)中定义异步函数上下文变量，用于日志处理

在`main.py`中编写如下内容：

~~~python
# 添加中间件，在每个请求中生成唯一的request_id
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # 调用路径函数之前，创建reqeust_id并保存
    set_req_id(uuid.uuid4())
    # print(f"请求开始准备执行....")
    # 调用路由函数
    response = await call_next(request)
    # print(f"请求执行完之后....")
    # 调用路由函数之后
    return response

# 添加路由器
app.include_router(query_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
~~~

## 4. 运行测试

运行: 执行main.py

测试方式一： 通过在线测试网页测试

- 访问地址： http://127.0.0.1:8000/docs

  ![image-20260617204303513](images/image-20260617204303513-17817001875021.png)

测试方式二：通过Apifox等接口测试工具进行测试，具体具体效果如下：

![image-20260312185315752](images/image-20260312185315752.png)
