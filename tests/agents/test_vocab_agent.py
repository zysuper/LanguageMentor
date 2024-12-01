import pytest
from unittest.mock import patch, MagicMock

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.vocab_agent import VocabAgent

class TestVocabAgent:
    @pytest.fixture
    def vocab_agent(self):
        # 创建一个测试用的 VocabAgent 实例
        return VocabAgent(session_id="test_session")

    def test_init(self, vocab_agent):
        # 测试初始化是否正确
        assert vocab_agent.name == "vocab_study"
        assert vocab_agent.prompt_file == "prompts/vocab_study_prompt.txt"
        assert vocab_agent.session_id == "test_session"

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session(self, mock_get_history, vocab_agent):
        # 创建模拟的历史记录对象
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        # 调用重启会话方法
        result = vocab_agent.restart_session()

        # 验证是否正确调用了相关方法
        mock_get_history.assert_called_once_with("test_session")
        mock_history.clear.assert_called_once()
        assert result == mock_history 