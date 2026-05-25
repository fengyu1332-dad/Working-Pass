#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告PDF生成器 v5.0 - 稳定字体版
使用内置字体 + 简化处理，避免中文显示问题
"""

import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ===============================
# 字体配置 - 优先尝试多个字体
# ===============================
CHINESE_FONT = 'Helvetica'
CHINESE_FONT_BOLD = 'Helvetica-Bold'

# 尝试多种字体路径
font_paths = [
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
]

for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
            CHINESE_FONT = 'ChineseFont'
            CHINESE_FONT_BOLD = 'ChineseFont'
            print(f"✅ 成功加载中文字体: {font_path}")
            break
        except Exception as e:
            print(f"⚠️ 加载字体失败 {font_path}: {e}")
            continue
else:
    print("⚠️ 未找到合适的中文字体，将使用默认字体")


# ===============================
# 颜色配置
# ===============================
PRIMARY_COLOR = HexColor('#1a365d')
SECONDARY_COLOR = HexColor('#2c5282')
ACCENT_COLOR = HexColor('#3182ce')
LIGHT_TEXT_COLOR = HexColor('#718096')
TEXT_COLOR = HexColor('#2d3748')


# ===============================
# PDF样式定义
# ===============================
def get_styles():
    styles = {}
    
    styles['MainTitle'] = ParagraphStyle(
        'MainTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=20,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=15,
        leading=26
    )
    
    styles['ChapterTitle'] = ParagraphStyle(
        'ChapterTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=14,
        textColor=PRIMARY_COLOR,
        spaceBefore=18,
        spaceAfter=10,
        leading=18
    )
    
    styles['SectionTitle'] = ParagraphStyle(
        'SectionTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=12,
        textColor=SECONDARY_COLOR,
        spaceBefore=14,
        spaceAfter=8,
        leading=15
    )
    
    styles['BodyText'] = ParagraphStyle(
        'BodyText',
        fontName=CHINESE_FONT,
        fontSize=10,
        textColor=TEXT_COLOR,
        alignment=TA_JUSTIFY,
        spaceBefore=6,
        spaceAfter=6,
        leading=14
    )
    
    styles['BulletText'] = ParagraphStyle(
        'BulletText',
        fontName=CHINESE_FONT,
        fontSize=10,
        textColor=TEXT_COLOR,
        spaceBefore=4,
        spaceAfter=4,
        leading=13,
        leftIndent=15
    )
    
    styles['DataSource'] = ParagraphStyle(
        'DataSource',
        fontName=CHINESE_FONT,
        fontSize=8,
        textColor=LIGHT_TEXT_COLOR,
        spaceBefore=6,
        spaceAfter=4,
        leading=11,
        alignment=TA_LEFT
    )
    
    return styles


# ===============================
# 内容解析器 - 简化版
# ===============================
class SimpleParser:
    
    @staticmethod
    def clean_text(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'`{1,3}', '', text)
        text = re.sub(r'[#*]', '', text)
        return text.strip()
    
    @staticmethod
    def parse_line(line):
        line = line.strip()
        
        if not line:
            return ('empty', '')
        
        if line.startswith('## '):
            return ('main_title', line[3:].strip())
        elif line.startswith('### '):
            return ('chapter', line[4:].strip())
        elif line.startswith('#### '):
            return ('section', line[5:].strip())
        
        if line.startswith('*数据来源') or line.startswith('*来源'):
            return ('datasource', line[1:].strip())
        
        if line.startswith('*'):
            return ('bullet', line[1:].strip())
        
        return ('paragraph', line.strip())
    
    @staticmethod
    def parse(content):
        elements = []
        lines = content.split('\n')
        
        for line in lines:
            line_type, content = SimpleParser.parse_line(line)
            elements.append((line_type, content))
        
        return elements


# ===============================
# PDF生成器 - v5.0
# ===============================
def generate_pdf(input_file, output_file=None):
    if output_file is None:
        output_file = input_file.replace('.txt', '.pdf')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    styles = get_styles()
    story = []
    elements = SimpleParser.parse(content)
    
    for el_type, el_content in elements:
        if el_type == 'empty':
            story.append(Spacer(1, 0.2*cm))
            
        elif el_type == 'main_title':
            story.append(Spacer(1, 1.5*cm))
            clean_title = SimpleParser.clean_text(el_content)
            story.append(Paragraph(clean_title, styles['MainTitle']))
            story.append(HRFlowable(width="80%", thickness=1, color=ACCENT_COLOR, spaceAfter=10))
            
        elif el_type == 'chapter':
            clean_title = SimpleParser.clean_text(el_content)
            story.append(Paragraph(clean_title, styles['ChapterTitle']))
            
        elif el_type == 'section':
            clean_title = SimpleParser.clean_text(el_content)
            story.append(Paragraph(clean_title, styles['SectionTitle']))
            
        elif el_type == 'paragraph':
            clean_text = SimpleParser.clean_text(el_content)
            if clean_text:
                story.append(Paragraph(clean_text, styles['BodyText']))
                
        elif el_type == 'bullet':
            clean_item = SimpleParser.clean_text(el_content)
            if clean_item:
                story.append(Paragraph('• ' + clean_item, styles['BulletText']))
            
        elif el_type == 'datasource':
            story.append(Paragraph(el_content, styles['DataSource']))
    
    doc.build(story)
    
    return output_file


# ===============================
# 批量转换
# ===============================
def batch_convert(reports_dir, output_dir=None):
    if output_dir is None:
        output_dir = reports_dir
    
    os.makedirs(output_dir, exist_ok=True)
    
    txt_files = sorted([f for f in os.listdir(reports_dir) if f.endswith('.txt')])
    
    results = []
    for i, filename in enumerate(txt_files, 1):
        input_path = os.path.join(reports_dir, filename)
        output_filename = filename.replace('.txt', '.pdf')
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            print(f"[{i}/{len(txt_files)}] 正在生成：{filename}")
            result = generate_pdf(input_path, output_path)
            results.append({
                'file': filename,
                'status': 'success',
                'output': output_path
            })
            print(f"    ✅ 完成: {output_filename}")
        except Exception as e:
            results.append({
                'file': filename,
                'status': 'error',
                'error': str(e)
            })
            print(f"    ❌ 失败：{str(e)}")
    
    return results


if __name__ == "__main__":
    print("="*60)
    print("专业星图 PDF生成器 v5.0 - 稳定字体版")
    print("="*60)
    
    reports_dir = "/workspace/data/reports"
    
    if os.path.exists(reports_dir):
        results = batch_convert(reports_dir)
        
        print("\n" + "="*60)
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"转换完成：{success_count}/{len(results)}")
        print("="*60)
    else:
        print(f"❌ 目录不存在：{reports_dir}")
