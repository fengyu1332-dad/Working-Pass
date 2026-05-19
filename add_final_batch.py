
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
        'code': '020205T',
        'name': '税收学',
        'category': '02 经济学',
        'category_icon': '💰',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '税收学专业培养掌握税收知识的专业人才，从事税务工作、税收筹划和税收研究。',
        'what_you_learn': '税法、税收学、税收筹划、税收管理、税务会计、国际税收',
        'suitable_for': '对税收和财务有兴趣的学生。',
        'career_outlook': '税务部门、企业、会计师事务所等对税收学人才有需求。',
        'xuefeng_comment': '税收学是财政和税务的重要专业，就业稳定。建议对税收有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、政治经济学、微观经济学、宏观经济学'], '大二': ['税法、税收学、财政学、会计学'], '大三': ['税收筹划、税收管理、税务会计、国际税收'], '大四': ['税务机构实习、毕业论文']},
        'top_universities': {'domestic': ['中国人民大学、中央财经大学、上海财经大学、西南财经大学'], 'international': ['哈佛大学、宾夕法尼亚大学、伦敦政治经济学院']}
    },
    {
        'code': '030303T',
        'name': '人类学',
        'category': '03 法学',
        'category_icon': '👥',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥6k-18k',
        'overview': '人类学专业培养掌握人类学知识的专业人才，从事文化研究、社会调查和文化保护工作。',
        'what_you_learn': '文化人类学、社会人类学、体质人类学、田野调查、人类学理论',
        'suitable_for': '对人类学和文化有兴趣的学生。',
        'career_outlook': '科研机构、博物馆、文化部门等对人类学人才有需求。',
        'xuefeng_comment': '人类学是研究人类文化和社会的重要专业，就业方向灵活。建议对人类学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['人类学概论、社会学概论、文化人类学、体质人类学'], '大二': ['社会人类学、人类学理论、田野调查方法、民族学'], '大三': ['人类学研究方法、文化研究、应用人类学、人类学专题'], '大四': ['田野调查实习、毕业论文']},
        'top_universities': {'domestic': ['北京大学、中国人民大学、复旦大学、中山大学'], 'international': ['哈佛大学、耶鲁大学、加州大学伯克利分校']}
    },
    {
        'code': '050109T',
        'name': '秘书学',
        'category': '05 文学',
        'category_icon': '📝',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-18k',
        'overview': '秘书学专业培养掌握秘书工作的专业人才，从事行政管理、办公管理和秘书工作。',
        'what_you_learn': '秘书学、文书学、档案学、行政管理、办公自动化、商务礼仪',
        'suitable_for': '对秘书工作和行政管理有兴趣的学生。',
        'career_outlook': '企业、政府部门、事业单位等对秘书学人才有需求。',
        'xuefeng_comment': '秘书学是行政管理的重要专业，就业稳定。建议对秘书工作有兴趣的同学报考。',
        'yearly_courses': {'大一': ['秘书学概论、文书学、档案学、行政管理'], '大二': ['办公自动化、商务礼仪、应用文写作、沟通技巧'], '大三': ['秘书实务、会议组织、公共关系、行政管理案例'], '大四': ['企业实习、毕业论文']},
        'top_universities': {'domestic': ['中国人民大学、复旦大学、南京大学、中山大学'], 'international': []}
    },
    {
        'code': '070103T',
        'name': '数理基础科学',
        'category': '07 理学',
        'category_icon': '📐',
        'difficulty': '⭐⭐⭐⭐',
        'salary_range': '¥8k-25k',
        'overview': '数理基础科学专业培养掌握数学和物理知识的专业人才，从事科学研究和技术应用工作。',
        'what_you_learn': '数学分析、高等代数、力学、热学、电磁学、光学、原子物理',
        'suitable_for': '对数学和物理有兴趣的学生。',
        'career_outlook': '科研机构、学校、高新技术企业等对数理基础科学人才有需求。',
        'xuefeng_comment': '数理基础科学是基础理学专业，就业方向广，研究生深造优势大。建议对数学和物理有兴趣的同学报考。',
        'yearly_courses': {'大一': ['数学分析、高等代数、解析几何、普通物理学'], '大二': ['常微分方程、复变函数、理论力学、电动力学'], '大三': ['量子力学、热统、实变函数、泛函分析'], '大四': ['科研机构实习、毕业论文']},
        'top_universities': {'domestic': ['北京大学、清华大学、复旦大学、中国科学技术大学'], 'international': ['普林斯顿大学、哈佛大学、麻省理工学院']}
    },
    {
        'code': '070402T',
        'name': '应用气象学',
        'category': '07 理学',
        'category_icon': '🌤️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '应用气象学专业培养掌握气象知识的专业人才，从事天气预报、气象服务和气候研究工作。',
        'what_you_learn': '大气科学、天气学、气候学、应用气象学、气象观测、气象预报',
        'suitable_for': '对气象和天气有兴趣的学生。',
        'career_outlook': '气象部门、民航、农业部门等对应用气象学人才有需求。',
        'xuefeng_comment': '应用气象学是气象服务的重要专业，就业稳定。建议对气象有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、大气科学导论、大气物理学'], '大二': ['天气学、气候学、动力气象学、大气探测'], '大三': ['应用气象学、气象预报、气象服务、农业气象'], '大四': ['气象部门实习、毕业论文']},
        'top_universities': {'domestic': ['南京信息工程大学、北京大学、南京大学、中山大学'], 'international': ['加州大学洛杉矶分校、华盛顿大学、英国雷丁大学']}
    },
    {
        'code': '070601T',
        'name': '大气科学',
        'category': '07 理学',
        'category_icon': '🌪️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '大气科学专业培养掌握大气科学知识的专业人才，从事天气预报、气候研究和气象服务工作。',
        'what_you_learn': '大气物理学、大气化学、天气学、气候学、动力气象学、大气探测',
        'suitable_for': '对大气和天气有兴趣的学生。',
        'career_outlook': '气象部门、科研机构、高校等对大气科学人才有需求。',
        'xuefeng_comment': '大气科学是气象研究的重要专业，就业稳定。建议对大气科学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、大气科学导论、大气物理学'], '大二': ['大气化学、天气学、动力气象学、大气探测'], '大三': ['气候学、数值天气预报、大气遥感、中尺度气象学'], '大四': ['气象部门实习、毕业论文']},
        'top_universities': {'domestic': ['南京信息工程大学、北京大学、南京大学、中山大学'], 'international': ['加州大学洛杉矶分校、华盛顿大学、英国雷丁大学']}
    },
    {
        'code': '080102T',
        'name': '工程力学',
        'category': '08 工学',
        'category_icon': '⚙️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-22k',
        'overview': '工程力学专业培养掌握力学知识的工程技术人才，从事工程设计、分析和研究工作。',
        'what_you_learn': '理论力学、材料力学、弹性力学、流体力学、固体力学、计算力学',
        'suitable_for': '对力学和工程有兴趣的学生。',
        'career_outlook': '设计院、科研机构、制造企业等对工程力学人才有需求。',
        'xuefeng_comment': '工程力学是工程的基础专业，就业面广。建议对力学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、理论力学、工程制图'], '大二': ['材料力学、弹性力学、流体力学、机械设计基础'], '大三': ['固体力学、计算力学、结构力学、实验力学'], '大四': ['设计院实习、毕业设计']},
        'top_universities': {'domestic': ['清华大学、哈尔滨工业大学、上海交通大学、浙江大学'], 'international': ['麻省理工学院、加州大学伯克利分校、斯坦福大学']}
    },
    {
        'code': '080702T',
        'name': '电子科学与技术',
        'category': '08 工学',
        'category_icon': '⚡',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-25k',
        'overview': '电子科学与技术专业培养掌握电子技术的工程技术人才，从事电子器件和系统的研发工作。',
        'what_you_learn': '电路原理、模拟电子技术、数字电子技术、半导体物理、微电子学、电子器件',
        'suitable_for': '对电子和半导体有兴趣的学生。',
        'career_outlook': '电子企业、半导体企业、科研机构等对电子科学人才有需求。',
        'xuefeng_comment': '电子科学与技术是信息产业的基础专业，就业前景好。建议对电子有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、电路原理、模拟电子技术'], '大二': ['数字电子技术、半导体物理、微电子学、信号与系统'], '大三': ['电子器件、集成电路、电子材料、光电子技术'], '大四': ['电子企业实习、毕业设计']},
        'top_universities': {'domestic': ['清华大学、电子科技大学、西安电子科技大学、上海交通大学'], 'international': ['麻省理工学院、斯坦福大学、加州大学伯克利分校']}
    },
    {
        'code': '082601T',
        'name': '生物医学工程',
        'category': '08 工学',
        'category_icon': '🏥',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-25k',
        'overview': '生物医学工程专业培养掌握生物医学技术的工程技术人才，从事医疗器械研发和医疗应用工作。',
        'what_you_learn': '生物医学工程、医学成像、医学信号处理、医疗器械、生物材料、康复工程',
        'suitable_for': '对生物和医学工程有兴趣的学生。',
        'career_outlook': '医疗器械企业、医院、科研机构等对生物医学工程人才有需求。',
        'xuefeng_comment': '生物医学工程是医学和工程的交叉学科，发展前景好。建议对生物医学工程有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、程序设计、人体解剖生理学'], '大二': ['生物化学、电子技术、信号与系统、生物医学工程概论'], '大三': ['医学成像、医学信号处理、医疗器械、生物材料'], '大四': ['医疗企业实习、毕业设计']},
        'top_universities': {'domestic': ['清华大学、上海交通大学、浙江大学、东南大学'], 'international': ['麻省理工学院、斯坦福大学、约翰霍普金斯大学']}
    },
    {
        'code': '100801T',
        'name': '中药学',
        'category': '10 医学',
        'category_icon': '🌿',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-22k',
        'overview': '中药学专业培养掌握中药知识的专业人才，从事中药研发、生产和鉴定工作。',
        'what_you_learn': '中药学、方剂学、中药鉴定学、中药炮制学、中药药剂学、中药药理学',
        'suitable_for': '对中药和传统医学有兴趣的学生。',
        'career_outlook': '中药企业、医院、科研机构等对中药学人才有需求。',
        'xuefeng_comment': '中药学是中国传统医学的重要专业，随着文化自信的提高，对中药学人才的需求在增长。建议对中药有兴趣的同学报考。',
        'yearly_courses': {'大一': ['中医学基础、中药学、方剂学、中医诊断学'], '大二': ['中药鉴定学、中药炮制学、中药药剂学、中药药理学'], '大三': ['中药化学、中药资源学、中药分析、中药制剂分析'], '大四': ['中药企业实习、毕业论文']},
        'top_universities': {'domestic': ['北京中医药大学、上海中医药大学、广州中医药大学、南京中医药大学'], 'international': []}
    },
    {
        'code': '120104T',
        'name': '房地产开发与管理',
        'category': '12 管理学',
        'category_icon': '🏠',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-22k',
        'overview': '房地产开发与管理专业培养掌握房地产知识的专业人才，从事房地产开发、经营和管理工作。',
        'what_you_learn': '房地产经济学、房地产开发、房地产估价、房地产市场营销、物业管理',
        'suitable_for': '对房地产和管理有兴趣的学生。',
        'career_outlook': '房地产企业、中介机构、金融机构等对房地产人才有需求。',
        'xuefeng_comment': '房地产开发与管理是房地产行业的重要专业，就业前景好。建议对房地产有兴趣的同学报考。',
        'yearly_courses': {'大一': ['管理学原理、微观经济学、宏观经济学、房地产经济学'], '大二': ['房地产开发、房地产估价、房地产市场营销、建筑工程概论'], '大三': ['房地产金融、物业管理、房地产法规、房地产投资分析'], '大四': ['房地产企业实习、毕业论文']},
        'top_universities': {'domestic': ['中国人民大学、重庆大学、上海财经大学、浙江大学'], 'international': ['宾夕法尼亚大学、加州大学伯克利分校、伦敦帝国学院']}
    },
    {
        'code': '120501T',
        'name': '图书馆学',
        'category': '12 管理学',
        'category_icon': '📚',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-18k',
        'overview': '图书馆学专业培养掌握图书馆知识的专业人才，从事图书馆管理、信息服务和文献研究工作。',
        'what_you_learn': '图书馆学、信息组织、信息检索、图书馆管理、数字图书馆、文献学',
        'suitable_for': '对图书馆和信息服务有兴趣的学生。',
        'career_outlook': '图书馆、档案馆、信息机构等对图书馆学人才有需求。',
        'xuefeng_comment': '图书馆学是信息管理的重要专业，就业稳定。建议对图书馆有兴趣的同学报考。',
        'yearly_courses': {'大一': ['图书馆学概论、信息组织、信息检索、目录学'], '大二': ['图书馆管理、数字图书馆、文献学、信息资源建设'], '大三': ['图书馆服务、图书馆技术、图书馆建筑、信息咨询'], '大四': ['图书馆实习、毕业论文']},
        'top_universities': {'domestic': ['北京大学、武汉大学、南开大学、南京大学'], 'international': ['华盛顿大学、伊利诺伊大学香槟分校、加州大学伯克利分校']}
    },
    {
        'code': '130506T',
        'name': '公共艺术',
        'category': '13 艺术学',
        'category_icon': '🎨',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '公共艺术专业培养掌握公共艺术知识的专业人才，从事公共艺术设计和创作工作。',
        'what_you_learn': '公共艺术设计、雕塑、壁画、环境艺术、公共艺术史、公共艺术理论',
        'suitable_for': '对公共艺术和设计有兴趣的学生。',
        'career_outlook': '设计公司、市政部门、文化机构等对公共艺术人才有需求。',
        'xuefeng_comment': '公共艺术是城市建设和文化建设的重要专业，就业前景好。建议对公共艺术有兴趣的同学报考。',
        'yearly_courses': {'大一': ['设计素描、设计色彩、公共艺术概论、雕塑基础'], '大二': ['公共艺术设计、壁画、环境艺术、公共艺术史'], '大三': ['公共艺术创作、城市雕塑、公共艺术理论、公共艺术项目管理'], '大四': ['设计公司实习、毕业设计']},
        'top_universities': {'domestic': ['中央美术学院、中国美术学院、清华大学美术学院、南京艺术学院'], 'international': ['中央圣马丁艺术与设计学院、罗德岛设计学院、皇家艺术学院']}
    },
    {
        'code': '050305T',
        'name': '编辑出版学',
        'category': '05 文学',
        'category_icon': '📚',
        'difficulty': '⭐⭐',
        'salary_range': '¥6k-18k',
        'overview': '编辑出版学专业培养掌握编辑出版知识的专业人才，从事图书编辑、出版发行和数字出版工作。',
        'what_you_learn': '编辑学、出版学、出版发行、数字出版、出版营销、出版法规',
        'suitable_for': '对编辑和出版有兴趣的学生。',
        'career_outlook': '出版社、杂志社、媒体公司等对编辑出版人才有需求。',
        'xuefeng_comment': '编辑出版学是文化产业的重要专业，就业稳定。建议对编辑出版有兴趣的同学报考。',
        'yearly_courses': {'大一': ['编辑学概论、出版学概论、中国文化概论、现代汉语'], '大二': ['编辑实务、出版发行、数字出版、出版营销'], '大三': ['出版法规、出版设计、出版史、出版经营管理'], '大四': ['出版社实习、毕业论文']},
        'top_universities': {'domestic': ['北京大学、复旦大学、南京大学、武汉大学'], 'international': ['纽约大学、加州大学洛杉矶分校、伦敦大学学院']}
    },
    {
        'code': '080909T',
        'name': '电子与计算机工程',
        'category': '08 工学',
        'category_icon': '💻',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥9k-28k',
        'overview': '电子与计算机工程专业培养掌握电子和计算机知识的工程技术人才，从事嵌入式系统和软硬件开发工作。',
        'what_you_learn': '电路原理、模拟电子技术、数字电子技术、程序设计、计算机组成原理、嵌入式系统',
        'suitable_for': '对电子和计算机有兴趣的学生。',
        'career_outlook': '电子企业、IT企业、科研机构等对电子与计算机工程人才有需求。',
        'xuefeng_comment': '电子与计算机工程是电子和计算机的交叉专业，就业前景好。建议对电子和计算机有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、程序设计、电路原理'], '大二': ['模拟电子技术、数字电子技术、数据结构、计算机组成原理'], '大三': ['嵌入式系统、计算机网络、操作系统、计算机应用'], '大四': ['IT企业实习、毕业设计']},
        'top_universities': {'domestic': ['清华大学、上海交通大学、浙江大学、电子科技大学'], 'international': ['麻省理工学院、斯坦福大学、加州大学伯克利分校']}
    },
    {
        'code': '081304T',
        'name': '制药工程',
        'category': '08 工学',
        'category_icon': '💊',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-22k',
        'overview': '制药工程专业培养掌握制药技术的工程技术人才，从事药品生产和工艺开发工作。',
        'what_you_learn': '制药工程、药物化学、药剂学、药物分析、化工原理、制药工艺',
        'suitable_for': '对制药和化工有兴趣的学生。',
        'career_outlook': '制药企业、化工企业、科研机构等对制药工程人才有需求。',
        'xuefeng_comment': '制药工程是制药行业的重要专业，就业前景好。建议对制药有兴趣的同学报考。',
        'yearly_courses': {'大一': ['高等数学、大学物理、无机化学、有机化学'], '大二': ['物理化学、生物化学、化工原理、药物化学'], '大三': ['制药工程、药剂学、药物分析、制药工艺'], '大四': ['制药企业实习、毕业设计']},
        'top_universities': {'domestic': ['华东理工大学、天津大学、中国药科大学、沈阳药科大学'], 'international': ['麻省理工学院、斯坦福大学、加州大学伯克利分校']}
    }
]

def main():
    print('=' * 70)
    print('📊 最后一批专业导入 - 达成450+目标！')
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

