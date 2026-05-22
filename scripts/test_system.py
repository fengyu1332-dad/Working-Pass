#!/usr/bin/env python3
"""
系统测试脚本
用于验证AI Agent系统的各个组件是否正常工作
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """测试所有依赖是否正确安装"""
    print("\n" + "="*60)
    print("测试1: 依赖导入检查")
    print("="*60)
    
    modules = [
        ("requests", "HTTP请求库"),
        ("openai", "OpenAI API"),
        ("anthropic", "Anthropic API"),
        ("pydantic", "数据验证"),
        ("loguru", "日志工具"),
        ("tqdm", "进度条"),
    ]
    
    success = True
    for module, desc in modules:
        try:
            __import__(module)
            print(f"  ✅ {module:15s} - {desc}")
        except ImportError as e:
            print(f"  ❌ {module:15s} - {desc} (未安装: {e})")
            success = False
    
    return success


def test_config():
    """测试配置加载"""
    print("\n" + "="*60)
    print("测试2: 配置系统检查")
    print("="*60)
    
    try:
        from config import config, load_config_from_env, AGENT_PROMPTS
        
        print(f"  ✅ 配置模块导入成功")
        print(f"     - 环境: {config.environment.value}")
        print(f"     - LLM提供商: {config.llm.provider.value}")
        print(f"     - 模型: {config.llm.model}")
        print(f"     - 数据库: {bool(config.database.url)}")
        print(f"     - Agent配置: {config.agent.enable_cache}")
        
        # 检查Prompts
        print(f"\n  Agent Prompts:")
        for name in AGENT_PROMPTS.keys():
            print(f"     - {name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """测试数据库连接"""
    print("\n" + "="*60)
    print("测试3: 数据库连接检查")
    print("="*60)
    
    try:
        from utils.database import get_supabase_client
        
        client = get_supabase_client()
        print(f"  ✅ Supabase客户端创建成功")
        print(f"     - URL: {client.url}")
        
        # 测试查询
        reports = client.get_reports(limit=1)
        print(f"  ✅ 查询报告成功 (获取到 {len(reports)} 条)")
        
        majors = client.get_majors(limit=1)
        print(f"  ✅ 查询专业成功 (获取到 {len(majors)} 条)")
        
        # 获取统计信息
        reports_count = client.get_reports_count()
        majors_count = client.get_all_majors_count()
        print(f"\n  📊 数据库统计:")
        print(f"     - 专业总数: {majors_count}")
        print(f"     - 报告总数: {reports_count}")
        print(f"     - 待生成: {majors_count - reports_count}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_client():
    """测试LLM客户端"""
    print("\n" + "="*60)
    print("测试4: LLM客户端检查")
    print("="*60)
    
    try:
        from utils.api_client import LLMFactory
        import os
        
        # 检查是否有API密钥
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
        
        print(f"  API密钥状态:")
        print(f"     - OpenAI: {'✅ 已配置' if has_openai else '⚠️ 未配置'}")
        print(f"     - Anthropic: {'✅ 已配置' if has_anthropic else '⚠️ 未配置'}")
        
        if not (has_openai or has_anthropic):
            print(f"\n  ⚠️ 警告: 没有配置任何LLM API密钥")
            print(f"     请在 .env 文件中配置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
            return False
        
        # 尝试创建客户端
        if has_openai:
            client = LLMFactory.get_client(
                "openai",
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-3.5-turbo"  # 使用便宜的模型测试
            )
            print(f"  ✅ OpenAI客户端创建成功")
        else:
            client = LLMFactory.get_client(
                "anthropic",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model="claude-3-haiku-20240307"
            )
            print(f"  ✅ Anthropic客户端创建成功")
        
        return True
        
    except Exception as e:
        print(f"  ❌ LLM客户端测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_system():
    """测试Agent系统（演示模式，不调用真实API）"""
    print("\n" + "="*60)
    print("测试5: Agent系统检查（演示模式）")
    print("="*60)
    
    try:
        # 测试Agent导入
        from ai_agent_demo import (
            DataCollectionAgent,
            DeepAnalysisAgent,
            XuefengCommentAgent,
            ComposerAgent,
            QualityAssuranceAgent,
            CoordinatorAgent
        )
        
        print(f"  ✅ 所有Agent模块导入成功")
        
        # 创建Agent实例
        data_agent = DataCollectionAgent()
        analysis_agent = DeepAnalysisAgent()
        comment_agent = XuefengCommentAgent()
        composer = ComposerAgent()
        qa_agent = QualityAssuranceAgent()
        coordinator = CoordinatorAgent()
        
        print(f"  ✅ Agent实例创建成功")
        
        # 运行演示（只运行一次，避免API调用）
        print(f"\n  🚀 运行演示测试...")
        
        result = coordinator.run({
            "major_code": "080901",
            "major_name": "计算机科学与技术",
            "category": "08 工学"
        })
        
        print(f"\n  📊 演示结果:")
        print(f"     - 任务ID: {result.get('task_id')}")
        print(f"     - 状态: {result.get('status').value}")
        print(f"     - 质量等级: {result.get('quality_score', 'N/A').value if result.get('quality_score') else 'N/A'}")
        print(f"     - 评分: {result.get('score_value', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quality_system():
    """测试质量评分系统"""
    print("\n" + "="*60)
    print("测试6: 质量评分系统检查")
    print("="*60)
    
    try:
        from ai_agent_demo import QualityScore
        
        print(f"  质量等级定义:")
        for level in QualityScore:
            print(f"     - {level.value}: {level.name}")
        
        # 测试评分
        from ai_agent_demo import QualityAssuranceAgent
        
        qa_agent = QualityAssuranceAgent()
        
        # 测试样本1：高质量报告
        high_quality_report = """
## 专业概述
计算机科学与技术是研究计算机的设计、制造和应用的学科...

## 课程安排
大一: 高等数学, 线性代数, C语言...
大二: 数据结构, 算法, 操作系统...

## 就业前景
就业前景广阔，可在IT行业、金融、电信等领域...

## 薪资范畴
¥15k-40k

## 雪峰点评
计算机专业是现在最火的专业之一...
        """
        
        # 测试样本2：低质量报告
        low_quality_report = """
## 专业概述
计算机专业很好。
        """
        
        # 评分
        score1, level1 = qa_agent._evaluate_quality(high_quality_report)
        score2, level2 = qa_agent._evaluate_quality(low_quality_report)
        
        print(f"\n  评分测试:")
        print(f"     - 高质量报告: {score1}分 ({level1.value}级)")
        print(f"     - 低质量报告: {score2}分 ({level2.value}级)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 质量评分系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results: dict):
    """打印测试总结"""
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n  通过: {passed}/{total}")
    
    if passed == total:
        print("\n  🎉 所有测试通过！系统已准备就绪。")
        print("\n  下一步操作:")
        print("     1. 运行演示: python ai_agent_demo.py")
        print("     2. 生成报告: python scripts/batch_generate.py --start 1 --end 10")
        print("     3. 查看文档: cat docs/QUICK_START.md")
    else:
        print("\n  ⚠️  部分测试失败，请检查上述错误信息。")
        print("\n  常见问题排查:")
        print("     1. 依赖安装: pip install -r requirements.txt")
        print("     2. API密钥: 检查 .env 文件")
        print("     3. 数据库: 检查 SUPABASE_URL 和 SUPABASE_KEY")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    print("\n" + "="*60)
    print("专业星图 AI Agent 系统 - 测试套件")
    print("="*60)
    
    tests = {
        "依赖检查": test_imports,
        "配置系统": test_config,
        "数据库连接": test_database,
        "LLM客户端": test_llm_client,
        "Agent系统": test_agent_system,
        "质量评分": test_quality_system,
    }
    
    results = {}
    
    for name, test_func in tests.items():
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n  ❌ {name} 执行出错: {e}")
            results[name] = False
        
        # 测试之间添加小延迟
        time.sleep(0.5)
    
    print_summary(results)
    
    # 返回成功/失败状态
    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
