import os                   #用于访问环境变量
# 从系统环境变量总获取DashScope API密钥
# 确保在运行此脚本前已设置DASHSCOPE_API_KEY
DASHSCOPE_QWEN_API_KEY = os.getenv("DASHSCOPE_API_KEY")

DASHSCOPE_OPENAI_API_KEY = os.getenv("DASHSCOPE_API_KEY")

QWEN_MODEL = "qwen3.7-max-2026-05-20"

OPENAI_MODEL = "使用时候再配置"