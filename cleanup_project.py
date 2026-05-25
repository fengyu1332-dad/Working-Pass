#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目清理脚本 - 清理临时文件，整理项目结构
"""
import os
import shutil

# 保留的重要文件
KEEP_FILES = {
    'config.py',
    'requirements.txt',
    'cleanup_project.py'  # 保留这个脚本自己
}

# 归档目录
ARCHIVE_DIR = 'scripts/archive'

def main():
    print('=' * 60)
    print('专业星图 - 项目清理脚本')
    print('=' * 60)
    
    # 确保归档目录存在
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    # 获取根目录下的所有Python文件
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    print(f'\n发现 {len(py_files)} 个Python文件')
    
    # 处理每个Python文件
    archived = 0
    kept = 0
    
    for filename in py_files:
        if filename in KEEP_FILES:
            print(f'✅ 保留: {filename}')
            kept += 1
        else:
            # 归档文件
            src = filename
            dst = os.path.join(ARCHIVE_DIR, filename)
            shutil.move(src, dst)
            print(f'📦 归档: {filename} -> {ARCHIVE_DIR}/')
            archived += 1
    
    # 处理旧版本HTML文件
    html_files = [f for f in os.listdir('.') if f.startswith('major_starmap_')]
    for filename in html_files:
        dst = os.path.join('archive/old_pages', filename)
        shutil.move(filename, dst)
        print(f'📦 归档: {filename} -> archive/old_pages/')
    
    print(f'\n清理完成！')
    print(f'✅ 保留: {kept} 个文件')
    print(f'📦 归档: {archived} 个Python脚本, {len(html_files)} 个旧页面')
    print(f'\n归档位置: {ARCHIVE_DIR}/')
    print('=' * 60)

if __name__ == '__main__':
    main()
