#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告内容清理脚本
1. 去除报告开头的指令性文字
2. 修复段落切分不合理的问题
3. 保持专业格式和结构
"""

import os
import re


def clean_report_content(content):
    """清理报告内容"""
    lines = content.split('\n')
    cleaned_lines = []
    skip_until = -1
    
    # 第一步：跳过开头的指令性内容，找到第一个真实标题
    for i, line in enumerate(lines):
        # 找到第一个##或###标题或---分隔符开始
        line = line.rstrip('\r')
        
        # 检测是否是开始标志
        if line.startswith('## ') or line.startswith('### ') or line.startswith('# '):
            skip_until = i
            break
        if line.strip() == '---':
            skip_until = i + 1
            break
    
    # 第二步：从开始位置开始处理
    for i in range(skip_until if skip_until != -1 else 0, len(lines)):
        line = lines[i].rstrip('\r')
        cleaned_lines.append(line)
    
    # 第三步：修复段落切分问题
    return fix_paragraph_breaks('\n'.join(cleaned_lines))


def fix_paragraph_breaks(text):
    """修复段落切分不合理的问题"""
    
    # 处理逻辑：
    # 1. 保留标题、列表项等结构化元素的换行
    # 2. 合并普通段落中不合理的换行
    lines = text.split('\n')
    result = []
    current_paragraph = []
    
    for line in lines:
        line = line.rstrip()
        
        # 判断是否是结构化元素
        is_structural = (
            line.startswith('#') or               # 标题
            line.startswith('*') or               # 列表
            line.startswith('-') or               # 列表
            re.match(r'^\d+\.\s', line) or        # 编号列表
            re.match(r'^\d+\.\d+\s', line) or     # 子项
            line.strip() == '' or                 # 空行
            line.strip() == '---' or              # 分隔符
            line.startswith('|')                  # 表格
        )
        
        if is_structural:
            # 如果有正在积累的段落，先保存
            if current_paragraph:
                result.append(' '.join(current_paragraph))
                current_paragraph = []
            result.append(line)
        else:
            # 普通文本，检查是否是段落的一部分
            # 判断是否应该合并：
            # - 当前行不是空的
            # - 当前行不以结束标点（。！？）结尾，并且下一行不是结构化元素
            if line.strip():
                # 检查上一行的结尾是否是完整的句子
                if current_paragraph:
                    last_line = current_paragraph[-1]
                    # 如果上一行以标点结尾或足够长，可能是段落结束
                    if last_line.endswith(('。', '！', '？', '：', '；', '.')) or len(last_line) > 60:
                        result.append(' '.join(current_paragraph))
                        current_paragraph = [line.strip()]
                    else:
                        # 继续合并
                        current_paragraph.append(line.strip())
                else:
                    current_paragraph.append(line.strip())
            else:
                # 空行，保存当前段落
                if current_paragraph:
                    result.append(' '.join(current_paragraph))
                    current_paragraph = []
                result.append('')
    
    # 处理最后一个段落
    if current_paragraph:
        result.append(' '.join(current_paragraph))
    
    # 第四步：清理多余的空格
    cleaned = []
    for line in result:
        # 去除多个空格
        cleaned_line = re.sub(r'\s+', ' ', line.strip())
        cleaned.append(cleaned_line)
    
    return '\n'.join(cleaned)


def process_file(filepath, backup_dir=None):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份原始文件
    if backup_dir:
        os.makedirs(backup_dir, exist_ok=True)
        filename = os.path.basename(filepath)
        backup_path = os.path.join(backup_dir, filename)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # 清理内容
    cleaned_content = clean_report_content(content)
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    return len(content), len(cleaned_content)


def process_directory(reports_dir, backup_dir=None):
    """批量处理目录下的报告"""
    txt_files = sorted([f for f in os.listdir(reports_dir) if f.endswith('.txt')])
    
    results = []
    for filename in txt_files:
        filepath = os.path.join(reports_dir, filename)
        try:
            print(f"正在处理：{filename}")
            old_size, new_size = process_file(filepath, backup_dir)
            results.append({
                'file': filename,
                'status': 'success',
                'old_size': old_size,
                'new_size': new_size
            })
            print(f"  ✅ 完成 ({old_size} → {new_size} 字节)")
        except Exception as e:
            results.append({
                'file': filename,
                'status': 'error',
                'error': str(e)
            })
            print(f"  ❌ 失败：{str(e)}")
    
    return results


if __name__ == "__main__":
    print("="*60)
    print("专业星图 - 报告内容清理工具")
    print("="*60)
    
    reports_dir = "/workspace/data/reports"
    backup_dir = "/workspace/data/reports/backup_before_clean"
    
    if os.path.exists(reports_dir):
        print(f"\n报告目录：{reports_dir}")
        print(f"备份目录：{backup_dir}")
        print()
        
        results = process_directory(reports_dir, backup_dir)
        
        print("\n" + "="*60)
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"处理完成：{success_count}/{len(results)}")
        print("="*60)
    else:
        print(f"❌ 目录不存在：{reports_dir}")
