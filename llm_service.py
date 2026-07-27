
from openai import OpenAI   #OPenAI 兼容API的客户端库，用于调用同意千问

from config import API_KEY, LLM_MODEL_NAME

from tools import weather_agent_tools

# 初始化OpenAI客户端，使用DashScope的兼容模式API端点
# 这个初始化步骤配置了API密钥和基础URL，使得我们可以通过标准0penAI接口调用阿里云的服务
client = OpenAI(
  api_key=API_KEY,
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def llm_chat_completions_use_tools(messages):

  # 检查API密钥是否存在，确保服务可用性
  # 如果未设置API密钥，立即返回错误提示
  if not API_KEY:
    return"错误:未设置DASHSCOPE_API_KEY环境变量，请设置后重试。"

  return client.chat.completions.create(
      model=LLM_MODEL_NAME,       #指定使用的模型名称
      messages=messages,      #传递完整的对话历史和当前消息
      tools=weather_agent_tools,           # <--- 关键点：把工具描述传给模型
      tool_choice="auto"      # 让模型自己决定要不要用工具
      # stream=False            #设置为非流式响应(一次性返回完整结果)
    )

def llm_chat_completions_no_tools(messages):
  # 检查API密钥是否存在，确保服务可用性
  # 如果未设置API密钥，立即返回错误提示
  if not API_KEY:
    return"错误:未设置DASHSCOPE_API_KEY环境变量，请设置后重试。"

  return client.chat.completions.create(
          model=LLM_MODEL_NAME,       #指定使用的模型名称
          messages=messages,      #传递完整的对话历史和当前消息
        )