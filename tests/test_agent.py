# 测试 Agent 核心逻辑（需 mock LLM）

import pytest
from unittest.mock import patch, MagicMock
import json


class TestRunAgent:
    """测试 Agent 核心循环"""

    @patch("agent.llm_client")
    def test_direct_reply_no_tool(self, mock_client):
        """模型直接回复（不调用工具）时，应返回文本内容"""
        # 模拟 LLM 返回一个不带 tool_calls 的 response
        mock_response = MagicMock()
        mock_response.choices[0].message.tool_calls = None
        mock_response.choices[0].message.content = "你好，有什么可以帮你的？"
        mock_client.chat_completion_with_tools.return_value = mock_response

        from agent import run_agent
        result = run_agent("你好")

        assert result == "你好，有什么可以帮你的？"
        mock_client.chat_completion_with_tools.assert_called_once()

    @patch("agent.llm_client")
    def test_tool_call_flow(self, mock_client):
        """模型调用工具后，应流式返回最终生成的回复"""
        # --- 第一次调用：chat_completion_with_tools，模型决定调用工具 ---
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_001"
        mock_tool_call.function.name = "get_weather_real"
        mock_tool_call.function.arguments = json.dumps({"city": "北京"})

        first_message = MagicMock()
        first_message.tool_calls = [mock_tool_call]
        first_message.content = None

        first_choice = MagicMock()
        first_choice.message = first_message

        first_response = MagicMock()
        first_response.choices = [first_choice]

        mock_client.chat_completion_with_tools.return_value = first_response

        # --- 第二次调用：chat_completion_stream，返回流式 chunk ---
        # 模拟 3 个 chunk
        chunk1 = MagicMock()
        chunk1.choices[0].delta.content = "北京今天晴，"

        chunk2 = MagicMock()
        chunk2.choices[0].delta.content = "25°C，"

        chunk3 = MagicMock()
        chunk3.choices[0].delta.content = "适合出行。"

        mock_client.chat_completion_stream.return_value = iter([chunk1, chunk2, chunk3])

        from agent import run_agent
        result = run_agent("北京天气怎么样？")

        assert result == "北京今天晴，25°C，适合出行。"
        mock_client.chat_completion_with_tools.assert_called_once()
        mock_client.chat_completion_stream.assert_called_once()

    # @patch("agent.llm_client")
    # def test_tool_call_flow(self, mock_client):
    #     """模型调用工具后，应返回最终生成的回复"""
    #     # --- 第一次调用：chat_completion_with_tools，模型决定调用工具 ---
    #     mock_tool_call = MagicMock()
    #     mock_tool_call.id = "call_001"
    #     mock_tool_call.function.name = "get_weather_real"
    #     mock_tool_call.function.arguments = json.dumps({"city": "北京"})

    #     first_message = MagicMock()
    #     first_message.tool_calls = [mock_tool_call]
    #     first_message.content = None

    #     first_choice = MagicMock()
    #     first_choice.message = first_message

    #     first_response = MagicMock()
    #     first_response.choices = [first_choice]

    #     # --- 第二次调用：chat_completion，模型根据工具结果生成最终回复 ---
    #     second_message = MagicMock()
    #     second_message.content = "北京今天晴，25°C，适合出行。"
    #     second_message.tool_calls = None

    #     second_choice = MagicMock()
    #     second_choice.message = second_message

    #     second_response = MagicMock()
    #     second_response.choices = [second_choice]

    #     # 第一次走 chat_completion_with_tools，第二次走 chat_completion
    #     mock_client.chat_completion_with_tools.return_value = first_response
    #     mock_client.chat_completion.return_value = second_response

    #     from agent import run_agent
    #     result = run_agent("北京天气怎么样？")

    #     assert result == "北京今天晴，25°C，适合出行。"
    #     mock_client.chat_completion_with_tools.assert_called_once()
    #     mock_client.chat_completion.assert_called_once()



    @patch("agent.llm_client")
    def test_with_history(self, mock_client):
        """传入历史对话时，messages 应包含历史"""
        mock_response = MagicMock()
        mock_response.choices[0].message.tool_calls = None
        mock_response.choices[0].message.content = "好的，我记得之前的对话。"
        mock_client.chat_completion_with_tools.return_value = mock_response

        from agent import run_agent
        history = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！"},
        ]
        result = run_agent("继续聊", history=history)

        assert result == "好的，我记得之前的对话。"
        # 验证调用时 messages 包含了历史 + 新消息
        call_args = mock_client.chat_completion_with_tools.call_args
        messages = call_args.kwargs.get("messages") or call_args[1].get("messages")
        assert len(messages) == 3  # 2条历史 + 1条新消息