#!/usr/bin/env python3
"""
简单测试DeepSeek API是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

import os

print("="*60)
print("DeepSeek API 测试")
print("="*60)

# 检查API密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("❌ 未找到 DEEPSEEK_API_KEY")
    print("请在 .env 文件中配置你的API密钥")
    sys.exit(1)

print(f"✅ 找到API密钥: {api_key[:10]}...")
print(f"✅ 使用模型: {os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')}")

# 测试API客户端
try:
    from utils.api_client import DeepSeekClient
    
    print("\n创建DeepSeek客户端...")
    client = DeepSeekClient(
        api_key=api_key,
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    )
    print("✅ 客户端创建成功")
    
    print("\n测试API调用（生成一条简单消息）...")
    test_prompt = "你好！请用一句话介绍一下自己。"
    
    response = client.generate(test_prompt)
    print("\n✅ API调用成功！")
    print(f"\n响应内容:")
    print("-"*60)
    print(response)
    print("-"*60)
    
    print("\n🎉 DeepSeek API 工作正常！")
    print("\n现在可以开始批量生成专业报告了。")
    print("\n建议的下一步:")
    print("  1. 测试单个报告: python scripts/batch_generate.py --test")
    print("  2. 生成前5个: python scripts/batch_generate.py --start 1 --end 5")
    print("  3. 生成前50个: python scripts/batch_generate.py --start 1 --end 50")
    print("  4. 生成全部611个: python scripts/batch_generate.py --start 1")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
