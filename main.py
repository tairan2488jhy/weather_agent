# Backend Service

from agent import run_agent

# 定义一个函数，用于调用通义千问max模型生成回复
def backendService(message, history):
  return run_agent(message, history)