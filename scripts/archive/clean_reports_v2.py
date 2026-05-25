#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版报告内容清理脚本
1. 彻底去除开头的指令性文字
2. 修复段落切分
3. 去除多余空行
4. 优化PDF生成器的段落处理
"""

import os
import re


def clean_report_content_v2(content):
    """清理报告内容 - 优化版"""
    lines = content.split('\n')
    
    # 第一步：找到真正的开始位置
    start_pos = 0
    for i, line in enumerate(lines):
        line = line.rstrip('\r')
        if line.startswith('#') or line.startswith('##') or line.startswith('###'):
            start_pos = i
            break
        if line.strip() == '---':
            start_pos = i + 1
            break
    
    # 第二步：从开始位置读取内容
    cleaned_lines = []
    for i in range(start_pos, len(lines)):
        line = lines[i].rstrip('\r')
        cleaned_lines.append(line)
    
    # 第三步：修复段落切分问题
    return fix_paragraph_breaks_v2('\n'.join(cleaned_lines))


def fix_paragraph_breaks_v2(text):
    """修复段落切分 - 更智能的版本"""
    lines = text.split('\n')
    result = []
    current_paragraph = []
    
    for line in lines:
        line = line.rstrip()
        stripped = line.strip()
        
        # 判断是否是特殊结构元素
        is_structural = (
            stripped.startswith('#') or 
            line.startswith('*') or
            line.startswith('-') or
            re.match(r'^\d+\.\s', line) or
            re.match(r'^\d+\.\d+\s', line) or
            line.startswith('|') or
            stripped == '' or
            stripped == '---'
        )
        
        if is_structural:
            # 保存当前段落
            if current_paragraph:
                result.append(' '.join(current_paragraph))
                current_paragraph = []
            result.append(line)
        else:
            # 普通文本
            if stripped:
                if current_paragraph:
                    last_line = current_paragraph[-1]
                    # 检查上一行是否应该结束
                    should_end = last_line.endswith(('。', '！', '？', '：', '；', '.'))
                    if should_end:
                        result.append(' '.join(current_paragraph))
                        current_paragraph = [stripped]
                    else:
                        current_paragraph.append(stripped)
                else:
                    current_paragraph.append(stripped)
            else:
                if current_paragraph:
                    result.append(' '.join(current_paragraph))
                    current_paragraph = []
                result.append('')
    
    # 处理最后一个段落
    if current_paragraph:
        result.append(' '.join(current_paragraph))
    
    # 清理多余空行和空格
    final_result = []
    last_was_empty = False
    for line in result:
        stripped = line.strip()
        if stripped:
            # 清理内部空格
            cleaned = re.sub(r'\s+', ' ', stripped)
            final_result.append(cleaned)
            last_was_empty = False
        else:
            if not last_was_empty:
                final_result.append('')
                last_was_empty = True
    
    return '\n'.join(final_result).strip()


def process_file_v2(filepath, backup_dir=None):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if backup_dir:
        os.makedirs(backup_dir, exist_ok=True)
        filename = os.path.basename(filepath)
        backup_path = os.path.join(backup_dir, filename)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    cleaned_content = clean_report_content_v2(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    return len(content), len(cleaned_content)


def process_directory_v2(reports_dir, backup_dir=None):
    """批量处理"""
    txt_files = sorted([f for f in os.listdir(reports_dir) if f.endswith('.txt')])
    results = []
    for filename in txt_files:
        filepath = os.path.join(reports_dir, filename)
        try:
            print(f"正在处理：{filename}")
            old_size, new_size = process_file_v2(filepath, backup_dir)
            results.append({'file': filename, 'status': 'success', 'old_size': old_size, 'new_size': new_size})
            print(f"  ✅ 完成")
        except Exception as e:
            results.append({'file': filename, 'status': 'error', 'error': str(e)})
            print(f"  ❌ 失败")
    return results


if __name__ == "__main__":
    print("="*60)
    print("专业星图 - 报告内容清理工具 v2")
    print("="*60)
    
    reports_dir = "/workspace/data/reports"
    backup_dir = "/workspace/data/reports/backup_before_clean_v2"
    
    if os.path.exists(reports_dir):
        results = process_directory_v2(reports_dir, backup_dir)
        print("="*60)
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"处理完成：{success_count}/{len(results)}")
        print("="*60)
