# -*- coding: utf-8 -*-
"""

- openai:用于调用兼容0penAI格式的API
- os:用于读取环境变量

环境变量要求:
      - DASHSCOPE_API_KEY:阿里云DashScope平台的API密钥，用于身份验证和模型访问

使用方法:
    1.设置环境变量:set DASHSCOPE_API_KEY=您的API密钥
    2.运行脚本:python GradioDemo.py
    3.在浏览器中访问:http://127.0.0.1:7860

使用示例:
```bash
#在Windows上设置环境变量
set DASHSCOPE_API_KEY=your_actual_api_key

#在Linux/Mac上设置环境变量   
export DASHSCOPE_API_KEY=your_actual_api_key

 #运行应用程序
python llm.py 
```

注意事项:
1.API密钥安全:DASHSCOPE APIKEY是敏感信息，请不要交到版本控制系统


py -3 --version

py -3 -m venv .venv 创建虚拟环境

.venv\Scripts\activate     激活虚拟环境

"""

# 导入必要的库
import gradio as gr         #Gradio库 用于创建Web界面
from main import backendService


# 如果未设置API密钥，提供油耗的错误提示
#if not api_key:
  
#使用ChatInterface组件，这是Gradio提供的专门用于创建聊天界面的组件
demo = gr.ChatInterface(
  fn = backendService,                                 # 指定处理聊天消息的回调函数，将调用通义千问API
  title = "通义千问",                             # 界面标题
  description="基于通义千问max的聊天机器人",        # 界面描述
  examples=[
    ["你好"],
    ["你叫什么名字"],
    ["给我讲一个笑话呗"]
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

