# backend/api.py

"""
API 接口层（Controller Layer）

#核心职责 对外暴露 HTTP API，负责协议转换

## 负责：① 定义 API Endpoint 如： POST /chat

不负责：
❌ Agent逻辑

❌ Tool调用

❌ Prompt构造

❌ LLM调用

"""

from fastapi import FastAPI, HTTPException, Request
from .schemas import ChatRequest, ChatResponse
from .service import process
from config import HOST, PORT
from logger import logger # 新增导入


app = FastAPI(title="Weather Agent Backend API")


# --- 中间件：记录所有 HTTP 请求 ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 请求进来时
    logger.info(f"API 请求: {request.method} {request.url.path}")
    # 处理请求
    response = await call_next(request)
    # 响应出去时
    logger.info(f"API 响应: {request.method} {request.url.path} - 状态码: {response.status_code}")
    return response



# --- 定义 API 路由 ---

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
  """
  API 接口层 (Controller Layer)

  职责：
  1. 定义 API Endpoint (POST /chat)
  2. 接收并校验请求数据（通过 Pydantic 模型）
  3. 调用业务层 (service.process)
  4. 包装并返回响应数据 
  """

  try:

   

    # 3. 调用业务层
    # 将请求体中的数据传递给 service 层的 process 函数
    reply = process(message=request.message, session_id=request.session_id)

    # 4. 包装并返回响应
    return ChatResponse(reply= reply, session_id=request.session_id) 

  except Exception as e:
    # --- 使用 logger 记录错误 ---
    logger.error(f"处理 /chat 请求时发生异常: {e}", exc_info=True) # exc_info=True 会记录完整的堆栈跟踪
    raise HTTPException(status_code=500, detail=str(e))
  
@app.get("/health")
async def health_check():
  """健康检查接口，用于确认服务是否正常运行"""
  return {"status": "ok"}


# --- 启动命令 ---
# 如果直接运行此文件，则启动 Uvicorn 服务器
if __name__ == "__main__":
  import uvicorn
  # 注意：uvicorn 有自己的日志系统，这里我们只配置我们应用的日志
  logger.info(f"启动服务: http://{HOST}:{PORT}")
  uvicorn.run(app, host=HOST, port=PORT)
