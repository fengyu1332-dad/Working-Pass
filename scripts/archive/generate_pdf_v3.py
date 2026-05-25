#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告PDF生成器 v3.0 - 最终优化版
增强段落分隔 + 优化视觉层次 + 提升阅读体验
"""

import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
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
            break
        except:
            pass

# ===============================
# 颜色配置
# ===============================
PRIMARY_COLOR = HexColor('#1a365d')
SECONDARY_COLOR = HexColor('#2c5282')
ACCENT_COLOR = HexColor('#3182ce')
LIGHT_TEXT_COLOR = HexColor('#718096')
TEXT_COLOR = HexColor('#2d3748')


# ===============================
# PDF样式定义 - v3.0 增强版
# ===============================
def get_styles():
    styles = {}
    
    # 主标题
    styles['MainTitle'] = ParagraphStyle(
        'MainTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=22,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=15,
        leading=28
    )
    
    # 章节标题 (### 一、xxx)
    styles['ChapterTitle'] = ParagraphStyle(
        'ChapterTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=15,
        textColor=PRIMARY_COLOR,
        spaceBefore=18,
        spaceAfter=10,
        leading=20
    )
    
    # 小节标题 (#### 1.1 xxx)
    styles['SectionTitle'] = ParagraphStyle(
        'SectionTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=13,
        textColor=SECONDARY_COLOR,
        spaceBefore=14,
        spaceAfter=8,
        leading=17
    )
    
    # 子标题 (##### xxx)
    styles['SubSectionTitle'] = ParagraphStyle(
        'SubSectionTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceBefore=10,
        spaceAfter=6,
        leading=14
    )
    
    # 正文段落 - 增加段间距
    styles['BodyText'] = ParagraphStyle(
        'BodyText',
        fontName=CHINESE_FONT,
        fontSize=10,
        textColor=TEXT_COLOR,
        alignment=TA_JUSTIFY,
        spaceBefore=8,
        spaceAfter=8,
        leading=15
    )
    
    # 列表项 - 更明显的样式
    styles['BulletText'] = ParagraphStyle(
        'BulletText',
        fontName=CHINESE_FONT,
        fontSize=10,
        textColor=TEXT_COLOR,
        spaceBefore=5,
        spaceAfter=5,
        leading=14,
        leftIndent=15,
        bulletIndent=5
    )
    
    # 数据来源
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
# 增强的内容解析器
# ===============================
class EnhancedParser:
    
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
        
        # 检测标题级别
        if line.startswith('## '):
            return ('main_title', line[3:].strip())
        elif line.startswith('### '):
            return ('chapter', line[4:].strip())
        elif line.startswith('#### '):
            return ('section', line[5:].strip())
        elif line.startswith('##### '):
            return ('subsection', line[6:].strip())
        
        # 数据来源
        if line.startswith('*数据来源') or line.startswith('*来源'):
            return ('datasource', line[1:].strip())
        
        # 列表项
        if line.startswith('*'):
            return ('bullet', line[1:].strip())
        elif re.match(r'^\d+\.\s', line):
            return ('numbered', line.strip())
        
        # 分隔符
        if line.strip() in ['---', '***', '___']:
            return ('separator', '')
        
        # 普通段落
        return ('paragraph', line.strip())
    
    @staticmethod
    def parse(content):
        elements = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_type, content = EnhancedParser.parse_line(line)
            
            if line_type == 'empty':
                # 空行保持，作为段落分隔
                elements.append(('empty', ''))
            elif line_type in ['main_title', 'chapter', 'section', 'subsection']:
                # 标题后不加分隔
                elements.append((line_type, content))
            elif line_type in ['bullet', 'numbered']:
                # 收集连续的列表项
                list_items = []
                while line_type in ['bullet', 'numbered']:
                    list_items.append(content)
                    i += 1
                    if i < len(lines):
                        line_type, content = EnhancedParser.parse_line(lines[i])
                    else:
                        line_type = 'end'
                        break
                # 回退一行（因为循环会多走一步）
                i -= 1
                elements.append(('list_start', list_items))
            elif line_type == 'datasource':
                elements.append(('datasource', content))
            elif line_type == 'separator':
                elements.append(('separator', ''))
            else:
                elements.append(('paragraph', content))
            
            i += 1
        
        return elements


# ===============================
# PDF生成器 - v3.0
# ===============================
def generate_pdf_v3(input_file, output_file=None):
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
    elements = EnhancedParser.parse(content)
    
    last_was_paragraph = False
    last_was_empty = False
    
    for el_type, el_content in elements:
        if el_type == 'empty':
            if last_was_paragraph and not last_was_empty:
                # 段落之间的空行 - 转换为额外的间距
                story.append(Spacer(1, 0.3*cm))
                last_was_empty = True
            continue
        
        last_was_empty = False
        
        if el_type in ['main_title']:
            story.append(Spacer(1, 1.5*cm))
            story.append(Paragraph(el_content, styles['MainTitle']))
            story.append(HRFlowable(width="80%", thickness=1, color=ACCENT_COLOR, spaceAfter=10))
            last_was_paragraph = False
            
        elif el_type == 'chapter':
            story.append(Spacer(1, 0.8*cm))
            story.append(Paragraph(el_content, styles['ChapterTitle']))
            last_was_paragraph = False
            
        elif el_type == 'section':
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph(el_content, styles['SectionTitle']))
            last_was_paragraph = False
            
        elif el_type == 'subsection':
            story.append(Paragraph(el_content, styles['SubSectionTitle']))
            last_was_paragraph = False
            
        elif el_type == 'paragraph':
            clean_text = EnhancedParser.clean_text(el_content)
            if clean_text:
                story.append(Paragraph(clean_text, styles['BodyText']))
                last_was_paragraph = True
                last_was_empty = False
                
        elif el_type == 'list_start':
            # 处理列表项
            for item in el_content:
                clean_item = EnhancedParser.clean_text(item)
                if clean_item:
                    story.append(Paragraph('• ' + clean_item, styles['BulletText']))
            last_was_paragraph = False
            
        elif el_type == 'datasource':
            story.append(Paragraph(el_content, styles['DataSource']))
            
        elif el_type == 'separator':
            story.append(Spacer(1, 0.2*cm))
            story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_TEXT_COLOR, spaceAfter=0.2*cm))
    
    doc.build(story)
    return output_file


# ===============================
# 批量转换
# ===============================
def batch_convert_v3(reports_dir, output_dir=None):
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
            result = generate_pdf_v3(input_path, output_path)
            results.append({
                'file': filename,
                'status': 'success',
                'output': output_path
            })
            print(f"    ✅ 完成")
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
    print("专业星图 PDF生成器 v3.0 - 最终优化版")
    print("="*60)
    
    reports_dir = "/workspace/data/reports"
    
    if os.path.exists(reports_dir):
        results = batch_convert_v3(reports_dir)
        
        print("\n" + "="*60)
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"转换完成：{success_count}/{len(results)}")
        print("="*60)
    else:
        print(f"❌ 目录不存在：{reports_dir}")
