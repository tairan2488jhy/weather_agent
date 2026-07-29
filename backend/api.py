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

from fastapi import FastAPI, HTTPException
from .schemas import ChatRequest, ChatResponse
from .service import process
from config import HOST, PORT


app = FastAPI(title="Weather Agent Backend API")


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
    raise HTTPException(status_code=500, detail=str(e))
  
@app.get("/health")
async def health_check():
  """健康检查接口，用于确认服务是否正常运行"""
  return {"status": "ok"}


# --- 启动命令 ---
# 如果直接运行此文件，则启动 Uvicorn 服务器
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host=HOST, port=PORT)
