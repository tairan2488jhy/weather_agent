import json
import time
from llm import create_llm_client, BaseLLMClient
from tools import weather_agent_tools, get_weather_real
from logger import logger

# ======== 初始化 LLM 客户端 ========
# 秩序改动这一行，就能切换整个 Agent 的底层模型
llm_client: BaseLLMClient = create_llm_client("qwen")


def run_agent(message: str, history: list = None) -> str:
  """
  调用通义千问max模型的函数

  参数：
      message(str):用户当前输入的消息内容
      history(list):聊天历史记录，支持两种格式：
                    -- 格式1：【（用户消息，助手回复），……】-元组列表格式
                    -- 格式2：【{"role":"user", "content": "消息内容"}，……】-字典列表格式

  返回:
      str:模型生成的回复内容，如果发生错误则返回格式化的错误信息

  功能说明:
    1.验证API密钥是否存在，确保服务可用性
    2.创建0penAI客户端，配置DashScope的兼容模式API端点
    3.构建包含历史对话和当前消息的完整消息列表，维护对话上下文
    4.处理不同格式的历史消息，确保兼容性
    5.调用通义千问模型qwen-max生成回复
    6.捕获并处理可能的异常，返回友好的错误信息

  错误处理:
    - API密钥不存在:返回错误提示，指导用户设置环境变量
    - 史记录格式错误:尝试多种格式解析，出错时记录日志但不中断执行
    - API调用失败:返回原始错误信息，便于调试
  """
 

  # 构建消息列表，用于维持对话上下文
  # 这个列表将被传递给模型，包含完整的对话历史和当前消息
  messages = []

  # 如果存在历史对话记录，将其添加到消息列表中
  if history:
    # 遍历历史记录，正确处理Gradio ChatInterface的消息格式
    # 这里添加了异常处理，确保即使历史记录格式不正确也不会导致程序崩溃
    try: 
      # 尝试处理字典格式的history(较新版本Gradio的格式)
      for msg in history:
        # 检查是否为字典格式且包含必要的'role'和'content'字段
        if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
          messages.append(msg)
        #检查是否为元组或列表格式(较旧版本Gradio的格式)
        elif isinstance(msg, (list, tuple)) and len(msg) == 2:
           # 兼容旧格式的历史记录[(user_msg,assistant_msg),...] 
           user_msg, assistant_msg = msg
           #将元组格式转换为API需要的字典格式
           messages.append({"role":"user", "content": user_msg})
           messages.append({"role":"assistant", "content": assistant_msg})
    except Exception as e:
      # 如果处理历史记录时出错，打印错误信息但继续执行
      # 这确保了即使历史记录处理失败，用户也能继续与模型交互
      print(f"处理历史记录时出错:{e}")

  # 添加当前用户的最新消息到消息列表中
  # 这确保了模型能够接收到用户的最新请求    
  messages.append({"role": "user", "content": message})

  # --- 记录请求开始 ---
  logger.info(f"收到用户请求: '{message}'")
  start_time = time.time() # 记录开始时间

  try:
    # 使用qwen-max模型，这是通义千问系列中的高性能版本   
    response = llm_client.chat_completion_with_tools(
      messages=messages,
      tools=weather_agent_tools,
      model=None
      )
    
    # --- 记录首次 LLM 响应 ---
    latency = time.time() - start_time
    logger.debug(f"首次 LLM 响应延迟: {latency:.2f}s")

    assistant_message = response.choices[0].message

    # 3. 判断模型是否需要调用工具
    if assistant_message.tool_calls:
      # 把模型的请求加入历史记录
      messages.append(assistant_message)

      for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments) #解析参数
        logger.info(f"正在执行工具: {function_name}, 参数: {function_args}")

        tool_start = time.time()

        # result = "没有结果返回"
        # 4. 执行真正的 python 函数

        try:
          if function_name == "get_weather_real":
            result = get_weather_real(**function_args)

          tool_latency = time.time() - tool_start
          logger.info(f"工具执行成功: {function_name}, 耗时: {tool_latency:.2f}s, 结果: {result}")

        except Exception as e:
          tool_latency = time.time() - tool_start
          logger.error(f"工具执行失败: {function_name}, 耗时: {tool_latency:.2f}s, 错误: {e}")
          result = f"Error: {e}"

        
      

        # return result
        # 如果不第二次调用大模型

        # 5. 把执行结果包装成"tool"角色的消息，放回历史
        messages.append({
          "role": "tool",
          "tool_call_id": tool_call.id,
          "name": function_name,
          "content": str(result)
        })   

      # 6. 第二次调用 LLM， 让他根据工具返回的结果生成最终的回复  

      # logger.info("正在请求 LLM 生成最终回复...")
      # second_response = llm_client.chat_completion(
      #   messages=messages,
      #   model=None
      #   )
      # final_latency = time.time() - start_time
      # logger.info(f"请求处理完成，总耗时: {final_latency:.2f}s")
      # return second_response.choices[0].message.content
      logger.info("正在请求 LLM 生成最终回复（流式）...")
      full_content = stream_and_collect(llm_client, messages)
      logger.info("请求处理完成")
      return full_content

    else:
      # 如果模型没有调用工具，直接返回它的回复
      total_latency = time.time() - start_time
      logger.info(f"模型直接回复，总耗时: {total_latency:.2f}s")
      return assistant_message.content


    # 提取并返回模型生成的回复内容
  
  except Exception as e:
    # 捕获并处理所有可能的异常，返回友好的错误信息
    return "Error: " + str(e)
  
def stream_and_collect(client: BaseLLMClient, messages: list) -> str:
  """
  流式输出并收集完整内容
  -- 实时打印到终端（打字机效果）
  -- 同时收集完整文本用于返回
  """
  stream = client.chat_completion_stream(messages=messages, model=None)

  parts = []
  for chunk in stream:
    if not chunk.choices:
      continue
    content = chunk.choices[0].delta.content
    if content:
      print("实时输出：", content, end="", flush=True) # 实时输出到终端
      parts.append(content)

  print() # 最后换行
  full_text = "".join(parts)
  return full_text