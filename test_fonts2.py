#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体测试和修复脚本
"""

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

print("="*60)
print("测试中文字体加载")
print("="*60)

# 检查字体文件
font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
print(f"\n字体文件: {font_path}")
print(f"存在: {os.path.exists(font_path)}")
if os.path.exists(font_path):
    print(f"大小: {os.path.getsize(font_path)} bytes")

# 尝试不同方式加载字体
print("\n尝试加载字体...")

# 方法1: 尝试作为普通TTF加载
try:
    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
    print("✅ 成功加载为普通字体")
except Exception as e:
    print(f"❌ 普通加载失败: {e}")

# 方法2: 尝试指定字体索引（对于TTC集合）
try:
    pdfmetrics.registerFont(TTFont('ChineseFont1', font_path, subfontIndex=0))
    print("✅ 成功加载第1个字体")
except Exception as e:
    print(f"❌ 索引0加载失败: {e}")

try:
    pdfmetrics.registerFont(TTFont('ChineseFont2', font_path, subfontIndex=1))
    print("✅ 成功加载第2个字体")
except Exception as e:
    print(f"❌ 索引1加载失败: {e}")

# 检查已注册的字体
print("\n已注册字体:")
fonts = list(pdfmetrics.getRegisteredFontNames())
for f in sorted(fonts):
    print(f"  - {f}")

# 检查是否有中文字体成功加载
has_chinese = any('Chinese' in f or 'wqy' in f.lower() for f in fonts)
print(f"\n中文字体加载: {'✅ 成功' if has_chinese else '❌ 失败'}")
