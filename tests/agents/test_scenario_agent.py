import pytest
from unittest.mock import mock_open, patch, MagicMock
from langchain_core.messages import AIMessage

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from agents.scenario_agent import ScenarioAgent

class TestScenarioAgent:
    """ScenarioAgent 类的测试用例"""

    @pytest.fixture
    def mock_prompt_file(self):
        """模拟提示文件内容"""
        return "Test scenario prompt"

    @pytest.fixture
    def mock_intro_file(self):
        """模拟介绍文件内容"""
        return """["Hello", "Hi"]"""

    @pytest.fixture
    def mock_session_history(self):
        """模拟会话历史"""
        history = MagicMock()
        history.messages = []
        return history

    def test_init(self, mock_prompt_file, mock_intro_file):
        """测试初始化"""
        with patch("builtins.open") as mock_file:
            mock_file.side_effect = [
                mock_open(read_data=mock_prompt_file).return_value,
                mock_open(read_data=mock_intro_file).return_value
            ]
            agent = ScenarioAgent("test_scenario")
            assert agent.name == "test_scenario"
            assert agent.prompt_file == "prompts/test_scenario_prompt.txt"
            assert agent.intro_file == "content/intro/test_scenario.json"

    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_empty_history(self, mock_get_history, mock_prompt_file, mock_intro_file):
        """测试开始新会话（空历史记录）"""
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_history.return_value = mock_history
        mock_history.add_message = MagicMock()

        with patch("builtins.open") as mock_file:
            mock_file.side_effect = [
                mock_open(read_data=mock_prompt_file).return_value,
                mock_open(read_data=mock_intro_file).return_value
            ]
            agent = ScenarioAgent("test_scenario")
            response = agent.start_new_session()
            
            assert response in ["Hello", "Hi"]
            mock_history.add_message.assert_called_once()

    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_existing_history(self, mock_get_history, mock_prompt_file, mock_intro_file):
        """测试开始新会话（已有历史记录）"""
        mock_history = MagicMock()
        last_message = AIMessage(content="Last message")
        mock_history.messages = [last_message]
        mock_get_history.return_value = mock_history

        with patch("builtins.open") as mock_file:
            mock_file.side_effect = [
                mock_open(read_data=mock_prompt_file).return_value,
                mock_open(read_data=mock_intro_file).return_value
            ]
            agent = ScenarioAgent("test_scenario")
            response = agent.start_new_session()
            
            assert response == "Last message"
            mock_history.add_message.assert_not_called() 