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

more_majors = [
    # 法学专业
    {
        "code": "030305T",
        "name": "老年学",
        "category": "03 法学",
        "category_icon": "👴",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "老年学是研究老龄化问题和老年服务的学科，培养从事老龄化研究和老年服务管理的专业人才。",
        "what_you_learn": "老年学概论、老年社会学、老年心理学、老年医学基础、养老服务管理、老年政策",
        "suitable_for": "对老年服务和老龄化问题感兴趣的学生。",
        "career_outlook": "老龄化社会，老年服务人才需求增长。就业在养老机构、社区服务中心等。",
        "xuefeng_comment": "老年学是新兴专业，随着老龄化加剧需求增长。就业在养老机构、社区服务、政府老龄部门等。工作稳定，适合有爱心的同学。",
        "yearly_courses": {"大一": ["社会学概论", "老年学概论", "心理学基础", "管理学原理"], "大二": ["老年社会学", "老年心理学", "老年医学基础", "老年护理"], "大三": ["养老服务管理", "老年政策", "老年经济学", "长期照护"], "大四": ["养老机构实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "华东师范大学", "南开大学"], "international": ["Oxford", "LSE", "Harvard", "UCL"]}
    },
    {
        "code": "030401",
        "name": "社会学",
        "category": "03 法学",
        "category_icon": "👥",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "社会学是研究社会结构和社会运行规律的社会科学，培养从事社会研究和公共管理的人才。",
        "what_you_learn": "社会学概论、社会学理论、社会研究方法、社会统计学、社会分层、社会问题",
        "suitable_for": "关注社会问题、对社会研究感兴趣的学生。",
        "career_outlook": "社会研究需求稳定。就业在政府研究部门、咨询公司、NGO等。",
        "xuefeng_comment": "社会学是比较传统的人文社科专业，就业在政府研究部门、咨询公司、NGO、媒体等。这个专业需要关注社会问题，有一定社会责任感。读研比例高。就业相对稳定。",
        "yearly_courses": {"大一": ["社会学概论", "社会学理论", "社会研究方法", "统计学"], "大二": ["社会分层", "社会问题", "社会心理学", "政治社会学"], "大三": ["经济社会学", "人口学", "城市社会学", "农村社会学"], "大四": ["研究机构或政府实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "南京大学", "清华大学"], "international": ["Harvard", "Oxford", "Cambridge", "LSE", "Stanford"]}
    },
    # 文学专业
    {
        "code": "050208T",
        "name": "翻译",
        "category": "05 文学",
        "category_icon": "🌐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "翻译是研究语言转换和跨文化交际的专业，培养从事口译和笔译的专业人才。",
        "what_you_learn": "基础英语、高级英语、翻译概论、口译基础、笔译实务、跨文化交际",
        "suitable_for": "英语好、语言天赋强、对翻译感兴趣的学生。",
        "career_outlook": "国际交流增多，翻译人才需求稳定。就业在翻译公司、外事部门、企业等。",
        "xuefeng_comment": "翻译是英语类专业的重要方向，就业在翻译公司、外事部门、企业国际部等。这个专业需要英语好、语言天赋强。可以考取CATTI翻译证书。读译硕有利于发展。薪资水平中等。",
        "yearly_courses": {"大一": ["基础英语", "高级英语", "英语听力", "英语口语"], "大二": ["翻译概论", "口译基础", "笔译实务", "跨文化交际"], "大三": ["同声传译", "文学翻译", "商务翻译", "科技翻译"], "大四": ["翻译公司或外事部门实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "广东外语外贸大学", "北京大学", "复旦大学"], "international": ["MIT", "Monterey", "Bath", "Leeds"]}
    },
    {
        "code": "050306T",
        "name": "国际新闻与传播",
        "category": "05 文学",
        "category_icon": "📺",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-23k",
        "overview": "国际新闻与传播是研究国际新闻报道和跨文化传播的专业，培养从事国际新闻工作的专门人才。",
        "what_you_learn": "新闻学概论、传播学、国际新闻报道、英语新闻写作、跨文化传播、媒介素养",
        "suitable_for": "英语好、沟通能力强、对国际新闻感兴趣的学生。",
        "career_outlook": "国际交流增多，国际新闻人才需求增长。就业在媒体、跨国公司、政府外宣部门等。",
        "xuefeng_comment": "国际新闻与传播是新闻学类专业的重要方向，就业在媒体国际部、跨国公司、政府外宣部门等。这个专业需要英语好、沟通能力强。就业稳定，薪资中等。读研可以提高竞争力。",
        "yearly_courses": {"大一": ["新闻学概论", "传播学概论", "英语精读", "新闻英语"], "大二": ["国际新闻报道", "英语新闻写作", "跨文化传播", "新闻摄影"], "大三": ["国际传播", "媒介素养", "全球媒体", "国际关系基础"], "大四": ["国际媒体或涉外机构实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "北京外国语大学", "上海外国语大学", "中国人民大学", "复旦大学"], "international": ["Columbia", "USC Annenberg", "LSE", "NYU"]}
    },
    # 历史学专业
    {
        "code": "060106T",
        "name": "文化遗产",
        "category": "06 历史学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "文化遗产是研究文化遗产保护与利用的专业，培养从事文化遗产保护和管理工作的专门人才。",
        "what_you_learn": "文化遗产概论、文化遗产保护、文物鉴定、博物馆学、考古学基础、文化遗产法规",
        "suitable_for": "对历史和文化遗产感兴趣的学生。",
        "career_outlook": "文化遗产保护受重视，相关人才需求稳定。就业在博物馆、文保单位、文化部门等。",
        "xuefeng_comment": "文化遗产是特色专业，就业在博物馆、文物考古机构、文化部门等。这个专业需要热爱历史和文化遗产。可以考公务员。就业稳定，工作环境好。",
        "yearly_courses": {"大一": ["历史学概论", "考古学概论", "博物馆学概论", "文物学基础"], "大二": ["文化遗产概论", "文化遗产保护", "文物鉴定", "文化遗产法规"], "大三": ["博物馆管理", "文化遗产利用", "文物保护技术", "非遗保护"], "大四": ["博物馆或文保单位实习"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "浙江大学", "四川大学"], "international": ["Oxford", "Cambridge", "UCL", "Edinburgh"]}
    },
    # 教育学专业
    {
        "code": "040108T",
        "name": "科学教育",
        "category": "04 教育学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "科学教育是培养中小学科学教师的师范专业，研究科学技术教育的方法和理论。",
        "what_you_learn": "科学教育学、普通物理学、普通化学、普通生物学、地球科学、科学实验教学",
        "suitable_for": "热爱科学、喜欢教育工作的学生。",
        "career_outlook": "科学教育受重视，科学教师需求稳定。就业在中小学、科普机构等。",
        "xuefeng_comment": "科学教育是师范类专业，就业在中小学担任科学教师或科普机构工作。这个专业需要各学科基础知识。可以考取教师资格证。就业稳定，工作稳定。",
        "yearly_courses": {"大一": ["教育学原理", "普通物理学", "普通化学", "普通生物学"], "大二": ["科学教育学", "地球科学", "科学实验技术", "科学技术史"], "大三": ["科学课程与教学", "科学探究", "科技制作", "科学教育研究方法"], "大四": ["中小学实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "华中师范大学", "东北师范大学", "陕西师范大学"], "international": ["Harvard", "Oxford", "Stanford", "Cambridge"]}
    },
    {
        "code": "040109T",
        "name": "汉语言",
        "category": "04 教育学",
        "category_icon": "📚",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "汉语言主要研究汉语语言现象和规律，培养从事语言研究和语文教学的专业人才。",
        "what_you_learn": "现代汉语、古代汉语、语言学概论、汉语语法学、汉语词汇学、文字学",
        "suitable_for": "对语言和文字感兴趣的学生。",
        "career_outlook": "中文教育需求稳定。就业在高校、中学、出版机构等。",
        "xuefeng_comment": "汉语言是语言学类专业，就业在高校、中学、出版机构等。这个专业需要热爱语言文字。读研比例高，可以成为语言学专家或语文教师。",
        "yearly_courses": {"大一": ["现代汉语", "古代汉语", "语言学概论", "文学概论"], "大二": ["汉语语法学", "汉语词汇学", "文字学", "音韵学"], "大三": ["汉语方言学", "社会语言学", "语言学史", "对外汉语教学概论"], "大四": ["中学或出版机构实习"]},
        "top_universities": {"domestic": ["北京大学", "北京师范大学", "复旦大学", "南京大学", "浙江大学"], "international": ["Oxford", "Cambridge", "Harvard", "MIT"]}
    },
    # 艺术学专业
    {
        "code": "130310T",
        "name": "影视摄影与制作",
        "category": "13 艺术学",
        "category_icon": "🎬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "影视摄影与制作是研究影视拍摄和后期制作的专业，培养从事电影电视创作的专业人才。",
        "what_you_learn": "摄影基础、影视摄像、影视剪辑、影视特效、调色、影视声音设计",
        "suitable_for": "对影视创作感兴趣、有艺术感觉的学生。",
        "career_outlook": "影视行业蓬勃发展，相关人才需求增长。就业在影视公司、电视台、网络平台等。",
        "xuefeng_comment": "影视摄影与制作是艺术类专业，就业在影视公司、电视台、网络平台等。这个专业需要艺术感觉和技术能力。就业竞争激烈，但收入可观。需要积累作品。",
        "yearly_courses": {"大一": ["摄影基础", "色彩学", "视觉艺术", "影视概论"], "大二": ["影视摄像", "影视剪辑", "影视声音", "导演基础"], "大三": ["影视特效", "调色", "纪录片创作", "短片创作"], "大四": ["影视公司实习"]},
        "top_universities": {"domestic": ["北京电影学院", "中国传媒大学", "上海戏剧学院", "浙江传媒学院", "中央戏剧学院"], "international": ["USC", "NYU Tisch", "AFI", "London Film School"]}
    },
    {
        "code": "130312T",
        "name": "艺术与科技",
        "category": "13 艺术学",
        "category_icon": "🎨",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "艺术与科技是艺术设计与数字技术结合的专业，培养从事数字艺术创作和科技艺术设计的专门人才。",
        "what_you_learn": "数字艺术设计、交互设计、虚拟现实艺术、增强现实艺术、新媒体艺术、数字媒体技术",
        "suitable_for": "对艺术和科技都有兴趣的学生。",
        "career_outlook": "数字艺术和科技艺术发展，人才需求增长。就业在互联网公司、游戏公司、展览设计等。",
        "xuefeng_comment": "艺术与科技是新兴交叉专业，就业在互联网公司、游戏公司、展览设计公司等。这个专业需要艺术感觉和科技能力。就业前景好，薪资水平较高。",
        "yearly_courses": {"大一": ["艺术概论", "设计基础", "数字媒体技术", "交互设计基础"], "大二": ["数字艺术设计", "虚拟现实艺术", "新媒体艺术", "用户体验设计"], "大三": ["增强现实艺术", "交互艺术创作", "科技艺术项目", "数字媒体专题"], "大四": ["科技公司或设计公司实习"]},
        "top_universities": {"domestic": ["中央美术学院", "中国美术学院", "清华大学", "上海美术学院", "广州美术学院"], "international": ["Royal College of Art", "Parsons", "RISD", "MIT Media Lab"]}
    },
    {
        "code": "130313T",
        "name": "舞蹈教育",
        "category": "13 艺术学",
        "category_icon": "💃",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "舞蹈教育是培养舞蹈教师和舞蹈教育研究者的师范专业，研究舞蹈教学的理论和方法。",
        "what_you_learn": "舞蹈基训、舞蹈编导、舞蹈教学法、舞蹈理论、舞蹈史、舞蹈解剖学",
        "suitable_for": "有舞蹈基础、热爱舞蹈教育事业的学生。",
        "career_outlook": "艺术教育受重视，舞蹈教师需求稳定。就业在舞蹈学校、中小学、培训机构等。",
        "xuefeng_comment": "舞蹈教育是艺术师范类专业，就业在舞蹈学校、中小学、培训机构等。这个专业需要有舞蹈基础。可以考取教师资格证。就业稳定，工作与爱好结合。",
        "yearly_courses": {"大一": ["舞蹈基训", "舞蹈编导基础", "舞蹈解剖学", "舞蹈理论"], "大二": ["舞蹈教学法", "中国舞蹈史", "外国舞蹈史", "舞蹈编导技法"], "大三": ["舞蹈教育学", "舞蹈创作", "舞蹈鉴赏", "舞蹈心理"], "大四": ["舞蹈学校或培训机构实习"]},
        "top_universities": {"domestic": ["北京舞蹈学院", "中央民族大学", "上海戏剧学院", "北京师范大学", "东北师范大学"], "international": ["Royal Academy of Dance", "Juilliard", "Trinity Laban", "RAM"]}
    },
    {
        "code": "130314T",
        "name": "流行音乐",
        "category": "13 艺术学",
        "category_icon": "🎤",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "流行音乐是研究流行音乐演唱、创作和制作的专业，培养从事流行音乐工作的专门人才。",
        "what_you_learn": "流行音乐演唱、声乐技巧、流行音乐理论、音乐制作、MIDI制作、录音技术",
        "suitable_for": "有音乐天赋、热爱流行音乐的学生。",
        "career_outlook": "音乐市场繁荣，流行音乐人才需求稳定。就业在唱片公司、演出机构、培训机构等。",
        "xuefeng_comment": "流行音乐是音乐类专业，就业在唱片公司、演出机构、培训机构等。这个专业需要有音乐天赋。就业竞争激烈，需要才华和机遇。可以成为歌手、音乐制作人、音乐教师等。",
        "yearly_courses": {"大一": ["声乐基础", "流行音乐概论", "音乐理论基础", "视唱练耳"], "大二": ["流行音乐演唱", "声乐技巧训练", "音乐制作基础", "MIDI制作"], "大三": ["录音技术", "音乐风格分析", "音乐商业", "原创音乐创作"], "大四": ["唱片公司或演出机构实习"]},
        "top_universities": {"domestic": ["上海音乐学院", "中央音乐学院", "四川音乐学院", "武汉音乐学院", "沈阳音乐学院"], "international": ["Berklee", "Juilliard", "Royal Academy of Music", "LACM"]}
    },
    {
        "code": "130315T",
        "name": "音乐教育",
        "category": "13 艺术学",
        "category_icon": "🎵",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "音乐教育是培养音乐教师的师范专业，研究音乐教学的理论和方法。",
        "what_you_learn": "声乐、钢琴、音乐教学法、和声学、曲式分析、音乐教育心理学",
        "suitable_for": "有音乐基础、热爱音乐教育事业的学生。",
        "career_outlook": "艺术教育受重视，音乐教师需求稳定。就业在中小学、音乐培训机构等。",
        "xuefeng_comment": "音乐教育是艺术师范类专业，就业在中小学、音乐培训机构等。这个专业需要有音乐基础。可以考取教师资格证。就业稳定，工作稳定有成就感。",
        "yearly_courses": {"大一": ["声乐", "钢琴", "音乐理论基础", "和声学"], "大二": ["曲式分析", "音乐教学法", "音乐教育心理学", "合唱与指挥"], "大三": ["音乐课程设计", "音乐教育研究方法", "奥尔夫音乐教学法", "达尔克罗兹教学法"], "大四": ["中小学实习"]},
        "top_universities": {"domestic": ["中央音乐学院", "上海音乐学院", "北京师范大学", "华东师范大学", "东北师范大学"], "international": ["Royal Academy of Music", "Juilliard", "Berklee", "Guildhall"]}
    },
    # 农学专业
    {
        "code": "090109T",
        "name": "设施农业科学与工程",
        "category": "09 农学",
        "category_icon": "🌿",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "设施农业科学与工程是研究设施农业技术和工程的专业，培养从事现代设施农业的高级人才。",
        "what_you_learn": "设施农业概论、温室设计与建造、农业设施环境调控、无土栽培技术、农业物联网、智能农业装备",
        "suitable_for": "对现代设施农业和农业工程感兴趣的学生。",
        "career_outlook": "设施农业发展，技术人才需求增长。就业在农业科技公司、农业园区等。",
        "xuefeng_comment": "设施农业是现代农业的重要方向，就业在农业科技公司、农业园区、智慧农业企业等。这个专业需要农业和工程知识。读研有利于发展。就业前景好。",
        "yearly_courses": {"大一": ["植物学", "工程力学", "设施农业概论", "气象学"], "大二": ["温室设计与建造", "农业设施环境调控", "作物栽培学", "灌溉排水工程"], "大三": ["无土栽培技术", "农业物联网", "智能农业装备", "设施农业经营管理"], "大四": ["农业科技企业实习"]},
        "top_universities": {"domestic": ["中国农业大学", "西北农林科技大学", "南京农业大学", "华中农业大学", "山东农业大学"], "international": ["Wageningen", "Cornell", "UC Davis", "Texas A&M"]}
    },
    {
        "code": "090403T",
        "name": "动物药学",
        "category": "09 农学",
        "category_icon": "💊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "动物药学是研究兽药研发和使用的专业，培养从事兽药研发、生产和使用的专门人才。",
        "what_you_learn": "兽医药理学、兽医学、动物生物化学、兽药制剂学、兽药分析、兽药法规",
        "suitable_for": "对动物药学感兴趣、有化学和生物学基础的学生。",
        "career_outlook": "兽药行业发展，技术人才需求稳定。就业在兽药企业、养殖场、动物医院等。",
        "xuefeng_comment": "动物药学是特色农学专业，就业在兽药企业、养殖场、动物医院、宠物医院等。这个专业需要化学和生物学基础。可以考取执业兽医师资格证。读研有利于发展。",
        "yearly_courses": {"大一": ["动物学", "动物解剖学", "普通化学", "有机化学"], "大二": ["动物生物化学", "兽医药理学", "兽医微生物学", "动物生理学"], "大三": ["兽药制剂学", "兽药分析", "兽药法规", "兽药生产技术"], "大四": ["兽药企业或动物医院实习"]},
        "top_universities": {"domestic": ["南京农业大学", "华中农业大学", "中国农业大学", "华南农业大学", "四川农业大学"], "international": ["Cornell", "UC Davis", "Texas A&M", "University of Edinburgh"]}
    },
    # 医学专业
    {
        "code": "100103T",
        "name": "海洋药学",
        "category": "10 医学",
        "category_icon": "🌊",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "海洋药学是研究海洋生物药用价值的学科，培养从事海洋药物研发的专门人才。",
        "what_you_learn": "海洋生物学、海洋药物化学、药理学、药物化学、海洋药物提取技术、天然药物化学",
        "suitable_for": "对海洋药物和生物制药感兴趣的学生。",
        "career_outlook": "海洋药物研发受重视，人才需求增长。就业在药物研发机构、海洋科研院所等。",
        "xuefeng_comment": "海洋药学是特色医学专业，就业在药物研发机构、海洋科研院所、生物制药公司等。这个专业需要化学和生物学基础。读研几乎是必然选择。就业前景好。",
        "yearly_courses": {"大一": ["海洋生物学", "普通化学", "有机化学", "生物化学"], "大二": ["海洋药物化学", "药理学", "药物化学", "微生物学"], "大三": ["海洋药物提取技术", "天然药物化学", "药物分析", "生物制药技术"], "大四": ["药物研发机构实习"]},
        "top_universities": {"domestic": ["中国海洋大学", "上海海洋大学", "厦门大学", "浙江大学", "复旦大学"], "international": ["Scripps", "Woods Hole", "UC San Diego", "University of Tokyo"]}
    }
]

def main():
    print("=" * 70)
    print("📖 开始导入其他学科专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in more_majors:
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
