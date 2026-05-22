#!/usr/bin/env python3
"""
专业星图 AI Agent 系统配置文件
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum


class LLMProvider(Enum):
    """LLM提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    BAIDU = "baidu"
    ALIBABA = "alibaba"
    LOCAL = "local"


class Environment(Enum):
    """运行环境"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: LLMProvider = LLMProvider.OPENAI
    model: str = "gpt-4"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    retry_times: int = 3


@dataclass
class AgentConfig:
    """Agent配置"""
    enable_cache: bool = True
    cache_ttl: int = 86400  # 24小时
    retry_times: int = 3
    timeout: int = 60
    log_level: str = "INFO"


@dataclass
class DatabaseConfig:
    """数据库配置"""
    url: str = ""
    anon_key: str = ""
    service_key: str = ""
    table_reports: str = "reports"
    table_majors: str = "majors"


@dataclass
class RateLimitConfig:
    """速率限制配置"""
    requests_per_minute: int = 60
    tokens_per_minute: int = 100000
    concurrent_requests: int = 5


@dataclass
class QualityConfig:
    """质量配置"""
    min_score_threshold: int = 60
    auto_retry_on_low_score: bool = True
    enable_human_review: bool = False
    human_review_threshold: int = 75


@dataclass
class SystemConfig:
    """系统配置"""
    environment: Environment = Environment.DEVELOPMENT
    llm: LLMConfig = field(default_factory=LLMConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)
    log_file: str = "ai_agent.log"


def load_config_from_env() -> SystemConfig:
    """从环境变量加载配置"""
    config = SystemConfig()
    
    # 加载LLM配置
    if os.getenv("OPENAI_API_KEY"):
        config.llm.provider = LLMProvider.OPENAI
        config.llm.api_key = os.getenv("OPENAI_API_KEY")
        config.llm.model = os.getenv("OPENAI_MODEL", "gpt-4")
    elif os.getenv("ANTHROPIC_API_KEY"):
        config.llm.provider = LLMProvider.ANTHROPIC
        config.llm.api_key = os.getenv("ANTHROPIC_API_KEY")
        config.llm.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus")
    
    # 加载数据库配置
    config.database.url = os.getenv("SUPABASE_URL", "")
    config.database.anon_key = os.getenv("SUPABASE_KEY", "")
    
    # 加载环境
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        config.environment = Environment.PRODUCTION
    elif env == "testing":
        config.environment = Environment.TESTING
    
    # 加载日志级别
    config.agent.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    return config


# 全局配置实例
config = load_config_from_env()


# Agent系统Prompt模板
AGENT_PROMPTS = {
    "data_collection": """你是一个专业的数据收集专家。请根据以下信息，补充并完善专业数据。

专业名称：{major_name}
专业代码：{major_code}
所属分类：{category}

现有数据：
{existing_data}

请补充以下缺失信息（如果现有数据已有，则直接使用）：
1. 专业概述（200-300字）
2. 适合人群（100字以内）
3. 就业前景（150-200字）
4. 薪资范围（具体数字）
5. 四年课程安排（分年级列出核心课程）

请以JSON格式返回完整数据。
""",

    "deep_analysis": """你是一个教育和职业发展专家。请对{major_name}专业进行深度分析。

专业基础数据：
{major_data}

请从以下维度进行深度分析：
1. 学科定位（150字）
2. 核心能力培养（200字）
3. 行业发展趋势（200字）
4. 就业市场分析（250字）
5. 职业发展路径（200字）
6. 技能要求（150字）

每个维度都要提供有价值的见解，不要过于空泛。
""",

    "xuefeng_comment": """你是张雪峰，一位深受学生喜爱的高考志愿填报专家。请对{major_name}专业进行点评。

专业数据：
{major_data}

请按照以下结构撰写点评：
【先说"痛点"】
1. 这个专业可能面临的问题或挑战
2. 就业、考研等方面的现实情况

【但也有优势】
1. 这个专业的优势和亮点
2. 适合报考的理由

【报考建议】
1. 什么样的学生适合报考
2. 填报志愿时的注意事项

【总结】
一句话总结

要求：
- 用口语化的表达，像和学生聊天一样
- 要真实、接地气，不要假大空
- 可以适当幽默，但不要过度
- 给出的建议要切实可行
- 字数控制在800-1200字
""",

    "quality_check": """你是一位专业的内容审核专家。请检查以下报告内容，并进行必要的修正。

报告内容：
{report_content}

请检查：
1. 内容是否完整
2. 信息是否准确
3. 逻辑是否通顺
4. 语言是否流畅
5. 格式是否规范

如果发现问题，请进行修正并返回修正后的完整报告。
如果没有问题，请直接返回原报告。
"""
}


# 报告质量评分权重
QUALITY_WEIGHTS = {
    "completeness": 0.2,      # 内容完整性
    "accuracy": 0.2,          # 信息准确性
    "depth": 0.2,            # 深度分析
    "practicality": 0.2,      # 实用性
    "expression": 0.1,        # 语言表达
    "format": 0.1            # 格式规范
}


# 报告内容结构模板
REPORT_TEMPLATE = """# {major_name}专业深度分析报告

## 一、专业概述
{overview}

## 二、课程安排
{curriculum}

## 三、就业前景
{career_outlook}

## 四、薪资范畴
{salary_range}

## 五、适合人群
{suitable_for}

## 六、顶级院校推荐
{top_universities}

## 七、深度分析
{deep_analysis}

## 八、雪峰点评
{xuefeng_comment}

---
*报告生成时间：{generated_at}*
*质量评分：{quality_score}*
"""


if __name__ == "__main__":
    # 测试配置加载
    print("当前配置：")
    print(f"环境: {config.environment.value}")
    print(f"LLM提供商: {config.llm.provider.value}")
    print(f"模型: {config.llm.model}")
    print(f"数据库: {config.database.url}")
