#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业报告PDF生成器 - 使用fpdf2
功能：将TXT格式的专业分析报告转换为精美的PDF文档
"""

import os
import re
from datetime import datetime
from fpdf import FPDF


class ProfessionalPDF(FPDF):
    """自定义PDF类"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        
    def header(self):
        """页眉"""
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, '专业深度分析报告', align='R')
            self.ln(15)
    
    def footer(self):
        """页脚"""
        self.set_y(-20)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'- {self.page_no()} -', align='C')
    
    def add_main_title(self, title):
        """添加主标题"""
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(26, 54, 93)
        self.ln(20)
        self.cell(0, 15, title, align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(10)
    
    def add_chapter(self, chapter_text):
        """添加章节标题"""
        self.ln(10)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(26, 54, 93)
        self.set_fill_color(247, 250, 252)
        self.cell(0, 12, '  ' + chapter_text, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(5)
    
    def add_subsection(self, title):
        """添加小节标题"""
        self.ln(5)
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(44, 82, 130)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
    
    def add_paragraph(self, text):
        """添加段落"""
        self.set_font('helvetica', '', 10)
        self.set_text_color(45, 55, 72)
        self.multi_cell(0, 6, text, align='J')
        self.ln(3)
    
    def add_bullet(self, text):
        """添加列表项"""
        self.set_font('helvetica', '', 10)
        self.set_text_color(45, 55, 72)
        self.set_x(15)
        self.cell(5, 6, chr(8226))
        self.multi_cell(0, 6, text, align='L')
    
    def add_numbered_item(self, text):
        """添加编号列表"""
        self.set_font('helvetica', '', 10)
        self.set_text_color(45, 55, 72)
        self.multi_cell(0, 6, '    ' + text, align='L')
    
    def add_data_source(self, source):
        """添加数据来源"""
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(113, 128, 150)
        self.cell(0, 6, source, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)


class ReportParser:
    """报告内容解析器"""
    
    @staticmethod
    def parse(content: str) -> list:
        """解析报告内容"""
        elements = []
        lines = content.split('\n')
        current_section = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if current_section:
                    current_section.append(line)
                continue
            
            # 主标题
            if line.startswith('## ') and '深度分析报告' in line:
                elements.append(('main_title', line.replace('## ', '').strip()))
                continue
            
            # 章节标题
            if (line.startswith('### 一、') or line.startswith('### 二、') or
                line.startswith('### 三、') or line.startswith('### 四、') or
                line.startswith('### 五、') or line.startswith('### 六、') or
                line.startswith('### 七、') or line.startswith('### 八、') or
                line.startswith('### 九、') or line.startswith('### 十、') or
                line.startswith('### 十一、') or line.startswith('### 十二、') or
                line.startswith('### 十三、') or line.startswith('### 十四、')):
                if current_section:
                    elements.append(('content', '\n'.join(current_section)))
                    current_section = []
                elements.append(('chapter', line.replace('### ', '').strip()))
                continue
            
            # 小节标题
            if line.startswith('#### ') and not line.startswith('#### *'):
                elements.append(('subsection', line.replace('#### ', '').strip()))
                continue
            
            # 数据来源
            if line.startswith('*数据来源：') or line.startswith('*来源：'):
                elements.append(('datasource', line))
                continue
            
            # 列表项
            if line.startswith('*'):
                elements.append(('bullet', line.lstrip('*').strip()))
                continue
            
            # 编号列表
            if re.match(r'^\d+\.\s+', line):
                elements.append(('numbered', line))
                continue
            
            current_section.append(line)
        
        if current_section:
            elements.append(('content', '\n'.join(current_section)))
        
        return elements
    
    @staticmethod
    def clean_markdown(text: str) -> str:
        """清理Markdown格式"""
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        return text


def generate_pdf(input_file: str, output_file: str = None) -> str:
    """生成PDF文档"""
    if output_file is None:
        output_file = input_file.replace('.txt', '.pdf')
    
    # 读取内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析报告
    parser = ReportParser()
    elements = parser.parse(content)
    
    # 创建PDF
    pdf = ProfessionalPDF()
    pdf.add_page()
    
    for element_type, text in elements:
        # 清理格式
        text = parser.clean_markdown(text)
        
        if element_type == 'main_title':
            pdf.add_main_title(text)
            
        elif element_type == 'chapter':
            pdf.add_chapter(text)
            
        elif element_type == 'subsection':
            pdf.add_subsection(text)
            
        elif element_type == 'content':
            # 处理段落
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if para:
                    pdf.add_paragraph(para)
            
        elif element_type == 'bullet':
            pdf.add_bullet(text)
            
        elif element_type == 'numbered':
            pdf.add_numbered_item(text)
            
        elif element_type == 'datasource':
            pdf.add_data_source(text)
    
    # 保存PDF
    pdf.output(output_file)
    return output_file


def batch_convert(reports_dir: str, output_dir: str = None):
    """批量转换"""
    if output_dir is None:
        output_dir = reports_dir
    
    os.makedirs(output_dir, exist_ok=True)
    
    txt_files = [f for f in os.listdir(reports_dir) if f.endswith('.txt')]
    
    results = []
    for txt_file in txt_files:
        input_path = os.path.join(reports_dir, txt_file)
        output_file = txt_file.replace('.txt', '.pdf')
        output_path = os.path.join(output_dir, output_file)
        
        try:
            result = generate_pdf(input_path, output_path)
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
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        result = generate_pdf(input_file, output_file)
        print(f"PDF已生成: {result}")
    else:
        reports_dir = '/workspace/data/reports'
        output_dir = '/workspace/data/reports'
        
        print("=" * 60)
        print("批量PDF转换工具 (fpdf2)")
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
