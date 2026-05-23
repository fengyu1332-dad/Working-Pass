#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 - 报告调用示例库
提供便捷的报告文件访问接口
作者：专业星图团队
日期：2026-05-23
"""

import os
from pathlib import Path
from report_manager import ReportManager


REPORTS_DIR = Path("/workspace/data/reports")


class ReportAccessor:
    """报告访问器 - 提供便捷的报告访问接口"""
    
    def __init__(self, reports_dir=None):
        self.reports_dir = Path(reports_dir) if reports_dir else REPORTS_DIR
        self.manager = ReportManager(self.reports_dir)
    
    def get_pdf_path(self, major_code):
        """获取PDF文件路径"""
        report = self.manager.get_by_code(major_code)
        if report and report['pdf']:
            return report['pdf_path']
        return None
    
    def get_txt_path(self, major_code):
        """获取TXT文件路径"""
        report = self.manager.get_by_code(major_code)
        if report and report['txt']:
            return report['txt_path']
        return None
    
    def read_txt_report(self, major_code):
        """读取TXT报告内容"""
        txt_path = self.get_txt_path(major_code)
        if txt_path:
            with open(txt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def get_all_major_codes(self):
        """获取所有专业代码列表"""
        reports = self.manager.list_all_reports()
        return [r['code'] for r in reports]
    
    def get_all_major_names(self):
        """获取所有专业名称列表"""
        reports = self.manager.list_all_reports()
        return [r['name'] for r in reports]
    
    def get_major_info(self, major_code):
        """获取专业完整信息"""
        return self.manager.get_by_code(major_code)
    
    def search_reports(self, keyword):
        """搜索报告"""
        return self.manager.search_by_name(keyword)


# === 快捷函数 ===

def get_report(major_code):
    """
    获取指定专业的报告文件信息
    
    Args:
        major_code: 专业代码，如 "080901"
    
    Returns:
        报告信息字典
    """
    accessor = ReportAccessor()
    return accessor.get_major_info(major_code)


def get_pdf(major_code):
    """
    获取指定专业的PDF路径
    
    Args:
        major_code: 专业代码
    
    Returns:
        PDF文件路径
    """
    accessor = ReportAccessor()
    return accessor.get_pdf_path(major_code)


def get_txt(major_code):
    """
    获取指定专业的TXT路径
    
    Args:
        major_code: 专业代码
    
    Returns:
        TXT文件路径
    """
    accessor = ReportAccessor()
    return accessor.get_txt_path(major_code)


def read_report(major_code):
    """
    读取指定专业的TXT报告内容
    
    Args:
        major_code: 专业代码
    
    Returns:
        报告内容字符串
    """
    accessor = ReportAccessor()
    return accessor.read_txt_report(major_code)


def list_reports():
    """
    列出所有报告
    
    Returns:
        报告列表
    """
    accessor = ReportAccessor()
    return accessor.manager.list_all_reports()


def search_reports(keyword):
    """
    搜索报告
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的报告列表
    """
    accessor = ReportAccessor()
    return accessor.search_reports(keyword)


if __name__ == "__main__":
    print("="*60)
    print("专业星图 - 报告调用示例库")
    print("="*60)
    print("\n使用示例:")
    print("\n1. 导入模块:")
    print("   from report_accessor import get_pdf, get_txt, read_report, list_reports")
    
    print("\n2. 获取PDF路径:")
    print("   pdf_path = get_pdf('080901')")
    print("   print(pdf_path)")
    
    print("\n3. 获取TXT路径:")
    print("   txt_path = get_txt('080901')")
    print("   print(txt_path)")
    
    print("\n4. 读取报告内容:")
    print("   content = read_report('080901')")
    print("   print(content[:100])")
    
    print("\n5. 列出所有报告:")
    print("   reports = list_reports()")
    print("   for r in reports:")
    print("       print(r['code'], r['name'])")
    
    print("\n6. 搜索报告:")
    print("   results = search_reports('法学')")
    print("   print(results)")
    
    print("\n" + "="*60)
    print("实际示例运行:")
    print("="*60)
    
    # 测试列出所有报告
    print("\n所有报告:")
    reports = list_reports()
    for r in reports[:3]:
        print(f"  - {r['code']}: {r['name']}")
    if len(reports) > 3:
        print(f"  ... 还有 {len(reports)-3} 个")
    
    # 测试获取单个报告
    if reports:
        code = reports[0]['code']
        print(f"\n获取专业 {code} 的信息:")
        info = get_report(code)
        if info:
            print(f"  专业名称: {info['name']}")
            print(f"  TXT: {info['txt_path']}")
            print(f"  PDF: {info['pdf_path']}")
