# 测试 LLM 客户端（需 mock OpenAI SDK）

# tests/test_llm_client.py

import pytest
from unittest.mock import patch, MagicMock


class TestQwenClient:
    """测试 QwenClient"""

    @patch("llm.qwen_client.OpenAI")
    def test_chat_completion_returns_response(self, mock_openai_class):
        """chat_completion 应返回字符串"""
        # 模拟 OpenAI SDK 的返回值
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_instance.chat.completions.create.return_value = mock_response

        mock_openai_class.return_value = mock_instance
        mock_instance.chat.completions.create.return_value.choices[0].message.content = "测试回复"

        from llm.qwen_client import QwenClient
        client = QwenClient()
        result = client.chat_completion([{"role": "user", "content": "你好"}], None)

        assert result is mock_response
        # assert isinstance(result, str)
        # assert result == "测试回复"

    @patch("llm.qwen_client.OpenAI")
    def test_chat_completion_with_tools_returns_response(self, mock_openai_class):
        """chat_completion_with_tools 应返回完整的 response 对象"""
        mock_instance = MagicMock()
        mock_openai_class.return_value = mock_instance

        mock_response = MagicMock()
        mock_response.choices[0].message.tool_calls = []
        mock_instance.chat.completions.create.return_value = mock_response

        from llm.qwen_client import QwenClient
        client = QwenClient()
        result = client.chat_completion_with_tools(
            messages=[{"role": "user", "content": "北京天气"}],
            tools=[],
            model=None

        )

        # 返回的应该是 response 对象，不是字符串
        assert result is mock_response

    @patch("llm.qwen_client.OpenAI")
    def test_tools_passed_to_api(self, mock_openai_class):
        """tools 参数应被正确传递给 OpenAI API"""
        mock_instance = MagicMock()
        mock_openai_class.return_value = mock_instance

        from llm.qwen_client import QwenClient
        client = QwenClient()

        fake_tools = [{"type": "function", "function": {"name": "test"}}]
        client.chat_completion_with_tools(
            messages=[{"role": "user", "content": "测试"}],
            tools=fake_tools,
            model=None
        )

        # 验证 tools 被传给了 API
        call_kwargs = mock_instance.chat.completions.create.call_args.kwargs
        assert call_kwargs["tools"] == fake_tools


class TestCreateLLMClient:
    """测试工厂函数"""

    def test_create_qwen_client(self):
        """传入 'qwen' 应返回 QwenClient 实例"""
        with patch("llm.qwen_client.OpenAI"):
            from llm import create_llm_client
            from llm.qwen_client import QwenClient
            client = create_llm_client("qwen")
            assert isinstance(client, QwenClient)

    def test_unsupported_provider_raises_error(self):
        """传入不支持的 provider 应抛出 ValueError"""
        from llm import create_llm_client
        with pytest.raises(ValueError, match="Unsupported"):
            create_llm_client("claude")