
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

majors = [
    {
        "code": "020101T",
        "name": "经济学",
        "category": "02 经济学",
        "category_icon": "💰",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "经济学专业培养掌握经济理论知识的人才，能在金融、政府等机构从事相关工作。",
        "what_you_learn": "微观经济学、宏观经济学、政治经济学、计量经济学、国际经济学",
        "suitable_for": "对经济感兴趣，数学好的学生。",
        "career_outlook": "金融机构、政府经济部门、企业等，就业面广。",
        "xuefeng_comment": "经济学专业就业面广，适合数学好的同学，考研后发展更好！",
        "yearly_courses": {"大一": ["高等数学", "政治经济学", "微观经济学", "宏观经济学"], "大二": ["计量经济学", "会计学", "统计学", "货币银行学"], "大三": ["国际经济学", "财政学", "产业经济学"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "清华大学"], "international": ["哈佛大学", "麻省理工学院"]}
    },
    {
        "code": "020301T",
        "name": "金融学",
        "category": "02 经济学",
        "category_icon": "🏦",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "金融学专业培养掌握金融知识的人才，能在银行、证券等机构工作。",
        "what_you_learn": "货币银行学、国际金融、证券投资学、公司金融、金融市场学",
        "suitable_for": "对金融感兴趣，数学好的学生。",
        "career_outlook": "银行、证券、基金等，就业好，收入高。",
        "xuefeng_comment": "金融学专业就业好，收入高，适合数学好的同学，非常热门！",
        "yearly_courses": {"大一": ["高等数学", "政治经济学", "微观经济学", "宏观经济学"], "大二": ["货币银行学", "国际金融", "会计学", "统计学"], "大三": ["证券投资学", "公司金融", "金融工程"], "大四": ["银行/证券实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "上海交通大学"], "international": ["哈佛大学", "宾夕法尼亚大学"]}
    },
    {
        "code": "020401T",
        "name": "国际经济与贸易",
        "category": "02 经济学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "国际经济与贸易专业培养掌握国贸知识的人才，能在企业从事外贸工作。",
        "what_you_learn": "国际贸易学、国际金融、国际贸易实务、国际商法、国际经济学",
        "suitable_for": "对国际贸易感兴趣，英语好的学生。",
        "career_outlook": "外贸企业、跨国公司、银行国际业务部等。",
        "xuefeng_comment": "国际经济与贸易专业适合英语好的同学，就业面广！",
        "yearly_courses": {"大一": ["高等数学", "政治经济学", "微观经济学", "宏观经济学"], "大二": ["国际贸易学", "国际金融", "会计学", "商务英语"], "大三": ["国际贸易实务", "国际商法", "国际市场营销"], "大四": ["外贸企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "上海对外经贸大学"], "international": ["哈佛大学", "伦敦政经学院"]}
    },
    {
        "code": "060101T",
        "name": "历史学",
        "category": "06 历史学",
        "category_icon": "📜",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-15k",
        "overview": "历史学专业培养掌握历史知识的人才，能在学校、博物馆等工作。",
        "what_you_learn": "中国古代史、中国近现代史、世界古代史、世界近现代史、史学理论",
        "suitable_for": "对历史感兴趣的学生。",
        "career_outlook": "教师、博物馆、出版社等。",
        "xuefeng_comment": "历史学专业就业稳定，适合想当老师的同学，或者继续深造！",
        "yearly_courses": {"大一": ["中国古代史", "世界古代史", "史学概论"], "大二": ["中国近现代史", "世界近现代史", "历史文选"], "大三": ["专门史课程", "史学理论与方法"], "大四": ["学校/博物馆实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "清华大学"], "international": ["牛津大学", "哈佛大学"]}
    },
    {
        "code": "050101T",
        "name": "汉语言文学",
        "category": "05 文学",
        "category_icon": "📖",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "汉语言文学专业培养掌握中文知识的人才，能在学校、媒体等工作。",
        "what_you_learn": "中国古代文学史、中国现当代文学史、外国文学史、文学理论、语言学",
        "suitable_for": "对文学感兴趣，文笔好的学生。",
        "career_outlook": "教师、编辑、公务员、新媒体等，就业面广。",
        "xuefeng_comment": "汉语言文学专业就业面广，适合文笔好的同学，考公也很有优势！",
        "yearly_courses": {"大一": ["中国古代文学史", "文学理论", "现代汉语"], "大二": ["中国现当代文学史", "外国文学史", "古代汉语"], "大三": ["语言学概论", "中国古典文献学", "应用写作"], "大四": ["学校/媒体实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京师范大学", "复旦大学", "南京大学"], "international": ["哈佛大学", "牛津大学"]}
    },
    {
        "code": "050201T",
        "name": "英语",
        "category": "05 文学",
        "category_icon": "🇬🇧",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "英语专业培养掌握英语的人才，能在学校、外贸、翻译等工作。",
        "what_you_learn": "基础英语、高级英语、英语听力、英语口语、英语写作、英美文学史",
        "suitable_for": "对英语感兴趣的学生。",
        "career_outlook": "教师、翻译、外贸、外企等，就业面广。",
        "xuefeng_comment": "英语专业就业面广，适合语言天赋好的同学！",
        "yearly_courses": {"大一": ["基础英语", "英语听力", "英语口语", "英语阅读"], "大二": ["高级英语", "英语写作", "英美文学史"], "大三": ["翻译理论与实践", "语言学导论", "英美国家概况"], "大四": ["学校/企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "南京大学"], "international": ["牛津大学", "剑桥大学"]}
    },
    {
        "code": "030301T",
        "name": "社会学",
        "category": "03 法学",
        "category_icon": "👥",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "社会学专业培养掌握社会知识的人才，能在政府、企业等工作。",
        "what_you_learn": "社会学概论、社会研究方法、社会统计学、社会工作、社会心理学",
        "suitable_for": "对社会问题感兴趣的学生。",
        "career_outlook": "政府部门、NGO、媒体、企业人力资源等。",
        "xuefeng_comment": "社会学专业就业面广，适合喜欢研究社会的同学！",
        "yearly_courses": {"大一": ["社会学概论", "人类学概论", "社会研究方法"], "大二": ["社会统计学", "心理学概论", "西方社会学理论"], "大三": ["发展社会学", "城市社会学", "社会工作"], "大四": ["政府/NGO实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "南京大学", "复旦大学"], "international": ["哈佛大学", "芝加哥大学"]}
    },
    {
        "code": "030201T",
        "name": "政治学与行政学",
        "category": "03 法学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "政治学专业培养掌握政治知识的人才，能在政府、事业单位等工作。",
        "what_you_learn": "政治学原理、中国政治制度、西方政治制度、行政管理学、政治思想史",
        "suitable_for": "对政治感兴趣的学生。",
        "career_outlook": "政府公务员、事业单位、媒体等。",
        "xuefeng_comment": "政治学专业适合考公，就业稳定！",
        "yearly_courses": {"大一": ["政治学原理", "西方政治思想史", "中国政治思想史"], "大二": ["中国政治制度", "西方政治制度", "行政管理学"], "大三": ["国际政治学", "公共政策学", "行政法学"], "大四": ["政府/事业单位实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "南开大学"], "international": ["哈佛大学", "普林斯顿大学"]}
    },
    {
        "code": "071001T",
        "name": "生物科学",
        "category": "07 理学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "生物科学专业培养掌握生物知识的人才，能在科研、药企等工作。",
        "what_you_learn": "普通生物学、生物化学、分子生物学、细胞生物学、遗传学",
        "suitable_for": "对生物感兴趣的学生。",
        "career_outlook": "科研院所、学校、药企等。",
        "xuefeng_comment": "生物科学专业适合深造，读研后发展好！",
        "yearly_courses": {"大一": ["高等数学", "普通化学", "有机化学", "普通生物学"], "大二": ["生物化学", "微生物学", "细胞生物学", "植物生物学"], "大三": ["分子生物学", "遗传学", "动物生物学"], "大四": ["科研院所实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "上海交通大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "071201T",
        "name": "统计学",
        "category": "07 理学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "统计学专业培养掌握统计知识的人才，能在金融、互联网等工作。",
        "what_you_learn": "数理统计、概率论、应用回归分析、抽样技术、统计软件",
        "suitable_for": "对数学和统计感兴趣的学生。",
        "career_outlook": "金融、互联网、市场调研等，需求大！",
        "xuefeng_comment": "统计学专业就业好，需求大，适合数学好的同学！",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "数理统计"], "大二": ["应用回归分析", "多元统计分析", "抽样技术"], "大三": ["时间序列分析", "统计软件", "贝叶斯统计"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "南开大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "120401T",
        "name": "公共事业管理",
        "category": "12 管理学",
        "category_icon": "🏢",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "公共事业管理专业培养管理人才，能在政府、事业单位等工作。",
        "what_you_learn": "公共管理学、公共政策学、公共经济学、社会学、行政法学",
        "suitable_for": "对公共管理感兴趣的学生。",
        "career_outlook": "政府、事业单位、NGO等。",
        "xuefeng_comment": "公共事业管理专业适合考公，就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "公共管理学", "公共经济学"], "大二": ["公共政策学", "行政法学", "社会学"], "大三": ["公共部门人力资源管理", "公共事业管理"], "大四": ["政府/事业单位实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "复旦大学", "北京大学", "清华大学"], "international": ["哈佛大学", "伦敦政经学院"]}
    },
    {
        "code": "120206T",
        "name": "人力资源管理",
        "category": "12 管理学",
        "category_icon": "👥",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "人力资源管理专业培养HR人才，能在企业从事人事工作。",
        "what_you_learn": "人力资源管理、组织行为学、劳动经济学、薪酬管理、招聘与配置",
        "suitable_for": "对人力资源工作感兴趣，沟通能力强的学生。",
        "career_outlook": "企业HR部门，需求稳定。",
        "xuefeng_comment": "人力资源管理专业就业稳定，适合善于沟通的同学！",
        "yearly_courses": {"大一": ["高等数学", "管理学原理", "微观经济学", "宏观经济学"], "大二": ["人力资源管理", "组织行为学", "劳动经济学"], "大三": ["招聘与配置", "培训与开发", "薪酬管理"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "上海交通大学", "北京大学", "中央财经大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "080901T",
        "name": "计算机科学与技术",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-30k",
        "overview": "计算机科学与技术专业培养编程人才，能在IT企业工作。",
        "what_you_learn": "C语言、数据结构、计算机组成原理、操作系统、计算机网络",
        "suitable_for": "对编程感兴趣的学生。",
        "career_outlook": "互联网企业、IT公司等，就业非常好！",
        "xuefeng_comment": "计算机专业就业非常好，收入高，强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "C语言程序设计", "线性代数", "离散数学"], "大二": ["数据结构", "计算机组成原理", "操作系统", "Java程序设计"], "大三": ["计算机网络", "数据库原理", "软件工程", "算法设计与分析"], "大四": ["IT企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "浙江大学", "上海交通大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080801T",
        "name": "自动化",
        "category": "08 工学",
        "category_icon": "🤖",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "自动化专业培养自动化人才，能在各种企业工作。",
        "what_you_learn": "自动控制原理、电路原理、模拟电子技术、数字电子技术、PLC编程",
        "suitable_for": "对自动化感兴趣的学生。",
        "career_outlook": "各种企业，就业面广！",
        "xuefeng_comment": "自动化专业就业面广，非常推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "电路原理"], "大二": ["模拟电子技术", "数字电子技术", "自动控制原理"], "大三": ["PLC编程", "过程控制", "运动控制"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "浙江大学", "上海交通大学", "哈尔滨工业大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080201T",
        "name": "机械工程",
        "category": "08 工学",
        "category_icon": "⚙️",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "机械工程专业培养机械人才，能在制造企业工作。",
        "what_you_learn": "工程力学、机械原理、机械设计、机械制图、金属工艺学",
        "suitable_for": "对机械感兴趣的学生。",
        "career_outlook": "制造企业，需求稳定！",
        "xuefeng_comment": "机械工程专业就业稳定，老牌专业！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["机械原理", "机械设计", "工程材料"], "大三": ["机械制造技术基础", "控制工程基础"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "上海交通大学", "浙江大学", "华中科技大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    }
]

count = 0
skipped = 0

for major in majors:
    ok, code = import_major(major)
    if ok:
        print(f"✅ {major['code']} - {major['name']} 成功")
        count += 1
    elif code == 409:
        print(f"⏭️ {major['code']} - {major['name']} 已存在")
        skipped += 1
    else:
        print(f"❌ {major['code']} - {major['name']} 失败")
    time.sleep(0.5)

print(f"\n导入完成！成功 {count}，跳过 {skipped}")
