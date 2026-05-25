#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告PDF生成器 v2.0 - 优化版
支持中文显示 + 更好的格式处理 + 错误恢复
"""

import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ===============================
# 中文字体配置
# ===============================
CHINESE_FONT_PATHS = [
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]

CHINESE_FONT = 'Helvetica'
CHINESE_FONT_BOLD = 'Helvetica-Bold'

for font_path in CHINESE_FONT_PATHS:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            CHINESE_FONT = 'ChineseFont'
            CHINESE_FONT_BOLD = 'ChineseFont'
            print(f"✅ 成功加载中文字体：{font_path}")
            break
        except Exception as e:
            print(f"⚠️  字体加载失败 {font_path}：{str(e)}")

# ===============================
# 颜色配置
# ===============================
PRIMARY_COLOR = HexColor('#1a365d')
SECONDARY_COLOR = HexColor('#2c5282')
TEXT_COLOR = HexColor('#2d3748')
LIGHT_TEXT_COLOR = HexColor('#718096')


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
        spaceAfter=30,
        spaceBefore=20,
        leading=26
    )
    
    styles['ChapterTitle'] = ParagraphStyle(
        'ChapterTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=20,
        spaceAfter=12,
        leading=22
    )
    
    styles['SectionTitle'] = ParagraphStyle(
        'SectionTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=13,
        textColor=SECONDARY_COLOR,
        spaceBefore=14,
        spaceAfter=8,
        leading=17
    )
    
    styles['SubSectionTitle'] = ParagraphStyle(
        'SubSectionTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceBefore=10,
        spaceAfter=5,
        leading=14
    )
    
    styles['BodyText'] = ParagraphStyle(
        'BodyText',
        fontName=CHINESE_FONT,
        fontSize=10,
        textColor=TEXT_COLOR,
        alignment=TA_JUSTIFY,
        spaceBefore=5,
        spaceAfter=5,
        leading=14
    )
    
    styles['BulletText'] = ParagraphStyle(
        'BulletText',
        fontName=CHINESE_FONT,
        fontSize=10,
        textColor=TEXT_COLOR,
        spaceBefore=3,
        spaceAfter=3,
        leading=13,
        leftIndent=20,
    )
    
    styles['DataSource'] = ParagraphStyle(
        'DataSource',
        fontName=CHINESE_FONT,
        fontSize=8,
        textColor=LIGHT_TEXT_COLOR,
        spaceBefore=6,
        spaceAfter=4,
        leading=11
    )
    
    return styles


# ===============================
# 内容解析器
# ===============================
class ReportParser:
    
    @staticmethod
    def clean_text(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'`{1,3}', '', text)
        return text.strip()
    
    @staticmethod
    def parse_line(line):
        line = line.strip()
        
        if not line:
            return ('empty', '')
        
        if line.startswith('## '):
            return ('chapter', line[3:].strip())
        elif line.startswith('### '):
            return ('section', line[4:].strip())
        elif line.startswith('#### '):
            return ('subsection', line[5:].strip())
        elif line.startswith('*数据来源') or line.startswith('*来源'):
            return ('datasource', line[1:].strip())
        elif line.startswith('*'):
            return ('bullet', line[1:].strip())
        elif re.match(r'^\d+\.\s+', line):
            return ('numbered', line.strip())
        elif line.startswith('---') or line.startswith('='):
            return ('separator', '')
        else:
            return ('paragraph', line.strip())
    
    @staticmethod
    def parse(content):
        elements = []
        lines = content.split('\n')
        current_paragraph = []
        
        for line in lines:
            line_type, content = ReportParser.parse_line(line)
            
            if line_type == 'empty':
                if current_paragraph:
                    joined_text = '\n'.join(current_paragraph).strip()
                    if joined_text:
                        elements.append(('paragraph', joined_text))
                    current_paragraph = []
            elif line_type in ['paragraph', 'bullet', 'numbered']:
                current_paragraph.append(line)
            else:
                if current_paragraph:
                    joined_text = '\n'.join(current_paragraph).strip()
                    if joined_text:
                        elements.append(('paragraph', joined_text))
                    current_paragraph = []
                elements.append((line_type, content))
        
        if current_paragraph:
            joined_text = '\n'.join(current_paragraph).strip()
            if joined_text:
                elements.append(('paragraph', joined_text))
        
        return elements


# ===============================
# PDF生成器
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
    elements = ReportParser.parse(content)
    
    main_title_found = False
    
    for el_type, el_content in elements:
        el_content = ReportParser.clean_text(el_content)
        
        if not el_content:
            continue
        
        if el_type in ['chapter', 'section'] and not main_title_found:
            story.append(Spacer(1, 2*cm))
            story.append(Paragraph(el_content, styles['MainTitle']))
            main_title_found = True
        elif el_type == 'chapter':
            story.append(Paragraph(el_content, styles['ChapterTitle']))
        elif el_type == 'section':
            story.append(Paragraph(el_content, styles['SectionTitle']))
        elif el_type == 'subsection':
            story.append(Paragraph(el_content, styles['SubSectionTitle']))
        elif el_type == 'paragraph':
            story.append(Paragraph(el_content, styles['BodyText']))
        elif el_type == 'bullet':
            story.append(Paragraph('• ' + el_content, styles['BulletText']))
        elif el_type == 'numbered':
            story.append(Paragraph(el_content, styles['BulletText']))
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
            print(f"    ✅ 成功：{output_filename}")
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
    print("专业星图 PDF生成器 v2.0")
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
