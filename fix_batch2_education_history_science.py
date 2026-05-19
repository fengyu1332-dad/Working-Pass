"""
系统性补充教育部2024年专业清单中的缺失专业
第二批：教育学、历史学、理学
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
    # ========== 04教育学 - 补充缺失专业 ==========
    {
        "code": "040102",
        "name": "科学教育",
        "category": "04 教育学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "科学教育专业培养掌握科学教育理论和方法的教师，能在中小学从事科学课程教学工作。",
        "what_you_learn": "科学教育学、普通物理学、普通化学、普通生物学、科学实验教学、自然科学概论",
        "suitable_for": "对科学教育感兴趣，理科基础扎实的学生。",
        "career_outlook": "中小学科学教师、科技馆辅导员等。",
        "xuefeng_comment": "科学教育专业就业稳定，适合想当科学老师的同学！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "大学化学", "普通生物学"], "大二": ["科学教育学", "自然科学概论", "科学实验教学"], "大三": ["科学技术史", "环境科学基础", "信息技术教育"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["华东师范大学", "北京师范大学", "华中师范大学", "华南师范大学"], "international": []}
    },
    {
        "code": "040103",
        "name": "人文教育",
        "category": "04 教育学",
        "category_icon": "📚",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "人文教育专业培养掌握人文教育理论和方法的教师，能在中小学从事人文社科类课程教学工作。",
        "what_you_learn": "人文教育学、中国文学、世界文学、中国历史、世界历史、地理学概论",
        "suitable_for": "对人文社科感兴趣，文科基础扎实的学生。",
        "career_outlook": "中小学人文社科教师、培训机构教师等。",
        "xuefeng_comment": "人文教育专业就业稳定，适合想当文科老师的同学！",
        "yearly_courses": {"大一": ["中国文学", "世界文学", "中国历史", "世界历史"], "大二": ["人文教育学", "地理学概论", "哲学概论"], "大三": ["人文社会科学专题", "教育心理学"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["华东师范大学", "北京师范大学", "东北师范大学"], "international": []}
    },
    {
        "code": "040104",
        "name": "教育技术学",
        "category": "04 教育学",
        "category_icon": "💻",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-14k",
        "overview": "教育技术学专业培养掌握教育技术和信息技术教学能力的专门人才，能在学校、教育技术企业等从事教育技术工作。",
        "what_you_learn": "教育技术学、教学系统设计、多媒体技术、教育软件开发、远程教育、教育影视制作",
        "suitable_for": "对教育技术感兴趣，既懂教育又懂技术的复合型人才。",
        "career_outlook": "学校电教中心、教育技术企业、在线教育平台等。",
        "xuefeng_comment": "教育技术学专业就业好，随着在线教育发展需求增长！",
        "yearly_courses": {"大一": ["教育学原理", "心理学概论", "程序设计基础"], "大二": ["教育技术学", "教学系统设计", "多媒体技术"], "大三": ["教育软件开发", "远程教育", "教育影视制作"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "华中师范大学", "华南师范大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "040106K",
        "name": "学前教育",
        "category": "04 教育学",
        "category_icon": "🎨",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "学前教育专业培养掌握学前教育理论和方法的幼儿教师，能在幼儿园等从事幼儿教育工作。",
        "what_you_learn": "学前教育学、学前儿童发展心理学、学前儿童卫生学、幼儿园课程与教学、幼儿园游戏理论与指导",
        "suitable_for": "喜欢小朋友，有爱心，有耐心，有才艺的学生。",
        "career_outlook": "幼儿园、幼教机构等，幼儿教师缺口很大！",
        "xuefeng_comment": "学前教育专业就业非常好，幼儿园老师缺口巨大！非常适合有爱心的同学！",
        "yearly_courses": {"大一": ["学前教育学", "学前儿童发展心理学", "美术基础", "音乐基础"], "大二": ["学前儿童卫生学", "幼儿园课程与教学", "舞蹈基础"], "大三": ["幼儿园游戏理论与指导", "学前儿童语言教育", "学前儿童科学教育"], "大四": ["幼儿园实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "南京师范大学", "浙江师范大学"], "international": ["哥伦比亚大学"]}
    },
    {
        "code": "040107K",
        "name": "小学教育",
        "category": "04 教育学",
        "category_icon": "🏫",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "小学教育专业培养掌握小学教育理论和方法的教师，能在小学从事各科教学工作。",
        "what_you_learn": "小学教育学、小学生发展心理学、小学语文教学论、小学数学教学论、小学英语教学论",
        "suitable_for": "喜欢小学生，有爱心，有耐心的学生。",
        "career_outlook": "小学教师，需求稳定。",
        "xuefeng_comment": "小学教育专业就业稳定，工作相对轻松！适合想当小学老师的同学！",
        "yearly_courses": {"大一": ["小学教育学", "小学生发展心理学", "教育学原理"], "大二": ["小学语文教学论", "小学数学教学论"], "大三": ["小学英语教学论", "小学科学教学论", "班级管理"], "大四": ["小学实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "东北师范大学", "华中师范大学"], "international": []}
    },
    {
        "code": "040108K",
        "name": "特殊教育",
        "category": "04 教育学",
        "category_icon": "👶",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "特殊教育专业培养掌握特殊教育理论和方法的教师，能在特殊教育学校等从事特殊儿童教育工作。",
        "what_you_learn": "特殊教育学、特殊儿童心理学、特殊儿童教育诊断、特殊教育课程与教学、特殊儿童康复训练",
        "suitable_for": "对特殊儿童有爱心，有耐心，有责任心的学生。",
        "career_outlook": "特殊教育学校、康复机构等，特殊教育教师缺口较大。",
        "xuefeng_comment": "特殊教育专业就业稳定，社会意义重大！非常适合有爱心的同学！",
        "yearly_courses": {"大一": ["特殊教育学", "特殊儿童心理学", "教育学原理"], "大二": ["特殊儿童教育诊断", "手语基础", "盲文基础"], "大三": ["特殊教育课程与教学", "特殊儿童康复训练"], "大四": ["特殊教育学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "华中师范大学", "重庆师范大学"], "international": []}
    },
    {
        "code": "040109T",
        "name": "华文教育",
        "category": "04 教育学",
        "category_icon": "🌏",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "华文教育专业培养掌握华文教育理论和方法的教师，能在海外华文学校从事华文教学工作。",
        "what_you_learn": "华文教育学、华文教学法、汉语基础、中华文化、跨文化交际",
        "suitable_for": "对华文教育感兴趣，有志于从事海外华文教学的学生。",
        "career_outlook": "海外华文学校、国际学校、孔子学院等。",
        "xuefeng_comment": "华文教育专业适合有志于海外华文教学的同学，就业有特色！",
        "yearly_courses": {"大一": ["华文教育学", "汉语基础", "中华文化"], "大二": ["华文教学法", "跨文化交际", "中国文学"], "大三": ["华文教材教法", "华文教育技术"], "大四": ["海外华文学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["暨南大学", "华东师范大学", "云南师范大学"], "international": []}
    },
    {
        "code": "040110TK",
        "name": "教育康复学",
        "category": "04 教育学",
        "category_icon": "💊",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-14k",
        "overview": "教育康复学专业培养掌握教育康复理论和方法的专门人才，能在康复机构、特殊教育学校从事教育康复工作。",
        "what_you_learn": "教育康复学、言语语言康复、听觉康复、特殊儿童教育诊断、教育康复技术",
        "suitable_for": "对教育康复感兴趣，有耐心的学生。",
        "career_outlook": "康复机构、特殊教育学校、医疗康复中心等。",
        "xuefeng_comment": "教育康复学专业就业好，随着康复需求增长，前景广阔！",
        "yearly_courses": {"大一": ["教育学原理", "心理学概论", "人体解剖学"], "大二": ["教育康复学", "言语语言康复", "听觉康复"], "大三": ["特殊儿童教育诊断", "教育康复技术"], "大四": ["康复机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "华中师范大学"], "international": []}
    },
    {
        "code": "040111T",
        "name": "卫生教育",
        "category": "04 教育学",
        "category_icon": "🏥",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "卫生教育专业培养掌握学校卫生教育和健康教育理论和方法的教师，能在学校从事卫生教育工作。",
        "what_you_learn": "学校卫生学、健康教育学、流行病学基础、营养学基础、心理健康教育",
        "suitable_for": "对卫生教育和健康教育感兴趣的学生。",
        "career_outlook": "中小学校医、健康教育教师、疾病预防控制中心等。",
        "xuefeng_comment": "卫生教育专业就业稳定，适合想在学校工作的同学！",
        "yearly_courses": {"大一": ["人体解剖学", "生理学", "基础医学概论"], "大二": ["学校卫生学", "健康教育学", "流行病学基础"], "大三": ["营养学基础", "心理健康教育", "健康评估"], "大四": ["学校/疾控中心实习", "毕业论文"]},
        "top_universities": {"domestic": ["华东师范大学", "北京师范大学", "华中师范大学"], "international": []}
    },
    {
        "code": "040112T",
        "name": "认知科学与技术",
        "category": "04 教育学",
        "category_icon": "🧠",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "认知科学与技术专业培养掌握认知科学理论和技术的交叉学科人才，能在高校、研究机构、企业等从事认知科学研究和技术开发工作。",
        "what_you_learn": "认知心理学、神经科学、人工智能、实验心理学、认知神经科学、认知建模",
        "suitable_for": "对认知科学感兴趣，兼具文理思维的学生。",
        "career_outlook": "高校、研究机构、科技企业等，前沿交叉学科，需求增长。",
        "xuefeng_comment": "认知科学与技术是前沿交叉学科，就业前景好！建议继续深造。",
        "yearly_courses": {"大一": ["认知心理学", "神经科学基础", "人工智能概论"], "大二": ["实验心理学", "认知神经科学", "程序设计基础"], "大三": ["认知建模", "脑与认知", "心理学研究方法"], "大四": ["研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "华东师范大学", "浙江大学"], "international": ["哈佛大学", "麻省理工学院"]}
    },
    {
        "code": "040206T",
        "name": "运动康复",
        "category": "04 教育学",
        "category_icon": "🏃",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-14k",
        "overview": "运动康复专业培养掌握运动康复理论和技术的专门人才，能在体育系统、医疗康复机构等从事运动康复工作。",
        "what_you_learn": "运动解剖学、运动生理学、运动损伤学、康复评定学、运动康复治疗技术、物理因子治疗",
        "suitable_for": "对运动康复感兴趣，有体育基础的学生。",
        "career_outlook": "体育系统康复中心、医疗康复机构、健身机构等。",
        "xuefeng_comment": "运动康复专业就业好，随着全民健身和康复意识提高，需求增长！",
        "yearly_courses": {"大一": ["运动解剖学", "运动生理学", "体育概论"], "大二": ["运动损伤学", "康复评定学", "人体发育学"], "大三": ["运动康复治疗技术", "物理因子治疗", "运动处方"], "大四": ["康复机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育大学", "武汉体育学院", "成都体育学院"], "international": []}
    },
    {
        "code": "040207T",
        "name": "休闲体育",
        "category": "04 教育学",
        "category_icon": "🏄",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "休闲体育专业培养掌握休闲体育理论和方法的专门人才，能在休闲体育产业从事经营管理工作。",
        "what_you_learn": "休闲体育概论、休闲体育产业经营、休闲体育项目与管理、旅游体育、户外运动",
        "suitable_for": "对休闲体育产业感兴趣，有体育特长的学生。",
        "career_outlook": "体育旅游企业、休闲体育俱乐部、户外运动机构等。",
        "xuefeng_comment": "休闲体育专业就业主要在体育产业，随着休闲体育产业发展，前景好！",
        "yearly_courses": {"大一": ["休闲体育概论", "体育概论", "休闲体育项目"], "大二": ["休闲体育产业经营", "旅游体育", "户外运动"], "大三": ["休闲体育赛事组织", "康体娱乐设施管理"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育大学", "武汉体育学院"], "international": []}
    },
    {
        "code": "040208T",
        "name": "体能训练",
        "category": "04 教育学",
        "category_icon": "💪",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "体能训练专业培养掌握体能训练理论和方法的专门人才，能在体育系统、健身机构等从事体能训练工作。",
        "what_you_learn": "运动训练学、体能训练原理与实践、运动解剖学、运动生理学、运动营养学",
        "suitable_for": "对体能训练感兴趣，体育基础扎实的学生。",
        "career_outlook": "体育系统体能训练师、健身机构、学校运动队等。",
        "xuefeng_comment": "体能训练专业就业好，专业性强！",
        "yearly_courses": {"大一": ["运动训练学", "运动解剖学", "运动生理学"], "大二": ["体能训练原理与实践", "运动营养学"], "大三": ["专项体能训练", "运动损伤预防"], "大四": ["运动队实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育大学", "武汉体育学院"], "international": []}
    },
    {
        "code": "040209T",
        "name": "冰雪运动",
        "category": "04 教育学",
        "category_icon": "⛷️",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-16k",
        "overview": "冰雪运动专业培养掌握冰雪运动理论和技能的专门人才，能在冰雪体育产业从事教学和运营管理工作。",
        "what_you_learn": "冰雪运动概论、滑雪运动、冰雪场馆运营管理、冰雪赛事组织、冰雪救护",
        "suitable_for": "对冰雪运动感兴趣，身体素质好的学生。",
        "career_outlook": "滑雪场、滑冰馆、冰雪体育企业等。",
        "xuefeng_comment": "冰雪运动专业随着2022冬奥会成功举办，冰雪产业发展迅速，前景好！",
        "yearly_courses": {"大一": ["冰雪运动概论", "冰雪运动基础", "体育概论"], "大二": ["滑雪运动", "滑冰运动", "冰雪场馆运营管理"], "大三": ["冰雪赛事组织", "冰雪救护", "冰雪产业经营"], "大四": ["冰雪场馆实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京体育大学", "哈尔滨体育学院", "沈阳体育学院"], "international": []}
    },
    
    # ========== 06历史学 - 补充缺失专业 ==========
    {
        "code": "060103",
        "name": "考古学",
        "category": "06 历史学",
        "category_icon": "🏺",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "考古学专业培养掌握考古学理论和方法的专业人才，能在考古研究机构、博物馆等从事考古发掘和研究工作。",
        "what_you_learn": "考古学概论、中国考古学、世界考古学、考古发掘技术、文物鉴定、博物馆学",
        "suitable_for": "对考古和文物感兴趣，能吃苦的学生。",
        "career_outlook": "考古研究所、博物馆、文物鉴定机构等。",
        "xuefeng_comment": "考古学是学术性很强的专业，需要田野考古发掘，工作辛苦但很有意义。建议继续深造。",
        "yearly_courses": {"大一": ["考古学概论", "中国古代史", "世界古代史"], "大二": ["中国考古学", "世界考古学", "古文字学"], "大三": ["考古发掘技术", "文物鉴定", "博物馆学"], "大四": ["考古工地实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "四川大学", "西北大学"], "international": ["哈佛大学", "牛津大学"]}
    },
    {
        "code": "060104",
        "name": "文物与博物馆学",
        "category": "06 历史学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "文物与博物馆学专业培养掌握文物保护和博物馆管理理论的专业人才，能在博物馆、文物机构等从事文物保护和博物馆管理工作。",
        "what_you_learn": "博物馆学概论、文物学概论、文物保护基础、博物馆藏品管理、博物馆陈列设计",
        "suitable_for": "对文物和博物馆工作感兴趣的学生。",
        "career_outlook": "博物馆、文物鉴定机构、文化遗产管理部门等。",
        "xuefeng_comment": "文物与博物馆学专业就业稳定，适合想从事文博工作的同学！",
        "yearly_courses": {"大一": ["博物馆学概论", "文物学概论", "中国古代史"], "大二": ["文物保护基础", "博物馆藏品管理", "文物鉴定"], "大三": ["博物馆陈列设计", "文化遗产管理"], "大四": ["博物馆实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "四川大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "060105T",
        "name": "文物保护技术",
        "category": "06 历史学",
        "category_icon": "🔧",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "文物保护技术专业培养掌握文物保护和修复技术的专业人才，能在文物修复机构、博物馆等从事文物保护和修复工作。",
        "what_you_learn": "文物保护基础、文物修复技术、文物分析技术、无机质文物保护、有机质文物保护",
        "suitable_for": "对文物修复感兴趣，动手能力强的学生。",
        "career_outlook": "文物修复机构、博物馆、考古研究所等。",
        "xuefeng_comment": "文物保护技术专业是技术性很强的专业，社会需求大！建议继续深造。",
        "yearly_courses": {"大一": ["文物保护基础", "化学基础", "文物学概论"], "大二": ["文物修复技术", "文物分析技术", "材料科学基础"], "大三": ["无机质文物保护", "有机质文物保护"], "大四": ["文物修复机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "西北大学", "南京大学", "四川大学"], "international": []}
    },
    {
        "code": "060107T",
        "name": "文化遗产",
        "category": "06 历史学",
        "category_icon": "🎭",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-14k",
        "overview": "文化遗产专业培养掌握文化遗产保护和管理理论的专业人才，能在文化遗产管理部门、规划设计院等从事文化遗产保护工作。",
        "what_you_learn": "文化遗产概论、文化遗产保护规划、文化遗产法律法规、文化遗产评估、非物质文化遗产保护",
        "suitable_for": "对文化遗产保护感兴趣的学生。",
        "career_outlook": "文化遗产管理部门、规划设计院、博物馆等。",
        "xuefeng_comment": "文化遗产专业就业稳定，随着文化遗产保护意识提高，需求增长！",
        "yearly_courses": {"大一": ["文化遗产概论", "中国古代史", "世界文化遗产概论"], "大二": ["文化遗产保护规划", "文化遗产法律法规", "文化遗产评估"], "大三": ["非物质文化遗产保护", "文化遗产数字化"], "大四": ["文化遗产机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "浙江大学", "厦门大学"], "international": []}
    },
    {
        "code": "060108T",
        "name": "古文字学",
        "category": "06 历史学",
        "category_icon": "📜",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "古文字学专业培养掌握古文字学理论和方法的专业人才，能在高校、研究所从事古文字研究工作。",
        "what_you_learn": "古文字学概论、甲骨学、金文研究、简帛学、古文字学理论与方法",
        "suitable_for": "对古文字研究感兴趣，有较好古文献基础的学生。",
        "career_outlook": "高校、研究机构、博物馆等。",
        "xuefeng_comment": "古文字学是冷门但非常重要的专业，就业主要在学术研究领域。建议继续深造。",
        "yearly_courses": {"大一": ["古文字学概论", "古代汉语", "中国古代史"], "大二": ["甲骨学", "金文研究", "古文字学理论与方法"], "大三": ["简帛学", "古文字学专题"], "大四": ["研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "武汉大学"], "international": []}
    },
    {
        "code": "060109T",
        "name": "科学史",
        "category": "06 历史学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-14k",
        "overview": "科学史专业培养掌握科学史理论和方法的交叉学科人才，能在高校、研究机构从事科技史研究工作。",
        "what_you_learn": "科学技术史、科学哲学、科学社会学、自然科学概论",
        "suitable_for": "对科学技术史感兴趣，兼具文理思维的学生。",
        "career_outlook": "高校、研究机构、科普机构等。",
        "xuefeng_comment": "科学史是交叉学科，就业主要在学术研究领域。建议继续深造。",
        "yearly_courses": {"大一": ["科学技术史", "科学哲学", "自然科学概论"], "大二": ["科学社会学", "中外科技史比较"], "大三": ["科技史专题研究", "科学思想史"], "大四": ["研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "中国科学技术大学"], "international": ["哈佛大学", "麻省理工学院"]}
    },
    
    # ========== 07理学 - 补充缺失专业 ==========
    {
        "code": "070102",
        "name": "信息与计算科学",
        "category": "07 理学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "信息与计算科学专业培养掌握数学和信息科学的交叉学科人才，能在IT企业、金融机构等从事算法设计、数据分析等工作。",
        "what_you_learn": "数学分析、高等代数、概率论、数值分析、数据结构、算法设计与分析",
        "suitable_for": "对数学和计算机都感兴趣的学生。",
        "career_outlook": "IT企业、金融机构、科研部门等，就业非常好！",
        "xuefeng_comment": "信息与计算科学专业是数学和计算机的交叉学科，就业非常好！强烈推荐！",
        "yearly_courses": {"大一": ["数学分析", "高等代数", "程序设计基础"], "大二": ["概率论", "数值分析", "数据结构"], "大三": ["算法设计与分析", "机器学习", "最优化方法"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "浙江大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "070202",
        "name": "应用物理学",
        "category": "07 理学",
        "category_icon": "⚛️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "应用物理学专业培养掌握物理学基础理论和应用技术的专门人才，能在科研机构、企业等从事技术研发工作。",
        "what_you_learn": "普通物理学、理论力学、量子力学、固体物理学、半导体物理、光电子技术",
        "suitable_for": "对物理技术应用感兴趣的学生。",
        "career_outlook": "科研院所、电子企业、光电企业等。",
        "xuefeng_comment": "应用物理学专业就业好，可以转向光电、半导体等热门方向！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "普通物理实验"], "大二": ["理论力学", "量子力学", "热力学与统计物理"], "大三": ["固体物理学", "半导体物理", "光电子技术"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "中国科学技术大学", "复旦大学"], "international": ["麻省理工学院", "加州理工学院"]}
    },
    {
        "code": "070203T",
        "name": "核物理",
        "category": "07 理学",
        "category_icon": "☢️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "核物理专业培养掌握核物理理论和技术的专门人才，能在核能研究机构、医疗单位等从事核技术应用工作。",
        "what_you_learn": "原子核物理、粒子物理、核电子学、核辐射探测、核技术应用、核医学",
        "suitable_for": "对核物理感兴趣的学生。",
        "career_outlook": "核能研究院所、核电站、医疗单位等。",
        "xuefeng_comment": "核物理是特殊专业，就业主要在核能领域。工作稳定，但需要持证上岗。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "原子物理"], "大二": ["原子核物理", "粒子物理", "核电子学"], "大三": ["核辐射探测", "核技术应用", "核医学"], "大四": ["核能机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "中国科学技术大学", "哈尔滨工业大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "070204T",
        "name": "声学",
        "category": "07 理学",
        "category_icon": "🔊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "声学专业培养掌握声学理论和技术的专门人才，能在声学研究所、音响企业等从事声学研究和产品开发工作。",
        "what_you_learn": "声学基础、物理声学、电声学、建筑声学、噪声控制、声学测量",
        "suitable_for": "对声学感兴趣的学生。",
        "career_outlook": "声学研究所、音响企业、建筑设计院、噪声治理企业等。",
        "xuefeng_comment": "声学是较冷门但技术性强的专业，就业稳定。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "声学基础"], "大二": ["物理声学", "电声学", "数学物理方法"], "大三": ["建筑声学", "噪声控制", "声学测量"], "大四": ["声学机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京大学", "中国科学技术大学", "华中科技大学"], "international": ["麻省理工学院"]}
    },
    {
        "code": "070302",
        "name": "应用化学",
        "category": "07 理学",
        "category_icon": "🧪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "应用化学专业培养掌握化学基础理论和应用技术的专门人才，能在化工企业、质检部门等从事化学分析和产品研发工作。",
        "what_you_learn": "无机化学、有机化学、分析化学、物理化学、化工原理、化学工艺学",
        "suitable_for": "对化学应用感兴趣，动手能力强的学生。",
        "career_outlook": "化工企业、质检机构、环保部门等。",
        "xuefeng_comment": "应用化学专业就业稳定，是化学类实用性强的专业！",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学"], "大二": ["分析化学", "物理化学", "化工原理"], "大三": ["化学工艺学", "精细化学品化学"], "大四": ["化工企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "南开大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "070303T",
        "name": "化学生物学",
        "category": "07 理学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "化学生物学专业培养掌握化学和生物学交叉知识的专门人才，能在生物医药企业、科研机构等从事化学生物学研究工作。",
        "what_you_learn": "无机化学、有机化学、生物化学、分子生物学、化学生物学、药物化学",
        "suitable_for": "对化学和生物学交叉领域感兴趣的学生。",
        "career_outlook": "生物医药企业、科研机构、制药企业等。",
        "xuefeng_comment": "化学生物学是前沿交叉学科，就业前景好！建议继续深造。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "生物化学"], "大二": ["分子生物学", "分析化学", "化学生物学"], "大三": ["药物化学", "生物无机化学"], "大四": ["科研机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "南开大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "070402",
        "name": "地理科学",
        "category": "07 理学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "地理科学专业培养掌握地理科学理论和方法的专门人才，能在学校、科研机构等从事地理科学研究和教学工作。",
        "what_you_learn": "自然地理学、人文地理学、地图学、地理信息系统、区域地理学",
        "suitable_for": "对地理科学感兴趣的学生。",
        "career_outlook": "学校、科研机构、国土资源部门等。",
        "xuefeng_comment": "地理科学专业就业稳定，主要从事教学和研究工作。",
        "yearly_courses": {"大一": ["地球概论", "自然地理学", "地图学"], "大二": ["人文地理学", "地理信息系统", "区域地理学"], "大三": ["地理学野外实习", "遥感概论"], "大四": ["学校/研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "华东师范大学", "南京大学", "兰州大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "070403",
        "name": "自然地理与资源环境",
        "category": "07 理学",
        "category_icon": "🌲",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "自然地理与资源环境专业培养掌握自然地理和资源环境理论的专门人才，能在环保部门、国土资源部门等从事资源环境研究和规划工作。",
        "what_you_learn": "自然地理学、资源科学、环境科学、土地资源管理、遥感与GIS",
        "suitable_for": "对自然地理和环境保护感兴趣的学生。",
        "career_outlook": "环保部门、国土资源部门、规划设计院等。",
        "xuefeng_comment": "自然地理与资源环境专业就业稳定，随着环保意识提高，需求增长！",
        "yearly_courses": {"大一": ["自然地理学", "地球概论", "环境科学概论"], "大二": ["资源科学", "土地资源管理", "遥感基础"], "大三": ["遥感与GIS", "环境影响评价"], "大四": ["国土/环保部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "兰州大学", "华东师范大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "070404",
        "name": "人文地理与城乡规划",
        "category": "07 理学",
        "category_icon": "🏙️",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "人文地理与城乡规划专业培养掌握人文地理和城乡规划理论的专门人才，能在规划设计院、国土资源部门等从事城乡规划工作。",
        "what_you_learn": "人文地理学、城市规划原理、区域规划、土地利用规划、地理信息系统",
        "suitable_for": "对人文地理和城市规划感兴趣的学生。",
        "career_outlook": "规划设计院、国土资源部门、房地产公司等。",
        "xuefeng_comment": "人文地理与城乡规划专业就业好，城乡规划人才需求大！",
        "yearly_courses": {"大一": ["人文地理学", "自然地理学", "城市规划概论"], "大二": ["城市规划原理", "区域规划", "地理信息系统"], "大三": ["土地利用规划", "城市设计"], "大四": ["规划设计院实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "同济大学", "南京大学", "华南理工大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "070405",
        "name": "地理信息科学",
        "category": "07 理学",
        "category_icon": "🗺️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "地理信息科学专业培养掌握地理信息系统理论和技术的专门人才，能在GIS企业、科研机构等从事地理信息系统开发和应用工作。",
        "what_you_learn": "地图学、地理信息系统、遥感概论、GIS程序设计、空间数据库、GIS应用开发",
        "suitable_for": "对地理信息系统感兴趣，计算机基础好的学生。",
        "career_outlook": "GIS企业、测绘部门、国土资源部门、互联网公司等。",
        "xuefeng_comment": "地理信息科学专业就业非常好，GIS在智慧城市、数字孪生等领域应用广泛！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "地图学", "程序设计基础"], "大二": ["地理信息系统", "遥感概论", "空间数据库"], "大三": ["GIS程序设计", "GIS应用开发", "WebGIS"], "大四": ["GIS企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "武汉大学", "南京大学", "华东师范大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "070501",
        "name": "大气科学",
        "category": "07 理学",
        "category_icon": "🌤️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "大气科学专业培养掌握大气科学理论和技术的专门人才，能在气象部门、环保部门等从事大气科学研究和气象服务工作。",
        "what_you_learn": "大气物理学、大气化学、天气学、气候学、气象预报、数值天气预报",
        "suitable_for": "对大气科学和气象学感兴趣的学生。",
        "career_outlook": "气象部门、环保部门、民航部门等。",
        "xuefeng_comment": "大气科学专业就业稳定，主要在气象系统，工作稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "大气科学概论"], "大二": ["大气物理学", "大气化学", "天气学"], "大三": ["气候学", "气象预报", "数值天气预报"], "大四": ["气象部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "南京信息工程大学", "兰州大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "070502",
        "name": "应用气象学",
        "category": "07 理学",
        "category_icon": "⛅",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "应用气象学专业培养掌握应用气象学理论和方法的专门人才，能在气象部门、农业部门等从事气象服务工作。",
        "what_you_learn": "气象学基础、农业气象学、气象服务学、气象信息处理、环境气象学",
        "suitable_for": "对应用气象学感兴趣的学生。",
        "career_outlook": "气象部门、农业部门、环保部门等。",
        "xuefeng_comment": "应用气象学专业就业稳定，主要在气象系统！",
        "yearly_courses": {"大一": ["高等数学", "气象学基础", "大气科学概论"], "大二": ["农业气象学", "气象服务学", "气象信息处理"], "大三": ["环境气象学", "气象灾害评估"], "大四": ["气象部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京信息工程大学", "北京大学", "兰州大学"], "international": []}
    },
    {
        "code": "070601",
        "name": "海洋科学",
        "category": "07 理学",
        "category_icon": "🌊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "海洋科学专业培养掌握海洋科学理论和技术的专门人才，能在海洋研究机构、海洋局等从事海洋科学研究工作。",
        "what_you_learn": "海洋学概论、物理海洋学、化学海洋学、生物海洋学、海洋地质学",
        "suitable_for": "对海洋科学感兴趣的学生。",
        "career_outlook": "海洋研究机构、海洋局、涉海企业等。",
        "xuefeng_comment": "海洋科学是战略性学科，就业前景好！建议继续深造。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "海洋学概论"], "大二": ["物理海洋学", "化学海洋学", "生物海洋学"], "大三": ["海洋地质学", "海洋调查与观测"], "大四": ["海洋研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国海洋大学", "厦门大学", "同济大学", "浙江大学"], "international": ["麻省理工学院", "加州大学圣地亚哥分校"]}
    },
    {
        "code": "070602",
        "name": "海洋技术",
        "category": "07 理学",
        "category_icon": "🚀",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "海洋技术专业培养掌握海洋技术理论和方法的专门人才，能在海洋技术企业、海洋局等从事海洋技术研发和应用工作。",
        "what_you_learn": "海洋学基础、海洋探测技术、海洋声学、海洋遥感技术、海洋测绘技术",
        "suitable_for": "对海洋技术感兴趣的学生。",
        "career_outlook": "海洋技术企业、海洋局、海军等。",
        "xuefeng_comment": "海洋技术专业就业好，海洋技术是国家战略重点领域！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "海洋学基础"], "大二": ["海洋探测技术", "海洋遥感技术", "海洋测绘技术"], "大三": ["海洋声学", "海洋信息技术"], "大四": ["海洋技术企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国海洋大学", "厦门大学", "哈尔滨工程大学"], "international": []}
    },
    {
        "code": "070701",
        "name": "地球物理学",
        "category": "07 理学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "地球物理学专业培养掌握地球物理学理论和技术的专门人才，能在能源勘探、灾害监测等部门从事地球物理探测工作。",
        "what_you_learn": "地球物理学概论、地震学、地磁学、重力学、勘探地球物理学",
        "suitable_for": "对地球物理学感兴趣的学生。",
        "career_outlook": "能源勘探企业、地震局、地质调查部门等。",
        "xuefeng_comment": "地球物理学专业就业稳定，主要在能源勘探和灾害监测领域！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "地球物理学概论"], "大二": ["地震学", "地磁学", "重力学"], "大三": ["勘探地球物理学", "地球物理观测"], "大四": ["勘探企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国科学技术大学", "武汉大学", "同济大学"], "international": ["哈佛大学", "加州理工学院"]}
    },
    {
        "code": "070702",
        "name": "空间科学与技术",
        "category": "07 理学",
        "category_icon": "🛸",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "空间科学与技术专业培养掌握空间科学和技术理论和方法的专门人才，能在航天部门、科研机构等从事空间科学研究工作。",
        "what_you_learn": "空间科学概论、天体力学、空间探测技术、航天器原理、空间环境",
        "suitable_for": "对空间科学和航天技术感兴趣的学生。",
        "career_outlook": "航天部门、中国科学院、卫星发射中心等。",
        "xuefeng_comment": "空间科学与技术专业就业好，是国家航天战略重点领域！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "空间科学概论"], "大二": ["天体力学", "空间探测技术", "航天器原理"], "大三": ["空间环境", "卫星遥感技术"], "大四": ["航天部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "中国科学技术大学", "北京航空航天大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "070801",
        "name": "地质学",
        "category": "07 理学",
        "category_icon": "🪨",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "地质学专业培养掌握地质学理论和方法的专门人才，能在地质勘查部门、科研机构等从事地质科学研究和勘查工作。",
        "what_you_learn": "地质学概论、结晶学与矿物学、岩石学、古生物学、地史学、构造地质学",
        "suitable_for": "对地质学感兴趣，能吃苦的学生。",
        "career_outlook": "地质勘查部门、矿业企业、科研机构等。",
        "xuefeng_comment": "地质学专业就业稳定，需要野外工作，适合能吃苦的同学！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "地质学概论"], "大二": ["结晶学与矿物学", "岩石学", "古生物学"], "大三": ["地史学", "构造地质学", "矿床学"], "大四": ["地质队实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "中国地质大学", "西北大学"], "international": ["哈佛大学", "加州理工学院"]}
    },
    {
        "code": "070802",
        "name": "地球化学",
        "category": "07 理学",
        "category_icon": "🧪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "地球化学专业培养掌握地球化学理论和方法的专门人才，能在地质勘查部门、环保部门等从事地球化学研究和调查工作。",
        "what_you_learn": "地球化学概论、同位素地球化学、环境地球化学、勘查地球化学、岩石地球化学",
        "suitable_for": "对地球化学感兴趣的学生。",
        "career_outlook": "地质勘查部门、环保部门、矿业企业等。",
        "xuefeng_comment": "地球化学专业就业稳定，主要在地质勘查和环境保护领域！",
        "yearly_courses": {"大一": ["高等数学", "大学化学", "地球化学概论"], "大二": ["同位素地球化学", "环境地球化学", "矿物学"], "大三": ["勘查地球化学", "岩石地球化学"], "大四": ["地质队/环保部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "中国地质大学", "西北大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "070902",
        "name": "生物技术",
        "category": "07 理学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "生物技术专业培养掌握生物技术理论和方法的专门人才，能在生物医药企业、农业企业等从事生物技术研发和应用工作。",
        "what_you_learn": "微生物学、生物化学、分子生物学、细胞生物学、基因工程、蛋白质工程",
        "suitable_for": "对生物技术感兴趣，实验动手能力强的学生。",
        "career_outlook": "生物医药企业、农业科技企业、科研机构等。",
        "xuefeng_comment": "生物技术专业就业好，是国家重点发展领域！建议继续深造。",
        "yearly_courses": {"大一": ["高等数学", "大学化学", "生物化学"], "大二": ["微生物学", "分子生物学", "细胞生物学"], "大三": ["基因工程", "蛋白质工程", "发酵工程"], "大四": ["生物企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "上海交通大学"], "international": ["哈佛大学", "麻省理工学院"]}
    },
    {
        "code": "071102",
        "name": "应用心理学",
        "category": "07 理学",
        "category_icon": "🧠",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "应用心理学专业培养掌握应用心理学理论和方法的专门人才，能在心理咨询机构、企业人力资源部门等从事心理服务和管理工作。",
        "what_you_learn": "普通心理学、发展心理学、实验心理学、心理咨询与治疗、人力资源管理心理学",
        "suitable_for": "对心理学应用感兴趣，善于沟通的学生。",
        "career_outlook": "心理咨询机构、企业HR部门、学校心理咨询中心、医院心理科等。",
        "xuefeng_comment": "应用心理学专业就业好，随着心理健康意识提高，需求越来越大！",
        "yearly_courses": {"大一": ["普通心理学", "实验心理学", "发展心理学"], "大二": ["心理咨询与治疗", "心理测量学", "社会心理学"], "大三": ["人力资源管理心理学", "临床心理学"], "大四": ["心理咨询机构/企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "北京大学", "浙江大学"], "international": ["哈佛大学", "斯坦福大学"]}
    }
]

count = 0
skipped = 0

print("开始补充教育学、历史学、理学类专业...")
print("="*60)

for major in majors:
    ok, code = import_major(major)
    if ok:
        print(f"✅ {major['code']} - {major['name']}")
        count += 1
    elif code == 409:
        print(f"⏭️ {major['code']} - {major['name']} (已存在)")
        skipped += 1
    else:
        print(f"❌ {major['code']} - {major['name']}")
    time.sleep(0.3)

print("="*60)
print(f"✅ 成功添加 {count} 个专业")
print(f"⏭️ 跳过 {skipped} 个(已存在)")
