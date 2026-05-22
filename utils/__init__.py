"""
专业星图 AI Agent 系统工具包
"""

from .api_client import (
    BaseLLMClient,
    OpenAIClient,
    AnthropicClient,
    BaiduClient,
    LLMFactory,
    get_default_client,
    cache
)

from .database import (
    SupabaseClient,
    get_supabase_client,
    save_report_to_database,
    load_reports_from_database
)

__version__ = "1.0.0"

__all__ = [
    'BaseLLMClient',
    'OpenAIClient', 
    'AnthropicClient',
    'BaiduClient',
    'LLMFactory',
    'get_default_client',
    'cache',
    'SupabaseClient',
    'get_supabase_client',
    'save_report_to_database',
    'load_reports_from_database',
]
