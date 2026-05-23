#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量监控与检查系统
提供报告质量评分、统计分析、问题报告等功能
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import DatabaseClient

# 报告输出目录
REPORTS_DIR = "data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


class QualityChecker:
    """质量检查器"""
    
    def __init__(self, db_client: DatabaseClient):
        self.db = db_client
    
    def check_report_quality(self, report: Dict) -> Dict:
        """检查单个报告的质量"""
        major_name = report.get('major_name', '未知')
        
        score = report.get('quality_score', 70)
        preview = report.get('preview_content', '')
        full = report.get('full_content', '')
        xuefeng = report.get('xuefeng_comment', '')
        
        issues = []
        detailed_scores = {}
        
        # 1. 长度检查
        if len(preview) < 200:
            issues.append("预览内容过短（<200字）")
            detailed_scores['preview_length'] = 5
        elif len(preview) > 600:
            detailed_scores['preview_length'] = 10
        else:
            detailed_scores['preview_length'] = 8
            
        if len(full) < 2000:
            issues.append("完整内容过短（<2000字）")
            detailed_scores['full_length'] = 4
        elif len(full) > 5000:
            detailed_scores['full_length'] = 10
        else:
            detailed_scores['full_length'] = 8
            
        if len(xuefeng) < 100:
            issues.append("雪峰点评过短（<100字）")
            detailed_scores['xuefeng_length'] = 4
        elif len(xuefeng) > 400:
            detailed_scores['xuefeng_length'] = 10
        else:
            detailed_scores['xuefeng_length'] = 8
        
        # 2. 内容完整性检查
        keywords = {
            'preview': ['简介', '课程', '就业'],
            'full': ['分析', '建议', '就业', '课程', '院校'],
            'xuefeng': ['报考', '选择', '建议']
        }
        
        for section, words in keywords.items():
            content = report.get(f"{section}_content", '') if section != 'xuefeng' else xuefeng
            found = sum(1 for w in words if w in content)
            if found < len(words) // 2:
                issues.append(f"{section}内容关键词不足")
            detailed_scores[f'{section}_keywords'] = found * 3
        
        # 3. 格式与结构检查
        if '1.' not in full and '一、' not in full:
            issues.append("完整内容缺少分段结构")
            detailed_scores['structure'] = 4
        else:
            detailed_scores['structure'] = 10
            
        # 计算总评分
        total_score = sum(detailed_scores.values()) / len(detailed_scores) * 10
        
        return {
            'major_name': major_name,
            'report_id': report.get('id'),
            'original_score': score,
            'calculated_score': round(total_score, 1),
            'issues': issues,
            'detailed_scores': detailed_scores,
            'needs_review': len(issues) > 0 or total_score < 70
        }
    
    def check_all_reports(self) -> List[Dict]:
        """检查所有报告的质量"""
        print("开始质量检查...")
        
        reports = self.db.get_all_reports()
        print(f"共找到 {len(reports)} 份报告")
        
        results = []
        for i, report in enumerate(reports, 1):
            if i % 20 == 0:
                print(f"检查进度: {i}/{len(reports)}")
            
            result = self.check_report_quality(report)
            results.append(result)
        
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(REPORTS_DIR, f"quality_check_{timestamp}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"质量检查完成，结果已保存到: {output_file}")
        return results
    
    def generate_statistics(self, check_results: List[Dict]) -> Dict:
        """生成质量统计报告"""
        total = len(check_results)
        needs_review = sum(1 for r in check_results if r['needs_review'])
        avg_score = sum(r['calculated_score'] for r in check_results) / total
        
        # 分数分布
        score_ranges = {
            '90-100': 0,
            '80-89': 0,
            '70-79': 0,
            '60-69': 0,
            '<60': 0
        }
        
        for r in check_results:
            score = r['calculated_score']
            if score >= 90:
                score_ranges['90-100'] += 1
            elif score >= 80:
                score_ranges['80-89'] += 1
            elif score >= 70:
                score_ranges['70-79'] += 1
            elif score >= 60:
                score_ranges['60-69'] += 1
            else:
                score_ranges['<60'] += 1
        
        # 常见问题统计
        issue_counts = {}
        for r in check_results:
            for issue in r['issues']:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        stats = {
            'total_reports': total,
            'needs_review': needs_review,
            'review_rate': round(needs_review / total * 100, 1),
            'average_score': round(avg_score, 1),
            'score_distribution': score_ranges,
            'common_issues': dict(sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            'generated_at': datetime.now().isoformat()
        }
        
        # 保存统计
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_file = os.path.join(REPORTS_DIR, f"quality_stats_{timestamp}.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        return stats
    
    def print_report(self, stats: Dict):
        """打印质量报告"""
        print("\n" + "="*60)
        print("专业星图 - 质量检查报告")
        print("="*60)
        print(f"报告总数: {stats['total_reports']}")
        print(f"平均质量评分: {stats['average_score']}")
        print(f"需审核报告: {stats['needs_review']} ({stats['review_rate']}%)")
        print("\n分数分布:")
        for range_name, count in stats['score_distribution'].items():
            percentage = count / stats['total_reports'] * 100
            print(f"  {range_name}: {count} ({percentage:.1f}%)")
        
        print("\n常见问题:")
        for issue, count in stats['common_issues'].items():
            print(f"  - {issue}: {count}次")
        
        print("\n" + "="*60)


class ReportExporter:
    """报告导出器"""
    
    def __init__(self, db_client: DatabaseClient):
        self.db = db_client
    
    def export_low_quality_reports(self, threshold: float = 70.0) -> List[Dict]:
        """导出低质量报告"""
        reports = self.db.get_all_reports()
        low_quality = []
        
        for report in reports:
            score = report.get('quality_score', 70)
            if score < threshold:
                low_quality.append(report)
        
        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(REPORTS_DIR, f"low_quality_{timestamp}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(low_quality, f, ensure_ascii=False, indent=2)
        
        print(f"导出 {len(low_quality)} 份低质量报告到: {output_file}")
        return low_quality


def main():
    parser = argparse.ArgumentParser(description="质量监控与检查系统")
    parser.add_argument("--check", action="store_true", help="执行质量检查")
    parser.add_argument("--stats", action="store_true", help="生成质量统计")
    parser.add_argument("--export-low", type=float, default=None, help="导出低于指定分数的报告")
    parser.add_argument("--full", action="store_true", help="执行完整检查流程")
    
    args = parser.parse_args()
    
    db = DatabaseClient()
    checker = QualityChecker(db)
    exporter = ReportExporter(db)
    
    if args.full:
        print("执行完整质量检查流程...")
        results = checker.check_all_reports()
        stats = checker.generate_statistics(results)
        checker.print_report(stats)
        exporter.export_low_quality_reports(70.0)
        
    elif args.check:
        results = checker.check_all_reports()
        stats = checker.generate_statistics(results)
        checker.print_report(stats)
        
    elif args.stats:
        reports = db.get_all_reports()
        results = [checker.check_report_quality(r) for r in reports]
        stats = checker.generate_statistics(results)
        checker.print_report(stats)
        
    elif args.export_low is not None:
        exporter.export_low_quality_reports(args.export_low)
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
