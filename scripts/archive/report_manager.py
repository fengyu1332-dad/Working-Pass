#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 - 报告文件管理工具 v1.0
提供报告的查询、统计、管理功能
作者：专业星图团队
日期：2026-05-23
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime


REPORTS_DIR = Path("/workspace/data/reports")


class ReportManager:
    """报告管理类"""
    
    def __init__(self, reports_dir=None):
        self.reports_dir = Path(reports_dir) if reports_dir else REPORTS_DIR
        if not self.reports_dir.exists():
            raise FileNotFoundError(f"报告目录不存在: {self.reports_dir}")
    
    def list_all_reports(self):
        """列出所有报告"""
        reports = []
        
        for txt_file in self.reports_dir.glob("report_*.txt"):
            major_code, major_name = self._parse_filename(txt_file.name)
            pdf_file = self.reports_dir / txt_file.name.replace('.txt', '.pdf')
            
            reports.append({
                'code': major_code,
                'name': major_name,
                'txt': txt_file.exists(),
                'pdf': pdf_file.exists(),
                'txt_size': txt_file.stat().st_size if txt_file.exists() else 0,
                'pdf_size': pdf_file.stat().st_size if pdf_file.exists() else 0,
                'txt_path': str(txt_file),
                'pdf_path': str(pdf_file) if pdf_file.exists() else None
            })
        
        return sorted(reports, key=lambda x: x['code'])
    
    def _parse_filename(self, filename):
        """解析文件名获取专业代码和名称"""
        # report_080901_计算机科学与技术.txt → 080901, 计算机科学与技术
        name = filename.replace('report_', '').replace('.txt', '').replace('.pdf', '')
        parts = name.split('_', 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return None, name
    
    def search_by_name(self, keyword):
        """按专业名称搜索"""
        reports = self.list_all_reports()
        keyword = keyword.lower()
        return [r for r in reports if keyword in r['name'].lower()]
    
    def get_by_code(self, major_code):
        """按专业代码获取报告"""
        reports = self.list_all_reports()
        for r in reports:
            if r['code'] == major_code:
                return r
        return None
    
    def check_integrity(self):
        """检查完整性"""
        reports = self.list_all_reports()
        issues = []
        
        for r in reports:
            if not r['txt']:
                issues.append(f"缺少TXT: {r['code']} {r['name']}")
            if not r['pdf']:
                issues.append(f"缺少PDF: {r['code']} {r['name']}")
        
        return {
            'total': len(reports),
            'complete': sum(1 for r in reports if r['txt'] and r['pdf']),
            'issues': issues
        }
    
    def get_statistics(self):
        """获取统计信息"""
        reports = self.list_all_reports()
        integrity = self.check_integrity()
        
        total_txt_size = sum(r['txt_size'] for r in reports)
        total_pdf_size = sum(r['pdf_size'] for r in reports)
        
        return {
            'total_reports': len(reports),
            'complete_reports': integrity['complete'],
            'total_txt_size': total_txt_size,
            'total_pdf_size': total_pdf_size,
            'total_size': total_txt_size + total_pdf_size,
            'reports': reports
        }
    
    def export_summary(self, output_file):
        """导出摘要到JSON文件"""
        stats = self.get_statistics()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        return output_file


def main():
    parser = argparse.ArgumentParser(description="专业星图 - 报告文件管理工具")
    parser.add_argument('--list', action='store_true', help='列出所有报告')
    parser.add_argument('--search', type=str, help='按名称搜索报告')
    parser.add_argument('--get', type=str, help='按专业代码获取报告')
    parser.add_argument('--check', action='store_true', help='检查报告完整性')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--export', type=str, help='导出摘要到JSON文件')
    
    args = parser.parse_args()
    
    try:
        manager = ReportManager()
        
        if args.list:
            reports = manager.list_all_reports()
            print_reports_list(reports)
        
        elif args.search:
            results = manager.search_by_name(args.search)
            print(f"\n搜索 '{args.search}' 找到 {len(results)} 个报告:\n")
            print_reports_list(results)
        
        elif args.get:
            report = manager.get_by_code(args.get)
            if report:
                print_report_detail(report)
            else:
                print(f"未找到专业代码为 {args.get} 的报告")
        
        elif args.check:
            integrity = manager.check_integrity()
            print_integrity_check(integrity)
        
        elif args.stats:
            stats = manager.get_statistics()
            print_statistics(stats)
        
        elif args.export:
            output_file = manager.export_summary(args.export)
            print(f"摘要已导出到: {output_file}")
        
        else:
            # 默认显示统计信息和报告列表
            stats = manager.get_statistics()
            print_statistics(stats)
            print("\n报告列表:")
            print_reports_list(stats['reports'])
    
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


def print_reports_list(reports):
    """打印报告列表"""
    print(f"{'代码':<10} {'专业名称':<20} {'TXT':<5} {'PDF':<5} {'TXT大小':<10} {'PDF大小':<10}")
    print("-" * 70)
    for r in reports:
        txt_icon = "✅" if r['txt'] else "❌"
        pdf_icon = "✅" if r['pdf'] else "❌"
        txt_size = f"{r['txt_size']/1024:.1f}KB" if r['txt_size'] else "-"
        pdf_size = f"{r['pdf_size']/1024:.1f}KB" if r['pdf_size'] else "-"
        print(f"{r['code']:<10} {r['name']:<20} {txt_icon:<5} {pdf_icon:<5} {txt_size:<10} {pdf_size:<10}")


def print_report_detail(report):
    """打印报告详情"""
    print(f"\n{'='*60}")
    print(f"专业名称: {report['name']}")
    print(f"专业代码: {report['code']}")
    print(f"{'='*60}")
    print(f"\nTXT文件:")
    print(f"  状态: {'✅ 存在' if report['txt'] else '❌ 缺失'}")
    if report['txt']:
        print(f"  路径: {report['txt_path']}")
        print(f"  大小: {report['txt_size']/1024:.1f} KB")
    print(f"\nPDF文件:")
    print(f"  状态: {'✅ 存在' if report['pdf'] else '❌ 缺失'}")
    if report['pdf']:
        print(f"  路径: {report['pdf_path']}")
        print(f"  大小: {report['pdf_size']/1024:.1f} KB")


def print_integrity_check(integrity):
    """打印完整性检查结果"""
    print(f"\n{'='*60}")
    print("报告完整性检查")
    print(f"{'='*60}")
    print(f"总报告数: {integrity['total']}")
    print(f"完整报告: {integrity['complete']}")
    print(f"缺失报告: {integrity['total'] - integrity['complete']}")
    
    if integrity['issues']:
        print(f"\n发现问题:")
        for issue in integrity['issues']:
            print(f"  - {issue}")
    else:
        print(f"\n✅ 所有报告完整!")


def print_statistics(stats):
    """打印统计信息"""
    print(f"\n{'='*60}")
    print("报告统计信息")
    print(f"{'='*60}")
    print(f"总报告数: {stats['total_reports']}")
    print(f"完整报告: {stats['complete_reports']}")
    print(f"\n存储信息:")
    print(f"  TXT总大小: {stats['total_txt_size']/1024:.1f} KB")
    print(f"  PDF总大小: {stats['total_pdf_size']/1024:.1f} KB")
    print(f"  总存储量: {stats['total_size']/1024:.1f} KB")


if __name__ == "__main__":
    main()
