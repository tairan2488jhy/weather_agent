# 260726 weather_agent 项目review

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




