import requests

weather_agent_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_real",
            "description": "获取指定城市的当前天气情况",
            "parameters": {
              "type": "object",
              "properties": {
                  "city": {
                    "type": "string",
                    "description": "The name of the city. such as 北京、上海"
                  }
              },
              "required": ["city"]
         }
        }
    }
]

# 这是实际干活的函数（你可以保留之前的模拟数据，或者接入真实API）
def get_weather(city):
    print(f"[系统日志] 正在查询 {city} 的天气...") 
    # 这里放你真实的查询逻辑，或者模拟数据
    mock_data = {"北京": "晴 26度", "上海": "小雨 24度"}
    return mock_data.get(city, f"{city}天气数据暂无，默认晴朗")

def get_weather_real(city):
  """
  调用真实的天气API获取天气信息
  """
  print(f"[系统日志]正在从真实API查询 {city} 的天气…")

  # 1. 构造API请求地址
  # 使用 wttr.in 这个免费的天气预报，~0表示当前天气，format=3 表示返回简洁的一行文本
  url = f"https://wttr.in/{city}?format=3&lang=zh"

  try:
    # 2. 发送GET请求
    response = requests.get(url, timeout=30) # 设置10秒超时


    # 3. 检查请求是否成功
    if response.status_code == 200:
      # 请求成功，返回天气文本
      return response.text
    else:
      # 请求失败，返回错误码
      return f"天气服务暂时不可用（错误码： {response.status_code}）"



  except Exception as e:
      # 捕获网络错误等异常
      return f"查询天气时发生网络错误： {str(e)}"
