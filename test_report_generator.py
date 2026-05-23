#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告生成测试（不依赖数据库，使用本地数据）
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

from utils.api_client import DeepSeekClient

# 示例专业数据
SAMPLE_MAJORS = [
    {
        "code": "010101",
        "name": "哲学",
        "category": "01 哲学",
        "description": "哲学专业学习如何思考、推理和论证",
        "courses": "中国哲学史、西方哲学史、逻辑学、伦理学、美学",
        "employment": "公务员、编辑、教师、智库研究员",
    },
    {
        "code": "080901",
        "name": "计算机科学与技术",
        "category": "08 工学",
        "description": "研究计算机的设计、制造和应用的学科",
        "courses": "数据结构、算法、操作系统、计算机网络、数据库",
        "employment": "软件工程师、算法工程师、产品经理、数据分析师",
    },
    {
        "code": "100201",
        "name": "临床医学",
        "category": "10 医学",
        "description": "培养从事医疗、预防、保健等工作的医学人才",
        "courses": "人体解剖学、生理学、病理学、药理学、诊断学",
        "employment": "医生、医学科研人员、医疗管理",
    }
]


def generate_single_report(major: dict, llm_client: DeepSeekClient) -> dict:
    """为单个专业生成报告"""
    major_name = major.get("name", "未知专业")
    major_code = major.get("code", "")
    print(f"\n{'='*60}")
    print(f"开始生成报告: {major_name} ({major_code})")
    print(f"{'='*60}")
    
    try:
        # 步骤1: 生成预览内容（免费部分）
        print("\n[1/3] 生成预览内容...")
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
        
        # 步骤2: 生成完整内容（付费部分）
        print("\n[2/3] 生成完整分析...")
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
        
        # 步骤3: 生成雪峰点评（单独一段）
        print("\n[3/3] 生成雪峰点评...")
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
        
        # 计算质量评分（简单版）
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
        }
        
        print(f"\n✅ 报告生成成功! 质量评分: {quality_score}")
        return report_data
        
    except Exception as e:
        print(f"\n❌ 生成报告失败: {major_name}, 错误: {str(e)}")
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


def save_report_to_file(report_data: dict, filename: str = None):
    """保存报告到本地文件"""
    if not filename:
        filename = f"report_{report_data['major_code']}_{report_data['major_name']}.txt"
    
    os.makedirs("data/reports", exist_ok=True)
    filepath = os.path.join("data/reports", filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{'='*60}\n")
        f.write(f"专业报告: {report_data['major_name']}\n")
        f.write(f"专业代码: {report_data['major_code']}\n")
        f.write(f"分类: {report_data['category']}\n")
        f.write(f"质量评分: {report_data['quality_score']}\n")
        f.write(f"{'='*60}\n\n")
        
        f.write(f"【预览内容】\n{report_data['preview_content']}\n\n")
        f.write(f"【完整分析】\n{report_data['full_content']}\n\n")
        f.write(f"【雪峰点评】\n{report_data['xuefeng_comment']}\n")
    
    print(f"✅ 报告已保存到: {filepath}")
    return filepath


def main():
    print("="*60)
    print("专业报告生成器 - 本地测试版")
    print("="*60)
    
    # 初始化LLM客户端
    llm_client = DeepSeekClient(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    )
    
    # 选择第一个专业
    major = SAMPLE_MAJORS[1]  # 计算机科学与技术
    
    # 生成报告
    report = generate_single_report(major, llm_client)
    
    # 保存到文件
    save_report_to_file(report)
    
    # 显示预览
    print("\n" + "="*60)
    print("报告预览:")
    print("="*60)
    print(f"\n【雪峰点评】\n{report['xuefeng_comment'][:300]}...")
    
    print("\n" + "="*60)
    print("🎉 测试成功!")
    print("="*60)
    print("\n现在可以:")
    print("1. 查看 data/reports/ 目录下的完整报告")
    print("2. 修改代码批量生成更多专业报告")


if __name__ == "__main__":
    main()
