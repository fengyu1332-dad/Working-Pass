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

economics_majors = [
    {
        "code": "020103T",
        "name": "国民经济管理",
        "category": "02 经济学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "国民经济管理是研究国民经济运行和管理的学科，培养从事宏观经济分析和管理的专业人才。",
        "what_you_learn": "政治经济学、西方经济学、计量经济学、国民经济管理学、宏观经济管理、产业经济学、区域经济学、政府经济学",
        "suitable_for": "对宏观经济分析和政府管理感兴趣的学生。",
        "career_outlook": "政府经济管理部门需求稳定，就业在发改委、统计局、财政局、政策研究室等。",
        "xuefeng_comment": "国民经济管理是经济学类的特色专业，培养宏观经济管理人才。这个专业需要较强的经济学和数学基础。就业主要在政府部门、金融机构、大型企业战略规划部门等。考公务员优势明显。读研有利于发展。适合对宏观经济分析感兴趣的学生。女生也很适合，工作环境相对稳定。毕业生可以从事经济分析、政策研究、战略规划等工作。",
        "yearly_courses": {"大一": ["政治经济学", "高等数学", "西方经济学", "管理学原理"], "大二": ["计量经济学", "统计学", "国民经济管理学", "金融学"], "大三": ["宏观经济管理", "产业经济学", "区域经济学", "政府经济学"], "大四": ["经济政策研究", "政府部门实习"]},
        "top_universities": {"domestic": ["中国人民大学", "中央财经大学", "上海财经大学", "复旦大学", "武汉大学"], "international": ["Harvard", "MIT", "Chicago", "LSE"]}
    },
    {
        "code": "020105T",
        "name": "商务经济学",
        "category": "02 经济学",
        "category_icon": "💼",
        "difficulty": "⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "商务经济学是研究商务活动中经济规律的学科，培养从事商务分析和决策的专门人才。",
        "what_you_learn": "微观经济学、宏观经济学、商务统计学、商务谈判、国际商务、市场营销、商务数据分析",
        "suitable_for": "对商务和数据分析感兴趣的学生。",
        "career_outlook": "商业分析人才需求增长，就业在商务部门、市场研究机构等。",
        "xuefeng_comment": "商务经济学是经济学类的实用专业，结合经济学和商务管理。就业在企业商务部门、市场研究机构、咨询公司等。这个专业需要经济学和商务知识。适合对商业分析和决策感兴趣的学生。就业面广，薪资中等。读研或出国深造有利于发展。女生也很适合，工作环境相对较好。",
        "yearly_courses": {"大一": ["微观经济学", "宏观经济学", "商务统计学", "管理学原理"], "大二": ["商务谈判", "国际商务", "市场营销", "会计学"], "大三": ["商务数据分析", "战略管理", "供应链管理", "电子商务"], "大四": ["商务实习"]},
        "top_universities": {"domestic": ["上海财经大学", "对外经济贸易大学", "中央财经大学", "西南财经大学", "暨南大学"], "international": ["Wharton", "London Business School", "INSEAD", "Columbia"]}
    },
    {
        "code": "020106T",
        "name": "能源经济",
        "category": "02 经济学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "能源经济是研究能源领域经济问题的学科，培养从事能源经济分析和管理的专业人才。",
        "what_you_learn": "能源经济学、国际能源市场、能源政策、能源技术经济、石油经济学、天然气经济学、可再生能源经济学",
        "suitable_for": "对能源产业和经济分析感兴趣的学生。",
        "career_outlook": "能源战略重要，就业在能源企业、发改委、能源局等。",
        "xuefeng_comment": "能源经济是经济学类的特色专业，结合能源产业和经济分析。就业在能源企业、政府能源管理部门、能源研究机构等。这个专业需要经济学和能源知识。随着能源转型，这个专业发展前景很好。读研比例较高，可以进入能源研究领域。男女都适合，就业稳定。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "能源概论"], "大二": ["能源经济学", "国际能源市场", "能源政策", "统计学"], "大三": ["能源技术经济", "石油经济学", "天然气经济学", "可再生能源经济学"], "大四": ["能源企业实习"]},
        "top_universities": {"domestic": ["中国人民大学", "中央财经大学", "中国石油大学", "中国地质大学", "厦门大学"], "international": ["MIT Sloan", "Stanford GSB", "Chicago", "Texas A&M"]}
    },
    {
        "code": "020107T",
        "name": "劳动经济学",
        "category": "02 经济学",
        "category_icon": "👥",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "劳动经济学是研究劳动力市场和劳动关系的学科，培养从事劳动经济分析和管理的专业人才。",
        "what_you_learn": "劳动经济学、人力资源管理、劳动法、社会保障、劳动统计、就业管理、劳动关系协调",
        "suitable_for": "对人力资源和劳动关系感兴趣的学生。",
        "career_outlook": "HR和社保部门需求稳定，就业在企业HR、社保部门等。",
        "xuefeng_comment": "劳动经济学是经济学类的实用专业，结合劳动力市场和劳动关系。就业在企业人力资源部门、社保管理部门、劳动研究机构等。这个专业需要经济学和管理知识。适合对人力资源和劳动关系感兴趣的学生。就业稳定，薪资中等。考公务员有优势。女生也很适合。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "管理学原理"], "大二": ["劳动经济学", "人力资源管理", "劳动法", "统计学"], "大三": ["社会保障", "劳动统计", "就业管理", "劳动关系协调"], "大四": ["企业HR部门实习"]},
        "top_universities": {"domestic": ["中国人民大学", "复旦大学", "上海财经大学", "南京大学", "武汉大学"], "international": ["Harvard", "Chicago", "Princeton", "LSE"]}
    },
    {
        "code": "020108T",
        "name": "经济工程",
        "category": "02 经济学",
        "category_icon": "🏗️",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "经济工程是经济学和工程技术的交叉学科，培养从事工程经济分析的专业人才。",
        "what_you_learn": "工程经济学、项目评估、成本控制、工程管理、财务管理、投资学、工程造价",
        "suitable_for": "对工程和经济分析都感兴趣的学生。",
        "career_outlook": "工程投资需要专业人才，就业在工程咨询公司、建筑企业等。",
        "xuefeng_comment": "经济工程是经济学和工程的交叉专业，培养工程经济分析人才。就业在工程咨询公司、建筑企业、投资公司等。这个专业需要经济学和工程知识，难度较大。适合对工程经济分析感兴趣的学生。薪资中等偏上，发展前景好。读研有利于深入发展。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "工程制图"], "大二": ["工程经济学", "项目评估", "财务管理", "工程力学"], "大三": ["成本控制", "工程管理", "投资学", "工程造价"], "大四": ["工程咨询公司实习"]},
        "top_universities": {"domestic": ["同济大学", "天津大学", "东南大学", "重庆大学", "华南理工大学"], "international": ["MIT", "Stanford", "Georgia Tech", "Imperial College"]}
    },
    {
        "code": "020203TK",
        "name": "国际税收",
        "category": "02 经济学",
        "category_icon": "💰",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "国际税收是研究跨境税收和国际税收协定的学科，培养从事国际税务管理的专业人才。",
        "what_you_learn": "税法、国际税收、税收协定、转让定价、税收筹划、国际税务、涉外税收管理",
        "suitable_for": "对税收和国际商务感兴趣的学生。",
        "career_outlook": "跨国企业税务需求增长，就业在税务局、会计师事务所等。",
        "xuefeng_comment": "国际税收是财政学类的特色专业，结合税法和国际税收。就业在税务局、会计师事务所、跨国企业税务部门等。这个专业需要税法和国际商务知识，是国家控制布点专业。适合对税务和国际商务感兴趣的学生。就业稳定，薪资中等偏上。考公务员有优势。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "税法"], "大二": ["国际税收", "税收协定", "转让定价", "税收筹划"], "大三": ["国际税务", "涉外税收管理", "会计学", "财务管理"], "大四": ["税务局或会计师事务所实习"]},
        "top_universities": {"domestic": ["中央财经大学", "上海财经大学", "西南财经大学", "厦门大学", "中南财经政法大学"], "international": ["London School of Economics", "Wharton", "Columbia", "Harvard"]}
    },
    {
        "code": "020307T",
        "name": "经济与金融",
        "category": "02 经济学",
        "category_icon": "💹",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "经济与金融是研究经济和金融结合的学科，培养从事经济金融分析的专业人才。",
        "what_you_learn": "经济学原理、货币银行学、金融学、投资学、金融市场学、公司金融、经济金融分析",
        "suitable_for": "对经济分析和金融市场感兴趣的学生。",
        "career_outlook": "金融机构分析人才需求稳定，就业在银行、证券、基金等。",
        "xuefeng_comment": "经济与金融是经济学和金融学的结合专业，培养复合型金融人才。就业在银行、证券公司、基金公司等。这个专业需要经济学和金融学基础，就业面广。适合对经济分析和金融市场感兴趣的学生。薪资中等偏上，发展前景好。读研或出国深造有优势。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "货币银行学"], "大二": ["金融学", "投资学", "金融市场学", "统计学"], "大三": ["公司金融", "经济金融分析", "金融工程", "风险管理"], "大四": ["金融机构实习"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "复旦大学", "上海交通大学", "上海财经大学"], "international": ["MIT", "Stanford", "Chicago", "London Business School"]}
    },
    {
        "code": "020309T",
        "name": "互联网金融",
        "category": "02 经济学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥13k-32k",
        "overview": "互联网金融是研究互联网和金融结合的学科，培养从事互联网金融管理的专业人才。",
        "what_you_learn": "金融学、互联网金融概论、网络支付、P2P网贷、互联网保险、金融科技、数据分析",
        "suitable_for": "对互联网和金融都感兴趣的学生。",
        "career_outlook": "金融科技发展，就业在互联网金融公司、银行科技部门等。",
        "xuefeng_comment": "互联网金融是金融学类的新兴专业，结合互联网和金融。就业在互联网金融公司、银行科技部门、金融科技公司等。这个专业需要金融学和计算机知识，更新快。适合对金融科技感兴趣的学生。薪资较高，发展前景好。需要持续学习新技术。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "金融学"], "大二": ["互联网金融概论", "网络支付", "P2P网贷", "统计学"], "大三": ["互联网保险", "金融科技", "数据分析", "网络安全"], "大四": ["互联网金融公司实习"]},
        "top_universities": {"domestic": ["上海交通大学", "浙江大学", "中央财经大学", "上海财经大学", "西南财经大学"], "international": ["Stanford", "MIT", "Carnegie Mellon", "UC Berkeley"]}
    },
    {
        "code": "020310T",
        "name": "金融科技",
        "category": "02 经济学",
        "category_icon": "🔗",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥14k-36k",
        "overview": "金融科技是研究金融和科技结合的学科，培养从事金融科技创新的专业人才。",
        "what_you_learn": "金融学、计算机科学、区块链、人工智能在金融应用、金融数据分析、支付清算",
        "suitable_for": "对金融和科技都感兴趣、有编程基础的学生。",
        "career_outlook": "金融科技人才需求爆发，就业在金融科技公司、银行科技部门等。",
        "xuefeng_comment": "金融科技是金融学类的热门新兴专业，结合金融和科技。就业在金融科技公司、银行科技部门、互联网公司金融部门等。这个专业需要金融学和计算机编程基础，对数学要求高。适合对金融科技创新感兴趣的学生。薪资很高，发展前景极好。读研深造有利于发展。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "Python编程"], "大二": ["金融学", "计算机科学", "数据结构", "统计学"], "大三": ["区块链", "人工智能在金融应用", "金融数据分析", "支付清算"], "大四": ["金融科技公司实习"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "上海交通大学", "复旦大学", "浙江大学"], "international": ["MIT Sloan", "Stanford", "Carnegie Mellon", "UC Berkeley"]}
    },
    {
        "code": "020311TK",
        "name": "金融审计",
        "category": "02 经济学",
        "category_icon": "🔍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "金融审计是研究金融领域审计的学科，培养从事金融审计的专业人才。",
        "what_you_learn": "审计学、金融学、金融审计、银行审计、证券审计、保险审计、金融风险管理",
        "suitable_for": "对审计和金融都感兴趣的学生。",
        "career_outlook": "金融审计需求稳定，就业在审计署、会计师事务所、金融机构内审等。",
        "xuefeng_comment": "金融审计是金融学类的特色专业，结合审计和金融，是国家控制布点专业。就业在审计署、会计师事务所、金融机构内审部门等。这个专业需要审计和金融知识，专业性强。适合对金融审计感兴趣的学生。就业稳定，薪资中等偏上。考公务员有优势。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "审计学"], "大二": ["金融学", "金融审计", "银行审计", "会计学"], "大三": ["证券审计", "保险审计", "金融风险管理", "财务管理"], "大四": ["审计署或会计师事务所实习"]},
        "top_universities": {"domestic": ["中央财经大学", "上海财经大学", "南京审计大学", "西南财经大学", "中南财经政法大学"], "international": ["London School of Economics", "Columbia", "Chicago", "Harvard"]}
    },
    {
        "code": "020401",
        "name": "国际经济与贸易",
        "category": "02 经济学",
        "category_icon": "🌐",
        "difficulty": "⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "国际经济与贸易是研究国际贸易和跨国经济合作的学科，培养从事国际贸易的专业人才。",
        "what_you_learn": "国际贸易实务、国际金融、国际市场营销、国际贸易惯例、国际商务谈判、外贸函电",
        "suitable_for": "英语好、对国际贸易感兴趣的学生。",
        "career_outlook": "对外开放持续，就业在外贸公司、跨国企业、海关等。",
        "xuefeng_comment": "国际经济与贸易是经典的经济学专业，培养国际贸易人才。就业在外贸公司、跨国企业、海关等。这个专业需要英语好，沟通能力强。适合对国际贸易感兴趣的学生。就业稳定，薪资中等。外贸经验积累后很有竞争力。读研或出国深造有利于发展。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "英语精读"], "大二": ["国际贸易实务", "国际金融", "国际市场营销", "统计学"], "大三": ["国际贸易惯例", "国际商务谈判", "外贸函电", "报关实务"], "大四": ["外贸公司实习"]},
        "top_universities": {"domestic": ["对外经济贸易大学", "上海财经大学", "中国人民大学", "复旦大学", "中央财经大学"], "international": ["London School of Economics", "Wharton", "Harvard", "Columbia"]}
    },
    {
        "code": "020403T",
        "name": "国际经济发展合作",
        "category": "02 经济学",
        "category_icon": "🤝",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "国际经济发展合作是研究国际发展援助和合作的学科，培养从事国际发展合作的专业人才。",
        "what_you_learn": "发展经济学、国际发展合作、国际援助、项目管理、国际政治经济、发展中国家研究",
        "suitable_for": "对国际发展和合作感兴趣的学生。",
        "career_outlook": "国际合作深化，就业在国际组织、政府外办、NGO等。",
        "xuefeng_comment": "国际经济发展合作是经济学类的新兴专业，研究国际发展合作。就业在国际组织、政府外办、NGO、跨国企业CSR部门等。这个专业需要经济学和国际政治知识，就业面相对窄但很有特色。适合对国际发展和合作感兴趣的学生。读研深造有利于发展。英语好有优势。",
        "yearly_courses": {"大一": ["政治经济学", "西方经济学", "高等数学", "发展经济学"], "大二": ["国际发展合作", "国际援助", "项目管理", "统计学"], "大三": ["国际政治经济", "发展中国家研究", "国际组织概论", "国际谈判"], "大四": ["国际组织或政府部门实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "中国人民大学", "上海交通大学"], "international": ["Harvard Kennedy School", "LSE", "Oxford", "Columbia"]}
    }
]

def main():
    print("=" * 70)
    print("📊 开始导入经济学类专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in economics_majors:
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
