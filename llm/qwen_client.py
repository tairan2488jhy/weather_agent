# llm/qwen_client.py


from openai import OpenAI
from .base import BaseLLMClient
from config import DASHSCOPE_QWEN_API_KEY, QWEN_MODEL

class QwenClient(BaseLLMClient):
  """
  通义千问适配器
  通过 DashScope 的 OpenAI 兼容接口调用 Qwen 模型
  """

  def __init__(self):
    self.client = OpenAI(
      api_key=DASHSCOPE_QWEN_API_KEY,
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

  def chat_completion(self, messages, model):
    model = model or QWEN_MODEL
    response = self.client.chat.completions.create(
      model=model,
      messages=messages
    )

    return response
  
  def chat_completion_with_tools(self, messages, tools, model):
    model = model or QWEN_MODEL
    response = self.client.chat.completions.create(
      model=model,
      messages=messages,
      tools=tools
    )
    
    # 返回原始响应对象， agent.py 从中提取信息
    return response

    