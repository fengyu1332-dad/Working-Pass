
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
        'code': '050223',
        'name': '瑞典语',
        'category': '05 文学',
        'category_icon': '🇸🇪',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '瑞典语专业培养掌握瑞典语语言文学的复合型人才，从事瑞典语翻译、教学和研究工作。',
        'what_you_learn': '瑞典语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对瑞典语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对瑞典语人才有需求。',
        'xuefeng_comment': '瑞典语是北欧国家的重要语言之一，随着中国与北欧合作的深入，对瑞典语人才的需求在增长。建议对北欧文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['瑞典语语音', '基础瑞典语', '瑞典文化概况', '英语'], '大二': ['瑞典语语法', '中级瑞典语', '瑞典文学选读', '瑞典社会'], '大三': ['高级瑞典语', '翻译理论与实践', '瑞典历史', '经贸瑞典语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['斯德哥尔摩大学', '乌普萨拉大学']}
    },
    {
        'code': '050228',
        'name': '希腊语',
        'category': '05 文学',
        'category_icon': '🇬🇷',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '希腊语专业培养掌握希腊语语言文学的复合型人才，从事希腊语翻译、教学和研究工作。',
        'what_you_learn': '希腊语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对希腊语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对希腊语人才有需求。',
        'xuefeng_comment': '希腊语是西方文明的重要语言，随着中希文化交流的深入，对希腊语人才的需求在增长。建议对希腊文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['希腊语语音', '基础希腊语', '希腊文化概况', '英语'], '大二': ['希腊语语法', '中级希腊语', '希腊文学选读', '希腊社会'], '大三': ['高级希腊语', '翻译理论与实践', '希腊历史', '经贸希腊语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['雅典大学', '亚里士多德大学']}
    },
    {
        'code': '080802T',
        'name': '轨道交通信号与控制',
        'category': '08 工学',
        'category_icon': '🚄',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-22k',
        'overview': '轨道交通信号与控制专业培养掌握轨道交通信号技术的工程技术人才，从事轨道交通信号系统的设计和维护工作。',
        'what_you_learn': '信号与系统、自动控制原理、轨道交通信号、列车运行控制、车站信号、区间信号',
        'suitable_for': '对轨道交通和信号控制有兴趣的学生。',
        'career_outlook': '轨道交通企业、铁路部门、设计院等对轨道交通信号与控制人才有需求。',
        'xuefeng_comment': '轨道交通信号与控制是轨道交通的重要专业，随着轨道交通的发展，对这方面人才的需求在增长。建议对轨道交通有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、电路原理、模拟电子技术'], '大二': ['数字电子技术、信号与系统、自动控制原理、微机原理'], '大三': ['轨道交通信号、列车运行控制、车站信号、区间信号'], '大四': ['轨道交通企业实习、毕业设计']},
        'top_universities': {'domestic': ['西南交通大学、北京交通大学、同济大学、东南大学'], 'international': ['麻省理工学院、加州大学伯克利分校、伦敦帝国学院']}
    },
    {
        'code': '090503T',
        'name': '设施农业科学与工程',
        'category': '09 农学',
        'category_icon': '🌱',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-18k',
        'overview': '设施农业科学与工程专业培养掌握设施农业技术的专业人才，从事设施农业的设计、生产和管理工作。',
        'what_you_learn': '设施农业、植物学、植物生理学、农业气象、设施园艺、无土栽培',
        'suitable_for': '对农业和设施农业有兴趣的学生。',
        'career_outlook': '农业企业、农业部门、科研机构等对设施农业科学与工程人才有需求。',
        'xuefeng_comment': '设施农业科学与工程是现代农业的重要专业，随着农业现代化的发展，对这方面人才的需求在增长。建议对农业有兴趣的同学报考。',
        'yearly_courses': {'大一': ['植物学、生物化学、植物生理学、农业气象'], '大二': ['设施农业、设施园艺、无土栽培、土壤学'], '大三': ['植物保护、园艺产品贮藏加工、设施环境控制、农业工程'], '大四': ['农业企业实习、毕业设计']},
        'top_universities': {'domestic': ['中国农业大学、南京农业大学、西北农林科技大学、山东农业大学'], 'international': ['瓦赫宁根大学、加州大学戴维斯分校、康奈尔大学']}
    },
    {
        'code': '130207T',
        'name': '舞蹈教育',
        'category': '13 艺术学',
        'category_icon': '💃',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-18k',
        'overview': '舞蹈教育专业培养掌握舞蹈教育知识的专业人才，从事舞蹈教学和舞蹈教育研究工作。',
        'what_you_learn': '舞蹈基础训练、舞蹈史、舞蹈教育学、舞蹈教学法、舞蹈创作、舞蹈解剖学',
        'suitable_for': '对舞蹈和教育有兴趣的学生。',
        'career_outlook': '学校、舞蹈机构、文化部门等对舞蹈教育人才有需求。',
        'xuefeng_comment': '舞蹈教育是艺术教育的重要专业，随着艺术教育的发展，对舞蹈教育人才的需求在增长。建议对舞蹈和教育有兴趣的同学报考。',
        'yearly_courses': {'大一': ['舞蹈基础训练、音乐基础、舞蹈史、舞蹈解剖学'], '大二': ['舞蹈教育学、舞蹈教学法、民间舞、现代舞'], '大三': ['舞蹈创作、舞蹈教学实践、艺术概论、舞蹈评论'], '大四': ['学校实习、毕业作品']},
        'top_universities': {'domestic': ['北京舞蹈学院、中央民族大学、上海戏剧学院、南京艺术学院'], 'international': ['茱莉亚学院、英国皇家舞蹈学院']}
    }
]

def main():
    print('=' * 70)
    print('📊 最后5个专业 - 突破450！')
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

