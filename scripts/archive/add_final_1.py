
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

def import_major(major):
    url = f'{SUPABASE_URL}/rest/v1/majors'
    data = json.dumps(major).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Prefer', 'return=minimal')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return True, response.status
    except urllib.error.HTTPError as e:
        return False, e.code if e.code != 409 else 409

majors_to_add = [
    {
        'code': '080206T',
        'name': '过程装备与控制工程',
        'category': '08 工学',
        'category_icon': '⚙️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '过程装备与控制工程专业培养掌握过程装备技术的工程技术人才，从事过程装备的设计和控制工作。',
        'what_you_learn': '过程装备设计、过程流体机械、过程控制原理、化工原理、机械设计、工程热力学',
        'suitable_for': '对过程装备和控制有兴趣的学生。',
        'career_outlook': '化工企业、能源企业、机械企业等对过程装备与控制工程人才有需求。',
        'xuefeng_comment': '过程装备与控制工程是化工和能源的重要专业，就业稳定。建议对过程装备和控制有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学', '大学物理', '工程制图', '机械设计基础'], '大二': ['理论力学', '材料力学', '化工原理', '工程热力学'], '大三': ['过程装备设计', '过程流体机械', '过程控制原理', '机械设计'], '大四': ['企业实习', '毕业设计']},
        'top_universities': {'domestic': ['浙江大学、天津大学、华东理工大学、大连理工大学'], 'international': ['麻省理工学院、加州大学伯克利分校、斯坦福大学']}
    }
]

def main():
    print('=' * 70)
    print('📊 最后1个专业 - 突破450！')
    print('=' * 70)
    
    success = failed = skipped = 0
    
    for major in majors_to_add:
        print(f'\n正在导入: {major["code"]} - {major["name"]}')
        ok, code = import_major(major)
        if ok or code in [200, 201]:
            success += 1
            print(f'✅ 成功')
        elif code == 409:
            skipped += 1
            print(f'⏭️ 已存在')
        else:
            failed += 1
            print(f'❌ 失败 (HTTP {code})')
        time.sleep(0.2)
    
    print(f'\n导入完成！成功: {success}, 跳过: {skipped}, 失败: {failed}')

if __name__ == '__main__':
    main()

