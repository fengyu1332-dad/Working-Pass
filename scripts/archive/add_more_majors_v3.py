
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
        'code': '050228',
        'name': '乌尔都语',
        'category': '05 文学',
        'category_icon': '🇵🇰',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-20k',
        'overview': '乌尔都语专业培养掌握乌尔都语语言文学的复合型人才，从事乌尔都语翻译、教学和研究工作。',
        'what_you_learn': '乌尔都语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对巴基斯坦及南亚语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对乌尔都语人才有需求。',
        'xuefeng_comment': '乌尔都语是巴基斯坦的官方语言，在印度也有使用。随着中国与巴基斯坦关系的深入发展，对乌尔都语人才的需求在不断增长。建议对南亚文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['乌尔都语语音', '基础乌尔都语', '巴基斯坦文化概况', '英语'], '大二': ['乌尔都语语法', '中级乌尔都语', '乌尔都文学选读', '巴基斯坦社会'], '大三': ['高级乌尔都语', '翻译理论与实践', '巴基斯坦历史', '经贸乌尔都语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学', '北京大学'], 'international': ['真纳大学', '旁遮普大学']}
    },
    {
        'code': '050229',
        'name': '希伯来语',
        'category': '05 文学',
        'category_icon': '🇮🇱',
        'difficulty': '⭐⭐⭐⭐',
        'salary_range': '¥9k-22k',
        'overview': '希伯来语专业培养掌握希伯来语语言文学的复合型人才，从事希伯来语翻译、教学和研究工作。',
        'what_you_learn': '希伯来语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对以色列及犹太语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、宗教研究等领域对希伯来语人才有需求。',
        'xuefeng_comment': '希伯来语是以色列的官方语言，有着悠久的历史和文化。随着中以合作的深化，对希伯来语人才的需求在增长。建议对犹太文化和中东研究有兴趣的同学报考。',
        'yearly_courses': {'大一': ['希伯来语语音', '基础希伯来语', '以色列文化概况', '英语'], '大二': ['希伯来语语法', '中级希伯来语', '希伯来文学选读', '犹太文化'], '大三': ['高级希伯来语', '翻译理论与实践', '以色列历史', '中东研究'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['希伯来大学', '特拉维夫大学']}
    },
    {
        'code': '050231',
        'name': '豪萨语',
        'category': '05 文学',
        'category_icon': '🇳🇬',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '豪萨语专业培养掌握豪萨语语言文学的复合型人才，从事豪萨语翻译、教学和研究工作。',
        'what_you_learn': '豪萨语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对西非语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对豪萨语人才有需求。',
        'xuefeng_comment': '豪萨语是西非重要的通用语言，在尼日利亚等国广泛使用。随着"一带一路"向非洲延伸，对豪萨语人才的需求在增长。建议对非洲文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['豪萨语语音', '基础豪萨语', '西非文化概况', '英语'], '大二': ['豪萨语语法', '中级豪萨语', '豪萨文学选读', '西非社会'], '大三': ['高级豪萨语', '翻译理论与实践', '西非历史', '经贸豪萨语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['伊巴丹大学', '卡诺大学']}
    },
    {
        'code': '050237',
        'name': '捷克语',
        'category': '05 文学',
        'category_icon': '🇨🇿',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-20k',
        'overview': '捷克语专业培养掌握捷克语语言文学的复合型人才，从事捷克语翻译、教学和研究工作。',
        'what_you_learn': '捷克语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对捷克及中东欧语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对捷克语人才有需求。',
        'xuefeng_comment': '捷克语是捷克的官方语言。随着中国与中东欧国家合作的深化，对捷克语人才的需求在增长。建议对中东欧文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['捷克语语音', '基础捷克语', '捷克文化概况', '英语'], '大二': ['捷克语语法', '中级捷克语', '捷克文学选读', '捷克社会'], '大三': ['高级捷克语', '翻译理论与实践', '捷克历史', '经贸捷克语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['查理大学']}
    },
    {
        'code': '050239',
        'name': '斯洛伐克语',
        'category': '05 文学',
        'category_icon': '🇸🇰',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '斯洛伐克语专业培养掌握斯洛伐克语语言文学的复合型人才，从事斯洛伐克语翻译、教学和研究工作。',
        'what_you_learn': '斯洛伐克语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对斯洛伐克及中东欧语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对斯洛伐克语人才有需求。',
        'xuefeng_comment': '斯洛伐克语是斯洛伐克的官方语言。随着中国与中东欧国家合作的深化，对斯洛伐克语人才的需求在增长。建议对中东欧文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['斯洛伐克语语音', '基础斯洛伐克语', '斯洛伐克文化概况', '英语'], '大二': ['斯洛伐克语语法', '中级斯洛伐克语', '斯洛伐克文学选读', '斯洛伐克社会'], '大三': ['高级斯洛伐克语', '翻译理论与实践', '斯洛伐克历史', '经贸斯洛伐克语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['布拉迪斯拉发大学']}
    },
    {
        'code': '050245',
        'name': '匈牙利语',
        'category': '05 文学',
        'category_icon': '🇭🇺',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-20k',
        'overview': '匈牙利语专业培养掌握匈牙利语语言文学的复合型人才，从事匈牙利语翻译、教学和研究工作。',
        'what_you_learn': '匈牙利语语音、语法、口语、阅读、写作、文学、文化、跨文化交际',
        'suitable_for': '对匈牙利及中东欧语言文化有浓厚兴趣的学生。',
        'career_outlook': '外交、经贸、教育、文化、旅游等领域对匈牙利语人才有需求。',
        'xuefeng_comment': '匈牙利语是匈牙利的官方语言，属于乌拉尔语系，很有特色。随着中国与中东欧国家合作的深化，对匈牙利语人才的需求在增长。建议对中东欧文化有兴趣的同学报考。',
        'yearly_courses': {'大一': ['匈牙利语语音', '基础匈牙利语', '匈牙利文化概况', '英语'], '大二': ['匈牙利语语法', '中级匈牙利语', '匈牙利文学选读', '匈牙利社会'], '大三': ['高级匈牙利语', '翻译理论与实践', '匈牙利历史', '经贸匈牙利语'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['北京外国语大学', '上海外国语大学'], 'international': ['罗兰大学']}
    },
    {
        'code': '070903T',
        'name': '地球信息科学与技术',
        'category': '07 理学',
        'category_icon': '🌍',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥10k-25k',
        'overview': '地球信息科学与技术专业培养掌握地球信息科学的专业人才，从事地理信息系统、遥感、全球定位等工作。',
        'what_you_learn': '地理信息系统、遥感技术、全球定位系统、数字图像处理、地图学、计算机编程',
        'suitable_for': '对地理信息和计算机技术有兴趣的学生。',
        'career_outlook': '测绘部门、环保部门、IT企业等对地球信息科学人才有需求。',
        'xuefeng_comment': '地球信息科学与技术是理学与计算机的交叉学科，随着数字经济的发展，对这方面人才的需求在增长。建议对地理和计算机都有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学', '大学物理', '计算机基础', '地图学'], '大二': ['地理信息系统', '遥感技术', '数字图像处理', 'GPS原理'], '大三': ['空间分析', 'GIS开发', '遥感影像解译', '数据库'], '大四': ['企业实习', '毕业设计']},
        'top_universities': {'domestic': ['武汉大学', '中国地质大学', '南京大学', '中山大学'], 'international': ['加州大学伯克利分校', '斯坦福大学']}
    },
    {
        'code': '071004T',
        'name': '生物技术',
        'category': '07 理学',
        'category_icon': '🧬',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥9k-28k',
        'overview': '生物技术专业培养掌握生物技术的专业人才，从事生物技术研发和应用工作。',
        'what_you_learn': '分子生物学、细胞生物学、生物化学、微生物学、基因工程、发酵工程',
        'suitable_for': '对生物科学和技术应用有兴趣的学生。',
        'career_outlook': '生物制药公司、农业科技公司、科研机构等对生物技术人才有需求。',
        'xuefeng_comment': '生物技术是21世纪的前沿学科，随着生物经济的发展，对这方面人才的需求在快速增长。建议对生物有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学', '无机化学', '有机化学', '普通生物学'], '大二': ['生物化学', '微生物学', '细胞生物学', '分子生物学'], '大三': ['基因工程', '发酵工程', '细胞工程', '生物信息学'], '大四': ['企业实习', '毕业设计']},
        'top_universities': {'domestic': ['北京大学', '清华大学', '复旦大学', '上海交通大学'], 'international': ['麻省理工学院', '斯坦福大学', '哈佛大学']}
    },
    {
        'code': '120209T',
        'name': '物业管理',
        'category': '12 管理学',
        'category_icon': '🏢',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-15k',
        'overview': '物业管理专业培养物业管理专业人才，从事物业的管理和服务工作。',
        'what_you_learn': '物业管理、房地产经济、社区管理、物业法规、客户服务、财务管理',
        'suitable_for': '对物业管理和服务行业有兴趣的学生。',
        'career_outlook': '物业公司、房地产公司等对物业管理人才有需求。',
        'xuefeng_comment': '物业管理是房地产行业的重要组成部分，随着房地产市场的发展，对物业管理人才的需求在增长。建议对管理和服务有兴趣的同学报考。',
        'yearly_courses': {'大一': ['管理学原理', '物业管理概论', '大学语文', '高等数学'], '大二': ['房地产经济学', '物业法规', '社区管理', '客户服务'], '大三': ['财务管理', '人力资源管理', '物业设备管理', '市场营销'], '大四': ['物业公司实习', '毕业论文']},
        'top_universities': {'domestic': ['北京林业大学', '中山大学', '武汉大学'], 'international': ['宾夕法尼亚州立大学']}
    },
    {
        'code': '090203T',
        'name': '茶学',
        'category': '09 农学',
        'category_icon': '🍵',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-16k',
        'overview': '茶学专业培养掌握茶叶生产和加工技术的专业人才，从事茶叶生产、加工、销售和研究工作。',
        'what_you_learn': '茶树栽培、茶叶加工、茶叶审评、茶文化、茶叶贸易、食品化学',
        'suitable_for': '对茶产业和茶文化有兴趣的学生。',
        'career_outlook': '茶叶公司、茶厂、农业部门等对茶学人才有需求。',
        'xuefeng_comment': '茶学是中国传统农学的重要专业，随着中国茶文化的复兴和茶产业的发展，对茶学人才的需求在增长。建议对茶有兴趣的同学报考。',
        'yearly_courses': {'大一': ['植物学', '生物化学', '植物生理学', '土壤学'], '大二': ['茶树栽培学', '茶叶加工学', '茶叶审评', '茶文化'], '大三': ['茶叶贸易', '食品化学', '茶树育种', '茶叶机械'], '大四': ['茶厂实习', '毕业设计']},
        'top_universities': {'domestic': ['安徽农业大学', '浙江大学', '湖南农业大学', '西南大学'], 'international': []}
    },
    {
        'code': '050311T',
        'name': '网络与新媒体',
        'category': '05 文学',
        'category_icon': '📱',
        'difficulty': '⭐⭐',
        'salary_range': '¥8k-25k',
        'overview': '网络与新媒体专业培养新媒体创作和运营人才，从事新媒体内容创作、运营和管理工作。',
        'what_you_learn': '新媒体概论、传播学、网络传播、新媒体运营、数字媒体技术、内容创作',
        'suitable_for': '对新媒体和内容创作有兴趣的学生。',
        'career_outlook': '媒体公司、互联网公司、广告公司等对新媒体人才有需求。',
        'xuefeng_comment': '网络与新媒体是新闻传播学的新兴专业，随着移动互联网和自媒体的发展，对这方面人才的需求在快速增长。建议对新媒体有兴趣的同学报考。',
        'yearly_courses': {'大一': ['新媒体概论', '传播学', '计算机基础', '写作'], '大二': ['网络传播', '新媒体运营', '数字媒体技术', '摄影摄像'], '大三': ['内容创作', '短视频制作', '数据分析', '广告学'], '大四': ['新媒体公司实习', '毕业设计']},
        'top_universities': {'domestic': ['中国传媒大学', '中国人民大学', '复旦大学', '浙江大学'], 'international': ['哥伦比亚大学', '伦敦政治经济学院']}
    },
    {
        'code': '080606T',
        'name': '光源与照明',
        'category': '08 工学',
        'category_icon': '💡',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥9k-22k',
        'overview': '光源与照明专业培养掌握光源和照明技术的专业人才，从事照明设计和产品研发工作。',
        'what_you_learn': '光源原理、照明设计、光学设计、电子技术、LED技术、智能照明',
        'suitable_for': '对光学和照明技术有兴趣的学生。',
        'career_outlook': '照明公司、电子公司、设计院等对光源与照明人才有需求。',
        'xuefeng_comment': '光源与照明是工学的重要专业，随着LED和智能照明的发展，对这方面人才的需求在增长。建议对光学和电子有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学', '大学物理', '电路原理', '模拟电子技术'], '大二': ['光源原理', '光学设计', '数字电子技术', '半导体物理'], '大三': ['照明设计', 'LED技术', '智能照明', '照明工程'], '大四': ['企业实习', '毕业设计']},
        'top_universities': {'domestic': ['复旦大学', '浙江大学', '东南大学', '华中科技大学'], 'international': ['加州大学伯克利分校', '麻省理工学院']}
    }
]

def main():
    print('=' * 70)
    print('📊 补充更多专业数据 (第三批)...')
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
