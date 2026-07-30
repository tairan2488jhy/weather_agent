# llm/openai_client.py

from openai import OpenAI
from .base import BaseLLMClient
from config import OPENAI_MODEL, DASHSCOPE_OPENAI_API_KEY


class OpenAIClient(BaseLLMClient):
    """
    OpenAI 适配器
    未来切换模型时，只需实例化此类即可
    """

    def __init__(self, base_url: str = None):
        self.client = OpenAI(
            api_key=DASHSCOPE_OPENAI_API_KEY,
            base_url=base_url  # 如果不传，默认使用 OpenAI 官方地址
        )

    def chat_completion(self, messages: list, model: str) -> str:
        response = self.client.chat.completions.create(
            model=model or OPENAI_MODEL,
            messages=messages
        )
        return response.choices[0].message.content

    def chat_completion_with_tools(self, messages: list, tools: list, model: str) -> dict:
        response = self.client.chat.completions.create(
            model=model or OPENAI_MODEL,
            messages=messages,
            tools=tools
        )
        return response
    
    def chat_completion_stream(self, messages: list, model: str) -> str:
        response = self.client.chat.completions.create(
            model=model or OPENAI_MODEL,
            messages=messages,
            stream=True
        )
        return response.choices[0].message.content