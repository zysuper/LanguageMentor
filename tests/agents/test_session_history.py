import pytest
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from agents.session_history import get_session_history, store

class TestSessionHistory:
    """session_history 模块的测试用例"""

    @pytest.fixture(autouse=True)
    def clear_store(self):
        """每个测试前清空存储"""
        store.clear()
        yield

    def test_get_new_session_history(self):
        """测试获取新的会话历史"""
        session_id = "test_session"
        history = get_session_history(session_id)
        
        assert isinstance(history, InMemoryChatMessageHistory)
        assert session_id in store
        assert len(history.messages) == 0

    def test_get_existing_session_history(self):
        """测试获取已存在的会话历史"""
        session_id = "test_session"
        first_history = get_session_history(session_id)
        first_history.add_message(HumanMessage(content="Hello"))
        
        second_history = get_session_history(session_id)
        assert second_history is first_history
        assert len(second_history.messages) == 1
        assert second_history.messages[0].content == "Hello"

    def test_multiple_sessions(self):
        """测试多个会话历史"""
        session_1 = get_session_history("session_1")
        session_2 = get_session_history("session_2")
        
        session_1.add_message(HumanMessage(content="Hello from 1"))
        session_2.add_message(AIMessage(content="Hello from 2"))
        
        assert len(session_1.messages) == 1
        assert len(session_2.messages) == 1
        assert session_1.messages[0].content == "Hello from 1"
        assert session_2.messages[0].content == "Hello from 2"

    def test_session_message_operations(self):
        """测试会话消息操作"""
        session = get_session_history("test_session")
        
        # 添加消息
        session.add_message(HumanMessage(content="User message"))
        session.add_message(AIMessage(content="AI response"))
        
        assert len(session.messages) == 2
        assert isinstance(session.messages[0], HumanMessage)
        assert isinstance(session.messages[1], AIMessage)
        
        # 清空消息
        session.clear()
        assert len(session.messages) == 0 