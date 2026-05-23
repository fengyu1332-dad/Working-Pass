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

from config import config
from utils.database import DatabaseClient
from utils.api_client import DeepSeekClient

# 进度记录文件
PROGRESS_FILE = "data/generation_progress.json"
LOG_FILE = "logs/batch_generate.log"

# 确保目录存在
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)


class BatchReportGenerator:
    """批量报告生成器"""
    
    def __init__(self, db_client: DatabaseClient, llm_client: DeepSeekClient):
        self.db = db_client
        self.llm = llm_client
        self.progress = self._load_progress()
        
    def _load_progress(self):
        """加载生成进度"""
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "generated": [],
            "failed": [],
            "skipped": [],
            "start_time": None,
            "last_update": None
        }
        
    def _save_progress(self):
        """保存进度"""
        self.progress["last_update"] = datetime.now().isoformat()
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
            
    def _log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}\n"
        print(log_line.strip())
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def generate_report_for_major(self, major: dict) -> dict:
        """为单个专业生成报告（简化版，实际应用应使用完整AI Agent系统）"""
        major_name = major.get('name', '未知专业')
        self._log(f"开始生成报告: {major_name}")
        
        try:
            # 步骤1: 准备数据
            base_info = {
                "name": major.get('name', ''),
                "category": major.get('category', ''),
                "description": major.get('description', ''),
                "courses": major.get('courses', ''),
                "employment": major.get('employment', ''),
                "universities": major.get('universities', '')
            }
            
            # 步骤2: 生成预览内容（免费部分）
            preview_prompt = f"""
            你是一个专业的教育分析师，请为"{base_info['name']}"专业生成一个免费的预览内容，
            包含：专业简介、核心课程摘要、就业前景概述。

            要求：
            1. 内容简洁明了，约300-500字
            2. 客观准确，有参考价值
            3. 不要涉及需要付费的深度分析

            基础信息：
            {json.dumps(base_info, ensure_ascii=False, indent=2)}
            """
            
            preview_content = self.llm.generate(preview_prompt, temperature=0.7)
            
            # 步骤3: 生成完整内容（付费部分）
            full_prompt = f"""
            你是张雪峰，一位知名的高考志愿填报专家。请为"{base_info['name']}"专业生成一份
            深度分析报告。

            报告结构：
            1. 专业深度解析（1000-1500字）
            2. 课程体系详解
            3. 就业趋势分析
            4. 院校选择指南
            5. 雪峰点评（以张雪峰老师的风格进行点评，风趣幽默但客观实用）

            基础信息：
            {json.dumps(base_info, ensure_ascii=False, indent=2)}

            请用专业、实用、接地气的语言撰写，总字数约3000-4000字。
            """
            
            full_content = self.llm.generate(full_prompt, temperature=0.8)
            
            # 步骤4: 质量评分（简单实现）
            quality_score = self._calculate_quality_score(preview_content, full_content)
            
            # 步骤5: 雪峰点评
            xuefeng_comment_prompt = f"""
            作为张雪峰老师，请为"{base_info['name']}"专业写一段点评。
            要求：
            1. 风格风趣幽默，像聊天一样
            2. 200-300字
            3. 有实用的报考建议
            4. 突出重点，不啰嗦
            """
            
            xuefeng_comment = self.llm.generate(xuefeng_comment_prompt, temperature=0.9)
            
            report_data = {
                "major_id": major.get('id'),
                "major_name": major_name,
                "preview_content": preview_content,
                "full_content": full_content,
                "xuefeng_comment": xuefeng_comment,
                "quality_score": quality_score,
                "price": 10,  # 默认10点数
                "is_premium": quality_score >= 80,
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            self._log(f"报告生成成功: {major_name}, 质量评分: {quality_score}")
            return report_data
            
        except Exception as e:
            self._log(f"生成报告失败: {major_name}, 错误: {str(e)}", "ERROR")
            raise
    
    def _calculate_quality_score(self, preview: str, full: str) -> int:
        """简单的质量评分"""
        score = 70  # 基础分
        
        # 长度评分
        if len(preview) > 400:
            score += 5
        if len(full) > 3000:
            score += 10
        
        # 关键词检查
        keywords = ['分析', '建议', '就业', '课程', '院校', '选择']
        found = sum(1 for kw in keywords if kw in full)
        score += found * 2
        
        return min(100, score)
    
    def save_report_to_db(self, report_data: dict):
        """保存报告到数据库"""
        try:
            # 检查是否已存在
            existing = self.db.get_report_by_major_id(report_data['major_id'])
            if existing:
                self._log(f"报告已存在，跳过: {report_data['major_name']}")
                return False
            
            # 保存到数据库
            self.db.create_report(report_data)
            self._log(f"报告已保存: {report_data['major_name']}")
            return True
            
        except Exception as e:
            self._log(f"保存报告失败: {report_data['major_name']}, 错误: {str(e)}", "ERROR")
            return False
    
    def generate_batch(self, start_id: int = 1, end_id: int = None, skip_existing: bool = True):
        """批量生成报告"""
        self._log("=" * 60)
        self._log("开始批量生成报告")
        self._log(f"范围: ID {start_id} - {end_id or '全部'}")
        self._log("=" * 60)
        
        # 记录开始时间
        if not self.progress.get("start_time"):
            self.progress["start_time"] = datetime.now().isoformat()
        
        # 获取专业列表
        majors = self.db.get_all_majors()
        self._log(f"共找到 {len(majors)} 个专业")
        
        # 过滤范围
        if end_id:
            majors = [m for m in majors if start_id <= m.get('id', 0) <= end_id]
        else:
            majors = [m for m in majors if m.get('id', 0) >= start_id]
        
        self._log(f"本次生成 {len(majors)} 个专业")
        
        # 逐个生成
        success_count = 0
        fail_count = 0
        skip_count = 0
        
        for i, major in enumerate(majors, 1):
            major_id = major.get('id')
            major_name = major.get('name', '未知')
            
            self._log(f"[{i}/{len(majors)}] 处理: ID={major_id}, {major_name}")
            
            # 检查是否已生成
            if skip_existing and str(major_id) in self.progress.get("generated", []):
                self._log(f"已生成，跳过: {major_name}")
                skip_count += 1
                continue
            
            try:
                # 生成报告
                report_data = self.generate_report_for_major(major)
                
                # 保存到数据库
                saved = self.save_report_to_db(report_data)
                
                if saved:
                    self.progress["generated"].append(str(major_id))
                    success_count += 1
                else:
                    self.progress["skipped"].append(str(major_id))
                    skip_count += 1
                
                # 保存进度
                self._save_progress()
                
                # 避免API限流，稍作等待
                time.sleep(1)
                
            except Exception as e:
                self.progress["failed"].append(str(major_id))
                fail_count += 1
                self._log(f"处理失败: {major_name}", "ERROR")
                
                # 保存进度
                self._save_progress()
                
                # 等待更长时间
                time.sleep(3)
        
        # 完成统计
        self._log("=" * 60)
        self._log("批量生成完成")
        self._log(f"成功: {success_count}")
        self._log(f"失败: {fail_count}")
        self._log(f"跳过: {skip_count}")
        self._log("=" * 60)
        
        return {
            "success": success_count,
            "failed": fail_count,
            "skipped": skip_count,
            "total": len(majors)
        }


def main():
    parser = argparse.ArgumentParser(description="批量生成专业报告")
    parser.add_argument("--start", type=int, default=1, help="起始专业ID")
    parser.add_argument("--end", type=int, default=None, help="结束专业ID")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="跳过已生成的")
    parser.add_argument("--test", action="store_true", help="测试模式，生成1个报告")
    
    args = parser.parse_args()
    
    # 初始化客户端
    db = DatabaseClient()
    llm = DeepSeekClient()
    
    # 创建生成器
    generator = BatchReportGenerator(db, llm)
    
    if args.test:
        print("测试模式：获取第一个专业并生成报告...")
        majors = db.get_all_majors()
        if majors:
            first_major = majors[0]
            print(f"测试专业: {first_major.get('name')}")
            report = generator.generate_report_for_major(first_major)
            print("\n生成成功！")
            print(f"质量评分: {report['quality_score']}")
            print(f"预览内容长度: {len(report['preview_content'])}")
            print(f"完整内容长度: {len(report['full_content'])}")
            print("\n雪峰点评:")
            print(report['xuefeng_comment'][:200] + "...")
        else:
            print("未找到专业数据")
    else:
        # 批量生成
        result = generator.generate_batch(
            start_id=args.start,
            end_id=args.end,
            skip_existing=args.skip_existing
        )
        
        print(f"\n生成结果: {result}")


if __name__ == "__main__":
    main()
