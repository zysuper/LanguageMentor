import pytest
import os
from loguru import logger

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.logger import LOG

class TestLogger:
    """logger 模块的测试用例"""

    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """设置和清理测试环境"""
        # 确保日志目录存在
        os.makedirs("logs", exist_ok=True)
        yield
        # 清理测试生成的日志文件
        if os.path.exists("logs/app.log"):
            os.remove("logs/app.log")

    def test_log_levels(self):
        """测试不同日志级别"""
        LOG.debug("Debug message")
        LOG.info("Info message")
        LOG.warning("Warning message")
        LOG.error("Error message")
        
        # 验证日志文件是否创建
        assert os.path.exists("logs/app.log")
        
        # 读取日志文件内容
        with open("logs/app.log", "r") as f:
            log_content = f.read()
            assert "Debug message" in log_content
            assert "Info message" in log_content
            assert "Warning message" in log_content
            assert "Error message" in log_content

    def test_log_format(self):
        """测试日志格式"""
        test_message = "Test log format"
        LOG.info(test_message)
        
        with open("logs/app.log", "r") as f:
            log_line = f.readlines()[-1]  # 获取最后一行
            
            # 验证日志格式
            assert "|" in log_line  # 检查分隔符
            assert "INFO" in log_line  # 检查日志级别
            assert test_message in log_line  # 检查消息内容
            assert "test_logger" in log_line  # 检查模块名

    def test_log_rotation(self):
        """测试日志轮换"""
        # 写入大量日志以触发轮换
        large_message = "x" * 1000  # 1KB 消息
        for _ in range(1100):  # 写入超过 1MB 的日志
            LOG.debug(large_message)
        
        # 验证是否创建了轮换日志文件
        log_files = [f for f in os.listdir("logs") if f.startswith("app.")]
        assert len(log_files) > 1  # 应该有多个日志文件 