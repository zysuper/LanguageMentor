import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from agents.conversation_agent import ConversationAgent

class TestConversationAgent:
    @pytest.fixture
    def conversation_agent(self):
        # 创建一个测试用的 ConversationAgent 实例
        return ConversationAgent(session_id="test_session")

    def test_init(self, conversation_agent):
        # 测试初始化是否正确
        assert conversation_agent.name == "conversation"
        assert conversation_agent.prompt_file == "prompts/conversation_prompt.txt"
        assert conversation_agent.session_id == "test_session" 