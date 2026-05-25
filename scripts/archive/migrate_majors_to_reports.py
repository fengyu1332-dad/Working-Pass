#!/usr/bin/env python3
"""
将 majors 表的数据迁移到 reports 表
"""
import requests
import json
import time

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

def get_majors():
    """获取所有专业数据"""
    print('📚 正在获取 majors 表数据...')
    response = requests.get(
        f'{SUPABASE_URL}/rest/v1/majors?select=*',
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        print(f'✅ 获取到 {len(data)} 条专业数据')
        return data
    else:
        print(f'❌ 获取数据失败: {response.text}')
        return []

def migrate_to_reports(majors):
    """将专业数据迁移到 reports 表"""
    print(f'\n🚀 开始迁移 {len(majors)} 条数据到 reports 表...')
    
    success_count = 0
    error_count = 0
    batch_size = 50
    
    for i in range(0, len(majors), batch_size):
        batch = majors[i:i+batch_size]
        reports = []
        
        for major in batch:
            # 提取专业代码（去掉T/K后缀用于查询）
            major_code = major.get('code', '')
            
            # 构建报告数据
            report = {
                'major_code': major_code,
                'major_name': major.get('name', ''),
                'category': major.get('category', ''),
                'preview_content': generate_preview(major),
                'full_content': generate_full_content(major),
                'status': 'published',
                'download_count': 0
            }
            reports.append(report)
        
        # 批量插入
        try:
            response = requests.post(
                f'{SUPABASE_URL}/rest/v1/reports',
                headers=headers,
                json=reports
            )
            
            if response.status_code in [200, 201]:
                success_count += len(reports)
                print(f'✅ 已迁移 {success_count}/{len(majors)} 条数据')
            else:
                error_count += len(reports)
                print(f'❌ 批量插入失败: {response.status_code} - {response.text[:100]}')
        
        except Exception as e:
            error_count += len(reports)
            print(f'❌ 批量插入异常: {e}')
        
        # 添加延迟以避免API限流
        time.sleep(0.5)
    
    print(f'\n📊 迁移完成！')
    print(f'   ✅ 成功: {success_count} 条')
    print(f'   ❌ 失败: {error_count} 条')
    
    return success_count, error_count

def generate_preview(major):
    """生成预览内容（前20%）"""
    sections = []
    
    # 专业概述
    if major.get('overview'):
        sections.append(f"【专业概述】\n{major.get('overview', '')}")
    
    # 适合人群
    if major.get('suitable_for'):
        sections.append(f"【适合人群】\n{major.get('suitable_for', '')}")
    
    # 雪峰点评（部分）
    if major.get('xuefeng_comment'):
        comment = major.get('xuefeng_comment', '')
        # 只取前200个字符
        preview_comment = comment[:200] if len(comment) > 200 else comment
        sections.append(f"【雪峰点评（预览）】\n{preview_comment}...\n\n（完整点评需解锁报告）")
    
    return '\n\n'.join(sections)

def generate_full_content(major):
    """生成完整报告内容"""
    sections = []
    
    # 专业概述
    if major.get('overview'):
        sections.append(f"【专业概述】\n{major.get('overview', '')}")
    
    # 课程安排
    if major.get('yearly_courses'):
        courses = major.get('yearly_courses')
        if isinstance(courses, str):
            try:
                courses = json.loads(courses)
            except:
                courses = {}
        sections.append(f"【四年课程安排】\n")
        for year, items in courses.items():
            if isinstance(items, list):
                sections.append(f"{year}: {', '.join(items)}")
    
    # 就业前景
    if major.get('career_outlook'):
        sections.append(f"【就业前景】\n{major.get('career_outlook', '')}")
    
    # 薪资范围
    if major.get('salary_range'):
        sections.append(f"【薪资范畴】\n{major.get('salary_range', '')}")
    
    # 适合人群
    if major.get('suitable_for'):
        sections.append(f"【适合人群】\n{major.get('suitable_for', '')}")
    
    # 顶级院校
    if major.get('top_universities'):
        unis = major.get('top_universities')
        if isinstance(unis, str):
            try:
                unis = json.loads(unis)
            except:
                unis = {}
        
        if unis.get('domestic'):
            sections.append(f"【国内顶级院校】\n{', '.join(unis.get('domestic', []))}")
        if unis.get('international'):
            sections.append(f"【国际顶级院校】\n{', '.join(unis.get('international', []))}")
    
    # 雪峰点评（完整）
    if major.get('xuefeng_comment'):
        sections.append(f"【雪峰点评】\n{major.get('xuefeng_comment', '')}")
    
    return '\n\n'.join(sections)

def main():
    print('=' * 60)
    print('🔄 专业星图 - 数据迁移工具')
    print('   将 majors 表数据迁移到 reports 表')
    print('=' * 60)
    
    # 1. 获取专业数据
    majors = get_majors()
    if not majors:
        print('❌ 没有数据可迁移，程序退出')
        return
    
    # 2. 迁移数据
    migrate_to_reports(majors)
    
    # 3. 验证结果
    print('\n🔍 验证迁移结果...')
    response = requests.get(
        f'{SUPABASE_URL}/rest/v1/reports?select=id&limit=1',
        headers=headers
    )
    if response.status_code == 200:
        print(f'✅ reports 表现在有数据了！')
    else:
        print(f'⚠️ 验证请求失败: {response.text}')
    
    print('\n🎉 迁移完成！')

if __name__ == '__main__':
    main()
