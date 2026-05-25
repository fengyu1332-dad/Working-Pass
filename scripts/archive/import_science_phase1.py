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
        return False, e.code

science_majors = [
    {
        "code": "070201",
        "name": "天文学",
        "category": "07 理学",
        "category_icon": "🌟",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "天文学是研究天体和宇宙的学科，培养从事天文学研究和教学的专门人才。",
        "what_you_learn": "天文学概论、天体物理学、天体力学、天体测量学、天体物理观测、宇宙学、星际介质与恒星物理、星系天文学",
        "suitable_for": "对天文学和天体物理感兴趣的学生。",
        "career_outlook": "天文研究领域，就业在天文台、科研院所、高校、航天部门等。",
        "xuefeng_comment": "天文学是天文学类的专业，研究天体和宇宙。就业在天文台、科研院所、高校、航天部门。这个专业需要对天文学和天体物理有兴趣，对物理和数学要求高。适合有科研能力强的学生。就业面相对窄但很稳定。读研比例非常高。",
        "yearly_courses": {"大一": ["天文学概论", "高等数学", "力学", "热学"], "大二": ["电磁学", "光学", "原子物理", "天文学导论"], "大三": ["天体物理学", "天体力学", "天体测量学", "天体物理观测技术"], "大四": ["宇宙学", "星系天文学", "宇宙天体物理", "天文台实习"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "北京师范大学", "中国科学技术大学", "南京大学"], "international": ["Caltech", "MIT", "Berkeley", "Princeton", "Harvard"]}
    },
    {
        "code": "070601",
        "name": "大气科学",
        "category": "07 理学",
        "category_icon": "🌤️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "大气科学是研究大气的学科，培养从事气象预报和研究的专门人才。",
        "what_you_learn": "大气科学概论、大气探测、天气学原理、动力气象学、天气诊断分析、大气物理学、大气化学、气象统计",
        "suitable_for": "对大气科学和气象感兴趣的学生。",
        "career_outlook": "气象领域，就业在气象局、民航、科研院所、高校等。",
        "xuefeng_comment": "大气科学是地球物理学类的专业，研究大气。就业在气象局、民航、科研院所、高校。这个专业需要对大气科学和气象有兴趣，对物理和数学要求较高。适合对自然现象感兴趣的学生。就业稳定，考公务员有优势。",
        "yearly_courses": {"大一": ["大气科学概论", "高等数学", "力学", "热学"], "大二": ["大气探测", "大气物理学", "大气探测"], "大三": ["天气学原理", "动力气象学", "天气诊断分析"], "大四": ["气象统计", "中尺度天气学", "短期天气预报", "气象局实习"]},
        "top_universities": {"domestic": ["南京大学", "北京大学", "南京信息工程大学", "中山大学", "中国海洋大学"], "international": ["MIT", "Berkeley", "Stanford", "Cambridge"]}
    },
    {
        "code": "070602",
        "name": "应用气象学",
        "category": "07 理学",
        "category_icon": "⛈️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "应用气象学是应用气象知识解决实际问题的学科，培养从事应用气象工作的专门人才。",
        "what_you_learn": "大气科学概论、天气学原理、动力气象学、应用气象学、气象服务、人工影响天气、专业气象预报、气象灾害防御",
        "suitable_for": "对应用气象工作感兴趣的学生。",
        "career_outlook": "气象服务领域，就业在气象局、民航、农业部门、企业等。",
        "xuefeng_comment": "应用气象学是地球物理学类的专业，应用气象知识。就业在气象局、民航、农业部门、企业。这个专业需要对应用气象工作有兴趣。适合对气象应用感兴趣的学生。就业稳定，考公务员有优势。",
        "yearly_courses": {"大一": ["大气科学概论", "高等数学", "力学", "热学"], "大二": ["天气学原理", "动力气象学", "天气诊断分析"], "大三": ["应用气象学", "气象服务", "人工影响天气"], "大四": ["专业气象预报", "气象灾害防御", "气象局或企业实习"]},
        "top_universities": {"domestic": ["南京信息工程大学", "南京大学", "中国农业大学", "中山大学", "成都信息工程大学"], "international": ["MIT", "Berkeley", "Stanford", "Cambridge"]}
    },
    {
        "code": "070701",
        "name": "海洋科学",
        "category": "07 理学",
        "category_icon": "🌊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "海洋科学是研究海洋的学科，培养从事海洋科学研究和海洋管理的专门人才。",
        "what_you_learn": "海洋科学导论、物理海洋学、海洋化学、海洋生物学、海洋地质、海洋技术、海洋资源管理",
        "suitable_for": "对海洋科学感兴趣的学生。",
        "career_outlook": "海洋领域，就业在海洋局、科研院所、高校、海洋企业等。",
        "xuefeng_comment": "海洋科学是海洋科学类的专业，研究海洋。就业在海洋局、科研院所、高校、海洋企业。这个专业需要对海洋科学有兴趣。适合对海洋有兴趣的学生。就业稳定，海洋强国战略下发展前景好。",
        "yearly_courses": {"大一": ["海洋科学导论", "高等数学", "普通化学", "普通物理"], "大二": ["物理海洋学", "海洋化学", "海洋生物学"], "大三": ["海洋地质", "海洋技术", "海洋资源管理"], "大四": ["海洋调查实习", "海洋局或科研院所实习"]},
        "top_universities": {"domestic": ["中国海洋大学", "厦门大学", "同济大学", "中山大学", "青岛海洋大学"], "international": ["Woods Hole", "Scripps", "MIT", "Berkeley"]}
    },
    {
        "code": "070801",
        "name": "地球物理学",
        "category": "07 理学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "地球物理学是研究地球物理的学科，培养从事地球物理研究和勘探的专门人才。",
        "what_you_learn": "地球物理学概论、地震学、地磁学、地电学、重力学、地震勘探、电法勘探",
        "suitable_for": "对地球物理感兴趣的学生。",
        "career_outlook": "地矿勘探领域，就业在地质局、地震局、石油公司、科研院所等。",
        "xuefeng_comment": "地球物理学是地球物理学类的专业，研究地球物理。就业在地质局、地震局、石油公司、科研院所。这个专业需要对地球物理有兴趣，对物理和数学要求较高。就业稳定。考公务员有优势。",
        "yearly_courses": {"大一": ["地球物理学概论", "高等数学", "力学", "热学"], "大二": ["电磁学", "地震学", "地磁学"], "大三": ["地电学", "重力学", "地震勘探"], "大四": ["电法勘探", "物探综合实习", "地质局或科研院所实习"]},
        "top_universities": {"domestic": ["中国科学技术大学", "北京大学", "清华大学", "中国地质大学", "武汉大学"], "international": ["MIT", "Berkeley", "Stanford", "Cambridge"]}
    },
    {
        "code": "070901",
        "name": "地质学",
        "category": "07 理学",
        "category_icon": "🪨",
        "difficulty": "⭐⭐",
        "salary_range": "¥10k-24k",
        "overview": "地质学是研究地球的学科，培养从事地质研究和勘探的专门人才。",
        "what_you_learn": "地质学概论、普通地质学、岩石学、矿物学、构造地质学、地层古生物学、矿床学",
        "suitable_for": "对地质学感兴趣的学生。",
        "career_outlook": "地矿勘探领域，就业在地质局、矿产企业、科研院所等。",
        "xuefeng_comment": "地质学是地质学类的专业，研究地球。就业在地质局、矿产企业、科研院所。这个专业需要对地质学有兴趣，需要野外工作。适合能吃苦的学生。就业稳定。考公务员有优势。",
        "yearly_courses": {"大一": ["地质学概论", "普通地质学", "高等数学", "普通化学"], "大二": ["岩石学", "矿物学", "构造地质学"], "大三": ["地层古生物学", "矿床学", "构造地质学"], "大四": ["野外地质实习", "地质填图实习", "地质局或矿产企业实习"]},
        "top_universities": {"domestic": ["中国地质大学", "北京大学", "南京大学", "西北大学", "吉林大学"], "international": ["MIT", "Berkeley", "Stanford", "Cambridge"]}
    },
    {
        "code": "070902",
        "name": "地球化学",
        "category": "07 理学",
        "category_icon": "⚗️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-26k",
        "overview": "地球化学是研究地球化学的学科，培养从事地球化学研究和勘探的专门人才。",
        "what_you_learn": "地球化学、分析化学、有机化学、物理化学、地球化学、同位素地球化学、勘查地球化学",
        "suitable_for": "对地球化学感兴趣的学生。",
        "career_outlook": "地矿勘探领域，就业在地质局、矿产企业、科研院所等。",
        "xuefeng_comment": "地球化学是地质学类的专业，研究地球化学。就业在地质局、矿产企业、科研院所。这个专业需要对地球化学有兴趣，需要化学基础好。就业稳定。考公务员有优势。",
        "yearly_courses": {"大一": ["地球化学", "分析化学", "有机化学", "物理化学"], "大二": ["地球化学", "普通地质学", "矿物学"], "大三": ["岩石学", "矿床学", "同位素地球化学"], "大四": ["勘查地球化学", "野外实习", "地质局或科研院所实习"]},
        "top_universities": {"domestic": ["中国地质大学", "中国科学技术大学", "北京大学", "南京大学", "吉林大学"], "international": ["MIT", "Berkeley", "Stanford", "Cambridge"]}
    },
    {
        "code": "071001",
        "name": "生物科学",
        "category": "07 理学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "生物科学是研究生命现象的学科，培养从事生物科学研究和教学的专门人才。",
        "what_you_learn": "动物学、植物学、微生物学、生物化学、细胞生物学、遗传学、分子生物学、生态学",
        "suitable_for": "对生物科学感兴趣的学生。",
        "career_outlook": "生物研究领域，就业在科研院所、高校、生物公司、医药企业等。",
        "xuefeng_comment": "生物科学是生物科学类的专业，研究生命现象。就业在科研院所、高校、生物公司、医药企业。这个专业需要对生物科学有兴趣。适合喜欢做实验的学生。就业前景好，但读研比例非常高。",
        "yearly_courses": {"大一": ["动物学", "植物学", "微生物学", "生物化学"], "大二": ["细胞生物学", "遗传学", "分子生物学", "普通物理"], "大三": ["生物化学", "分子生物学", "生态学"], "大四": ["生物信息学", "发育生物学", "科研实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "上海交通大学", "武汉大学"], "international": ["Harvard", "MIT", "Stanford", "Cambridge"]}
    },
    {
        "code": "071002",
        "name": "生物技术",
        "category": "07 理学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "生物技术是应用生物科学的学科，培养从事生物技术研究和开发的专门人才。",
        "what_you_learn": "生物化学、分子生物学、微生物学、生物工程、细胞工程、基因工程、生物制药",
        "suitable_for": "对生物技术感兴趣的学生。",
        "career_outlook": "生物技术领域，就业在生物公司、医药企业、科研院所、高校等。",
        "xuefeng_comment": "生物技术是生物科学类的专业，应用生物科学。就业在生物公司、医药企业、科研院所、高校。这个专业需要对生物技术有兴趣，喜欢做实验。就业前景好，读研比例高。",
        "yearly_courses": {"大一": ["生物化学", "微生物学", "有机化学", "物理化学"], "大二": ["分子生物学", "细胞生物学", "微生物学"], "大三": ["生物工程", "细胞工程", "基因工程"], "大四": ["生物制药", "发酵工程", "生物公司或科研院所实习"]},
        "top_universities": {"domestic": ["复旦大学", "北京大学", "清华大学", "上海交通大学", "武汉大学"], "international": ["MIT", "Stanford", "Berkeley", "Cambridge"]}
    },
    {
        "code": "071003",
        "name": "生物信息学",
        "category": "07 理学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥14k-36k",
        "overview": "生物信息学是生物学和计算机科学结合的学科，培养从事生物信息研究和分析的专门人才。",
        "what_you_learn": "生物化学、分子生物学、计算机科学、统计学、生物信息学、基因组学、蛋白质组学、生物信息软件",
        "suitable_for": "对生物信息学感兴趣的学生。",
        "career_outlook": "生物信息领域，就业在生物公司、医药企业、科研院所、高校等。",
        "xuefeng_comment": "生物信息学是生物科学类的专业，生物学和计算机科学结合。就业在生物公司、医药企业、科研院所、高校。这个专业需要对生物信息学有兴趣，需要生物、计算机、数学都好。就业前景非常好，薪资高。读研比例高。",
        "yearly_courses": {"大一": ["生物化学", "分子生物学", "计算机科学", "统计学"], "大二": ["生物信息学", "基因组学", "分子生物学"], "大三": ["蛋白质组学", "生物信息软件", "编程"], "大四": ["生物信息算法", "系统生物学", "生物公司或科研院所实习"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "复旦大学", "上海交通大学", "华中科技大学"], "international": ["MIT", "Stanford", "Berkeley", "Cambridge"]}
    },
    {
        "code": "071101",
        "name": "心理学",
        "category": "07 理学",
        "category_icon": "🧠",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "心理学是研究心理现象的学科，培养从事心理学研究和应用的专门人才。",
        "what_you_learn": "普通心理学、实验心理学、心理统计学、心理测量学、发展心理学、人格心理学、社会心理学",
        "suitable_for": "对心理学感兴趣的学生。",
        "career_outlook": "心理学领域，就业在心理咨询机构、学校、医院、企业等。",
        "xuefeng_comment": "心理学是心理学类的专业，研究心理现象。就业在心理咨询机构、学校、医院、企业。这个专业需要对心理学有兴趣，有同理心。就业前景好，适合有心理咨询师需求增长。读研比例高。",
        "yearly_courses": {"大一": ["普通心理学", "实验心理学", "心理统计学", "普通心理学"], "大二": ["发展心理学", "人格心理学", "社会心理学"], "大三": ["临床心理学", "心理测量学", "心理咨询"], "大四": ["应用心理学", "心理咨询实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "北京大学", "西南大学", "浙江大学"], "international": ["Harvard", "Stanford", "Berkeley", "Cambridge"]}
    },
    {
        "code": "071102",
        "name": "应用心理学",
        "category": "07 理学",
        "category_icon": "💭",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "应用心理学是应用心理学知识的学科，培养从事心理学应用的专门人才。",
        "what_you_learn": "普通心理学、实验心理学、心理统计学、心理测量学、应用心理学、心理咨询、人力资源管理",
        "suitable_for": "对应用心理学感兴趣的学生。",
        "career_outlook": "心理学应用领域，就业在心理咨询机构、学校、企业、医院等。",
        "xuefeng_comment": "应用心理学是心理学类的专业，应用心理学知识。就业在心理咨询机构、学校、企业、医院。这个专业需要对应用心理学有兴趣，有同理心。就业前景好，适合有做心理咨询或企业人力资源管理兴趣的学生。",
        "yearly_courses": {"大一": ["普通心理学", "实验心理学", "心理统计学", "心理学"], "大二": ["应用心理学", "心理咨询", "社会心理学"], "大三": ["人力资源管理", "心理咨询", "心理测量学"], "大四": ["应用心理学实习", "心理咨询实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "北京大学", "西南大学", "浙江大学"], "international": ["Harvard", "Stanford", "Berkeley", "Cambridge"]}
    },
    {
        "code": "071201",
        "name": "统计学",
        "category": "07 理学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-32k",
        "overview": "统计学是研究统计方法的学科，培养从事统计工作和数据分析的专门人才。",
        "what_you_learn": "统计学、概率论、数理统计、应用统计、多元统计分析、时间序列分析、统计软件、抽样技术",
        "suitable_for": "对统计学和数据分析感兴趣的学生。",
        "career_outlook": "统计分析领域，就业在统计局、金融机构、企业、科研院所等。",
        "xuefeng_comment": "统计学是统计学类的专业，研究统计方法。就业在统计局、金融机构、企业、科研院所。这个专业需要对统计学和数据分析有兴趣，数学基础好。就业前景非常好，薪资高。",
        "yearly_courses": {"大一": ["统计学", "概率论", "数理统计", "高等数学"], "大二": ["应用统计", "多元统计分析", "时间序列分析"], "大三": ["统计软件", "抽样技术", "统计预测与决策"], "大四": ["应用统计学", "统计实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "上海财经大学", "华东师范大学"], "international": ["MIT", "Stanford", "Berkeley", "Cambridge"]}
    },
    {
        "code": "071202",
        "name": "应用统计学",
        "category": "07 理学",
        "category_icon": "📈",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-32k",
        "overview": "应用统计学是应用统计方法的学科，培养从事统计应用的专门人才。",
        "what_you_learn": "统计学、概率论、数理统计、应用统计、多元统计分析、时间序列分析、统计软件、抽样技术",
        "suitable_for": "对应用统计学和数据分析感兴趣的学生。",
        "career_outlook": "统计应用领域，就业在金融机构、企业、政府部门等。",
        "xuefeng_comment": "应用统计学是统计学类的专业，应用统计方法。就业在金融机构、企业、政府部门。这个专业需要对应用统计学和数据分析有兴趣，数学基础好。就业前景非常好，薪资高。",
        "yearly_courses": {"大一": ["统计学", "概率论", "数理统计", "高等数学"], "大二": ["应用统计", "多元统计分析", "时间序列分析"], "大三": ["统计软件", "抽样技术", "统计预测"], "大四": ["应用统计学", "统计实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "上海财经大学", "华东师范大学"], "international": ["MIT", "Stanford", "Berkeley", "Cambridge"]}
    }
]

def main():
    print("=" * 70)
    print("🔬 开始导入理学类专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in science_majors:
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
