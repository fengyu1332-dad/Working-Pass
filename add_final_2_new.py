
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
        'code': '050234',
        'name': '荷兰语',
        'category': '05 文学',
        'category_icon': '🇳🇱',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '荷兰语专业培养掌握荷兰语语言文学的复合型人才，从事荷兰语翻译、教学和研究工作。',
        'what_you_learn': '荷兰语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对荷兰语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对荷兰语人才有需求。',
        'xuefeng_comment': '荷兰语是欧洲重要语言之一，随着中荷合作的深入，对荷兰语人才的需求在增长。建议对欧洲文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['荷兰语语音', '基础荷兰语', '荷兰文化概况', '英语'], '大二': ['荷兰语语法', '中级荷兰语', '荷兰文学选读', '荷兰社会'], '大三': ['高级荷兰语', '翻译理论与实践', '荷兰历史', '经贸荷兰语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['阿姆斯特丹大学', '莱顿大学']}
    },
    {
        'code': '080204T',
        'name': '材料成型及控制工程',
        'category': '08 工学',
        'category_icon': '⚙️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '材料成型及控制工程专业培养掌握材料成型技术的工程技术人才，从事材料成型工艺的设计和控制工作。',
        'what_you_learn': '材料科学基础、材料成型工艺、金属塑性成型、塑料成型、模具设计、控制工程',
        'suitable_for': '对材料和工程有兴趣的学生。',
        'career_outlook': '制造企业、材料企业、科研机构等对材料成型及控制工程人才有需求。',
        'xuefeng_comment': '材料成型及控制工程是传统优势专业，就业稳定。建议对材料和工程有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学', '大学物理', '工程制图', '材料科学基础'], '大二': ['理论力学', '材料力学', '机械设计基础', '材料成型工艺'], '大三': ['金属塑性成型', '塑料成型', '模具设计', '控制工程'], '大四': ['企业实习', '毕业设计']},
        'top_universities': {'domestic': ['华中科技大学、哈尔滨工业大学、上海交通大学、大连理工大学'], 'international': ['麻省理工学院、加州大学伯克利分校、斯坦福大学']}
    }
]

def main():
    print('=' * 70)
    print('📊 最后2个新专业 - 达成450！')
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

