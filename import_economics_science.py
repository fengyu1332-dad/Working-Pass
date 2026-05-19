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

# 经济学和理学专业
more_majors = [
    # 经济学专业
    {
        "code": "020308T",
        "name": "金融数学",
        "category": "02 经济学",
        "category_icon": "📈",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥14k-35k",
        "overview": "金融数学是应用数学方法解决金融问题的交叉学科，培养既有数学基础又有金融知识的复合型人才。",
        "what_you_learn": "数学分析、概率论、数理统计、金融工程、衍生品定价、随机过程、固定收益证券",
        "suitable_for": "数学基础扎实、对金融工程感兴趣的学生。",
        "career_outlook": "金融科技发展，金融数学人才需求增长。就业在证券公司、基金公司、银行等。",
        "xuefeng_comment": "金融数学是数学和金融的交叉学科，就业在证券公司、基金公司、银行、期货公司等。这个专业对数学要求很高，需要有较强的数学天赋。建议数学好的同学报考。读研深造比例很高。就业前景好，薪资水平高。",
        "yearly_courses": {"大一": ["数学分析", "高等代数", "政治经济学", "微观经济学"], "大二": ["概率论", "数理统计", "宏观经济学", "金融学"], "大三": ["金融工程", "衍生品定价", "随机过程", "固定收益证券"], "大四": ["金融机构实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "上海交通大学", "南开大学"], "international": ["Princeton", "MIT", "Stanford", "Oxford"]}
    },
    {
        "code": "020309T",
        "name": "经济统计学",
        "category": "02 经济学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "经济统计学是统计学在经济领域的应用，培养运用统计方法分析经济问题的专业人才。",
        "what_you_learn": "统计学、计量经济学、国民经济统计、时间序列分析、抽样技术、R语言",
        "suitable_for": "数学和统计学基础好、对经济分析感兴趣的学生。",
        "career_outlook": "数据时代，统计人才需求增长。就业在统计局、咨询公司、金融机构等。",
        "xuefeng_comment": "经济统计学是统计学和经济学的结合，就业在统计局、咨询公司、金融机构、市场调研公司等。这个专业需要统计学基础，实用性强。可以考取统计师等证书。就业前景好，薪资中等偏上。读研深造可以有更好发展。",
        "yearly_courses": {"大一": ["数学分析", "高等代数", "政治经济学", "微观经济学"], "大二": ["统计学", "概率论", "宏观经济学", "计量经济学"], "大三": ["国民经济统计", "时间序列分析", "抽样技术", "R语言"], "大四": ["统计局或咨询公司实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "厦门大学", "上海财经大学", "中央财经大学"], "international": ["Harvard", "MIT", "Stanford", "LSE"]}
    },
    {
        "code": "020310T",
        "name": "资源与环境经济学",
        "category": "02 经济学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "资源与环境经济学是研究资源利用和环境保护经济规律的专业，培养从事资源与环境管理的专业人才。",
        "what_you_learn": "资源经济学、环境经济学、生态经济学、资源管理、环境评估、可持续发展",
        "suitable_for": "对资源与环境问题感兴趣、关心可持续发展的学生。",
        "career_outlook": "环保意识增强，相关人才需求增长。就业在环保部门、研究机构、企业等。",
        "xuefeng_comment": "资源与环境经济学是特色经济学专业，就业在环保部门、研究机构、环境咨询公司等。这个专业需要了解环境和经济学知识。就业稳定，薪资中等。可以考公务员，环保部门是不错的选择。读研比例高。",
        "yearly_courses": {"大一": ["经济学原理", "高等数学", "环境科学概论", "资源学"], "大二": ["资源经济学", "环境经济学", "生态经济学", "环境管理"], "大三": ["资源管理", "环境评估", "可持续发展", "环境政策"], "大四": ["环保部门或研究机构实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "上海交通大学", "浙江大学"], "international": ["Oxford", "Cambridge", "LSE", "Yale"]}
    },
    {
        "code": "020401",
        "name": "贸易经济",
        "category": "02 经济学",
        "category_icon": "🌐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-23k",
        "overview": "贸易经济是研究国内贸易和国际贸易运行规律的专业，培养从事贸易经营和管理的专门人才。",
        "what_you_learn": "贸易经济学、国际贸易实务、国际结算、市场营销、跨境电商、贸易英语",
        "suitable_for": "沟通能力强、对贸易业务感兴趣的学生。",
        "career_outlook": "国际贸易发展，贸易人才需求稳定。就业在外贸公司、跨境电商企业等。",
        "xuefeng_comment": "贸易经济是实用经济学专业，就业在外贸公司、跨境电商企业、货代公司等。这个专业需要沟通能力和贸易知识。可以考取报关员、外销员等证书。就业稳定，薪资中等。读研可以提高竞争力。",
        "yearly_courses": {"大一": ["经济学原理", "高等数学", "市场营销", "贸易英语"], "大二": ["贸易经济学", "国际贸易实务", "国际结算", "商法"], "大三": ["跨境电商", "外贸函电", "国际物流", "商品学"], "大四": ["外贸企业实习"]},
        "top_universities": {"domestic": ["对外经济贸易大学", "上海财经大学", "中国人民大学", "南开大学", "厦门大学"], "international": ["LSE", "MIT", "Harvard", "Wharton"]}
    },
    {
        "code": "020402",
        "name": "国际商务",
        "category": "02 经济学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "国际商务是研究跨国经营活动和管理的专业，培养从事国际商务运营和管理的复合型人才。",
        "what_you_learn": "国际商务概论、国际贸易实务、国际市场营销、国际商法跨文化管理、国际商务谈判",
        "suitable_for": "英语好、沟通能力强、对国际商务有兴趣的学生。",
        "career_outlook": "全球化深入，国际商务人才需求增长。就业在跨国公司、外贸企业等。",
        "xuefeng_comment": "国际商务是很有前景的专业，就业在跨国公司、外贸企业、金融机构海外部门等。这个专业需要英语好、沟通能力强。可以考取国际商务师等证书。读研或留学有利于发展。薪资水平中等偏高。",
        "yearly_courses": {"大一": ["经济学原理", "管理学原理", "英语精读", "国际商务概论"], "大二": ["国际贸易实务", "国际市场营销", "国际商法", "跨文化管理"], "大三": ["国际商务谈判", "国际结算", "国际物流", "国际投资"], "大四": ["跨国公司或外贸企业实习"]},
        "top_universities": {"domestic": ["对外经济贸易大学", "上海财经大学", "北京大学", "复旦大学", "中山大学"], "international": ["LSE", "Harvard", "Wharton", "INSEAD"]}
    },
    # 理学专业
    {
        "code": "070102",
        "name": "信息与计算科学",
        "category": "07 理学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥13k-30k",
        "overview": "信息与计算科学是数学与计算机科学的交叉学科，培养掌握算法和数据科学的专业人才。",
        "what_you_learn": "数学分析、代数与几何、算法与数据结构、数值分析、信息论、机器学习",
        "suitable_for": "数学和计算机基础好、对算法和数据科学感兴趣的学生。",
        "career_outlook": "算法人才需求爆发，就业在互联网公司、金融机构、科技企业等。",
        "xuefeng_comment": "信息与计算科学是数学和计算机的交叉专业，就业在互联网公司、金融机构、科技企业等。这个专业对数学和编程都有要求，就业前景很好。可以成为算法工程师、数据科学家等。读研深造有更好发展。薪资水平高。",
        "yearly_courses": {"大一": ["数学分析", "高等代数", "程序设计基础", "离散数学"], "大二": ["算法与数据结构", "数值分析", "概率论", "信息论"], "大三": ["机器学习", "大数据技术", "人工智能", "计算机网络"], "大四": ["科技企业实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "浙江大学", "上海交通大学"], "international": ["MIT", "Stanford", "Carnegie Mellon", "Berkeley"]}
    },
    {
        "code": "070103",
        "name": "数理基础科学",
        "category": "07 理学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "数理基础科学是强化数学和物理基础的理科专业，培养从事科学研究的高级人才。",
        "what_you_learn": "数学分析、高等代数、理论力学、电动力学、量子力学、数学物理方法",
        "suitable_for": "热爱基础学科、有志从事科学研究的学生。",
        "career_outlook": "基础学科研究人才稀缺，适合继续深造。就业在高校、科研院所等。",
        "xuefeng_comment": "数理基础科学是基础学科专业，主要培养科研人才。这个专业难度大，适合真正热爱数学和物理的同学。读研读博几乎是必然选择。可以成为科学家或大学教授，社会地位高。",
        "yearly_courses": {"大一": ["数学分析", "高等代数", "普通物理学", "理论力学"], "大二": ["数学物理方法", "电动力学", "量子力学", "统计物理"], "大三": ["微分几何", "泛函分析", "粒子物理", "固体物理"], "大四": ["科研训练"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "南京大学", "中国科学技术大学"], "international": ["MIT", "Harvard", "Princeton", "Stanford", "Caltech"]}
    },
    {
        "code": "070602",
        "name": "海洋技术",
        "category": "07 理学",
        "category_icon": "🌊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-26k",
        "overview": "海洋技术是研究海洋探测和开发技术的专业，培养从事海洋科学研究和技术应用的人才。",
        "what_you_learn": "海洋学概论、海洋探测技术、海洋遥感、物理海洋学、海洋化学、海洋生物学",
        "suitable_for": "对海洋科学和技术感兴趣的学生。",
        "career_outlook": "海洋强国战略，海洋技术人才需求增长。就业在海洋科研机构、海洋局等。",
        "xuefeng_comment": "海洋技术是特色理科专业，就业在海洋科研机构、海洋局、海洋石油企业等。这个专业有一定行业特色。读研比例高。可以考公务员，海洋部门是不错的选择。",
        "yearly_courses": {"大一": ["海洋学概论", "普通物理学", "普通化学", "生物学基础"], "大二": ["物理海洋学", "海洋化学", "海洋生物学", "海洋探测技术"], "大三": ["海洋遥感", "海洋调查技术", "海洋资源", "海洋环境监测"], "大四": ["海洋科研机构实习"]},
        "top_universities": {"domestic": ["中国海洋大学", "厦门大学", "浙江大学", "同济大学", "上海海洋大学"], "international": ["Scripps Institution", "Woods Hole", "WHOI", "UCSB"]}
    },
    {
        "code": "070802",
        "name": "空间科学与技术",
        "category": "07 理学",
        "category_icon": "🚀",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "空间科学与技术是研究空间探测和航天技术的专业，培养从事航天科技研究的高级人才。",
        "what_you_learn": "航天器原理、空间探测技术、天体力学、遥感原理与应用、空间物理、卫星导航",
        "suitable_for": "对航天和空间科学感兴趣、有志从事航天事业的学生。",
        "career_outlook": "航天事业发展，空间技术人才需求增长。就业在航天院所、卫星应用企业等。",
        "xuefeng_comment": "空间科学与技术是很有前景的专业，就业在航天科研院所、卫星应用企业、军队航天部门等。这个专业需要较强的理工科基础。可以参与国家重大航天工程，很有成就感。读研比例高。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "大学物理", "航天概论"], "大二": ["理论力学", "天体力学", "空间物理", "遥感原理"], "大三": ["航天器原理", "空间探测技术", "卫星导航", "遥感应用"], "大四": ["航天院所实习"]},
        "top_universities": {"domestic": ["北京航空航天大学", "哈尔滨工业大学", "南京航空航天大学", "西北工业大学", "北京大学"], "international": ["MIT", "Stanford", "Caltech", "CU Boulder"]}
    },
    {
        "code": "071003",
        "name": "海洋资源与环境",
        "category": "07 理学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-24k",
        "overview": "海洋资源与环境是研究海洋资源和海洋环境保护的专业，培养从事海洋资源开发与保护的人才。",
        "what_you_learn": "海洋学、海洋资源学、海洋环境科学、海洋生态学、海洋管理、海洋化学",
        "suitable_for": "对海洋资源和环境保护感兴趣的学生。",
        "career_outlook": "海洋资源开发与保护并重，相关人才需求稳定。就业在海洋局、海洋保护区等。",
        "xuefeng_comment": "海洋资源与环境是特色专业，就业在海洋局、海洋保护区、海洋研究机构等。这个专业需要了解海洋科学和环境科学知识。可以考公务员，海洋部门是不错的选择。读研比例高。",
        "yearly_courses": {"大一": ["海洋学", "普通生物学", "普通化学", "环境科学概论"], "大二": ["海洋资源学", "海洋化学", "海洋生态学", "海洋生物学"], "大三": ["海洋环境科学", "海洋管理", "海洋保护区管理", "海洋监测"], "大四": ["海洋机构实习"]},
        "top_universities": {"domestic": ["中国海洋大学", "厦门大学", "上海海洋大学", "浙江海洋大学", "广东海洋大学"], "international": ["Scripps", "WHOI", "UCSB", "University of Miami"]}
    },
    {
        "code": "071102",
        "name": "应用心理学",
        "category": "07 理学",
        "category_icon": "🧠",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "应用心理学是将心理学理论应用于实际问题的专业，培养从事心理咨询和人力资源等工作的人才。",
        "what_you_learn": "普通心理学、发展心理学、社会心理学、咨询心理学、心理测量、人力资源管理",
        "suitable_for": "对心理学感兴趣、善于与人沟通的学生。",
        "career_outlook": "心理健康意识提高，应用心理学人才需求增长。就业在心理咨询机构、企业HR等。",
        "xuefeng_comment": "应用心理学是热门专业，就业在心理咨询机构、企业人力资源部门、学校心理咨询中心等。这个专业需要善于与人沟通，有同理心。可以考取心理咨询师证书。读研有利于成为专业心理咨询师。",
        "yearly_courses": {"大一": ["普通心理学", "实验心理学", "人体解剖学", "统计学"], "大二": ["发展心理学", "社会心理学", "心理测量", "咨询心理学"], "大三": ["变态心理学", "人力资源管理", "心理治疗技术", "团体辅导"], "大四": ["心理咨询机构或企业实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "北京大学", "华南师范大学", "华中师范大学"], "international": ["Harvard", "Stanford", "Yale", "UCL"]}
    }
]

def main():
    print("=" * 70)
    print("📚 开始导入经济学和理学专业...")
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
