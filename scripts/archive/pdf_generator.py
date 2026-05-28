#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告PDF生成器 v4.1 - 最终字体修复版
增强段落分隔 + 优化视觉层次 + 页眉页脚 + 中文字体修复
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
from reportlab.pdfgen import canvas as pdfcanvas


# ===============================
# 中文字体配置
# ===============================
CHINESE_FONT = 'Helvetica'
CHINESE_FONT_BOLD = 'Helvetica'

# 注册中文字体
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
if os.path.exists(font_path):
    try:
        pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
        CHINESE_FONT = 'ChineseFont'
        CHINESE_FONT_BOLD = 'ChineseFont'
        print(f"成功加载中文字体: {font_path}")
    except Exception as e:
        print(f"加载字体失败 {font_path}: {e}")
else:
    print(f"字体文件不存在: {font_path}")

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
        fontSize=22,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=15,
        leading=28
    )
    
    styles['ChapterTitle'] = ParagraphStyle(
        'ChapterTitle',
        fontName=CHINESE_FONT_BOLD,
        fontSize=15,
        textColor=PRIMARY_COLOR,
        spaceBefore=18,
        spaceAfter=10,
        leading=20
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
        spaceAfter=6,
        leading=14
    )
    
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
# 内容解析器
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
        
        if line.startswith('## '):
            return ('main_title', line[3:].strip())
        elif line.startswith('### '):
            return ('chapter', line[4:].strip())
        elif line.startswith('#### '):
            return ('section', line[5:].strip())
        elif line.startswith('##### '):
            return ('subsection', line[6:].strip())
        
        if line.startswith('*数据来源') or line.startswith('*来源'):
            return ('datasource', line[1:].strip())
        
        if line.startswith('*'):
            return ('bullet', line[1:].strip())
        elif re.match(r'^\d+\.\s', line):
            return ('numbered', line.strip())
        
        if line.strip() in ['---', '***', '___']:
            return ('separator', '')
        
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
                elements.append(('empty', ''))
            elif line_type in ['main_title', 'chapter', 'section', 'subsection']:
                elements.append((line_type, content))
            elif line_type in ['bullet', 'numbered']:
                list_items = []
                while line_type in ['bullet', 'numbered']:
                    list_items.append(content)
                    i += 1
                    if i < len(lines):
                        line_type, content = EnhancedParser.parse_line(lines[i])
                    else:
                        line_type = 'end'
                        break
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
# 页眉页脚回调函数
# ===============================
def _draw_header_footer(canvas_obj, doc):
    """绘制页眉页脚"""
    canvas_obj.saveState()
    
    page_width, page_height = A4
    page_num = canvas_obj._pageNumber
    
    # 页眉
    canvas_obj.setFont(CHINESE_FONT, 9)
    canvas_obj.setFillColor(LIGHT_TEXT_COLOR)
    
    # 页眉内容 - 中间位置
    header_text = "职业星图-专业深度报告"
    text_width = canvas_obj.stringWidth(header_text, CHINESE_FONT, 9)
    x_position = (page_width - text_width) / 2
    canvas_obj.drawString(x_position, page_height - 1.5*cm, header_text)
    
    # 页眉下方细线
    canvas_obj.setStrokeColor(ACCENT_COLOR)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(2.5*cm, page_height - 1.8*cm, page_width - 2.5*cm, page_height - 1.8*cm)
    
    # 页脚
    # 页脚细线
    canvas_obj.line(2.5*cm, 2*cm, page_width - 2.5*cm, 2*cm)
    
    # 页脚页码 - 中间位置（无法获取总页数，仅显示当前页码
    footer_text = f"{page_num}页"
    text_width = canvas_obj.stringWidth(footer_text, CHINESE_FONT, 9)
    x_position = (page_width - text_width) / 2
    canvas_obj.drawString(x_position, 1.2*cm, footer_text)
    
    canvas_obj.restoreState()


# ===============================
# PDF生成器 - v4.1
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
    elements = EnhancedParser.parse(content)
    
    last_was_paragraph = False
    last_was_empty = False
    
    for el_type, el_content in elements:
        if el_type == 'empty':
            if last_was_paragraph and not last_was_empty:
                story.append(Spacer(1, 0.3*cm))
                last_was_empty = True
            continue
        
        last_was_empty = False
        
        if el_type == 'main_title':
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
    
    # 使用标准回调函数方式
    doc.build(story, onFirstPage=_draw_header_footer, onLaterPages=_draw_header_footer)
    
    return output_file


# ===============================
# 批量转换
# ===============================
def batch_convert(reports_dir, output_dir=None):
    """批量转换TXT报告为PDF"""
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
    print("专业星图 PDF生成器 v4.1 - 带页眉页脚（字体修复版）")
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
