#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 - 完整批量PDF生成工作流 v1.0
整合了文本清理、格式化、PDF生成的完整流程
作者：专业星图团队
日期：2026-05-23
"""

import os
import sys
from pathlib import Path


def main():
    print("="*70)
    print("专业星图 - 完整批量PDF生成工作流 v1.0")
    print("="*70)
    print()
    
    # 检查依赖
    print("步骤 1/4: 检查依赖...")
    try:
        import reportlab
        print("  ✅ reportlab 已安装")
    except ImportError:
        print("  ❌ 请先运行: pip install reportlab")
        return
    
    # 检查目录
    reports_dir = Path("/workspace/data/reports")
    if not reports_dir.exists():
        print(f"  ❌ 报告目录不存在: {reports_dir}")
        return
    
    txt_files = sorted([f for f in reports_dir.iterdir() if f.suffix == '.txt'])
    print(f"  找到 {len(txt_files)} 个TXT报告文件")
    
    # 步骤2: 清理报告文本
    print()
    print("步骤 2/4: 清理报告文本...")
    try:
        # 导入并运行清理脚本
        sys.path.insert(0, '/workspace')
        from clean_reports_v2 import process_directory_v2
        backup_dir = reports_dir / "backup_before_clean"
        results = process_directory_v2(str(reports_dir), str(backup_dir))
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"  ✅ 清理完成: {success_count}/{len(results)}")
    except Exception as e:
        print(f"  ⚠️  清理时出现问题: {e}")
        print("  继续执行PDF生成...")
    
    # 步骤3: 生成PDF
    print()
    print("步骤 3/4: 生成PDF文档...")
    try:
        from pdf_generator import batch_convert
        results = batch_convert(str(reports_dir))
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"  ✅ PDF生成完成: {success_count}/{len(results)}")
    except Exception as e:
        print(f"  ❌ PDF生成失败: {e}")
        return
    
    # 步骤4: 验证结果
    print()
    print("步骤 4/4: 验证生成结果...")
    pdf_files = sorted([f for f in reports_dir.iterdir() if f.suffix == '.pdf'])
    print(f"  已生成 {len(pdf_files)} 个PDF文档")
    for pdf_file in pdf_files[:5]:
        size_kb = pdf_file.stat().st_size / 1024
        print(f"    - {pdf_file.name} ({size_kb:.1f} KB)")
    if len(pdf_files) > 5:
        print(f"    ... 还有 {len(pdf_files)-5} 个文档")
    
    print()
    print("="*70)
    print("🎉 批量生成工作流完成！")
    print("="*70)
    print()
    print("输出目录:")
    print(f"  {reports_dir}")
    print()
    print("所有文件列表:")
    for f in sorted(reports_dir.iterdir()):
        if f.suffix in ['.txt', '.pdf']:
            print(f"  {f.name}")


if __name__ == "__main__":
    main()
