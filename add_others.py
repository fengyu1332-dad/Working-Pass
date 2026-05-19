
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
        "code": "040101K",
        "name": "教育学",
        "category": "04 教育学",
        "category_icon": "📚",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "教育学专业培养掌握教育科学基本理论和知识的人才，能在教育行政部门、学校等从事教育工作。",
        "what_you_learn": "教育学原理、教育心理学、课程与教学论、中国教育史、外国教育史",
        "suitable_for": "对教育事业有热情，喜欢和孩子或年轻人打交道的学生。",
        "career_outlook": "中小学教师、教育行政部门、培训机构等，需求稳定。",
        "xuefeng_comment": "教育学专业适合想做老师的同学，就业稳定，假期多，社会认可度高！",
        "yearly_courses": {"大一": ["教育学原理", "普通心理学", "中国教育史", "外国教育史"], "大二": ["教育心理学", "课程与教学论", "德育原理"], "大三": ["教育社会学", "教育研究方法", "教育管理学"], "大四": ["教育实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "南京师范大学", "西南大学"], "international": ["哥伦比亚大学", "斯坦福大学"]}
    },
    {
        "code": "040102K",
        "name": "学前教育",
        "category": "04 教育学",
        "category_icon": "🎨",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "学前教育专业培养掌握学前教育知识的人才，能在幼儿园等从事幼教工作。",
        "what_you_learn": "学前教育学、学前儿童发展心理学、学前儿童卫生学、幼儿园课程与教学",
        "suitable_for": "喜欢和小朋友在一起，有耐心，有才艺的学生。",
        "career_outlook": "幼儿园、幼教机构等，幼儿教师缺口很大！",
        "xuefeng_comment": "学前教育专业就业非常好，幼儿园老师缺口很大，工作环境单纯，非常适合有爱心的同学！",
        "yearly_courses": {"大一": ["学前教育学", "学前儿童发展心理学", "美术基础", "音乐基础"], "大二": ["学前儿童卫生学", "幼儿园课程与教学", "舞蹈"], "大三": ["学前儿童语言教育", "学前儿童数学教育", "学前儿童科学教育"], "大四": ["幼儿园实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "南京师范大学", "浙江师范大学"], "international": ["哥伦比亚大学"]}
    },
    {
        "code": "040104K",
        "name": "体育教育",
        "category": "04 教育学",
        "category_icon": "⚽",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-14k",
        "overview": "体育教育专业培养掌握体育教育知识的人才，能在学校等从事体育教学和训练工作。",
        "what_you_learn": "运动解剖学、运动生理学、体育心理学、学校体育学、运动训练学",
        "suitable_for": "热爱体育运动，身体条件好的学生。",
        "career_outlook": "中小学体育老师、健身教练等，需求稳定。",
        "xuefeng_comment": "体育教育专业适合热爱运动的同学，当体育老师工作相对轻松，假期多！",
        "yearly_courses": {"大一": ["运动解剖学", "运动生理学", "体育心理学", "田径"], "大二": ["学校体育学", "运动训练学", "篮球", "足球"], "大三": ["运动保健学", "体育管理学", "羽毛球"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育大学", "武汉体育学院", "华南师范大学"], "international": ["春田学院"]}
    },
    {
        "code": "050301T",
        "name": "新闻学",
        "category": "05 文学",
        "category_icon": "📰",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "新闻学专业培养掌握新闻知识的人才，能在媒体等从事新闻工作。",
        "what_you_learn": "新闻学概论、传播学概论、新闻采访、新闻写作、新闻编辑",
        "suitable_for": "对新闻工作感兴趣，文笔好，善于沟通的学生。",
        "career_outlook": "传统媒体、新媒体、企事业单位宣传部门等，就业面广。",
        "xuefeng_comment": "新闻学专业就业面广，传统媒体、新媒体都能去，适合文笔好的同学！",
        "yearly_courses": {"大一": ["新闻学概论", "传播学概论", "中国新闻史", "外国新闻史"], "大二": ["新闻采访", "新闻写作", "新闻编辑", "新闻摄影"], "大三": ["新闻评论", "广播电视新闻", "媒介经营与管理"], "大四": ["媒体实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "复旦大学", "中国传媒大学", "武汉大学"], "international": ["哥伦比亚大学", "伦敦政经学院"]}
    },
    {
        "code": "120201T",
        "name": "工商管理",
        "category": "12 管理学",
        "category_icon": "💼",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "工商管理专业培养掌握管理知识的人才，能在企业等从事管理工作。",
        "what_you_learn": "管理学原理、微观经济学、宏观经济学、市场营销、人力资源管理",
        "suitable_for": "对管理工作感兴趣，沟通组织能力强的学生。",
        "career_outlook": "企业管理、人力资源、市场营销等，就业面广。",
        "xuefeng_comment": "工商管理专业就业面广，但竞争也激烈，建议多实习，积累经验！",
        "yearly_courses": {"大一": ["管理学原理", "微观经济学", "宏观经济学", "高等数学"], "大二": ["市场营销学", "会计学原理", "财务管理", "统计学"], "大三": ["人力资源管理", "生产运作管理", "企业战略管理"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "清华大学", "上海交通大学", "复旦大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "120202T",
        "name": "市场营销",
        "category": "12 管理学",
        "category_icon": "🛒",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "市场营销专业培养掌握营销知识的人才，能在企业等从事营销工作。",
        "what_you_learn": "市场营销学、消费者行为学、市场调研、营销策划、广告学",
        "suitable_for": "对营销工作感兴趣，善于沟通，思维活跃的学生。",
        "career_outlook": "企业营销部门、广告公司等，需求大。",
        "xuefeng_comment": "市场营销专业就业好，市场需求大，适合善于沟通的同学！",
        "yearly_courses": {"大一": ["市场营销学", "微观经济学", "宏观经济学", "高等数学"], "大二": ["消费者行为学", "市场调研", "统计学", "会计学"], "大三": ["营销策划", "广告学", "品牌管理", "网络营销"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "上海交通大学"], "international": ["西北大学", "沃顿商学院"]}
    },
    {
        "code": "120203T",
        "name": "会计学",
        "category": "12 管理学",
        "category_icon": "📊",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "会计学专业培养掌握会计知识的人才，能在企业、银行等从事会计工作。",
        "what_you_learn": "会计学原理、中级财务会计、高级财务会计、成本会计、审计学",
        "suitable_for": "细心，有耐心，对数字敏感的学生。",
        "career_outlook": "企业财务部门、会计师事务所、银行等，需求非常稳定！",
        "xuefeng_comment": "会计学专业就业非常稳定，企业、银行、事务所都需要，适合细心的同学！",
        "yearly_courses": {"大一": ["高等数学", "微观经济学", "会计学原理", "经济法"], "大二": ["中级财务会计", "成本会计", "税法", "统计学"], "大三": ["高级财务会计", "审计学", "财务管理", "管理会计"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "厦门大学", "上海财经大学", "中央财经大学"], "international": ["芝加哥大学", "宾夕法尼亚大学"]}
    },
    {
        "code": "120204T",
        "name": "财务管理",
        "category": "12 管理学",
        "category_icon": "💰",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "财务管理专业培养掌握财务管理知识的人才，能在企业、银行等从事财务工作。",
        "what_you_learn": "会计学原理、财务管理、财务分析、投资学、公司理财",
        "suitable_for": "对财务工作感兴趣，细心，对数字敏感的学生。",
        "career_outlook": "企业财务部门、银行、证券等，需求稳定。",
        "xuefeng_comment": "财务管理专业就业好，企业、银行都需要，适合细心的同学！",
        "yearly_courses": {"大一": ["高等数学", "微观经济学", "宏观经济学", "会计学原理"], "大二": ["财务管理", "中级财务会计", "税法", "统计学"], "大三": ["高级财务会计", "财务分析", "投资学", "公司理财"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["上海财经大学", "西南财经大学", "中国人民大学", "中央财经大学"], "international": ["沃顿商学院", "芝加哥大学"]}
    },
    {
        "code": "130201T",
        "name": "音乐表演",
        "category": "13 艺术学",
        "category_icon": "🎵",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-20k",
        "overview": "音乐表演专业培养掌握音乐表演技能的人才，能在文艺团体等从事表演工作。",
        "what_you_learn": "专业主科、视唱练耳、乐理、中西方音乐史、和声",
        "suitable_for": "有音乐特长，热爱表演的学生。",
        "career_outlook": "文艺团体、培训学校等，就业面广。",
        "xuefeng_comment": "音乐表演专业适合有音乐特长的同学，就业面广，还可以自己开班！",
        "yearly_courses": {"大一": ["专业主科", "视唱练耳", "乐理", "中国音乐史"], "大二": ["专业主科", "和声", "西方音乐史", "曲式分析"], "大三": ["专业主科", "室内乐", "艺术实践"], "大四": ["毕业音乐会", "毕业论文"]},
        "top_universities": {"domestic": ["中央音乐学院", "上海音乐学院", "中国音乐学院", "星海音乐学院"], "international": ["茱莉亚学院", "柯蒂斯音乐学院"]}
    },
    {
        "code": "130501T",
        "name": "设计学类",
        "category": "13 艺术学",
        "category_icon": "🎨",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "设计学类专业培养掌握设计知识的人才，能在设计公司等从事设计工作。",
        "what_you_learn": "设计素描、设计色彩、构成设计、设计史、计算机辅助设计",
        "suitable_for": "对设计感兴趣，有美术基础，创新能力强的学生。",
        "career_outlook": "设计公司、互联网公司、企业设计部门等，需求大！",
        "xuefeng_comment": "设计学类专业就业好，互联网公司、设计公司都需要，适合喜欢创意的同学！",
        "yearly_courses": {"大一": ["设计素描", "设计色彩", "平面构成", "色彩构成"], "大二": ["立体构成", "设计史", "计算机辅助设计"], "大三": ["专业设计", "设计方法学", "设计心理学"], "大四": ["设计公司实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学美术学院", "中央美术学院", "中国美术学院", "同济大学"], "international": ["罗德岛设计学院", "帕森斯设计学院"]}
    },
    {
        "code": "130502T",
        "name": "视觉传达设计",
        "category": "13 艺术学",
        "category_icon": "🖼️",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "视觉传达设计专业培养掌握视觉设计知识的人才，能在设计公司等从事设计工作。",
        "what_you_learn": "平面设计、标志设计、包装设计、书籍设计、广告设计",
        "suitable_for": "对视觉设计感兴趣，有美术基础的学生。",
        "career_outlook": "设计公司、互联网公司、广告公司等，需求大！",
        "xuefeng_comment": "视觉传达设计专业就业好，互联网公司、广告公司都需要！",
        "yearly_courses": {"大一": ["设计素描", "设计色彩", "平面构成", "色彩构成"], "大二": ["立体构成", "设计史", "计算机辅助设计", "图形设计"], "大三": ["标志设计", "包装设计", "书籍设计", "广告设计"], "大四": ["设计公司实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学美术学院", "中央美术学院", "中国美术学院", "广州美术学院"], "international": ["罗德岛设计学院", "中央圣马丁艺术与设计学院"]}
    },
    {
        "code": "130503T",
        "name": "环境设计",
        "category": "13 艺术学",
        "category_icon": "🏘️",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "环境设计专业培养掌握环境设计知识的人才，能在设计公司等从事设计工作。",
        "what_you_learn": "室内设计、景观设计、建筑初步、设计制图、材料与构造",
        "suitable_for": "对环境设计感兴趣，有美术基础的学生。",
        "career_outlook": "建筑设计公司、房地产公司等，需求大！",
        "xuefeng_comment": "环境设计专业就业好，房地产、装修公司都需要！",
        "yearly_courses": {"大一": ["设计素描", "设计色彩", "平面构成", "色彩构成"], "大二": ["立体构成", "设计史", "建筑初步", "设计制图"], "大三": ["室内设计", "景观设计", "材料与构造"], "大四": ["设计公司实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学美术学院", "中央美术学院", "中国美术学院", "同济大学"], "international": ["罗德岛设计学院", "帕森斯设计学院"]}
    },
    {
        "code": "030101K",
        "name": "法学",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-20k",
        "overview": "法学专业培养掌握法律知识的人才，能在律师事务所、法院等从事法律工作。",
        "what_you_learn": "法理学、宪法、民法、刑法、民事诉讼法、刑事诉讼法",
        "suitable_for": "对法律工作感兴趣，记忆力好，逻辑能力强的学生。",
        "career_outlook": "律师、法官、检察官、企业法务等，需要通过法考。",
        "xuefeng_comment": "法学专业就业好，但需要通过法考，适合记忆力好的同学！",
        "yearly_courses": {"大一": ["法理学", "宪法", "中国法制史", "民法总论"], "大二": ["民法分论", "刑法总论", "刑法分论", "民事诉讼法"], "大三": ["刑事诉讼法", "行政法与行政诉讼法", "经济法", "商法"], "大四": ["律所实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民大学", "中国政法大学", "北京大学", "华东政法大学"], "international": ["哈佛大学法学院", "耶鲁大学法学院"]}
    },
    {
        "code": "070101T",
        "name": "数学与应用数学",
        "category": "07 理学",
        "category_icon": "📐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "数学与应用数学专业培养掌握数学知识的人才，能在学校、企业等从事相关工作。",
        "what_you_learn": "数学分析、高等代数、解析几何、常微分方程、概率论与数理统计",
        "suitable_for": "对数学感兴趣，逻辑思维强的学生。",
        "career_outlook": "教师、数据分析、金融等，就业面广。",
        "xuefeng_comment": "数学专业就业面广，当老师、做数据分析、金融都可以，非常推荐！",
        "yearly_courses": {"大一": ["数学分析", "高等代数", "解析几何", "普通物理"], "大二": ["常微分方程", "概率论", "数理统计", "复变函数"], "大三": ["实变函数", "泛函分析", "数值分析", "数学模型"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "中国科学技术大学", "清华大学"], "international": ["普林斯顿大学", "哈佛大学"]}
    },
    {
        "code": "070201T",
        "name": "物理学",
        "category": "07 理学",
        "category_icon": "⚛️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "物理学专业培养掌握物理知识的人才，能在学校、科研院所等从事相关工作。",
        "what_you_learn": "普通物理、理论力学、热力学与统计物理、电动力学、量子力学",
        "suitable_for": "对物理感兴趣，逻辑思维强的学生。",
        "career_outlook": "教师、科研、半导体等，就业面广。",
        "xuefeng_comment": "物理学专业适合深造，读研后发展好，也可以转半导体、金融等领域！",
        "yearly_courses": {"大一": ["高等数学", "力学", "热学", "电磁学"], "大二": ["光学", "原子物理学", "理论力学", "数学物理方法"], "大三": ["热力学与统计物理", "电动力学", "量子力学"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "中国科学技术大学", "复旦大学"], "international": ["麻省理工学院", "加州理工学院"]}
    },
    {
        "code": "070301T",
        "name": "化学",
        "category": "07 理学",
        "category_icon": "🧪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "化学专业培养掌握化学知识的人才，能在学校、化工企业等从事相关工作。",
        "what_you_learn": "无机化学、有机化学、分析化学、物理化学、结构化学",
        "suitable_for": "对化学感兴趣，动手能力强的学生。",
        "career_outlook": "教师、化工、制药等，需求稳定。",
        "xuefeng_comment": "化学专业就业稳定，化工、制药都需要，适合喜欢做实验的同学！",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["物理化学", "仪器分析", "化工原理"], "大三": ["结构化学", "有机合成", "物理化学实验"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "中国科学技术大学", "复旦大学"], "international": ["加州大学伯克利分校", "麻省理工学院"]}
    },
    {
        "code": "080701T",
        "name": "电子信息工程",
        "category": "08 工学",
        "category_icon": "📱",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "电子信息工程专业培养掌握电子信息知识的工程师，能在IT企业等从事相关工作。",
        "what_you_learn": "电路分析、模拟电子技术、数字电子技术、信号与系统、通信原理",
        "suitable_for": "对电子和通信感兴趣，动手能力强的学生。",
        "career_outlook": "IT企业、通信公司等，就业非常好！",
        "xuefeng_comment": "电子信息工程专业就业非常好，IT企业、通信公司都需要，适合喜欢编程和电子的同学！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "电路分析"], "大二": ["模拟电子技术", "数字电子技术", "信号与系统", "C语言"], "大三": ["通信原理", "数字信号处理", "单片机原理", "嵌入式系统"], "大四": ["IT企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["电子科技大学", "西安电子科技大学", "清华大学", "北京邮电大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "082502T",
        "name": "环境工程",
        "category": "08 工学",
        "category_icon": "🌱",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "环境工程专业培养掌握环境工程知识的工程师，能在环保企业等从事相关工作。",
        "what_you_learn": "水污染控制工程、大气污染控制工程、固体废物处理工程、环境监测",
        "suitable_for": "对环保感兴趣的学生。",
        "career_outlook": "环保企业、市政等，需求稳定。",
        "xuefeng_comment": "环境工程专业就业稳定，环保行业受重视，前景好！",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "工程制图"], "大二": ["物理化学", "水力学", "环境监测"], "大三": ["水污染控制工程", "大气污染控制工程", "固体废物处理工程"], "大四": ["环保企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "同济大学", "哈尔滨工业大学", "浙江大学"], "international": ["斯坦福大学", "加州大学伯克利分校"]}
    },
    {
        "code": "080601T",
        "name": "电气工程及其自动化",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "电气工程及其自动化专业培养掌握电气工程知识的工程师，能在电力企业等从事相关工作。",
        "what_you_learn": "电路分析、电机学、电力系统分析、电力电子技术、自动控制原理",
        "suitable_for": "对电气感兴趣的学生。",
        "career_outlook": "电力公司、电气企业等，就业非常稳定！",
        "xuefeng_comment": "电气工程专业就业非常稳定，国家电网、发电厂都是好去处，非常推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "电路分析"], "大二": ["模拟电子技术", "数字电子技术", "电机学", "自动控制原理"], "大三": ["电力系统分析", "电力电子技术", "继电保护"], "大四": ["电力企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "西安交通大学", "华中科技大学", "浙江大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "081001T",
        "name": "土木工程",
        "category": "08 工学",
        "category_icon": "🏗️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "土木工程专业培养掌握土木工程知识的工程师，能在建筑企业等从事相关工作。",
        "what_you_learn": "材料力学、结构力学、土力学、混凝土结构设计、钢结构设计",
        "suitable_for": "对建筑感兴趣，动手能力强的学生。",
        "career_outlook": "建筑企业、设计院等，需求稳定。",
        "xuefeng_comment": "土木工程专业就业稳定，建筑、房地产都需要，但初期可能辛苦！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "材料力学"], "大二": ["结构力学", "土力学", "测量学"], "大三": ["混凝土结构设计", "钢结构设计", "土木工程施工"], "大四": ["建筑企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["同济大学", "清华大学", "哈尔滨工业大学", "东南大学"], "international": ["麻省理工学院", "加州大学伯克利分校"]}
    },
    {
        "code": "081101T",
        "name": "化学工程与工艺",
        "category": "08 工学",
        "category_icon": "🏭",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "化学工程与工艺专业培养掌握化工知识的工程师，能在化工企业等从事相关工作。",
        "what_you_learn": "化工原理、化工热力学、化学反应工程、化工工艺学",
        "suitable_for": "对化工感兴趣的学生。",
        "career_outlook": "化工企业、制药等，需求稳定。",
        "xuefeng_comment": "化学工程与工艺专业就业稳定，化工、制药都需要！",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "工程制图"], "大二": ["物理化学", "化工原理", "化工热力学"], "大三": ["化学反应工程", "化工工艺学", "化工设计"], "大四": ["化工企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["天津大学", "华东理工大学", "北京化工大学", "大连理工大学"], "international": ["麻省理工学院", "加州大学伯克利分校"]}
    },
    {
        "code": "090101T",
        "name": "农学",
        "category": "09 农学",
        "category_icon": "🌾",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "农学专业培养掌握农学知识的人才，能在农业企业等从事相关工作。",
        "what_you_learn": "植物学、植物生理学、生物化学、遗传学、作物栽培学",
        "suitable_for": "对农业感兴趣的学生。",
        "career_outlook": "农业企业、农科院等，需求稳定。",
        "xuefeng_comment": "农学专业就业稳定，国家重视农业，前景好！",
        "yearly_courses": {"大一": ["高等数学", "植物学", "有机化学", "无机化学"], "大二": ["植物生理学", "生物化学", "遗传学", "土壤学"], "大三": ["作物栽培学", "作物育种学", "植物保护学"], "大四": ["农业企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "浙江大学", "华中农业大学"], "international": ["康奈尔大学", "加州大学戴维斯分校"]}
    },
    {
        "code": "101101T",
        "name": "护理学",
        "category": "10 医学",
        "category_icon": "👩⚕️",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "护理学专业培养掌握护理知识的人才，能在医院从事护理工作。",
        "what_you_learn": "护理学基础、内科护理学、外科护理学、妇产科护理学、儿科护理学",
        "suitable_for": "对护理工作感兴趣，有耐心，有爱心的学生。",
        "career_outlook": "医院、诊所等，护士缺口很大！",
        "xuefeng_comment": "护理学专业就业非常好，护士缺口很大，工作稳定，但辛苦！",
        "yearly_courses": {"大一": ["人体解剖学", "生理学", "生物化学", "护理学基础"], "大二": ["病理学", "药理学", "健康评估"], "大三": ["内科护理学", "外科护理学", "妇产科护理学"], "大四": ["医院实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京协和医学院", "复旦大学上海医学院", "上海交通大学医学院", "北京大学医学部"], "international": ["约翰霍普金斯大学", "宾夕法尼亚大学"]}
    },
    {
        "code": "100102K",
        "name": "生物医学",
        "category": "10 医学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "生物医学专业培养掌握生物医学知识的人才，能在科研院所、药企等从事相关工作。",
        "what_you_learn": "人体解剖学、生理学、生物化学、分子生物学、细胞生物学",
        "suitable_for": "对生物医学感兴趣的学生。",
        "career_outlook": "科研院所、药企、医院等，前景好！",
        "xuefeng_comment": "生物医学专业前景好，适合深造读研读博！",
        "yearly_courses": {"大一": ["高等数学", "普通化学", "有机化学", "生物化学"], "大二": ["生理学", "生物化学", "分子生物学", "细胞生物学"], "大三": ["生理学实验", "生物化学实验", "分子生物学实验"], "大四": ["科研机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "上海交通大学", "复旦大学"], "international": ["哈佛大学", "麻省理工学院"]}
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
