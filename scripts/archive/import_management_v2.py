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

management_majors = [
    {
        "code": "120207",
        "name": "审计学",
        "category": "12 管理学",
        "category_icon": "🔍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "审计学是研究审计理论和方法的专业，培养从事财务审计、内部审计和政府审计的专业人才。",
        "what_you_learn": "财务会计、审计学原理、财务审计、内部审计、政府审计、审计软件应用、风险管理",
        "suitable_for": "细心、严谨、有职业道德、对财务工作感兴趣的学生。",
        "career_outlook": "企业合规要求提高，审计人才需求稳定。就业在会计师事务所、企业内审部门、审计署等。",
        "xuefeng_comment": "审计学是会计类专业的重要方向，就业主要在会计师事务所、企业内审部门、审计机关等。这个专业需要细心、严谨、有职业道德，工作压力适中。就业稳定，薪资水平中等偏上。可以考取注册会计师CPA、审计师等证书。建议有财务基础、对审计工作有兴趣的同学报考。女生比较适合，工作相对稳定。审计工作对于维护社会经济秩序有重要作用。",
        "yearly_courses": {"大一": ["会计学原理", "管理学原理", "经济学原理", "法学基础"], "大二": ["财务会计", "成本会计", "审计学原理", "财务管理"], "大三": ["财务审计", "内部审计", "政府审计", "审计软件应用"], "大四": ["审计实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京审计大学", "上海财经大学", "中山大学", "厦门大学", "东北财经大学"], "international": ["London School of Economics", "NYU Stern", "University of Chicago Booth", "Harvard"]}
    },
    {
        "code": "120209",
        "name": "物业管理",
        "category": "12 管理学",
        "category_icon": "🏢",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "物业管理是研究物业服务企业经营和管理的专业，培养从事物业管理和服务的高级专门人才。",
        "what_you_learn": "物业管理概论、物业设施设备管理、物业法规、物业企业经营管理、房地产经营管理、社区服务管理",
        "suitable_for": "沟通能力强、服务意识好、对房地产和社区服务感兴趣的学生。",
        "career_outlook": "房地产和物业行业发展，物业管理人才需求增长。就业在物业管理公司、房地产企业、社区服务机构等。",
        "xuefeng_comment": "物业管理是管理类专业中比较实用的方向，就业主要在物业管理公司、房地产企业、社区服务机构等。这个专业工作相对稳定，但起步薪资可能不高，需要有耐心。可以考取物业管理师资格证。建议沟通能力强、服务意识好的同学报考。男生女生都适合。随着物业服务行业的发展，这个专业的需求在增长。",
        "yearly_courses": {"大一": ["管理学原理", "物业管理概论", "房地产经济学", "物业法规"], "大二": ["物业设施设备管理", "物业企业经营管理", "房地产经营管理", "社区服务管理"], "大三": ["物业经营管理实务", "物业服务质量管理", "物业管理信息系统"], "大四": ["物业管理实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "中国人民大学", "南京审计大学"], "international": ["MIT", "Harvard", "Stanford", "LBS"]}
    },
    {
        "code": "120208",
        "name": "资产评估",
        "category": "12 管理学",
        "category_icon": "💎",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "资产评估是对各类资产进行价值评估的专业，培养从事资产评估和房地产估价的专业人才。",
        "what_you_learn": "资产评估原理、企业价值评估、房地产估价、无形资产评估、机电设备评估、资产评估实务",
        "suitable_for": "细心严谨、有财务基础、对资产价值评估感兴趣的学生。",
        "career_outlook": "产权交易和投资活动增多，资产评估需求增长。就业在评估事务所、银行、房地产企业等。",
        "xuefeng_comment": "资产评估是一个有特色的管理类专业，就业主要在评估事务所、房地产估价公司、银行、法院等。这个专业需要财务和工程技术知识，工作专业性较强。可以考取资产评估师、房地产估价师等证书。建议有财务基础、对评估工作有兴趣的同学报考。就业相对稳定。",
        "yearly_courses": {"大一": ["会计学原理", "管理学原理", "经济学原理", "法学基础"], "大二": ["资产评估原理", "房地产估价", "企业价值评估", "无形资产评估"], "大三": ["机电设备评估", "资产评估实务", "建筑构造与识图", "财务报告分析"], "大四": ["评估事务所实习"]},
        "top_universities": {"domestic": ["上海财经大学", "中央财经大学", "厦门大学", "东北财经大学", "南京审计大学"], "international": ["London School of Economics", "NYU Stern", "University of Chicago", "Columbia"]}
    },
    {
        "code": "120210",
        "name": "文化产业管理",
        "category": "12 管理学",
        "category_icon": "🎭",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "文化产业管理是研究文化产业发展和运营管理的专业，培养从事文化产业经营管理的复合型人才。",
        "what_you_learn": "文化产业概论、文化产业政策、文化项目策划与运营、文化市场营销、文化创意产业、博物馆管理",
        "suitable_for": "对文化产业有兴趣、有创意、沟通能力强的学生。",
        "career_outlook": "文化产业发展迅速，文创人才需求增长。就业在文化企业、博物馆、美术馆、演出机构等。",
        "xuefeng_comment": "文化产业管理是新兴的管理类专业，就业主要在文化企业、博物馆、美术馆、演出机构、广告公司等。这个专业需要有文化素养和创意能力，工作相对有趣。可以考取文化经纪人等证书。建议对文化产业有兴趣、有创意的同学报考。薪资水平中等，但工作环境较好。",
        "yearly_courses": {"大一": ["管理学原理", "文化产业概论", "文化经济学", "艺术基础"], "大二": ["文化产业政策", "文化项目策划与运营", "文化市场营销", "文化创意产业"], "大三": ["博物馆管理", "演艺经纪", "文化遗产保护", "数字文化产业"], "大四": ["文化产业实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "北京大学", "清华大学", "上海交通大学", "南京大学"], "international": ["NYU Tisch", "Columbia", "USC", "London Arts"]}
    },
    {
        "code": "120211",
        "name": "劳动与社会保障",
        "category": "12 管理学",
        "category_icon": "🛡️",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "劳动与社会保障是研究社会保险、劳动关系和就业保障的专业，培养从事人力资源和社会保障管理的专门人才。",
        "what_you_learn": "劳动经济学、社会保障概论、社会保险、人力资源管理、劳动关系、劳动合同法",
        "suitable_for": "对社会保障和劳动关系感兴趣、沟通能力强的学生。",
        "career_outlook": "社会保障体系完善，人力资源和社保人才需求稳定。就业在政府部门、人力资源公司、企业HR等。",
        "xuefeng_comment": "劳动与社会保障是比较稳定的管理类专业，就业主要在政府社会保障部门、人力资源公司、企业人力资源部门等。这个专业考公务员很有优势，工作稳定。可以考取人力资源管理师、劳动关系协调员等证书。建议想从事稳定工作的同学报考。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "劳动经济学", "社会学基础"], "大二": ["社会保障概论", "社会保险", "人力资源管理", "劳动关系"], "大三": ["劳动合同法", "就业管理", "社会保障基金管理", "劳动争议处理"], "大四": ["政府部门或企业实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "南京大学", "浙江大学"], "international": ["Harvard", "LSE", "Oxford", "Cambridge"]}
    },
    {
        "code": "120212",
        "name": "体育经济与管理",
        "category": "12 管理学",
        "category_icon": "⚽",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "体育经济与管理是研究体育产业运营和管理的专业，培养从事体育产业经营管理的复合型人才。",
        "what_you_learn": "体育经济学、体育管理学、体育产业运营、体育市场营销、赛事管理、体育经纪人",
        "suitable_for": "对体育产业有兴趣、有商业头脑、沟通能力强的学生。",
        "career_outlook": "体育产业蓬勃发展，体育经营管理人才需求增长。就业在体育俱乐部、赛事公司、体育用品企业等。",
        "xuefeng_comment": "体育经济与管理是新兴的交叉学科专业，就业主要在体育俱乐部、赛事公司、体育用品企业、体育媒体等。这个专业需要既懂体育又懂管理，工作相对有趣。可以考取体育经纪人等证书。建议对体育产业有兴趣、有商业头脑的同学报考。薪资水平中等，但发展空间大。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "体育概论", "体育经济学"], "大二": ["体育管理学", "体育产业运营", "体育市场营销", "运动项目基础"], "大三": ["赛事管理", "体育经纪人", "体育法律", "数字体育"], "大四": ["体育机构实习"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育学院", "北京师范大学", "复旦大学", "上海交通大学"], "international": ["University of Michigan", "Columbia", "NYU", "USC"]}
    },
    {
        "code": "120213",
        "name": "海事管理",
        "category": "12 管理学",
        "category_icon": "🚢",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "海事管理是研究水上交通和港口运营管理的专业，培养从事航运和港口管理的专门人才。",
        "what_you_learn": "航海概论、海事管理、港口运营管理、航运管理、海商法、国际航运政策、水上交通安全管理",
        "suitable_for": "对航运和港口管理有兴趣、愿意从事水上交通相关工作的学生。",
        "career_outlook": "航运业和港口物流发展，海事管理人才需求稳定。就业在港航企业、海事局、航道局等。",
        "xuefeng_comment": "海事管理是比较特色的管理类专业，就业主要在港航企业、海事局、航道局、引航站等。这个专业有一定行业特色，需要学习航海和航运知识。男生比较适合，部分岗位可能需要出海或值夜班。就业稳定，薪资在管理类专业中属于中等偏上。",
        "yearly_courses": {"大一": ["管理学原理", "航海概论", "经济学原理", "海商法基础"], "大二": ["海事管理", "港口运营管理", "航运管理", "物流管理基础"], "大三": ["水上交通安全管理", "国际航运政策", "港口规划", "航道工程"], "大四": ["港航企业实习"]},
        "top_universities": {"domestic": ["大连海事大学", "上海海事大学", "武汉理工大学", "集美大学", "宁波大学"], "international": ["MIT", "World Maritime University", "Imperial College London", "University of Southampton"]}
    },
    {
        "code": "120214",
        "name": "公共关系学",
        "category": "12 管理学",
        "category_icon": "📣",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "公共关系学是研究组织形象塑造和传播管理的专业，培养从事公关传播和品牌管理的专门人才。",
        "what_you_learn": "公共关系原理、危机公关、品牌管理、媒体关系、广告学、传播学、社交媒体运营",
        "suitable_for": "沟通能力强、有创意、善于表达的学社。",
        "career_outlook": "企业品牌意识增强，公关人才需求增长。就业在公关公司、企业公关部门、媒体等。",
        "xuefeng_comment": "公共关系学是很有特色的管理类专业，就业主要在公关公司、企业公关部门、媒体宣传部、政府新闻部门等。这个专业需要沟通能力强、有创意、善于表达。可以考取公关员等证书。建议性格开朗、有创意的同学报考。薪资水平中等，但发展空间大。",
        "yearly_courses": {"大一": ["管理学原理", "传播学概论", "公共关系原理", "广告学基础"], "大二": ["危机公关", "品牌管理", "媒体关系", "写作基础"], "大三": ["社交媒体运营", "企业传播", "公共关系案例", "舆情分析"], "大四": ["公关公司或企业实习"]},
        "top_universities": {"domestic": ["中山大学", "复旦大学", "上海外国语大学", "中国传媒大学", "华南理工大学"], "international": ["NYU", "USC Annenberg", "LSE", "Columbia Journalism"]}
    },
    {
        "code": "120215",
        "name": "保密管理",
        "category": "12 管理学",
        "category_icon": "🔒",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "保密管理是研究国家秘密和商业秘密保护的专业，培养从事保密管理和信息安全管理的专门人才。",
        "what_you_learn": "保密管理概论、保密法规、信息安全、保密技术、商业秘密保护、保密监督检查",
        "suitable_for": "政治素质高、保密意识强、对信息安全管理感兴趣的学生。",
        "career_outlook": "保密工作日益重要，保密管理人才需求增长。就业在国家安全部门、保密局、企业保密部门等。",
        "xuefeng_comment": "保密管理是特殊的专业方向，就业主要在国家安全部门、保密局、政府机关、军队、大型企业的保密部门等。这个专业需要政治素质高、保密意识强。就业稳定，但有一定行业门槛。可以考取保密师等证书。建议政治可靠、有志从事保密工作的同学报考。",
        "yearly_courses": {"大一": ["管理学原理", "保密管理概论", "法学基础", "信息安全基础"], "大二": ["保密法规", "商业秘密保护", "保密技术", "保密史"], "大三": ["保密监督检查", "保密案例分析", "信息安全保密", "密码学基础"], "大四": ["保密部门实习"]},
        "top_universities": {"domestic": ["北京交通大学", "北京电子科技学院", "复旦大学", "上海交通大学", "南京大学"], "international": ["Johns Hopkins", "Carnegie Mellon", "MIT", "Stanford"]}
    },
    {
        "code": "120216",
        "name": "大数据管理与应用",
        "category": "12 管理学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥14k-35k",
        "overview": "大数据管理与应用是研究大数据采集、存储、分析和应用的交叉学科，培养从事数据管理和数据应用的专业人才。",
        "what_you_learn": "大数据概论、数据采集与处理、数据存储与管理、数据分析与挖掘、大数据可视化、数据治理",
        "suitable_for": "对大数据和数据分析感兴趣、有较好数学和计算机基础的学生。",
        "career_outlook": "数据时代，大数据人才需求爆发。就业在互联网公司、金融机构、咨询公司等。",
        "xuefeng_comment": "大数据管理与应用是新兴热门专业，就业在互联网公司、金融机构、咨询公司、政府部门等。这个专业需要数学和计算机基础，对数据敏感。就业前景非常好，薪资水平高。可以考取数据分析师等证书。建议对大数据有兴趣的同学报考。读研深造可以有更好的发展。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "Python编程", "数据库基础"], "大二": ["大数据概论", "数据采集与处理", "数据存储与管理", "统计学基础"], "大三": ["数据分析与挖掘", "大数据可视化", "数据治理", "机器学习基础"], "大四": ["企业实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "中国人民大学", "上海交通大学"], "international": ["MIT", "Stanford", "Carnegie Mellon", "UC Berkeley"]}
    },
    {
        "code": "120217",
        "name": "供应链管理",
        "category": "12 管理学",
        "category_icon": "📦",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "供应链管理是研究产品从供应商到消费者的全流程管理的专业，培养从事供应链优化和运营管理的专门人才。",
        "what_you_learn": "供应链管理、采购管理、仓储管理、物流管理、运营管理、供应链金融、供应链信息系统",
        "suitable_for": "逻辑思维强、对供应链和物流感兴趣的学生。",
        "career_outlook": "电商和物流行业发展，供应链管理人才需求增长。就业在电商平台、物流企业、制造业等。",
        "xuefeng_comment": "供应链管理是很有前景的管理类专业，就业在电商平台、物流企业、制造业、零售企业等。这个专业涉及采购、生产、物流、销售等多个环节，需要较强逻辑思维。可以考取供应链管理师等证书。建议对供应链和物流有兴趣的同学报考。就业前景好，薪资水平中等偏上。",
        "yearly_courses": {"大一": ["管理学原理", "运筹学", "经济学原理", "物流学基础"], "大二": ["供应链管理", "采购管理", "仓储管理", "生产运营管理"], "大三": ["物流管理", "供应链金融", "供应链信息系统", "供应链风险管理"], "大四": ["供应链企业实习"]},
        "top_universities": {"domestic": ["浙江大学", "复旦大学", "上海交通大学", "中山大学", "厦门大学"], "international": ["MIT", "Michigan Ross", "Warwick", "Kellogg", "INSEAD"]}
    },
    {
        "code": "120218",
        "name": "农林经济管理",
        "category": "12 管理学",
        "category_icon": "🌾",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "农林经济管理是研究农业和林业经济运行规律的专业，培养从事农业经济管理和农村发展的专门人才。",
        "what_you_learn": "农业经济学、林业经济学、农村社会学、农业政策学、农产品营销、农业技术经济学",
        "suitable_for": "对农业经济和农村发展有兴趣的学生。",
        "career_outlook": "乡村振兴战略实施，农林经济人才需求增长。就业在农业部门、农村发展机构、农业企业等。",
        "xuefeng_comment": "农林经济管理是比较有特色的管理类专业，就业在农业部门、农村发展机构、农业企业、农产品贸易公司等。这个专业需要了解农业和农村特点。建议对农业经济和农村发展有兴趣的同学报考。可以考公务员，农业部门、林业局等是不错的选择。工作稳定，但薪资水平一般。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "农学概论", "社会学基础"], "大二": ["农业经济学", "林业经济学", "农村社会学", "农业政策学"], "大三": ["农产品营销", "农业技术经济学", "农村发展规划", "农产品贸易"], "大四": ["农业部门或企业实习"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "浙江大学", "华中农业大学", "西北农林科技大学"], "international": ["Cornell", "Wageningen", "UC Davis", "Reading"]}
    },
    {
        "code": "120219",
        "name": "劳动关系管理",
        "category": "12 管理学",
        "category_icon": "🤝",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "劳动关系管理是研究企业劳动关系和劳动争议处理的专业，培养从事人力资源和劳动关系协调的专门人才。",
        "what_you_learn": "劳动关系学、劳动经济学、劳动法学、劳动合同管理、劳动争议处理、员工关系管理、集体谈判",
        "suitable_for": "沟通能力强、对劳动关系和劳动法感兴趣的学生。",
        "career_outlook": "劳动关系日益复杂，劳动关系人才需求增长。就业在企业HR部门、劳动仲裁机构、工会等。",
        "xuefeng_comment": "劳动关系管理是很有实用价值的管理类专业，就业在企业人力资源部门、劳动仲裁机构、工会组织等。这个专业需要熟悉劳动法律法规，沟通协调能力强。可以考取劳动关系协调员等证书。建议对劳动关系和劳动法有兴趣的同学报考。就业稳定，工作有挑战性。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "劳动经济学", "法学基础"], "大二": ["劳动关系学", "劳动法学", "劳动合同管理", "人力资源管理"], "大三": ["劳动争议处理", "员工关系管理", "集体谈判", "社会保险"], "大四": ["劳动仲裁机构或企业实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "上海交通大学", "华东师范大学"], "international": ["ILR School Cornell", "LSE", "Oxford", "Harvard"]}
    },
    {
        "code": "120220",
        "name": "邮政管理",
        "category": "12 管理学",
        "category_icon": "📮",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "邮政管理是研究邮政和快递运营管理的专业，培养从事邮政和快递企业管理的专门人才。",
        "what_you_learn": "邮政管理、快递运营管理、物流管理、邮政业务管理、邮政网络规划、邮政法规",
        "suitable_for": "对邮政和快递行业有兴趣、愿意从事运营管理工作的学生。",
        "career_outlook": "快递行业发展迅速，邮政管理人才需求稳定。就业在邮政集团、快递公司、物流企业等。",
        "xuefeng_comment": "邮政管理是特色管理类专业，就业在邮政集团、快递公司、物流企业等。这个专业有一定行业特色，但就业面相对较窄。建议对邮政和快递行业有兴趣的同学报考。工作稳定，但薪资水平一般。可以向物流管理方向发展。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "物流学基础", "邮政概论"], "大二": ["邮政管理", "快递运营管理", "邮政业务管理", "市场营销"], "大三": ["邮政网络规划", "物流信息系统", "邮政法规", "供应链管理"], "大四": ["邮政或快递企业实习"]},
        "top_universities": {"domestic": ["北京邮电大学", "南京邮电大学", "重庆邮电大学", "西安邮电大学", "北京交通大学"], "international": ["MIT", "Georgia Tech", "Michigan", "Penn State"]}
    },
    {
        "code": "120221",
        "name": "航空服务艺术与管理",
        "category": "12 管理学",
        "category_icon": "✈️",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "航空服务艺术与管理是研究航空服务运营和管理的专业，培养从事航空服务管理和空中服务的专门人才。",
        "what_you_learn": "航空服务概论、航空服务礼仪、航空运营管理、航空法律法规、跨文化交际、航空英语",
        "suitable_for": "形象气质好、沟通能力强、对航空服务有兴趣的学生。",
        "career_outlook": "民航业发展，航空服务人才需求增长。就业在航空公司、机场、高端服务业等。",
        "xuefeng_comment": "航空服务艺术与管理是特色管理类专业，就业在航空公司、机场、高端服务业等。这个专业对形象气质有一定要求，需要良好的沟通能力。女生比较适合。可以成为空乘人员或航空服务管理人员。薪资水平中等偏高，工作环境较好。",
        "yearly_courses": {"大一": ["管理学原理", "航空服务概论", "航空服务礼仪", "航空英语"], "大二": ["航空运营管理", "航空法律法规", "跨文化交际", "服务心理学"], "大三": ["航空服务管理", "机场运营管理", "航空市场营销", "民航概论"], "大四": ["航空公司或机场实习"]},
        "top_universities": {"domestic": ["北京航空航天大学", "南京航空航天大学", "中国民航大学", "上海工程技术大学", "广州民航职业技术学院"], "international": ["Embry-Riddle", "Purdue", "Cranfield", "Hong Kong PolyU"]}
    }
]

def main():
    print("=" * 70)
    print("📊 开始导入管理学新专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in management_majors:
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
