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

law_majors_1 = [
    {
        "code": "030104T",
        "name": "信用风险管理与法律防控",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "信用风险管理与法律防控是研究信用风险和法律防控的交叉学科，培养从事信用管理和法律风险防控的专业人才。",
        "what_you_learn": "民法学、商法学、信用管理、风险管理学、企业法务、合同管理、合规管理",
        "suitable_for": "对信用管理和法律风险防控感兴趣的学生。",
        "career_outlook": "企业合规需求增长，就业在企业法务、银行风控、信用管理等。",
        "xuefeng_comment": "信用风险管理与法律防控是法学类的新兴专业，结合信用管理和法律。就业在企业法务、银行风控部门、信用管理公司等。这个专业需要法学和管理知识，实用性强。适合对信用管理和法律风险防控感兴趣的学生。就业稳定，薪资中等偏上。需要不断学习新的法规。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "民法学", "管理学原理"], "大二": ["商法学", "信用管理", "风险管理学", "民事诉讼法"], "大三": ["企业法务", "合同管理", "合规管理", "金融法"], "大四": ["企业法务实习"]},
        "top_universities": {"domestic": ["中国政法大学", "中央财经大学", "西南政法大学", "华东政法大学", "上海交通大学"], "international": ["Harvard Law", "Stanford Law", "Columbia Law", "LSE"]}
    },
    {
        "code": "030105T",
        "name": "国际经贸规则",
        "category": "03 法学",
        "category_icon": "🌐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "国际经贸规则是研究国际贸易法律规则的学科，培养从事国际经贸法律事务的专业人才。",
        "what_you_learn": "国际法、国际经济法、国际贸易法、世界贸易组织法、国际投资法、国际商事仲裁、国际商法",
        "suitable_for": "英语好、对国际经贸法律感兴趣的学生。",
        "career_outlook": "国际贸易发展，就业在外贸企业、国际律所、海关等。",
        "xuefeng_comment": "国际经贸规则是法学类的特色专业，研究国际经贸法律规则。就业在外贸企业、国际律所、海关、商务局等。这个专业需要英语好，国际视野广。适合对国际经贸法律感兴趣的学生。就业稳定，薪资中等偏上。读研或出国深造有利于发展。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "国际法", "英语精读"], "大二": ["国际经济法", "国际贸易法", "世界贸易组织法", "国际私法"], "大三": ["国际投资法", "国际商事仲裁", "国际商法", "国际谈判"], "大四": ["外贸企业或国际律所实习"]},
        "top_universities": {"domestic": ["中国政法大学", "对外经济贸易大学", "上海财经大学", "复旦大学", "华东政法大学"], "international": ["Harvard Law", "Stanford Law", "Columbia Law", "NYU Law"]}
    },
    {
        "code": "030106TK",
        "name": "司法警察学",
        "category": "03 法学",
        "category_icon": "👮",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "司法警察学是研究司法警察工作的学科，培养从事司法警察工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "法学基础、司法警察学、刑事执行、押解与看管、安全保卫、警务技能、司法文书写作",
        "suitable_for": "对司法警察工作感兴趣、有责任感的学生。",
        "career_outlook": "司法机关需求稳定，就业在法院、检察院司法警察部门等。",
        "xuefeng_comment": "司法警察学是法学类的公安学专业，培养司法警察人才，是国家控制布点专业。就业在法院、检察院司法警察部门。这个专业需要责任感和纪律性。适合对司法警察工作感兴趣的学生。就业稳定，工作有一定的危险性和挑战性。考公务员有优势。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "刑法学", "刑事诉讼法"], "大二": ["司法警察学", "刑事执行", "押解与看管", "安全保卫"], "大三": ["警务技能", "司法文书写作", "警察心理学", "体能训练"], "大四": ["法院或检察院实习"]},
        "top_universities": {"domestic": ["中国人民公安大学", "中央司法警官学院", "西南政法大学", "华东政法大学", "西北政法大学"], "international": ["FBI Academy", "Scotland Yard", "Interpol", "RCMP"]}
    },
    {
        "code": "030107TK",
        "name": "社区矫正",
        "category": "03 法学",
        "category_icon": "🏡",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "社区矫正是研究社区矫正工作的学科，培养从事社区矫正工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "法学基础、社区矫正学、社会学、心理学、个案工作、小组工作、社区矫正实务",
        "suitable_for": "对社会工作和社区矫正感兴趣、有耐心的学生。",
        "career_outlook": "社区矫正发展，就业在司法局社区矫正机构、街道社区等。",
        "xuefeng_comment": "社区矫正是法学类的新兴专业，培养社区矫正人才，是国家控制布点专业。就业在司法局社区矫正机构、街道社区。这个专业需要耐心和爱心。适合对社会工作和社区矫正感兴趣的学生。就业稳定，薪资中等。考公务员有优势。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "刑法学", "社会学"], "大二": ["社区矫正学", "心理学", "社会工作概论", "个案工作"], "大三": ["小组工作", "社区矫正实务", "司法社会工作", "社区矫正政策法规"], "大四": ["司法局或街道社区实习"]},
        "top_universities": {"domestic": ["中央司法警官学院", "中国政法大学", "西南政法大学", "华东政法大学", "上海政法学院"], "international": ["University of Cambridge", "Oxford", "LSE", "University of Pennsylvania"]}
    },
    {
        "code": "030108TK",
        "name": "纪检监察",
        "category": "03 法学",
        "category_icon": "🔍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "纪检监察是研究纪检监察工作的学科，培养从事纪检监察工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "法学基础、纪检监察学、中共党史、行政法学、监察法、审计学、纪检监察实务",
        "suitable_for": "对纪检监察工作感兴趣、有责任感的学生。",
        "career_outlook": "纪检监察工作重要，就业在纪委监委、企业纪检监察部门等。",
        "xuefeng_comment": "纪检监察是法学类的新兴专业，培养纪检监察人才，是国家控制布点专业。就业在纪委监委、企业纪检监察部门、党政机关。这个专业需要责任感和纪律性。适合对纪检监察工作感兴趣的学生。就业稳定，发展前景好。考公务员有优势。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "中共党史", "行政法学"], "大二": ["纪检监察学", "监察法", "审计学", "刑事诉讼法"], "大三": ["纪检监察实务", "党内法规", "行政监察", "监察调查"], "大四": ["纪委监委或企业纪检监察部门实习"]},
        "top_universities": {"domestic": ["中国政法大学", "中央财经大学", "西南政法大学", "华东政法大学", "西北政法大学"], "international": ["Harvard Kennedy School", "LSE", "Oxford", "Cambridge"]}
    },
    {
        "code": "030109TK",
        "name": "国际法",
        "category": "03 法学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-32k",
        "overview": "国际法是研究国际法律规则的学科，培养从事国际法务的专业人才，是国家控制布点专业。",
        "what_you_learn": "国际法、国际私法、国际经济法、国际人权法、国际海洋法、国际环境法、国际商事仲裁",
        "suitable_for": "英语好、对国际法感兴趣的学生。",
        "career_outlook": "国际化发展，就业在国际组织、外办、国际律所等。",
        "xuefeng_comment": "国际法是法学类的专业，培养国际法人才，是国家控制布点专业。就业在国际组织、外办、国际律所、跨国企业。这个专业需要英语好，国际视野广。适合对国际法感兴趣的学生。就业稳定，薪资较高。读研或出国深造几乎是必须的。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "国际法", "英语精读"], "大二": ["国际私法", "国际经济法", "国际人权法", "国际组织法"], "大三": ["国际海洋法", "国际环境法", "国际商事仲裁", "国际谈判"], "大四": ["国际组织或外办实习"]},
        "top_universities": {"domestic": ["中国政法大学", "北京大学", "复旦大学", "武汉大学", "华东政法大学"], "international": ["Harvard Law", "Stanford Law", "NYU Law", "LSE"]}
    },
    {
        "code": "030110TK",
        "name": "司法鉴定学",
        "category": "03 法学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "司法鉴定学是研究司法鉴定技术的学科，培养从事司法鉴定工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "法学基础、司法鉴定学、法医学、物证技术学、文书鉴定、痕迹鉴定、法医鉴定",
        "suitable_for": "对司法鉴定和科学技术感兴趣的学生。",
        "career_outlook": "司法鉴定需求稳定，就业在司法鉴定机构、公安技术部门等。",
        "xuefeng_comment": "司法鉴定学是法学类的专业，培养司法鉴定人才，是国家控制布点专业。就业在司法鉴定机构、公安技术部门、法院技术部门。这个专业需要法学和科学技术知识。适合对司法鉴定和科学技术感兴趣的学生。就业稳定，专业性强。可以考取司法鉴定人资格。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "刑法学", "刑事诉讼法"], "大二": ["司法鉴定学", "法医学", "物证技术学", "生理学"], "大三": ["文书鉴定", "痕迹鉴定", "法医鉴定", "微量物证鉴定"], "大四": ["司法鉴定机构实习"]},
        "top_universities": {"domestic": ["中国政法大学", "西南政法大学", "华东政法大学", "西北政法大学", "西安交通大学"], "international": ["Johns Hopkins", "MIT Media Lab", "Imperial College", "Cambridge"]}
    },
    {
        "code": "030111TK",
        "name": "国家安全学",
        "category": "03 法学",
        "category_icon": "🛡️",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "国家安全学是研究国家安全的学科，培养从事国家安全工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "国家安全学、法学基础、政治学、国际关系、国家安全法、保密学、情报学基础",
        "suitable_for": "对国家安全事业感兴趣、政治素质高的学生。",
        "career_outlook": "国家安全重要，就业在国家安全部门、党政机关等。",
        "xuefeng_comment": "国家安全学是法学类的新兴专业，培养国家安全人才，是国家控制布点专业。就业在国家安全部门、党政机关、军队等。这个专业需要政治素质高，纪律性强。适合对国家安全事业感兴趣的学生。就业稳定，发展前景好。对身体素质有要求。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "国家安全学", "政治学"], "大二": ["国际关系", "国家安全法", "保密学", "情报学基础"], "大三": ["国家安全战略", "反恐怖主义", "网络安全", "国家安全实务"], "大四": ["国家安全部门或党政机关实习"]},
        "top_universities": {"domestic": ["中国政法大学", "中国人民大学", "国际关系学院", "北京大学", "复旦大学"], "international": ["Harvard Kennedy School", "Johns Hopkins SAIS", "Georgetown", "LSE"]}
    },
    {
        "code": "030112TK",
        "name": "海外利益安全",
        "category": "03 法学",
        "category_icon": "🌏",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "海外利益安全是研究海外利益保护的学科，培养从事海外利益安全工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "法学基础、海外利益安全、国际关系、国际安全、领事保护、风险管理、海外安全管理",
        "suitable_for": "英语好、对海外利益保护感兴趣的学生。",
        "career_outlook": "海外利益保护重要，就业在外办、国企海外部门、安保公司等。",
        "xuefeng_comment": "海外利益安全是法学类的新兴专业，培养海外利益保护人才，是国家控制布点专业。就业在外办、国企海外部门、海外安保公司、跨国企业。这个专业需要英语好，国际视野广。适合对海外利益保护感兴趣的学生。就业前景好，有一定的外派机会。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "海外利益安全", "国际关系"], "大二": ["国际安全", "领事保护", "风险管理", "英语精读"], "大三": ["海外安全管理", "国际政治经济", "海外安全实务", "国际危机管理"], "大四": ["外办或国企海外部门实习"]},
        "top_universities": {"domestic": ["中国政法大学", "国际关系学院", "中国人民大学", "北京大学", "复旦大学"], "international": ["Harvard Kennedy School", "Johns Hopkins SAIS", "LSE", "Georgetown"]}
    },
    {
        "code": "030203",
        "name": "外交学",
        "category": "03 法学",
        "category_icon": "🎖️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "外交学是研究外交理论和实践的学科，培养从事外交和外事工作的专业人才。",
        "what_you_learn": "外交学概论、外交史、国际关系、国际政治、国际法、外交礼仪、外事谈判",
        "suitable_for": "英语好、对外交和外事工作感兴趣的学生。",
        "career_outlook": "外交事业发展，就业在外交部、外办、国际组织等。",
        "xuefeng_comment": "外交学是政治学类的专业，培养外交人才。就业在外交部、外办、国际组织、新闻媒体国际部。这个专业需要英语好，对外形象气质佳。适合对外交和外事工作感兴趣的学生。考外交部是主要发展方向。读研或出国深造有利于发展。竞争比较激烈。",
        "yearly_courses": {"大一": ["政治学概论", "外交学概论", "中国外交史", "英语精读"], "大二": ["外交史", "国际关系", "国际政治", "国际法"], "大三": ["外交礼仪", "外事谈判", "国际政治经济学", "公共外交"], "大四": ["外交部或外办实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "外交学院", "复旦大学", "上海外国语大学"], "international": ["Harvard", "Oxford", "LSE", "Sciences Po"]}
    }
]

def main():
    print("=" * 70)
    print("⚖️ 开始导入法学类专业（第一批）...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in law_majors_1:
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
