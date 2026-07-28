# 对外暴漏统一接口
# llm/__init__.py

from .base import BaseLLMClient
from .qwen_client import QwenClient
from .openai_client import OpenAIClient

def create_llm_client(provider: str="qwen") -> BaseLLMClient:
  """
  工厂函数，根据 provider 名称创建对应的 LLM 客户端


  :param provider: "qwen" | "openai" | 未来扩展更多
  :return: BaseLLMClient 的实例
  """

  providers = {
    "qwen": QwenClient,
    "openai": OpenAIClient
  }

  client_class = providers.get(provider.lower())
  if not client_class:
    raise ValueError(f"不支持的 LLM 供应商：{ provider }, 当前支持： {list(providers.keys)}")
  
  return client_class()