# 测试工具函数

# tests/test_weather_tool.py

import pytest
from tools import get_weather_real


class TestGetWeatherReal:
    """测试天气查询工具"""

    def test_known_city(self):
        """已知城市应返回天气字符串"""
        result = get_weather_real("北京")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_unknown_city(self):
        """未知城市应返回提示信息"""
        result = get_weather_real("亚特兰蒂斯")
        assert isinstance(result, str)
        assert "暂无" in result or "未找到" in result or "暂无数据" in result

    def test_return_type_is_string(self):
        """返回值必须是字符串（Agent 需要 str 类型）"""
        result = get_weather_real("上海")
        assert type(result) == str

    def test_empty_input(self):
        """空字符串输入不应崩溃"""
        result = get_weather_real("")
        assert isinstance(result, str)