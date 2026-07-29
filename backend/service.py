# backend/service.py\
from typing import Optional, Dict, Any
from agent import run_agent
from .schemas import AgentContext
from logger import logger # 新增导入

# 简单的内存会话存储，用于演示。生产环境建议使用Redis。

_session_store: Dict[str, list] = {}

def process(message: str, session_id: Optional[str] = None) -> str:
  """
  业务处理核心函数。


  职责：
  1. 接收请求参数（message, session_id）
  2. 准备上下文（从 _session_store 中获取历史对话）
  3. 调用核心 Agent 逻辑（agent.run_agent）
  4. 更新上下文（将本轮对话存入 _session_store）
  5. 返回结果
  """

  # --- 记录业务请求 ---
  logger.info(f"业务层收到请求 - Session: {session_id}, 消息: '{message}'")

  # 1. & 2. 准备上下文（Prepare Context）
  # 如果 session_id 不存在, 则初始化为空列表
  history = _session_store.get(session_id, [])
  context = AgentContext(session_id=session_id, history=history)


  # 3. 调用 Agent（Call Agent）
  # 将当前的 message 和 history 传递给核心的 agent 逻辑
  # 注意： 这里假设 agent.run_agent 能够正确处理 history 并返回最终的文本回复
  reply = run_agent(message, context.history)

  # 4. 更新上下文（Update Context）
  # 将本轮对话（用户提问和AI回复）追加到历史记录中
  # 注意：你的 agent.run_agent 内部可能已经处理了 history 的更新
  # 如果没有，你需要在这里手动更新 _session_store
  # 为了简化，我们假设 run_agent 只返回结果，不负责更新外部状态
  if session_id:
    # 将本轮对话记录下来，以便下次使用
    # 这里的格式需要和你的 agent.py 中解析 history 的格式保持一致
    new_history = history + [
      {"role": "user", "content": message},
      {"role": "assistant", "content": reply},
    ]
    _session_store[session_id] = new_history

  # --- 记录业务响应 ---
  logger.info(f"业务层处理完成 - Session: {session_id}")

  # 5. 返回结果
  return reply



