# logger.py

import logging
import sys

def setup_logger():
  """
  配置并返回一个全部 logger 实例
  """
  # 1. 创建一个 logger
  logger = logging.getLogger("weather_agent")
  logger.setLevel(logging.DEBUG) # 设置为最低级别，具体级别由 Handler 控制


  # 2. 防止重复添加 Handler (在热加载等场景下很重要)
  if logger.handlers:
    return logger
  
  # 3. 创建一个 Formatter (日志格式)
  # 格式:[时间]【级别】[文件名：行号]-日志内容
  formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )


  # 4. 创建 Handler: 输出到控制台 （stdout）
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setLevel(logging.INFO) # 控制台显示 INFO 及以上级别的日志
  console_handler.setFormatter(formatter)

  # 5. 创建 Handler：输出到文件 (可选，用于持久化)
  file_handler = logging.FileHandler("app.log", encoding="utf-8")
  file_handler.setLevel(logging.DEBUG) # 文件记录所有 DEBUG 及以上级别的日志
  file_handler.setFormatter(formatter)

  # 6. 将 Handler 添加到 logger
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)

  return logger 


# 创建一个全局的 logger 实例， 供项目其他地方直接导入使用
logger = setup_logger()