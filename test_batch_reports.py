#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告生成测试 - 批量测试5个不同专业
验证质量一致性和风格稳定性
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

from utils.api_client import DeepSeekClient


# 测试专业列表（包含不同类型）
TEST_MAJORS = [
    {
        "code": "080901",
        "name": "计算机科学与技术",
        "category": "08 工学",
        "description": "研究计算机的设计、制造和应用",
        "courses": "数据结构、算法、操作系统、计算机网络、数据库",
        "employment": "软件工程师、算法工程师、产品经理、数据分析师"
    },
    {
        "code": "100201",
        "name": "临床医学",
        "category": "10 医学",
        "description": "培养从事医疗、预防、保健等工作的医学人才",
        "courses": "人体解剖学、生理学、病理学、药理学、诊断学、内科学、外科学",
        "employment": "临床医生、医学研究员、医疗管理、医疗机构"
    },
    {
        "code": "030101",
        "name": "法学",
        "category": "03 法学",
        "description": "研究法律现象、法律规范和法律实践",
        "courses": "法理学、宪法学、刑法学、民法学、商法学、刑事诉讼法、民事诉讼法",
        "employment": "律师、法官、检察官、法律顾问、企业法务"
    },
    {
        "code": "020401",
        "name": "新闻学",
        "category": "02 文学",
        "description": "研究新闻传播规律和新闻工作实务",
        "courses": "新闻学概论、传播学、新闻采访、新闻写作、新闻编辑、广播电视新闻学",
        "employment": "记者、编辑、主播、媒体策划、公关专员"
    },
    {
        "code": "020301",
        "name": "金融学",
        "category": "02 经济学",
        "description": "研究货币、金融市场、金融机构及金融政策",
        "courses": "货币银行学、国际金融、证券投资学、公司金融、金融工程、保险学",
        "employment": "银行、证券、基金、保险、信托、金融监管"
    }
]


def generate_single_report(major: dict, llm_client: DeepSeekClient, index: int) -> dict:
    """为单个专业生成报告"""
    major_name = major.get("name", "未知专业")
    major_code = major.get("code", "")
    print(f"\n{'='*60}")
    print(f"[{index}/5] 开始生成: {major_name} ({major_code})")
    print(f"{'='*60}")
    
    try:
        # 步骤1: 生成预览内容
        print(f"[{index}/5][1/3] 生成预览内容...")
        preview_prompt = f"""你是一个专业的教育分析师。请为"{major_name}"专业生成一个简洁的预览内容。

要求：
1. 内容包括：专业简介、核心课程摘要、就业前景概述
2. 字数约300-500字
3. 语言通俗易懂，有参考价值

专业信息：
- 专业名称：{major_name}
- 专业代码：{major_code}
- 所属分类：{major.get('category', '')}
- 现有描述：{major.get('description', '')}
"""
        
        preview_content = llm_client.generate(preview_prompt, temperature=0.7)
        
        # 步骤2: 生成完整内容
        print(f"[{index}/5][2/3] 生成完整分析...")
        full_prompt = f"""你是张雪峰，一位深受学生喜爱的高考志愿填报专家。请为"{major_name}"专业生成一份深度分析报告。

请按照以下结构撰写：

## 一、专业概述
（150-200字，详细介绍这个专业学什么）

## 二、课程安排
（分年级列出核心课程，4-6门课程/年级）

## 三、就业前景
（200-300字，包括就业方向、行业发展、岗位需求等）

## 四、薪资范畴
（给出具体的数字范围，如：¥8k-20k/月）

## 五、雪峰点评
（张雪峰老师的风格：幽默、接地气、实用，200-300字）

专业信息：
- 专业名称：{major_name}
- 专业代码：{major_code}
- 所属分类：{major.get('category', '')}
- 现有描述：{major.get('description', '')}
- 现有课程：{major.get('courses', '')}
- 就业信息：{major.get('employment', '')}

请用中文撰写，语言要专业、实用、接地气。
"""
        
        full_content = llm_client.generate(full_prompt, temperature=0.8)
        
        # 步骤3: 生成雪峰点评
        print(f"[{index}/5][3/3] 生成雪峰点评...")
        xuefeng_prompt = f"""你是张雪峰，一位深受学生喜爱的高考志愿填报专家。请为"{major_name}"专业写一段点评。

要求：
1. 风格：幽默、接地气、像和学生聊天一样
2. 内容要真实，不要假大空
3. 给出实用的报考建议
4. 200-300字

专业信息：
- 专业名称：{major_name}
- 专业代码：{major_code}
- 就业前景：{major.get('employment', '')}
"""
        
        xuefeng_comment = llm_client.generate(xuefeng_prompt, temperature=0.9)
        
        # 计算质量评分
        quality_score = calculate_quality_score(preview_content, full_content, xuefeng_comment)
        
        # 准备报告数据
        report_data = {
            "major_code": major_code,
            "major_name": major_name,
            "category": major.get("category", ""),
            "preview_content": preview_content,
            "full_content": full_content,
            "xuefeng_comment": xuefeng_comment,
            "quality_score": quality_score,
            "price": 10,
            "is_premium": quality_score >= 75,
            "generated_at": datetime.now().isoformat()
        }
        
        print(f"[{index}/5] ✅ 报告生成成功! 质量评分: {quality_score}")
        return report_data
        
    except Exception as e:
        print(f"[{index}/5] ❌ 生成失败: {str(e)}")
        raise


def calculate_quality_score(preview: str, full: str, xuefeng: str) -> int:
    """计算质量评分"""
    score = 60  # 基础分
    
    # 长度评分
    if len(preview) > 300:
        score += 5
    if len(full) > 1500:
        score += 10
    if len(xuefeng) > 150:
        score += 5
    
    # 关键词检查
    keywords = ["课程", "就业", "前景", "建议", "报考", "薪资", "专业"]
    found = sum(1 for kw in keywords if kw in full)
    score += found * 3
    
    return min(100, score)


def save_report_to_file(report_data: dict) -> str:
    """保存报告到文件"""
    os.makedirs("data/reports", exist_ok=True)
    filename = f"report_{report_data['major_code']}_{report_data['major_name']}.txt"
    filepath = os.path.join("data/reports", filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{'='*60}\n")
        f.write(f"专业报告: {report_data['major_name']}\n")
        f.write(f"专业代码: {report_data['major_code']}\n")
        f.write(f"分类: {report_data['category']}\n")
        f.write(f"质量评分: {report_data['quality_score']}\n")
        f.write(f"生成时间: {report_data['generated_at']}\n")
        f.write(f"{'='*60}\n\n")
        
        f.write(f"【预览内容】\n{report_data['preview_content']}\n\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"【完整分析】\n{report_data['full_content']}\n\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"【雪峰点评】\n{report_data['xuefeng_comment']}\n")
    
    return filepath


def generate_summary(reports: list) -> dict:
    """生成测试总结"""
    scores = [r['quality_score'] for r in reports]
    avg_score = sum(scores) / len(scores)
    
    # 分类统计
    categories = {}
    for r in reports:
        cat = r['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)
    
    summary = {
        "total_reports": len(reports),
        "average_score": round(avg_score, 1),
        "min_score": min(scores),
        "max_score": max(scores),
        "scores": scores,
        "categories": {cat: len(majors) for cat, majors in categories.items()},
        "all_passed": all(score >= 70 for score in scores),
        "quality_grade": "A" if avg_score >= 90 else "B" if avg_score >= 75 else "C"
    }
    
    return summary


def print_summary(summary: dict, reports: list):
    """打印测试总结"""
    print("\n" + "="*60)
    print("📊 批量测试总结")
    print("="*60)
    
    print(f"\n🎯 总体评分: {summary['average_score']}/100 ({summary['quality_grade']}级)")
    print(f"✅ 最高分: {summary['max_score']}/100")
    print(f"⚠️  最低分: {summary['min_score']}/100")
    print(f"📋 质量达标: {'✅ 全部通过' if summary['all_passed'] else '❌ 部分未达标'}")
    
    print(f"\n📁 分类统计:")
    for cat, count in summary['categories'].items():
        print(f"   - {cat}: {count} 个专业")
    
    print(f"\n📊 各专业评分:")
    for i, r in enumerate(reports, 1):
        score = r['quality_score']
        status = "✅" if score >= 75 else "⚠️" if score >= 60 else "❌"
        print(f"   {i}. {r['major_name']}: {score}/100 {status}")
    
    print("\n" + "="*60)
    
    # 质量评价
    if summary['quality_grade'] == 'A':
        print("🎉 优秀！报告质量非常高，可以直接使用！")
    elif summary['quality_grade'] == 'B':
        print("👍 良好！报告质量可以接受，个别地方可微调。")
    else:
        print("⚠️  一般！建议优化提示词后再生成。")
    
    print("\n📂 报告文件已保存到: data/reports/")
    print("="*60)


def main():
    print("="*60)
    print("专业报告批量测试 - 5个不同专业")
    print("="*60)
    print(f"\n测试专业列表:")
    for i, major in enumerate(TEST_MAJORS, 1):
        print(f"  {i}. {major['name']} ({major['category']})")
    print()
    
    # 初始化LLM客户端
    llm_client = DeepSeekClient(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    )
    
    # 批量生成报告
    reports = []
    start_time = datetime.now()
    
    for i, major in enumerate(TEST_MAJORS, 1):
        try:
            report = generate_single_report(major, llm_client, i)
            filepath = save_report_to_file(report)
            reports.append(report)
            print(f"[{i}/5] ✅ 已保存: {filepath}")
            
            # 适当延迟避免API限流
            if i < len(TEST_MAJORS):
                print(f"[{i}/5] 等待2秒...")
                import time
                time.sleep(2)
                
        except Exception as e:
            print(f"[{i}/5] ❌ 失败: {str(e)}")
            continue
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # 生成总结
    if reports:
        summary = generate_summary(reports)
        print_summary(summary, reports)
        
        print(f"\n⏱️  总耗时: {int(duration)} 秒")
        print(f"📊 平均每份: {int(duration/len(reports))} 秒")
        print(f"💰 预计成本: ¥{len(reports) * 0.1:.2f}")
        
        # 保存测试报告
        summary_filepath = "data/reports/test_summary.json"
        os.makedirs("data/reports", exist_ok=True)
        with open(summary_filepath, "w", encoding="utf-8") as f:
            import json
            f.write(json.dumps({
                "summary": summary,
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False, indent=2))
        
        print(f"\n✅ 测试报告已保存: {summary_filepath}")
    else:
        print("\n❌ 没有成功生成任何报告！")


if __name__ == "__main__":
    main()
