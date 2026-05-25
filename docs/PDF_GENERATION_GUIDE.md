# 专业星图 PDF 批量生成系统

## 概述

这是一个完整的、可复用的专业报告PDF批量生成系统，包含文本清理、格式化、PDF生成的完整工作流。

## 核心文件

### 1. pdf_generator.py - PDF生成器（最终版）
主要功能：
- 将TXT格式的专业报告转换为专业排版的PDF
- 支持中文显示（使用文泉驿字体）
- 完整的样式系统和层次结构

主要函数：
- `generate_pdf(input_file, output_file=None)`: 生成单个PDF
- `batch_convert(reports_dir, output_dir=None)`: 批量转换TXT为PDF

### 2. clean_reports_v2.py - 文本清理工具
主要功能：
- 自动去除报告开头的指令性文字
- 修复段落切分问题
- 清理多余空行和空格

主要函数：
- `clean_report_content_v2(content)`: 清理单个报告内容
- `process_directory_v2(reports_dir, backup_dir)`: 批量清理目录中的报告

### 3. batch_generate_all.py - 完整批量工作流
整合了所有步骤，一键生成所有PDF：
1. 检查依赖和目录
2. 清理报告文本
3. 生成PDF文档
4. 验证生成结果

## 排版规范

### 标题层级

| Markdown | 样式 | 字号 | 颜色 |
|----------|------|------|------|
| `## 标题` | 主标题 | 22pt | 深蓝色 (#1a365d) |
| `### 一、标题` | 章节标题 | 15pt | 深蓝色 (#1a365d) |
| `#### 1.1 标题` | 小节标题 | 13pt | 蓝色 (#2c5282) |
| `##### 标题` | 子标题 | 11pt | 深灰色 (#2d3748) |

### 段落和列表
- **段落间距**: 8pt 前后间距 + 0.3cm 段落分隔
- **行间距**: 15pt (正文), 14pt (列表)
- **列表项**: 圆点符号，缩进15pt

### 页面设置
- **尺寸**: A4 (210mm × 297mm)
- **边距**: 2.5cm 四边
- **对齐方式**: 两端对齐（正文），居中（标题）

## 使用方法

### 快速开始（推荐）

```bash
cd /workspace
python batch_generate_all.py
```

### 自定义使用

#### 1. 仅清理文本
```bash
cd /workspace
python clean_reports_v2.py
```

#### 2. 仅生成PDF
```bash
cd /workspace
python pdf_generator.py
```

#### 3. 作为模块使用

```python
# 导入模块
from pdf_generator import generate_pdf, batch_convert
from clean_reports_v2 import clean_report_content_v2

# 单个文件
generate_pdf('data/reports/report_080901_计算机科学与技术.txt')

# 批量转换
batch_convert('data/reports')

# 清理单个报告内容
with open('my_report.txt', 'r', encoding='utf-8') as f:
    content = f.read()
clean_content = clean_report_content_v2(content)
```

## 目录结构

```
/workspace/
├── pdf_generator.py              # PDF生成器（最终版）
├── clean_reports_v2.py           # 文本清理工具
├── batch_generate_all.py         # 完整批量工作流
├── data/
│   └── reports/
│       ├── report_020301_金融学.txt
│       ├── report_020301_金融学.pdf
│       ├── report_020401_新闻学.txt
│       ├── report_020401_新闻学.pdf
│       ├── ...
│       └── backup_before_clean/  # 自动备份目录
└── requirements.txt              # 依赖列表
```

## 依赖安装

```bash
pip install reportlab
```

## 字体支持

系统使用文泉驿微米黑（wqy-microhei.ttc）作为中文字体。

Linux系统安装：
```bash
sudo apt-get install fonts-wqy-microhei
```

## 报告格式要求

### TXT报告格式
```
### 一、专业概述
#### 1.1 专业定义与学科定位
本专业旨在培养具备良好数理基础...

#### 1.2 培养目标
培养目标1...
培养目标2...

### 二、课程安排与学习内容
...
```

### 要点：
- 使用Markdown风格的标题（###, ####, #####）
- 段落之间留空行分隔
- 列表项使用 * 或数字开头
- 数据来源标注在段落下方，格式为：*数据来源：...*

## 问题排查

### 中文显示为方框
- 确认文泉驿字体已安装
- 检查 `pdf_generator.py` 中的字体路径配置

### PDF生成失败
- 检查TXT文件是否为UTF-8编码
- 查看错误信息，确保依赖完整

### 段落格式不对
- 确保TXT文件中有正确的空行分隔
- 运行文本清理工具重新格式化

## 版本历史

- **v3.0 (当前版)**: 增强段落分隔，优化视觉层次
- **v2.0**: 修复中文显示，改进排版
- **v1.0**: 初始版本

## 联系方式

如有问题，请查看项目根目录下的相关文档。
