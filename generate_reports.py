#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告生成器 - 完整解决方案
生成：HTML（浏览器直接查看） + PDF（weasyprint，支持中文）
"""

import os
import re
import json
from datetime import datetime


# ===============================
# HTML模板
# ===============================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px 60px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a365d;
            text-align: center;
            font-size: 28px;
            padding-bottom: 20px;
            border-bottom: 2px solid #3182ce;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #1a365d;
            font-size: 20px;
            margin: 30px 0 15px;
            padding-left: 10px;
            border-left: 4px solid #3182ce;
        }}
        h3 {{
            color: #2c5282;
            font-size: 17px;
            margin: 20px 0 10px;
        }}
        p {{
            margin: 10px 0;
            text-align: justify;
        }}
        ul {{
            margin: 10px 0 10px 25px;
        }}
        li {{
            margin: 5px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #e2e8f0;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #f7fafc;
            font-weight: 600;
        }}
        .data-source {{
            font-size: 12px;
            color: #718096;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; padding: 30px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""


# ===============================
# 内容解析器
# ===============================
def parse_markdown_to_html(content):
    lines = content.split('\n')
    html_parts = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            html_parts.append('<p>&nbsp;</p>')
            continue
        
        # 标题
        if line.startswith('## '):
            title = line[3:].strip()
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)
            html_parts.append(f'<h1>{title}</h1>')
        elif line.startswith('### '):
            title = line[4:].strip()
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)
            html_parts.append(f'<h2>{title}</h2>')
        elif line.startswith('#### '):
            title = line[5:].strip()
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)
            html_parts.append(f'<h3>{title}</h3>')
        
        # 列表项
        elif line.startswith('*'):
            item = line[1:].strip()
            item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item)
            if item.startswith('数据来源') or item.startswith('来源'):
                html_parts.append(f'<div class="data-source">{item}</div>')
            else:
                html_parts.append(f'<li>{item}</li>')
        
        # 普通段落
        else:
            # 处理粗体
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            if line.strip():
                html_parts.append(f'<p>{line}</p>')
    
    # 合并相邻的li
    result = []
    in_list = False
    for part in html_parts:
        if part.startswith('<li>'):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(part)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(part)
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)


# ===============================
# 生成HTML
# ===============================
def generate_html(input_file, output_file=None):
    if output_file is None:
        output_file = input_file.replace('.txt', '.html')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title = "专业深度分析报告"
    first_line = content.split('\n')[0]
    if first_line.startswith('##'):
        title = re.sub(r'\*\*', '', first_line[2:].strip())
    
    html_content = parse_markdown_to_html(content)
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return output_file


# ===============================
# 使用weasyprint生成PDF（如果可用）
# ===============================
def generate_pdf_weasyprint(html_file, output_file=None):
    if output_file is None:
        output_file = html_file.replace('.html', '.pdf')
    
    try:
        from weasyprint import HTML
        HTML(filename=html_file).write_pdf(output_file)
        return output_file
    except ImportError:
        print("⚠️ weasyprint未安装，跳过PDF生成")
        return None


# ===============================
# 批量处理
# ===============================
def batch_process(reports_dir):
    os.makedirs(reports_dir, exist_ok=True)
    
    txt_files = sorted([f for f in os.listdir(reports_dir) if f.endswith('.txt')])
    
    results = []
    for i, filename in enumerate(txt_files, 1):
        input_path = os.path.join(reports_dir, filename)
        
        try:
            print(f"[{i}/{len(txt_files)}] 处理：{filename}")
            
            # 生成HTML
            html_file = input_path.replace('.txt', '.html')
            html_result = generate_html(input_path, html_file)
            print(f"    ✅ HTML: {os.path.basename(html_result)}")
            
            # 尝试生成PDF
            pdf_file = generate_pdf_weasyprint(html_result)
            if pdf_file:
                print(f"    ✅ PDF: {os.path.basename(pdf_file)}")
            
            results.append({
                'file': filename,
                'status': 'success',
                'html': html_result,
                'pdf': pdf_file
            })
            
        except Exception as e:
            results.append({
                'file': filename,
                'status': 'error',
                'error': str(e)
            })
            print(f"    ❌ 失败：{str(e)}")
    
    return results


# ===============================
# 主函数
# ===============================
if __name__ == "__main__":
    print("="*60)
    print("专业星图 报告生成器 - 完整解决方案")
    print("="*60)
    
    reports_dir = "/workspace/data/reports"
    
    if os.path.exists(reports_dir):
        results = batch_process(reports_dir)
        
        print("\n" + "="*60)
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"处理完成：{success_count}/{len(results)}")
        print("\n📋 使用说明：")
        print("  - HTML文件：可以直接在浏览器中打开，完美支持中文")
        print("  - 可通过 http://localhost:3456/data/reports/ 访问")
        print("="*60)
    else:
        print(f"❌ 目录不存在：{reports_dir}")
