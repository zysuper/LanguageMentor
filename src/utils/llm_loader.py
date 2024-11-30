import yaml
import os
from langchain_openai import ChatOpenAI 
from langchain_ollama.chat_models import ChatOllama  # 导入 ChatOllama 模型
from loguru import logger

# 加载LLM配置
class LLMLoader:
    def __init__(self, config_path="llm.yaml"):
        """初始化LLM加载器"""
        self.config_path = config_path
        self.models = {}
        self._load_config()
    
    def _load_config(self):
        """从yaml文件加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            for model_config in config.get('models', []):
                model_type = model_config.get('type', '').lower()
                temperature = model_config.get('temperature', 0.7)
                max_tokens = model_config.get('max_tokens', 2048)
                model_name = model_config.get('model_name')
                
                if model_type == 'openai':
                    base_url = model_config.get('base_url', 'https://api.openai-hk.com')

                    self.models[model_name] = ChatOpenAI(
                        model_name=model_name,
                        temperature=temperature,
                        api_key=os.getenv('OPENAI_HK_API_KEY'),
                        base_url=base_url,
                        max_tokens=max_tokens
                    )
                elif model_type == 'ollama':
                    # 获取 Ollama 服务器 URL 配置
                    base_url = model_config.get('base_url', 'http://localhost:11434')
                    self.models[model_name] = ChatOllama(
                        model=model_name,
                        temperature=temperature,
                        base_url=base_url,
                        max_tokens=max_tokens
                    )
                else:
                    logger.warning(f"不支持的模型类型: {model_type}")
                    
        except Exception as e:
            logger.error(f"加载LLM配置文件失败: {str(e)}")
            raise
    
    def get_model(self, model_name):
        """获取指定名称的模型实例"""
        if model_name not in self.models:
            raise ValueError(f"模型 {model_name} 未在配置中找到")
        return self.models[model_name]
    
    def list_models(self):
        """列出所有可用的模型名称"""
        return list(self.models.keys())


