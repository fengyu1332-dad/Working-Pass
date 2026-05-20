#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为缺少名校推荐的专业填充数据
"""

import urllib.request
import urllib.error
import json
import ssl
import time

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 名校推荐数据库（按学科类别）
UNIVERSITIES_DB = {
    'computer': {
        'domestic': ['清华大学', '北京大学', '浙江大学', '国防科技大学', '北京航空航天大学', '哈尔滨工业大学', '上海交通大学', '南京大学', '华中科技大学', '电子科技大学'],
        'international': ['麻省理工学院', '斯坦福大学', '卡内基梅隆大学', '加州大学伯克利分校', '牛津大学', '剑桥大学', '哈佛大学', 'ETH苏黎世联邦理工学院']
    },
    'engineering': {
        'domestic': ['清华大学', '上海交通大学', '浙江大学', '哈尔滨工业大学', '北京航空航天大学', '天津大学', '东南大学', '华中科技大学', '西安交通大学', '同济大学'],
        'international': ['麻省理工学院', '斯坦福大学', '加州大学伯克利分校', '帝国理工学院', '苏黎世联邦理工学院', '东京大学', '代尔夫特理工大学', '密歇根大学']
    },
    'medicine': {
        'domestic': ['北京协和医学院', '北京大学医学部', '复旦大学上海医学院', '上海交通大学医学院', '中山大学中山医学院', '华中科技大学同济医学院', '四川大学华西医学院', '浙江大学医学院'],
        'international': ['哈佛大学医学院', '约翰·霍普金斯大学', '牛津大学医学院', '剑桥大学医学院', '斯坦福大学医学院', '帝国理工学院医学院', '东京大学医学院', '卡罗林斯卡学院']
    },
    'economics': {
        'domestic': ['北京大学', '清华大学', '复旦大学', '上海交通大学', '中国人民大学', '浙江大学', '南京大学', '中央财经大学', '对外经济贸易大学', '厦门大学'],
        'international': ['哈佛大学', '斯坦福大学', '麻省理工学院', '伦敦商学院', '沃顿商学院', '牛津大学', '剑桥大学', '芝加哥大学']
    },
    'science': {
        'domestic': ['北京大学', '清华大学', '复旦大学', '南京大学', '中国科学技术大学', '浙江大学', '上海交通大学', '南开大学', '吉林大学', '武汉大学'],
        'international': ['麻省理工学院', '哈佛大学', '斯坦福大学', '加州大学伯克利分校', '剑桥大学', '牛津大学', '东京大学', '苏黎世联邦理工学院']
    },
    'liberal_arts': {
        'domestic': ['北京大学', '清华大学', '复旦大学', '南京大学', '中国人民大学', '浙江大学', '武汉大学', '北京师范大学', '华东师范大学', '中山大学'],
        'international': ['哈佛大学', '斯坦福大学', '牛津大学', '剑桥大学', '哥伦比亚大学', '芝加哥大学', '耶鲁大学', '普林斯顿大学']
    },
    'art': {
        'domestic': ['中央美术学院', '中国美术学院', '清华大学美术学院', '四川美术学院', '广州美术学院', '湖北美术学院', '鲁迅美术学院', '天津美术学院'],
        'international': ['皇家艺术学院', '伦敦艺术大学', '帕森斯设计学院', '罗德岛设计学院', '普拉特学院', '纽约视觉艺术学院', '艺术中心设计学院', '萨凡纳艺术与设计学院']
    },
    'education': {
        'domestic': ['北京师范大学', '华东师范大学', '华南师范大学', '华中师范大学', '东北师范大学', '陕西师范大学', '南京师范大学', '浙江师范大学'],
        'international': ['哈佛大学教育学院', '伦敦大学学院教育学院', '斯坦福大学教育学院', '哥伦比亚大学教师学院', '墨尔本大学教育学院', '密歇根大学教育学院']
    },
    'law': {
        'domestic': ['中国政法大学', '北京大学法学院', '中国人民大学法学院', '华东政法大学', '武汉大学法学院', '西南政法大学', '吉林大学法学院', '复旦大学法学院'],
        'international': ['哈佛大学法学院', '耶鲁大学法学院', '斯坦福大学法学院', '牛津大学法学院', '剑桥大学法学院', '伦敦政治经济学院', '哥伦比亚大学法学院', '纽约大学法学院']
    },
    'agriculture': {
        'domestic': ['中国农业大学', '浙江大学', '南京农业大学', '华中农业大学', '西北农林科技大学', '北京林业大学', '华南农业大学', '四川农业大学'],
        'international': ['瓦赫宁根大学', '加州大学戴维斯分校', '康奈尔大学', '德克萨斯农工大学', '密歇根州立大学', '普渡大学', '爱荷华州立大学', '苏赛克斯大学']
    },
    'management': {
        'domestic': ['清华大学', '北京大学', '复旦大学', '上海交通大学', '中国人民大学', '浙江大学', '南京大学', '中山大学', '厦门大学', '武汉大学'],
        'international': ['哈佛商学院', '斯坦福商学院', '沃顿商学院', '伦敦商学院', '麻省理工斯隆管理学院', '欧洲工商管理学院', '哥伦比亚大学商学院', '西北大学凯洛格商学院']
    },
    'default': {
        'domestic': ['北京大学', '清华大学', '复旦大学', '上海交通大学', '浙江大学', '南京大学', '中国人民大学', '武汉大学'],
        'international': ['哈佛大学', '斯坦福大学', '麻省理工学院', '牛津大学', '剑桥大学', '加州大学伯克利分校', '耶鲁大学', '普林斯顿大学']
    }
}

def get_category_type(code, name):
    """根据专业代码和名称判断类别"""
    # 计算机相关
    if any(k in name for k in ['计算机', '软件', '网络', '信息安全', '人工智能', '数据科学', '大数据', '物联网', '数字媒体']) or code.startswith('0809'):
        return 'computer'
    
    # 医学相关
    if code.startswith('10'):
        return 'medicine'
    
    # 工程相关（建筑、机械、电子等）
    if any(k in name for k in ['建筑', '土木', '机械', '电气', '电子', '通信', '自动化', '化工', '材料', '能源', '环境']) or code.startswith('08'):
        return 'engineering'
    
    # 经济金融相关
    if any(k in name for k in ['经济', '金融', '财政', '税务', '保险', '投资']) or code.startswith('02'):
        return 'economics'
    
    # 理科相关
    if code.startswith('07'):
        return 'science'
    
    # 文科相关
    if any(k in name for k in ['文学', '历史', '哲学', '法学', '法律', '政治', '社会', '外语', '新闻', '传播', '教育']) or code.startswith('01') or code.startswith('03') or code.startswith('04') or code.startswith('05') or code.startswith('06'):
        return 'liberal_arts'
    
    # 艺术相关
    if code.startswith('13') or any(k in name for k in ['艺术', '设计', '音乐', '美术', '舞蹈', '戏剧', '影视']):
        return 'art'
    
    # 教育相关
    if any(k in name for k in ['教育']) or code.startswith('04'):
        return 'education'
    
    # 法律相关
    if any(k in name for k in ['法学', '法律', '政治']) or code.startswith('03'):
        return 'law'
    
    # 农学相关
    if code.startswith('09'):
        return 'agriculture'
    
    # 管理相关
    if code.startswith('12') or any(k in name for k in ['管理', '工商', '会计', '财务', '物流', '电商']):
        return 'management'
    
    return 'default'

def check_universities(top_unis):
    """检查是否有有效的数据"""
    if not top_unis:
        return False
    if isinstance(top_unis, str):
        try:
            top_unis = json.loads(top_unis)
        except:
            return False
    if isinstance(top_unis, dict):
        domestic = top_unis.get('domestic', [])
        international = top_unis.get('international', [])
        return bool(domestic or international)
    return False

def main():
    print('=' * 80)
    print('为缺少名校推荐的专业填充数据')
    print('=' * 80)
    
    # 获取所有专业
    print('\n正在获取所有专业列表...')
    url = f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name,top_universities'
    req = urllib.request.Request(url)
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    
    with urllib.request.urlopen(req, context=ctx) as response:
        all_majors = json.loads(response.read().decode('utf-8'))
    
    print(f'成功获取 {len(all_majors)} 个专业！')
    
    success_count = 0
    fail_count = 0
    
    print('\n开始更新专业...')
    for i, major in enumerate(all_majors, 1):
        major_id = major['id']
        code = major['code']
        name = major['name']
        top_unis = major.get('top_universities')
        
        # 如果已经有数据，跳过
        if check_universities(top_unis):
            continue
        
        # 根据专业类型获取推荐学校
        category_type = get_category_type(code, name)
        universities = UNIVERSITIES_DB.get(category_type, UNIVERSITIES_DB['default'])
        
        # 更新
        update_url = f'{SUPABASE_URL}/rest/v1/majors?id=eq.{major_id}'
        data = json.dumps({'top_universities': universities}).encode('utf-8')
        req = urllib.request.Request(update_url, data=data, method='PATCH')
        req.add_header('apikey', SUPABASE_KEY)
        req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15):
                success_count += 1
                print(f'✅ [{i}/{len(all_majors)}] {code} {name} ({category_type})')
        except Exception as e:
            fail_count += 1
            print(f'❌ [{i}/{len(all_majors)}] {code} {name}: {str(e)}')
        
        time.sleep(0.1)
    
    print('\n' + '=' * 80)
    print(f'更新完成！成功: {success_count}, 失败: {fail_count}')
    print('=' * 80)


if __name__ == '__main__':
    main()
