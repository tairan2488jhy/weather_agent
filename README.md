
# 260726 模拟天气agent 触发大模型调用

# 激活python 虚拟环境  
```
.venv\Scripts\activate
```

# 重启应用的语句
```
#bash
while true; do python app.py; echo "重启中..."; sleep 1; done

#powershell
while ($true) { python app.py; Write-Host "重启中..."; Start-Sleep -Seconds 1 }
```

# 在项目中开始调试代码 
## VSCode 引入python依赖 开启调试

# 接入正式的天气 api 
1. pip install requests
  
# 作为独立项目，升级，完成项目升级 github项目地址 

# 增加 backend 服务层 
启动顺序：
# 终端 1：启动后端（FastAPI）
uvicorn backend.api:app --reload

# 终端 2：启动前端（Gradio）
python app.py


