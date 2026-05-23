#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成专业报告脚本
支持断点续传、进度监控、质量评分
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

from utils.database import get_supabase_client
from utils.api_client import DeepSeekClient

# 进度记录文件
PROGRESS_FILE = "data/generation_progress.json"
LOG_FILE = "logs/batch_generate.log"

# 确保目录存在
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)


def log(message: str, level: str = "INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def load_progress():
    """加载生成进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "generated": [],
        "failed": [],
        "skipped": [],
        "start_time": None,
        "last_update": None
    }


def save_progress(progress: dict):
    """保存进度"""
    progress["last_update"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def generate_single_report(major: dict, llm_client: DeepSeekClient) -> dict:
    """为单个专业生成报告"""
    major_name = major.get("name", "未知专业")
    major_code = major.get("code", "")
    log(f"开始生成报告: {major_name} ({major_code})")
    
    try:
        # 步骤1: 生成预览内容（免费部分）
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
            "price": 10,  # 默认10点数
            "is_premium": quality_score >= 75,
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        log(f"报告生成成功: {major_name}, 质量评分: {quality_score}")
        return report_data
        
    except Exception as e:
        log(f"生成报告失败: {major_name}, 错误: {str(e)}", "ERROR")
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


def save_report(db_client, report_data: dict):
    """保存报告到数据库"""
    try:
        # 检查是否已存在
        existing = db_client.get_report_by_code(report_data["major_code"])
        if existing:
            log(f"报告已存在，跳过: {report_data['major_name']}")
            return False
        
        # 保存到数据库
        db_client.create_report(report_data)
        log(f"报告已保存: {report_data['major_name']}")
        return True
        
    except Exception as e:
        log(f"保存报告失败: {report_data['major_name']}, 错误: {str(e)}", "ERROR")
        return False


def main():
    parser = argparse.ArgumentParser(description="批量生成专业报告")
    parser.add_argument("--start", type=int, default=1, help="起始专业ID")
    parser.add_argument("--end", type=int, default=None, help="结束专业ID")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="跳过已生成的")
    parser.add_argument("--test", action="store_true", help="测试模式，生成1个报告")
    
    args = parser.parse_args()
    
    # 初始化客户端
    db_client = get_supabase_client()
    llm_client = DeepSeekClient(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    )
    
    # 加载进度
    progress = load_progress()
    if not progress.get("start_time"):
        progress["start_time"] = datetime.now().isoformat()
    
    # 获取专业列表
    log("="*60)
    log("开始批量生成报告")
    log("="*60)
    
    majors = db_client.get_majors()
    log(f"共找到 {len(majors)} 个专业")
    
    # 如果是测试模式，只取第一个
    if args.test:
        majors = majors[:1]
        log("测试模式：只生成1个专业的报告")
    else:
        # 过滤范围
        if args.end:
            majors = [m for m in majors if args.start <= m.get("id", 0) <= args.end]
        else:
            majors = [m for m in majors if m.get("id", 0) >= args.start]
        
        log(f"本次生成 {len(majors)} 个专业")
    
    # 逐个生成
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for i, major in enumerate(majors, 1):
        major_id = major.get("id")
        major_code = major.get("code", "")
        major_name = major.get("name", "未知")
        
        log(f"[{i}/{len(majors)}] 处理: ID={major_id}, {major_name}")
        
        # 检查是否已生成
        if args.skip_existing and major_code in progress.get("generated", []):
            log(f"已生成，跳过: {major_name}")
            skip_count += 1
            continue
        
        try:
            # 生成报告
            report_data = generate_single_report(major, llm_client)
            
            # 保存到数据库
            saved = save_report(db_client, report_data)
            
            if saved:
                progress["generated"].append(major_code)
                success_count += 1
            else:
                progress["skipped"].append(major_code)
                skip_count += 1
            
            # 保存进度
            save_progress(progress)
            
            # 避免API限流，适当延迟
            if not args.test:
                time.sleep(1)
            
        except Exception as e:
            progress["failed"].append(major_code)
            fail_count += 1
            log(f"处理失败: {major_name}", "ERROR")
            
            # 保存进度
            save_progress(progress)
            
            # 失败后等待更久
            time.sleep(3)
    
    # 完成统计
    log("="*60)
    log("批量生成完成")
    log(f"成功: {success_count}")
    log(f"失败: {fail_count}")
    log(f"跳过: {skip_count}")
    log("="*60)
    
    # 测试模式下显示结果
    if args.test and success_count > 0:
        log("\n🎉 测试成功！")
        log("\n现在可以开始批量生成了！")
        log("\n建议的操作:")
        log("  1. 生成前5个: python scripts/batch_generate.py --start 1 --end 5")
        log("  2. 生成前50个: python scripts/batch_generate.py --start 1 --end 50")
        log("  3. 生成全部: python scripts/batch_generate.py --start 1")


if __name__ == "__main__":
    main()
