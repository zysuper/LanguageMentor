import pytest
import gradio as gr

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def mock_gradio_blocks():
    """提供一个模拟的 gradio Blocks 对象"""
    with gr.Blocks() as demo:
        yield demo

@pytest.fixture
def mock_logger(mocker):
    """提供一个模拟的 logger 对象"""
    return mocker.patch('utils.logger.LOG') 