# 260726 weather_agent 项目review

# 0 项目文件功能解析 --伴随项目review进程，这些文件会有部分功能消亡或者职责变迁
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


# 1 开发和运行环境的准备
1. 激活python 虚拟环境  
```
.venv\Scripts\activate
```

2. 重启应用的语句
```
#bash
while true; do python app.py; echo "重启中..."; sleep 1; done

#powershell
while ($true) { python app.py; Write-Host "重启中..."; Start-Sleep -Seconds 1 }
```

3. 在项目中开始调试代码 
## VSCode 引入python依赖 开启调试

# 2 接入正式的天气 api 
1. pip install requests
  
# 3 作为独立项目，升级，完成项目升级 github项目地址 

# 4 增加 backend 服务层 
启动顺序：
# 终端 1：启动后端（FastAPI）
uvicorn backend.api:app --reload

# 终端 2：启动前端（Gradio）
python app.py

# 5 完善config.py 增加 .env 生产环境配置
# LLM 配置
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen3.7-max-2026-05-20
LLM_TIMEOUT=30

# 服务配置
HOST=0.0.0.0
PORT=8000
DEBUG=true

# 6 完善日志输出
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

# 7 引入测试模块

在项目根目录（Wether_Agent/）下执行：
pytest tests/ -v

```
# 基础：运行全部，显示每个用例名称
pytest tests/ -v

# 详细：显示 print 输出（调试时有用）
pytest tests/ -v -s

# 快速失败：遇到第一个失败就停，省时间
pytest tests/ -v -x

# 失败重跑：自动重跑失败的用例 2 次（需装 pytest-rerunfailures）
pytest tests/ -v --reruns 2

# 只看结果摘要：通过显示 . ，失败显示 F
pytest tests/

```




