#!/usr/bin/env python3
import os
import glob

def fix_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复HTML转义字符
        content = content.replace('&lt;', '<').replace('&gt;', '>')
        
        # 检查是否真的修改了
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Fixed: {file_path}')
            return True
        else:
            print(f'✅ Already OK: {file_path}')
            return False
    except Exception as e:
        print(f'❌ Error processing {file_path}: {e}')
        return False

def main():
    # 修复根目录的HTML文件
    html_files = []
    html_files.extend(glob.glob('*.html'))
    html_files.extend(glob.glob('user/*.html'))
    html_files.extend(glob.glob('admin/*.html'))
    
    print(f'Found {len(html_files)} HTML files to check...')
    print('-' * 60)
    
    fixed_count = 0
    for html_file in html_files:
        if fix_html_file(html_file):
            fixed_count += 1
    
    print('-' * 60)
    print(f'Total fixed: {fixed_count} files')

if __name__ == '__main__':
    os.chdir('/workspace')
    main()
