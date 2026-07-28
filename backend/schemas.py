# backend/schemas.py

"""
# 数据模型定义层 Data Contract
## 核心职责： 定义系统之间传递的数据格式。 
类似：

Java DTO
TypeScript Interface


"""

from pydantic import BaseModel, Field
from typing import Optional

# ======== 请求模型（Request）========

class ChatRequest(BaseModel):
  """
  前端 -> 后端的请求数据格式
  这是系统之间的“数据契约”，任何调用方法都必须遵守
  """
  message: str = Field(..., description="用户输入的消息", min_length=1)
  session_id: Optional[str] = Field(None, description="会话ID，用于多轮对话上下文关联")

# ======== 响应模型（Response）========

class ChatResponse(BaseModel):
  """
  后端 -> 前端的响应数据格式
  """
  reply: str = Field(..., description="Agent 的回复内容")
  session_id: Optional[str] = Field(None, description="当前会话ID")

# ======== 内部传递模型 (Internal) ========
# 如果未来 service -> agent 之间需要更复杂的数据结构，也可以在这里定义
# 例如：

class AgentContext(BaseModel):
  """
  Service -> Agent 的内部上下文
  前端不感知，仅后端内部使用
  """

  session_id: Optional[str] = None
  history: list = Field(default_factory=list, description="历史对话记录")