import os                   #用于访问环境变量

from dotenv import load_dotenv


# 加载 .env 文件（自动读取项目根目录的 .env）
load_dotenv()

# 从系统环境变量总获取DashScope API密钥
# 确保在运行此脚本前已设置DASHSCOPE_API_KEY
DASHSCOPE_QWEN_API_KEY = os.getenv("DASHSCOPE_API_KEY")

DASHSCOPE_OPENAI_API_KEY = os.getenv("DASHSCOPE_API_KEY")

QWEN_MODEL = os.getenv("QW_LLM_MODEL_NAME")

OPENAI_MODEL = os.getenv("OPENAI_LLM_MODEL_NAME")

LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))

# ========== 服务配置 ==========
HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(os.getenv("PORT", "8000"))

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# 服务调用
SERVICE_API_URL=os.getenv("SERVICE_API_URL");