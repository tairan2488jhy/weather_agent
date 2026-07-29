# 先构建能够调用Qwen 大模型的天气agent基本架构

# 引入大模型api 成功调用

# 研究agent的基本思路 完成 输入--》 tool-》llm的交互

# 修改代码，研究没有第二次调用LLM，会怎样影响调用结果

# 接入正式的天气api 26/07/27 14:47 

# 让他看起来更像一个工程

# 项目改造方向：企业级的布局应用
---

### 📂 项目文件职责详解

#### 1. `config.py` —— 项目的“配置中心”
- **职责**：存放所有**常量**和**敏感信息**。
- **为什么要分出来**：如果你换了 API Key，或者想换个模型测试，不需要去翻几百行代码，只改这一个文件即可。
- **应该放什么**：
    - `DASHSCOPE_API_KEY` (建议从环境变量读取)
    - `MODEL_NAME` (例如 "qwen-max")
    - `BASE_URL`
    - 系统提示词 (`SYSTEM_PROMPT`)

#### 2. `tools.py` —— Agent 的“工具箱”
- **职责**：存放所有**工具函数的定义**以及**工具的 JSON 描述**。
- **为什么要分出来**：Agent 的核心能力就是调用工具。随着你增加“查股票”、“写邮件”等功能，这里会越来越长。把它独立出来，`app.py` 就清爽了。
- **应该放什么**：
    - `get_weather` 函数（包含真实的 API 调用逻辑）。
    - `tools_definition` 列表（即那个告诉大模型怎么调用工具的 JSON 字典）。

#### 3. `llm.py` —— 与大脑对话的“传声筒”
- **职责**：封装与大模型交互的底层逻辑。
- **为什么要分出来**：调用 API 的代码（初始化 Client、处理 `try-except`、解析 `response`）是很枯燥且通用的。把它封装好，以后无论在哪里想调用大模型，直接 `import llm` 就行。
- **应该放什么**：
    - `call_llm(messages, tools=None)` 函数。
    - 负责处理 OpenAI/DashScope 的 SDK 调用。
    - 负责处理流式输出（如果未来需要）。

#### 4. `agent.py` —— 项目的“总指挥” (核心逻辑)
- **职责**：编排整个对话流程。它是连接用户、LLM 和 Tools 的桥梁。
- **为什么要分出来**：这是你之前写在 `app.py` 里 `call_qwen` 函数的核心部分。它决定了：“用户说话了 -> 调 LLM -> LLM 说要调工具 -> 调工具 -> 再调 LLM -> 返回结果”这个复杂的循环逻辑。
- **应该放什么**：
    - `run_agent(user_message, history)` 函数。
    - 这里的逻辑是：接收消息 -> 调用 `llm.py` -> 判断是否有 `tool_calls` -> 如果有，去 `tools.py` 找函数执行 -> 再次调用 `llm.py`。

#### 5. `app.py` —— 纯粹的“界面层”
- **职责**：只负责**展示**和**接收输入**。它不应该包含任何业务逻辑。
- **现状**：现在它太胖了。
- **理想状态**：它应该非常短，只负责启动 Gradio，并把用户的输入转发给 `agent.py`。

#### 6. 其他文件
- `requirements.txt`: 记录依赖库（如 `gradio`, `openai`, `requests`），方便别人一键安装环境。
- `.gitignore`: 告诉 Git 哪些文件不要上传（比如 `.venv` 虚拟环境文件夹，`.env` 密钥文件）。
- `README.md`: 项目说明书，教别人怎么运行你的代码。

---

### 🚀 重构路线图：如何把代码“搬”出去？

建议你按照以下顺序进行重构（Refactoring）：

1.  **第一步（搬家配置）**：新建 `config.py`，把 API Key 和模型名字移过去。
2.  **第二步（搬家工具）**：新建 `tools.py`，把 `get_weather` 函数和那个巨大的 JSON 字典移过去。
3.  **第三步（搬家大脑）**：新建 `llm.py`，把 `client.chat.completions.create` 那部分代码封装成一个函数。
4.  **第四步（整理指挥）**：新建 `agent.py`，把处理 `tool_calls` 循环的逻辑放进去，让它调用 `llm.py` 和 `tools.py`。
5.  **第五步（瘦身 App）**：最后回到 `app.py`，删掉所有逻辑，只保留 `gr.ChatInterface(fn=agent.run_agent, ...)`。

这样拆分后，你的代码不仅看起来专业，而且如果你想把 Gradio 换成命令行版本，或者加个网页前端，只需要改 `app.py`，其他逻辑完全不用动！


# 拆分项目遇到的问题

1. 包冲突
   pip list | findstr llm


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



# 6 增加 .env 完善配置文件，并且 .env 被 gitignore 完善config

# 7 发现作为一个完整的系统，日志目前时缺失的，因此我需要记录兄完成的运行和错误日志



