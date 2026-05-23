#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告PDF生成器
功能：将TXT格式的专业分析报告转换为精美的PDF文档
"""

import os
import re
from datetime import datetime
from typing import List, Tuple, Dict
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# 全局样式配置
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 2.5 * cm
RIGHT_MARGIN = 2.5 * cm
TOP_MARGIN = 2.5 * cm
BOTTOM_MARGIN = 2.5 * cm

# 颜色配置
PRIMARY_COLOR = HexColor('#1a365d')
SECONDARY_COLOR = HexColor('#2c5282')
ACCENT_COLOR = HexColor('#3182ce')
LIGHT_BG_COLOR = HexColor('#f7fafc')
BORDER_COLOR = HexColor('#e2e8f0')
TEXT_COLOR = HexColor('#2d3748')
LIGHT_TEXT_COLOR = HexColor('#718096')

class PDFStyles:
    """PDF样式管理"""
    
    @staticmethod
    def get_styles():
        """获取所有样式定义"""
        styles = {}
        
        # 标题样式
        styles['MainTitle'] = ParagraphStyle(
            'MainTitle',
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=PRIMARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=30,
            spaceBefore=20,
            leading=32
        )
        
        styles['SubTitle'] = ParagraphStyle(
            'SubTitle',
            fontName='Helvetica',
            fontSize=12,
            textColor=LIGHT_TEXT_COLOR,
            alignment=TA_CENTER,
            spaceAfter=15,
            leading=16
        )
        
        styles['ChapterTitle'] = ParagraphStyle(
            'ChapterTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=PRIMARY_COLOR,
            alignment=TA_LEFT,
            spaceBefore=25,
            spaceAfter=15,
            leading=22,
            borderWidth=0,
            borderColor=ACCENT_COLOR,
            borderPadding=5
        )
        
        styles['SectionTitle'] = ParagraphStyle(
            'SectionTitle',
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=SECONDARY_COLOR,
            alignment=TA_LEFT,
            spaceBefore=18,
            spaceAfter=10,
            leading=18
        )
        
        styles['SubSectionTitle'] = ParagraphStyle(
            'SubSectionTitle',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=TEXT_COLOR,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            leading=15
        )
        
        styles['BodyText'] = ParagraphStyle(
            'BodyText',
            fontName='Helvetica',
            fontSize=10,
            textColor=TEXT_COLOR,
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=15,
            firstLineIndent=20
        )
        
        styles['BodyTextNoIndent'] = ParagraphStyle(
            'BodyTextNoIndent',
            fontName='Helvetica',
            fontSize=10,
            textColor=TEXT_COLOR,
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=15
        )
        
        styles['BulletText'] = ParagraphStyle(
            'BulletText',
            fontName='Helvetica',
            fontSize=10,
            textColor=TEXT_COLOR,
            alignment=TA_LEFT,
            spaceBefore=3,
            spaceAfter=3,
            leading=14,
            leftIndent=20,
            bulletIndent=10
        )
        
        styles['DataSource'] = ParagraphStyle(
            'DataSource',
            fontName='Helvetica-Oblique',
            fontSize=8,
            textColor=LIGHT_TEXT_COLOR,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4,
            leading=11
        )
        
        styles['Footer'] = ParagraphStyle(
            'Footer',
            fontName='Helvetica',
            fontSize=8,
            textColor=LIGHT_TEXT_COLOR,
            alignment=TA_CENTER,
            leading=10
        )
        
        styles['Highlight'] = ParagraphStyle(
            'Highlight',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=ACCENT_COLOR,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=8,
            leading=14
        )
        
        return styles


class ReportParser:
    """报告内容解析器"""
    
    @staticmethod
    def parse(content: str) -> List[Tuple[str, any]]:
        """解析报告内容并分类"""
        elements = []
        lines = content.split('\n')
        current_section = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 跳过空行但保留段落分隔
            if not line:
                if current_section:
                    current_section.append(line)
                continue
            
            # 检测标题级别
            if line.startswith('## ') and '深度分析报告' in line:
                # 主标题
                elements.append(('main_title', line.replace('## ', '').strip()))
                continue
            
            elif line.startswith('### 一、') or line.startswith('### 二、') or \
                 line.startswith('### 三、') or line.startswith('### 四、') or \
                 line.startswith('### 五、') or line.startswith('### 六、') or \
                 line.startswith('### 七、') or line.startswith('### 八、') or \
                 line.startswith('### 九、') or line.startswith('### 十、') or \
                 line.startswith('### 十一、') or line.startswith('### 十二、') or \
                 line.startswith('### 十三、') or line.startswith('### 十四、'):
                # 章节标题
                if current_section:
                    elements.append(('content', '\n'.join(current_section)))
                    current_section = []
                elements.append(('chapter', line.replace('### ', '').strip()))
            
            elif line.startswith('#### ') and not line.startswith('#### *'):
                # 小节标题
                elements.append(('subsection', line.replace('#### ', '').strip()))
            
            elif line.startswith('|'):
                # 表格行
                current_section.append(line)
            
            elif line.startswith('*数据来源：') or line.startswith('*来源：'):
                # 数据来源
                elements.append(('datasource', line))
            
            elif line.startswith('*'):
                # 无序列表
                clean_line = line.lstrip('*').strip()
                elements.append(('bullet', clean_line))
            
            elif re.match(r'^\d+\.\s+', line):
                # 带编号的列表
                elements.append(('numbered', line))
            
            else:
                current_section.append(line)
        
        # 处理最后的段落
        if current_section:
            elements.append(('content', '\n'.join(current_section)))
        
        return elements
    
    @staticmethod
    def clean_markdown(text: str) -> str:
        """清理Markdown格式，转换为纯文本"""
        # 处理加粗 **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        return text


class PDFGenerator:
    """PDF文档生成器"""
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.styles = PDFStyles.get_styles()
        self.page_numbers = []
        
    def create_canvas(self, filename):
        """创建画布并添加页眉页脚"""
        return canvas.Canvas(filename, pagesize=A4)
    
    def add_page_numbering(self, canvas, doc):
        """添加页码"""
        page_num = canvas.getPageNumber()
        text = f"- {page_num} -"
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(LIGHT_TEXT_COLOR)
        canvas.drawCentredString(PAGE_WIDTH / 2, 1.5 * cm, text)
        canvas.restoreState()
    
    def add_header(self, canvas, doc):
        """添加页眉"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(LIGHT_TEXT_COLOR)
        canvas.drawString(LEFT_MARGIN, PAGE_HEIGHT - 1.5 * cm, "专业深度分析报告")
        canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 1.5 * cm, 
                               datetime.now().strftime('%Y-%m-%d'))
        canvas.restoreState()
    
    def generate(self, report_content: str, title: str = "专业深度分析报告"):
        """生成PDF文档"""
        # 创建文档
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            leftMargin=LEFT_MARGIN,
            rightMargin=RIGHT_MARGIN,
            topMargin=TOP_MARGIN + 1*cm,
            bottomMargin=BOTTOM_MARGIN + 1*cm
        )
        
        # 解析报告内容
        parser = ReportParser()
        elements = parser.parse(report_content)
        
        # 构建PDF元素
        story = []
        
        for element_type, content in elements:
            if element_type == 'main_title':
                story.append(Spacer(1, 2*cm))
                story.append(Paragraph(content, self.styles['MainTitle']))
                
            elif element_type == 'chapter':
                story.append(Spacer(1, 0.5*cm))
                # 添加章节分隔线
                story.append(Paragraph(f"<font color='#3182ce'>━</font> {content}", 
                                      self.styles['ChapterTitle']))
                
            elif element_type == 'subsection':
                story.append(Paragraph(content, self.styles['SubSectionTitle']))
                
            elif element_type == 'content':
                # 处理段落内容 - 清理Markdown格式
                clean_content = ReportParser.clean_markdown(content)
                paragraphs = clean_content.split('\n\n')
                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        continue
                    story.append(Paragraph(para, self.styles['BodyText']))
                
            elif element_type == 'bullet':
                # 处理列表项 - 清理Markdown格式
                clean_content = ReportParser.clean_markdown(content)
                story.append(Paragraph(f"• {clean_content}", self.styles['BulletText']))
                
            elif element_type == 'numbered':
                # 处理编号列表 - 清理Markdown格式
                clean_content = ReportParser.clean_markdown(content)
                story.append(Paragraph(clean_content, self.styles['BulletText']))
                
            elif element_type == 'datasource':
                story.append(Paragraph(content, self.styles['DataSource']))
                
            elif element_type == 'table':
                # 表格处理
                story.append(content)
        
        # 构建PDF
        doc.build(story, 
                 onFirstPage=self.add_page_numbering,
                 onLaterPages=self.add_page_numbering)
        
        return self.output_path


def txt_to_pdf(input_file: str, output_file: str = None) -> str:
    """将TXT报告转换为PDF"""
    if output_file is None:
        output_file = input_file.replace('.txt', '.pdf')
    
    # 读取TXT内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取专业名称作为标题
    title_match = re.search(r'深度分析报告', content)
    title = title_match.group(0) if title_match else "专业深度分析报告"
    
    # 生成PDF
    generator = PDFGenerator(output_file)
    generator.generate(content, title)
    
    return output_file


def batch_convert(reports_dir: str, output_dir: str = None):
    """批量转换报告为PDF"""
    if output_dir is None:
        output_dir = reports_dir
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有TXT报告
    txt_files = [f for f in os.listdir(reports_dir) if f.endswith('.txt')]
    
    results = []
    for txt_file in txt_files:
        input_path = os.path.join(reports_dir, txt_file)
        output_file = txt_file.replace('.txt', '.pdf')
        output_path = os.path.join(output_dir, output_file)
        
        try:
            result = txt_to_pdf(input_path, output_path)
            results.append({
                'file': txt_file,
                'status': 'success',
                'output': result
            })
            print(f"✓ 成功转换: {txt_file} -> {output_file}")
        except Exception as e:
            results.append({
                'file': txt_file,
                'status': 'error',
                'error': str(e)
            })
            print(f"✗ 转换失败: {txt_file} - {str(e)}")
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # 单文件转换
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        result = txt_to_pdf(input_file, output_file)
        print(f"PDF已生成: {result}")
    else:
        # 批量转换
        reports_dir = '/workspace/data/reports'
        output_dir = '/workspace/data/reports'
        
        print("=" * 60)
        print("批量PDF转换工具")
        print("=" * 60)
        print(f"\n源目录: {reports_dir}")
        print(f"输出目录: {output_dir}")
        print()
        
        results = batch_convert(reports_dir, output_dir)
        
        print()
        print("=" * 60)
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"转换完成: {success_count}/{len(results)} 个文件成功")
        print("=" * 60)
