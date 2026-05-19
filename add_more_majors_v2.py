
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
    url = f"{SUPABASE_URL}/rest/v1/majors"
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
        "code": "050241",
        "name": "丹麦语",
        "category": "05 文学",
        "category_icon": "🇩🇰",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "丹麦语专业培养掌握丹麦语语言文学的专门人才，从事丹麦语翻译、教学和研究工作。",
        "what_you_learn": "丹麦语语音、语法、口语、阅读、写作、文学、文化、跨文化交际",
        "suitable_for": "对丹麦及北欧语言文化有兴趣的学生。",
        "career_outlook": "外事、经贸、教育、文化、旅游等领域对丹麦语人才有需求。",
        "xuefeng_comment": "丹麦设计闻名世界，丹麦语人才在相关领域有独特优势。建议对丹麦文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["丹麦语语音、基础丹麦语", "丹麦文化概况", "英语"], "大二": ["丹麦语语法、中级丹麦语", "丹麦文学选读", "丹麦社会"], "大三": ["高级丹麦语、翻译理论与实践", "丹麦史", "经贸丹麦语"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学"], "international": ["University of Copenhagen", "Aarhus University"]}
    },
    {
        "code": "050242",
        "name": "芬兰语",
        "category": "05 文学",
        "category_icon": "🇫🇮",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "芬兰语专业培养掌握芬兰语语言文学的专门人才，从事芬兰语翻译、教学和研究工作。",
        "what_you_learn": "芬兰语语音、语法、口语、阅读、写作、文学、文化、跨文化交际",
        "suitable_for": "对芬兰语言文化有兴趣的学生。",
        "career_outlook": "外事、经贸、教育、文化、旅游等领域对芬兰语人才有需求。",
        "xuefeng_comment": "芬兰教育世界领先，芬兰语人才在教育交流领域很重要。建议对芬兰文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["芬兰语语音、基础芬兰语", "芬兰文化概况", "英语"], "大二": ["芬兰语语法、中级芬兰语", "芬兰文学选读", "芬兰社会"], "大三": ["高级芬兰语、翻译理论与实践", "芬兰史", "经贸芬兰语"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学"], "international": ["University of Helsinki", "Aalto University"]}
    },
    {
        "code": "050243",
        "name": "挪威语",
        "category": "05 文学",
        "category_icon": "🇳🇴",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "挪威语专业培养掌握挪威语语言文学的专门人才，从事挪威语翻译、教学和研究工作。",
        "what_you_learn": "挪威语语音、语法、口语、阅读、写作、文学、文化、跨文化交际",
        "suitable_for": "对挪威及北欧语言文化有兴趣的学生。",
        "career_outlook": "外事、经贸、教育、文化、旅游等领域对挪威语人才有需求。",
        "xuefeng_comment": "挪威在海洋工程等领域领先，挪威语人才有独特就业机会。建议对挪威文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["挪威语语音、基础挪威语", "挪威文化概况", "英语"], "大二": ["挪威语语法、中级挪威语", "挪威文学选读", "挪威社会"], "大三": ["高级挪威语、翻译理论与实践", "挪威史", "经贸挪威语"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学"], "international": ["University of Oslo", "NTNU"]}
    },
    {
        "code": "050244",
        "name": "希腊语",
        "category": "05 文学",
        "category_icon": "🇬🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "希腊语专业培养掌握希腊语语言文学的专门人才，从事希腊语翻译、教学和研究工作。",
        "what_you_learn": "希腊语语音、语法、口语、阅读、写作、文学、文化、跨文化交际",
        "suitable_for": "对希腊语言文化有兴趣的学生。",
        "career_outlook": "外事、教育、文化、科研、旅游等领域对希腊语人才有需求。",
        "xuefeng_comment": "希腊是西方文明发源地，学习希腊语对研究西方文化很有帮助。建议对希腊文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["希腊语语音、基础希腊语", "希腊文化概况", "英语"], "大二": ["希腊语语法、中级希腊语", "希腊文学选读", "希腊社会"], "大三": ["高级希腊语、翻译理论与实践", "希腊史", "经贸希腊语"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学"], "international": ["University of Athens", "Aristotle University"]}
    },
    {
        "code": "030605TK",
        "name": "警犬技术",
        "category": "03 法学",
        "category_icon": "🐕",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "警犬技术专业培养掌握警犬训练和使用技能的专门人才，从事警犬训练和使用工作。",
        "what_you_learn": "警犬学、警犬训练、警犬使用、刑事侦查学、治安管理学",
        "suitable_for": "热爱动物、有志于公安事业的学生。",
        "career_outlook": "公安部门对警犬技术人才有稳定需求。",
        "xuefeng_comment": "警犬技术专业特色鲜明，在刑事侦查、治安等领域作用重要。建议热爱动物、有志于公安事业的同学报考。",
        "yearly_courses": {"大一": ["法学基础", "公安学基础", "警犬学概论", "动物学基础"], "大二": ["警犬训练学、警犬使用学", "刑事侦查学", "治安管理学"], "大三": ["警犬实战训练、犯罪心理学", "刑事技术", "禁毒学"], "大四": ["公安部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国刑事警察学院", "中国人民警察大学"], "international": []}
    },
    {
        "code": "030607TK",
        "name": "边防指挥",
        "category": "03 法学",
        "category_icon": "🎖️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "边防指挥专业培养从事边防指挥工作的专门人才，负责边境防卫和管理指挥工作。",
        "what_you_learn": "边防指挥、边防管理、军事法学、战术学、边境管理学",
        "suitable_for": "有志于公安边防指挥事业的学生。",
        "career_outlook": "公安边防部门对边防指挥人才有稳定需求。",
        "xuefeng_comment": "边防指挥专业培养指挥人才，责任重大，使命光荣。建议有志于公安边防指挥事业的同学报考。",
        "yearly_courses": {"大一": ["法学基础", "边防管理概论", "军事理论", "管理学基础"], "大二": ["边防指挥学、战术学", "边防法学、军事法学"], "大三": ["边防情报、边防战术", "边境涉外工作、军事训练"], "大四": ["边防部队实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民警察大学", "中国人民武装警察部队学院"], "international": []}
    },
    {
        "code": "030608TK",
        "name": "消防指挥",
        "category": "03 法学",
        "category_icon": "🚒",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "消防指挥专业培养从事消防指挥工作的专门人才，负责火灾扑救和应急救援指挥工作。",
        "what_you_learn": "消防指挥、灭火战术、消防技术装备、消防工程、应急救援学",
        "suitable_for": "有志于消防事业的学生。",
        "career_outlook": "消防救援部门对消防指挥人才有稳定需求。",
        "xuefeng_comment": "消防指挥专业培养消防指挥员，职业光荣，责任重大。建议有志于消防事业的同学报考。",
        "yearly_courses": {"大一": ["法学基础", "消防学概论", "军事理论", "工程力学"], "大二": ["消防指挥学、灭火战术学", "消防技术装备、消防工程学"], "大三": ["应急救援学、火灾调查", "抢险救援战术、消防管理"], "大四": ["消防部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民警察大学", "中国消防救援学院"], "international": []}
    },
    {
        "code": "080206",
        "name": "过程装备与控制工程",
        "category": "08 工学",
        "category_icon": "⚙️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "过程装备与控制工程专业培养装备设计制造和控制的工程人才，从事化工、石油等行业的装备设计和控制工作。",
        "what_you_learn": "过程装备设计、控制工程、机械设计、工程力学、化工原理",
        "suitable_for": "对机械和化工装备有兴趣的学生。",
        "career_outlook": "化工、石油、能源、机械等行业对过程装备与控制工程人才有需求。",
        "xuefeng_comment": "过控专业是传统优势专业，就业稳定，适用领域广。建议对机械和化工装备有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学、大学物理", "工程制图、工程力学"], "大二": ["机械设计基础、化工原理", "电工电子学、工程材料"], "大三": ["过程装备设计、控制工程", "过程流体机械、压力容器设计"], "大四": ["企业实习", "毕业设计"]},
        "top_universities": {"domestic": ["浙江大学", "西安交通大学", "华东理工大学", "大连理工大学"], "international": ["MIT", "Stanford", "UC Berkeley"]}
    },
    {
        "code": "080601",
        "name": "电气工程及其自动化",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-30k",
        "overview": "电气工程及其自动化专业培养电气系统设计运行的工程人才，从事电力系统、电机电器等领域的工作。",
        "what_you_learn": "电路、电机学、电力系统、自动控制原理、电力电子技术",
        "suitable_for": "对电气技术有兴趣的学生。",
        "career_outlook": "电力、电气、制造等行业对电气工程及其自动化人才有需求。",
        "xuefeng_comment": "电气专业是工科王牌专业，就业面广，待遇好。建议对电气技术有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学、大学物理", "工程制图、电路原理"], "大二": ["模拟电子技术、数字电子技术", "电机学、自动控制原理"], "大三": ["电力系统分析、电力电子技术", "电气控制技术、电力拖动"], "大四": ["企业实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学", "西安交通大学", "华中科技大学", "浙江大学"], "international": ["MIT", "Stanford", "UC Berkeley"]}
    },
    {
        "code": "081201",
        "name": "测绘工程",
        "category": "08 工学",
        "category_icon": "🗺️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "测绘工程专业培养测绘数据采集处理的工程技术人才，从事测绘、国土、建筑等领域的工作。",
        "what_you_learn": "测量学、大地测量、工程测量、遥感原理与应用、地理信息系统",
        "suitable_for": "对地理信息技术有兴趣的学生。",
        "career_outlook": "测绘、国土、建筑、交通等行业对测绘工程人才有需求。",
        "xuefeng_comment": "测绘工程专业应用领域广，现代测绘技术发展快。建议对地理信息技术有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学、大学物理", "测量学基础、工程制图"], "大二": ["大地测量学、误差理论", "摄影测量、遥感原理"], "大三": ["工程测量学、地理信息系统", "GPS原理与应用、数字测图"], "大四": ["企业实习", "毕业设计"]},
        "top_universities": {"domestic": ["武汉大学", "解放军信息工程大学", "中国矿业大学", "同济大学"], "international": ["MIT", "Stanford", "Delft University"]}
    },
    {
        "code": "101002",
        "name": "医学实验技术",
        "category": "10 医学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "医学实验技术专业培养医学实验技术专门人才，从事医学实验和检验工作。",
        "what_you_learn": "基础医学、医学实验技术、医学检验、分子生物学、生物化学",
        "suitable_for": "对医学实验技术有兴趣的学生。",
        "career_outlook": "医院、科研院所、生物公司等对医学实验技术人才有需求。",
        "xuefeng_comment": "医学实验技术专业实用性强，是医学研究的重要支撑。建议对医学实验技术有兴趣的同学报考。",
        "yearly_courses": {"大一": ["人体解剖学、组织胚胎学", "生理学、生物化学"], "大二": ["医学微生物学、免疫学", "病理学、药理学"], "大三": ["医学检验技术、分子生物学", "医学实验技术、细胞生物学"], "大四": ["医院实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学医学部", "北京协和医学院", "复旦大学上海医学院", "上海交通大学医学院"], "international": ["Johns Hopkins", "Harvard Medical"]}
    },
    {
        "code": "120104",
        "name": "房地产开发与管理",
        "category": "12 管理学",
        "category_icon": "🏢",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "房地产开发与管理专业培养房地产行业管理人才，从事房地产开发、经营和管理工作。",
        "what_you_learn": "房地产开发、房地产经营、工程管理、工程估价、房地产金融",
        "suitable_for": "对房地产行业有兴趣的学生。",
        "career_outlook": "房地产企业、建筑企业、中介机构等对房地产开发与管理人才有需求。",
        "xuefeng_comment": "房地产专业适应市场需求，就业机会多。建议对房地产行业有兴趣的同学报考。",
        "yearly_courses": {"大一": ["管理学原理、经济学原理", "房地产经济学、工程制图"], "大二": ["房地产开发、房地产经营", "工程管理、工程估价"], "大三": ["房地产金融、房地产法", "物业管理、市场营销"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["重庆大学", "同济大学", "东南大学", "清华大学"], "international": ["Wharton", "Harvard Business"]}
    },
    {
        "code": "120214",
        "name": "文化产业管理",
        "category": "12 管理学",
        "category_icon": "🎭",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "文化产业管理专业培养文化产业经营管理人才，从事文化产业运营和管理工作。",
        "what_you_learn": "文化产业管理、文化经济学、文化市场营销、文化创意产业、传媒学",
        "suitable_for": "对文化产业有兴趣、有创意的学生。",
        "career_outlook": "文化企业、媒体、文化场馆等对文化产业管理人才有需求。",
        "xuefeng_comment": "文化产业蓬勃发展，文管专业前景好。建议对文化产业有兴趣、有创意的同学报考。",
        "yearly_courses": {"大一": ["管理学原理、文化产业概论", "文化经济学、艺术基础"], "大二": ["文化产业政策、文化项目策划", "文化市场营销、文化创意产业"], "大三": ["传媒经营管理、文化经纪", "数字文化产业、文化遗产保护"], "大四": ["文化企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国传媒大学", "北京大学", "上海交通大学", "南京大学"], "international": ["NYU Tisch", "USC Annenberg"]}
    },
    {
        "code": "090106",
        "name": "种子科学与工程",
        "category": "09 农学",
        "category_icon": "🌾",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "种子科学与工程专业培养种子研发生产技术人才，从事种子研发、生产和推广工作。",
        "what_you_learn": "种子学、作物育种学、种子生产技术、种子检验、种子贮藏加工",
        "suitable_for": "对种业有兴趣的学生。",
        "career_outlook": "种子企业、农业科研、农技推广等对种子科学与工程人才有需求。",
        "xuefeng_comment": "种业是农业的芯片，种子专业非常重要。建议对种业有兴趣的同学报考。",
        "yearly_courses": {"大一": ["植物学、生物化学", "植物生理学、遗传学"], "大二": ["作物育种学、种子学", "植物病理学、农业昆虫学"], "大三": ["种子生产技术、种子检验", "种子贮藏加工、种子经营"], "大四": ["种子企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "华中农业大学", "西北农林科技大学"], "international": ["Cornell", "UC Davis"]}
    },
    {
        "code": "090502",
        "name": "野生动物与自然保护区管理",
        "category": "09 农学",
        "category_icon": "🦌",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "野保专业培养野生动物保护和自然保护区管理人才，从事野生动物保护和保护区管理工作。",
        "what_you_learn": "野生动物学、保护生物学、自然保护区管理、动物生态学、保护遗传学",
        "suitable_for": "热爱自然和野生动物的学生。",
        "career_outlook": "自然保护区、林业部门、动物园等对野生动物与自然保护区管理人才有需求。",
        "xuefeng_comment": "生态保护日益重要，野保专业意义重大。建议热爱自然和野生动物的同学报考。",
        "yearly_courses": {"大一": ["动物学、植物学", "生态学、保护生物学"], "大二": ["野生动物学、动物生理学", "自然保护区管理、保护遗传学"], "大三": ["野生动物管理学、保护法学", "野生动物繁育、生态监测"], "大四": ["自然保护区实习", "毕业论文"]},
        "top_universities": {"domestic": ["东北林业大学", "北京林业大学", "西南林业大学", "东北师范大学"], "international": ["WWF Conservation Programs", "Durrell Wildlife"]}
    },
    {
        "code": "020102",
        "name": "经济统计学",
        "category": "02 经济学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-30k",
        "overview": "经济统计学专业培养经济统计分析人才，从事经济统计、数据分析和经济研究工作。",
        "what_you_learn": "统计学、经济学、计量经济学、抽样调查、数据分析、统计软件",
        "suitable_for": "对数据和经济分析有兴趣的学生。",
        "career_outlook": "政府统计部门、金融机构、企业市场研究等对经济统计学人才有需求。",
        "xuefeng_comment": "大数据时代，统计学专业就业好，发展前景广阔。建议对数据和经济分析有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学、线性代数", "微观经济学、宏观经济学"], "大二": ["统计学、概率论与数理统计", "计量经济学、抽样调查"], "大三": ["时间序列分析、多元统计分析", "统计软件、数据分析"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "厦门大学", "中央财经大学", "上海财经大学"], "international": ["Harvard", "MIT", "Stanford"]}
    },
    {
        "code": "050217",
        "name": "蒙古语",
        "category": "05 文学",
        "category_icon": "🇲🇳",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "蒙古语专业培养掌握蒙古语语言文学的专门人才，从事蒙古语翻译、教学和研究工作。",
        "what_you_learn": "蒙古语语音、语法、口语、阅读、写作、文学、文化、蒙汉互译",
        "suitable_for": "对蒙古语言文化有浓厚兴趣的学生。",
        "career_outlook": "教育部门、外交外事机构、经贸企业、文化传播机构等对蒙古语人才有需求。",
        "xuefeng_comment": "蒙古语专业是非常有特色的民族语言专业。虽然学习人数不多，但就业前景非常稳定。随着中蒙两国在经济、文化、教育等领域的交流日益频繁，对蒙古语人才的需求持续增长。建议同学们在校期间除了学好专业知识外，还可以辅修一些经济、法律、新闻等相关知识，这样就业面会更宽。",
        "yearly_courses": {"大一": ["蒙古语语音、基础蒙古语", "蒙古文化概况、蒙汉翻译"], "大二": ["蒙古语语法、中级蒙古语", "蒙古文学史、蒙古民俗学"], "大三": ["高级蒙古语、蒙汉互译", "蒙古历史、中蒙关系"], "大四": ["企事业单位实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中央民族大学", "内蒙古大学", "内蒙古师范大学"], "international": ["National University of Mongolia"]}
    },
    {
        "code": "050218",
        "name": "藏语",
        "category": "05 文学",
        "category_icon": "🏔️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "藏语专业培养掌握藏语语言文学的专门人才，从事藏语教学、翻译、研究和管理工作。",
        "what_you_learn": "藏语语音、藏语语法、藏语口语、藏语阅读、藏语写作、藏文文学史、藏族文化概论、翻译理论与实践",
        "suitable_for": "对藏族语言文化有浓厚兴趣的学生。",
        "career_outlook": "主要在教育部门、文化机构、新闻出版单位、民族事务部门从事教学、翻译、研究、编辑、管理等工作。",
        "xuefeng_comment": "藏语专业是一个非常有价值的民族语言专业。随着国家对民族地区发展的重视和对民族文化保护的加强，对藏语人才的需求越来越大。这个专业不仅能让你掌握一门独特的语言，还能让你深入了解藏族灿烂的文化。建议同学们在校期间认真学习专业知识，多参加社会实践。",
        "yearly_courses": {"大一": ["藏语语音、基础藏语", "藏文文法、藏文化概论"], "大二": ["藏语语法、中级藏语", "藏文文学史、翻译理论"], "大三": ["高级藏语、藏汉互译", "藏传佛教概论、藏族历史"], "大四": ["相关单位实习", "毕业论文"]},
        "top_universities": {"domestic": ["中央民族大学", "西藏大学", "青海民族大学", "西南民族大学"], "international": ["Tibet University"]}
    },
    {
        "code": "050219",
        "name": "维吾尔语",
        "category": "05 文学",
        "category_icon": "🏜️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "维吾尔语专业培养掌握维吾尔语语言文学的专门人才，从事维吾尔语教学、翻译、研究和管理工作。",
        "what_you_learn": "维吾尔语语音、维吾尔语语法、维吾尔语口语、维吾尔语阅读、维吾尔语写作、维吾尔文学史、维吾尔文化概论、翻译理论与实践",
        "suitable_for": "对维吾尔族语言文化有浓厚兴趣的学生。",
        "career_outlook": "主要在教育部门、文化机构、新闻出版单位、民族事务部门从事教学、翻译、研究、编辑、管理等工作。",
        "xuefeng_comment": "维吾尔语专业是一个非常重要的民族语言专业。新疆作为我国重要的边疆地区，对维吾尔语人才的需求非常大。这个专业不仅能让你掌握一门重要的少数民族语言，还能让你深入了解维吾尔族的文化和新疆的历史。建议同学们在校期间认真学习专业知识，积极参加社会实践活动。",
        "yearly_courses": {"大一": ["维吾尔语语音、基础维吾尔语", "维吾尔文文法、维吾尔文化概论"], "大二": ["维吾尔语语法、中级维吾尔语", "维吾尔文学史、翻译理论"], "大三": ["高级维吾尔语、维汉互译", "维吾尔民俗学、新疆历史"], "大四": ["相关单位实习", "毕业论文"]},
        "top_universities": {"domestic": ["中央民族大学", "新疆大学", "新疆师范大学", "喀什大学"], "international": ["Xinjiang University"]}
    }
]

def main():
    print("=" * 70)
    print("📊 继续补充专业数据...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in majors_to_add:
        print(f"\n正在导入: {major['code']} - {major['name']}")
        ok, code = import_major(major)
        if ok or code in [200, 201]:
            success += 1
            print(f"✅ 成功")
        elif code == 409:
            skipped += 1
            print(f"⏭️ 已存在")
        else:
            failed += 1
            print(f"❌ 失败 (HTTP {code})")
        time.sleep(0.2)
    
    print(f"\n导入完成！成功: {success}, 跳过: {skipped}, 失败: {failed}")

if __name__ == "__main__":
    main()
