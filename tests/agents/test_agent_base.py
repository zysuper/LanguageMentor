import pytest
from unittest.mock import mock_open, patch, MagicMock
import os
import sys
from utils.logger import LOG

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from agents.agent_base import AgentBase

class TestAgent(AgentBase):
    """用于测试的具体 Agent 实现"""
    def __init__(self, name="test_agent", prompt_file="test.txt", intro_file=None, session_id=None):
        super().__init__(name, prompt_file, intro_file, session_id)

class TestAgentBase:
    """AgentBase 类的测试用例"""

    @pytest.fixture
    def mock_prompt_file(self):
        """模拟提示文件内容"""
        return "Test prompt content"

    @pytest.fixture
    def mock_intro_file(self):
        """模拟介绍文件内容"""
        return """["So, you're here for the R&D Engineer position today?"]"""

    def test_init_basic(self, mock_prompt_file):
        """测试基本初始化"""
        with patch("builtins.open", mock_open(read_data=mock_prompt_file)):
            agent = TestAgent()
            assert agent.name == "test_agent"
            assert agent.prompt == mock_prompt_file
            assert agent.intro_messages == []

    def test_init_with_intro(self, mock_prompt_file, mock_intro_file):
        """测试带有介绍文件的初始化"""
        with patch("builtins.open") as mock_file:
            mock_file.side_effect = [
                mock_open(read_data=mock_prompt_file).return_value,
                mock_open(read_data=mock_intro_file).return_value
            ]
            agent = TestAgent(intro_file="intro.json")
            assert agent.intro_messages == ["So, you're here for the R&D Engineer position today?"]

    def test_load_prompt_file_not_found(self):
        """测试提示文件不存在的情况"""
        with pytest.raises(FileNotFoundError):
            TestAgent(prompt_file="nonexistent.txt")

    def test_load_intro_file_not_found(self):
        """测试介绍文件不存在的情况"""
        with patch("builtins.open", mock_open(read_data="Test prompt")):
            with pytest.raises(ValueError):
                TestAgent(intro_file="nonexistent.json")

    def test_load_intro_invalid_json(self, mock_prompt_file):
        """测试介绍文件包含无效 JSON 的情况"""
        with patch("builtins.open") as mock_file:
            mock_file.side_effect = [
                mock_open(read_data=mock_prompt_file).return_value,
                mock_open(read_data="invalid json").return_value
            ]
            with pytest.raises(ValueError):
                TestAgent(intro_file="invalid.json")

    def test_chat_with_history(self, mock_prompt_file):
        """测试聊天功能"""

        mock_chatbot_with_history = MagicMock()
        mock_chatbot_with_history.invoke.return_value = MagicMock()
        mock_chatbot_with_history.invoke.return_value.content = "Test response"
        
        with patch("builtins.open", mock_open(read_data=mock_prompt_file)):
            agent = TestAgent()
            agent.chatbot_with_history = mock_chatbot_with_history
            response = agent.chat_with_history("Hello")
            
            assert response == "Test response"
            #mock_logger.debug.assert_called_once() 
