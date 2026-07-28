# llm/base.py
# 抽象基类-定义接口规范

from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
  """
  LLM 客户端抽象类。
  所有 LLM 适配器都必须继承此类，并实现一下两个方法。
  """

  @abstractmethod
  def chat_completion(self, messages: list, model: str) -> str:
    """
    普通对话（无工具调用）

    :param message: OpenAI 格式的消息列表
    :param model: 模型名称
    :return: 模型的文本回复
    """
    pass

  @abstractmethod
  def chat_completion_with_tools(self, messages: list, tools: list, model: str) -> str:
    """
    带工具调用的对话


    :param messages: OpenAI 格式的消息列表
    :param tools: 工具定义列表（OpenAI function calling 格式）
    :param model: 模型名称
    :return: 模型的原始响应（dict），包含 tool_calls 等信息
    """
    pass
