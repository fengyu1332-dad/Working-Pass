
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
        'code': '050227',
        'name': '老挝语',
        'category': '05 文学',
        'category_icon': '🇱🇦',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '老挝语专业培养掌握老挝语语言文学的复合型人才，从事老挝语翻译、教学和研究工作。',
        'what_you_learn': '老挝语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对老挝语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对老挝语人才有需求。',
        'xuefeng_comment': '老挝语是东南亚国家的重要语言之一，随着中国与东盟合作的深入，对老挝语人才的需求在增长。建议对东南亚文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['老挝语语音', '基础老挝语', '老挝文化概况', '英语'], '大二': ['老挝语语法', '中级老挝语', '老挝文学选读', '老挝社会'], '大三': ['高级老挝语', '翻译理论与实践', '老挝历史', '经贸老挝语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学', '云南民族大学'], 'international': ['老挝国立大学']}
    },
    {
        'code': '050230',
        'name': '越南语',
        'category': '05 文学',
        'category_icon': '🇻🇳',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '越南语专业培养掌握越南语语言文学的复合型人才，从事越南语翻译、教学和研究工作。',
        'what_you_learn': '越南语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对越南语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对越南语人才有需求。',
        'xuefeng_comment': '越南语是东南亚国家的重要语言之一，随着中越经贸文化交流的深入，对越南语人才的需求在增长。建议对东南亚文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['越南语语音', '基础越南语', '越南文化概况', '英语'], '大二': ['越南语语法', '中级越南语', '越南文学选读', '越南社会'], '大三': ['高级越南语', '翻译理论与实践', '越南历史', '经贸越南语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学', '云南民族大学', '广西民族大学'], 'international': ['河内国家大学', '胡志明市国家大学']}
    }
]

def main():
    print('=' * 70)
    print('📊 最后2个专业 - 达成450！')
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

