#!/usr/bin/env python3
"""
LLM API客户端 - 支持多种LLM提供商
"""

import os
import time
import json
from typing import Dict, Optional, Any, List
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """LLM客户端基类"""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)
        self.timeout = kwargs.get("timeout", 60)
        self.retry_times = kwargs.get("retry_times", 3)
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass
    
    def _retry_on_failure(self, func, *args, **kwargs):
        """失败重试装饰器"""
        last_error = None
        for attempt in range(self.retry_times):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(2 ** attempt)  # 指数退避
        raise last_error


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT客户端"""
    
    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = kwargs.get("base_url", "https://api.openai.com/v1")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """调用OpenAI API生成文本"""
        import requests
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        def _call_api():
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        
        return self._retry_on_failure(_call_api)


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude客户端"""
    
    def __init__(self, api_key: str, model: str = "claude-3-opus", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = kwargs.get("base_url", "https://api.anthropic.com/v1")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """调用Anthropic API生成文本"""
        import requests
        
        messages = [{"role": "user", "content": prompt}]
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        def _call_api():
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]
        
        return self._retry_on_failure(_call_api)


class BaiduClient(BaseLLMClient):
    """百度文心一言客户端"""
    
    def __init__(self, api_key: str, model: str = "ernie-4.0-8k-latest", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.api_secret = kwargs.get("api_secret", "")
        self.base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """调用百度API生成文本"""
        import requests
        
        # 生成access_token（简化版，实际需要缓存）
        import base64
        import hmac
        import hashlib
        from urllib.parse import urlencode
        from datetime import datetime
        
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        token_response = requests.post(token_url, params=params)
        access_token = token_response.json().get("access_token")
        
        headers = {"Content-Type": "application/json"}
        
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        def _call_api():
            response = requests.post(
                f"{self.base_url}?access_token={access_token}",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()["result"]
        
        return self._retry_on_failure(_call_api)


class LLMFactory:
    """LLM客户端工厂"""
    
    _clients: Dict[str, BaseLLMClient] = {}
    
    @classmethod
    def get_client(cls, provider: str, **kwargs) -> BaseLLMClient:
        """获取LLM客户端"""
        cache_key = f"{provider}_{kwargs.get('model', 'default')}"
        
        if cache_key not in cls._clients:
            if provider == "openai":
                cls._clients[cache_key] = OpenAIClient(**kwargs)
            elif provider == "anthropic":
                cls._clients[cache_key] = AnthropicClient(**kwargs)
            elif provider == "baidu":
                cls._clients[cache_key] = BaiduClient(**kwargs)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        
        return cls._clients[cache_key]


def get_default_client() -> BaseLLMClient:
    """获取默认LLM客户端（从环境变量）"""
    if os.getenv("OPENAI_API_KEY"):
        return LLMFactory.get_client(
            "openai",
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4")
        )
    elif os.getenv("ANTHROPIC_API_KEY"):
        return LLMFactory.get_client(
            "anthropic",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus")
        )
    else:
        raise ValueError("No LLM API key found in environment")


# 简单缓存机制
class SimpleCache:
    """简单内存缓存"""
    
    def __init__(self, ttl: int = 3600):
        self._cache: Dict[str, tuple] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        self._cache[key] = (value, time.time())
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()


# 全局缓存实例
cache = SimpleCache()


if __name__ == "__main__":
    # 测试代码
    print("LLM API客户端工厂")
    print("支持的提供商：")
    print("1. OpenAI (GPT-4, GPT-3.5)")
    print("2. Anthropic (Claude 3)")
    print("3. 百度文心一言")
