
# 导入必要的库
import gradio as gr         #Gradio库 用于创建Web界面
import requests
import uuid
from config import SERVICE_API_URL

# =========== 配置 ==========
API_URL = SERVICE_API_URL

# 当前浏览器会话生成唯一 ID, 保证多轮对话上下文连续
SESSION_ID = str(uuid.uuid4())


# ======== 核心函数 ========
def chat_with_api(message: str, history: list) -> str:
  """
  通过 HTTP 请求调用后端 API
  - message: 用户当前输入
  - history: Gradio 自动传入的对话历史（仅用于界面展示，后端自己管理真实历史）
  """
  try:
    response = requests.post(
      API_URL,
      json={
        "message": message,
        "session_id": SESSION_ID
      },
      timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data["reply"]
  except requests.exceptions.ConnectionError:
    return "❌ 无法连接到后端服务，请确认已执行： uvicorn backend.api:app --reload"
  except requests.exceptions.Timeout:
    return "❌ 请求超时，Agent 处理时间过长"
  except Exception as e:
    return f"❌ 请求失败：{str(e)}"

# 如果未设置API密钥，提供油耗的错误提示
#if not api_key:
  
#使用ChatInterface组件，这是Gradio提供的专门用于创建聊天界面的组件
demo = gr.ChatInterface(
  fn = chat_with_api,                                 # 指定处理聊天消息的回调函数，将调用通义千问API
  title = "🌤️ 天气 Agent",                             # 界面标题
  description="通过 API 调用后端天气 Agent（Gradio 前端 → FastAPI 后端）",        # 界面描述
  examples=[
    ["北京天气怎么样"],
    ["上海今天下雨吗"],
    ["杭州明天多少度"]
  ]
)


#主程序入口点
#当直接运行此脚本时，启动GradioWeb服务器
if __name__ == "__main__":
  # 启动Gradio服务，默认监听本地7860端口
  # 用户访问该URL即可与通义千问Turbo模型进行交互
  demo.launch(theme=gr.themes.Soft())













# gradio version 1

# import gradio as gr

# def reverse_test(text):
#   return text[::-1]

# def helloByName(name):
#   return "你好，"+name

# demo = gr.Interface(
#   fn=helloByName,
#   inputs="text",
#   outputs="text"
# )

# # demo.launch()

# ## 函数例子2

# def reverse_and_count(text):
#   reversed_text = text[::-1]
#   length = len(text)
#   return reversed_text, length


# demo1 = gr.Interface(
#   fn=reverse_and_count,
#   inputs="text",
#   outputs= ["text", "number"],
#   title="文本处理工具",
#   description="输入一段文字返回倒叙文字及字符数量",
#   examples=[["Hello LLM"], ["Hello Dankjhy"]]
#   )

# demo1.launch()

