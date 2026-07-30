# 改造任务1 明确目标

## 先构建能够调用Qwen 大模型的天气agent基本架构

## 引入大模型api 成功调用

## 研究agent的基本思路 完成 输入--》 tool-》llm的交互

## 修改代码，研究没有第二次调用LLM，会怎样影响调用结果

## 接入正式的天气api 26/07/27 14:47 

## 让他看起来更像一个工程

## 项目改造方向：企业级的布局应用
---

### 🚀 重构路线图：如何把代码“搬”出去？

建议你按照以下顺序进行重构（Refactoring）：

1.  **第一步（搬家配置）**：新建 `config.py`，把 API Key 和模型名字移过去。
2.  **第二步（搬家工具）**：新建 `tools.py`，把 `get_weather` 函数和那个巨大的 JSON 字典移过去。
3.  **第三步（搬家大脑）**：新建 `llm.py`，把 `client.chat.completions.create` 那部分代码封装成一个函数。
4.  **第四步（整理指挥）**：新建 `agent.py`，把处理 `tool_calls` 循环的逻辑放进去，让它调用 `llm.py` 和 `tools.py`。
5.  **第五步（瘦身 App）**：最后回到 `app.py`，删掉所有逻辑，只保留 `gr.ChatInterface(fn=agent.run_agent, ...)`。

这样拆分后，你的代码不仅看起来专业，而且如果你想把 Gradio 换成命令行版本，或者加个网页前端，只需要改 `app.py`，其他逻辑完全不用动！


# 改造任务1 增加backend 服务层

#   schemas 数据流程图
### 📌 数据流总览

```
┌──────────┐                          ┌──────────────────────────────────────┐
│          │   ChatRequest            │              backend/                │
│  app.py  │ ─────────────────────▶   │                                      │
│ (前端)   │   { message, session_id }│  api.py ──调用──▶ service.py         │
│          │                          │    │                    │            │
│          │   ChatResponse           │    │ 使用               │ 使用        │
│          │ ◀─────────────────────   │    ▼                    ▼            │
└──────────┘   { reply, session_id }  │  schemas.py ◀── 统一数据契约 ──▶     │
                                      │  (ChatRequest, ChatResponse,         │
                                      │   AgentContext)                       │
                                      └──────────────────────────────────────┘
``` 



# 改造任务2 增加 .env 完善配置文件，并且 .env 被 gitignore 完善config

# 改造任务3 发现作为一个完整的系统，日志目前时缺失的，因此我需要记录兄完成的运行和错误日志
输出日志：
2026-07-29 15:53:05 - INFO - api.py:35 - API 请求: POST /chat
2026-07-29 15:53:05 - INFO - service.py:25 - 业务层收到请求 - Session: 9a712d9b-8dd8-48ae-bb32-f14f37a7d31c, 消息: '北京天气怎么样'
2026-07-29 15:53:05 - INFO - agent.py:71 - 收到用户请求: '北京天气怎么样'
2026-07-29 15:53:10 - INFO - agent.py:96 - 正在执行工具: get_weather_real, 参数: {'city': '北京'}
[系统日志]正在从真实API查询 北京 的天气…
2026-07-29 15:53:11 - INFO - agent.py:108 - 工具执行成功: get_weather_real, 耗时: 1.20s, 结果: 北京: 🌤️  +36°C
2026-07-29 15:53:11 - INFO - agent.py:131 - 正在请求 LLM 生成最终回复...
2026-07-29 15:53:14 - INFO - agent.py:137 - 请求处理完成，总耗时: 9.03s
2026-07-29 15:53:14 - INFO - service.py:53 - 业务层处理完成 - Session: 9a712d9b-8dd8-48ae-bb32-f14f37a7d31c
2026-07-29 15:53:14 - INFO - api.py:39 - API 响应: POST /chat - 状态码: 200
INFO:     127.0.0.1:59827 - "POST /chat HTTP/1.1" 200 OK

# 改造任务4 增加测试模块和测试单元

# 改造任务5 增加 llm 返回的 steam


