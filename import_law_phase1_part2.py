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

law_majors_2 = [
    {
        "code": "030205",
        "name": "国际事务与国际关系",
        "category": "03 法学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "国际事务与国际关系是研究国际关系和国际事务的学科，培养从事国际事务工作的专业人才。",
        "what_you_learn": "国际关系、国际政治、国际法、国际政治经济学、外交学、国际组织、全球治理",
        "suitable_for": "英语好、对国际事务和国际关系感兴趣的学生。",
        "career_outlook": "国际交流增多，就业在国际组织、外办、媒体国际部等。",
        "xuefeng_comment": "国际事务与国际关系是政治学类的专业，培养国际事务人才。就业在国际组织、外办、媒体国际部、跨国企业。这个专业需要英语好，国际视野广。适合对国际事务和国际关系感兴趣的学生。就业稳定，发展前景好。读研或出国深造有利于发展。",
        "yearly_courses": {"大一": ["政治学概论", "国际关系", "国际政治", "英语精读"], "大二": ["国际法", "国际政治经济学", "外交学", "国际组织"], "大三": ["全球治理", "国际安全", "国际政治思想史", "地区研究"], "大四": ["国际组织或外办实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "外交学院", "国际关系学院"], "international": ["Harvard", "Oxford", "LSE", "Sciences Po"]}
    },
    {
        "code": "030206TK",
        "name": "政治学经济学与哲学",
        "category": "03 法学",
        "category_icon": "📜",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "政治学经济学与哲学是PPE交叉学科，培养复合型人文社科人才，是国家控制布点专业。",
        "what_you_learn": "政治学、经济学、哲学、政治哲学、政治经济学、西方哲学史、中国哲学史",
        "suitable_for": "对人文社科有广泛兴趣、想成为复合型人才的学生。",
        "career_outlook": "复合型人才受欢迎，就业在政府、智库、媒体、企业等。",
        "xuefeng_comment": "政治学经济学与哲学是PPE交叉学科，是国家控制布点专业。这个专业知识覆盖面广，适合对人文社科有广泛兴趣的学生。就业面广，可以在政府、智库、媒体、企业等工作。读研比例很高，非常适合继续深造。就业稳定，发展前景好。",
        "yearly_courses": {"大一": ["政治学概论", "经济学原理", "哲学概论", "高等数学"], "大二": ["政治哲学", "政治经济学", "西方哲学史", "中国哲学史"], "大三": ["政治学研究方法", "经济学研究方法", "哲学研究方法", "社会理论"], "大四": ["智库或政府部门实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "中国人民大学", "复旦大学", "武汉大学"], "international": ["Oxford", "Cambridge", "LSE", "Durham"]}
    },
    {
        "code": "030207TK",
        "name": "国际组织与全球治理",
        "category": "03 法学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-28k",
        "overview": "国际组织与全球治理是研究国际组织和全球治理的学科，培养从事国际组织工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "国际组织、全球治理、国际关系、国际法、国际政治经济学、国际组织实习、国际谈判",
        "suitable_for": "英语好、对国际组织和全球治理感兴趣的学生。",
        "career_outlook": "全球治理重要，就业在国际组织、外办、跨国企业等。",
        "xuefeng_comment": "国际组织与全球治理是政治学类的新兴专业，培养国际组织人才，是国家控制布点专业。就业在国际组织、外办、跨国企业、国际NGO。这个专业需要英语好，国际视野广。适合对国际组织和全球治理感兴趣的学生。就业前景好，有机会到国际组织实习工作。",
        "yearly_courses": {"大一": ["政治学概论", "国际组织", "全球治理", "英语精读"], "大二": ["国际关系", "国际法", "国际政治经济学", "国际组织概论"], "大三": ["全球治理理论", "国际组织实务", "国际谈判", "联合国研究"], "大四": ["国际组织实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "外交学院", "国际关系学院"], "international": ["Harvard Kennedy School", "LSE", "Oxford", "Georgetown"]}
    },
    {
        "code": "030304",
        "name": "女性学",
        "category": "03 法学",
        "category_icon": "♀️",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "女性学是研究女性问题的学科，培养从事妇女工作和性别研究的专业人才。",
        "what_you_learn": "女性学概论、女性史、女性主义、社会性别研究、妇女工作实务、性别与发展",
        "suitable_for": "对性别问题和妇女工作感兴趣的学生。",
        "career_outlook": "妇女事业发展，就业在妇联、NGO、媒体、政府部门等。",
        "xuefeng_comment": "女性学是社会学类的专业，研究女性问题。就业在妇联、NGO、媒体、政府部门、高校。这个专业需要对性别问题和妇女工作有兴趣。女生报考比例很高。就业稳定，薪资中等。适合对妇女事业感兴趣的学生。",
        "yearly_courses": {"大一": ["社会学概论", "女性学概论", "女性史", "妇女运动史"], "大二": ["女性主义", "社会性别研究", "性别心理学", "社会工作"], "大三": ["妇女工作实务", "性别与发展", "妇女法", "性别研究方法"], "大四": ["妇联或NGO实习"]},
        "top_universities": {"domestic": ["中华女子学院", "北京大学", "中国人民大学", "复旦大学", "南京大学"], "international": ["Harvard", "Oxford", "Cambridge", "University of California"]}
    },
    {
        "code": "030305T",
        "name": "家政学",
        "category": "03 法学",
        "category_icon": "🏠",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "家政学是研究家庭生活管理的学科，培养从事家政服务和管理的专业人才。",
        "what_you_learn": "家政学概论、营养学、家庭管理学、家庭教育学、家庭理财、家庭保健、居室设计",
        "suitable_for": "对家庭管理和家政服务感兴趣的学生。",
        "career_outlook": "家政服务需求增长，就业在家政公司、高端家政、物业管理等。",
        "xuefeng_comment": "家政学是社会学类的专业，研究家庭生活管理。就业在家政公司、高端家政、物业管理、社区服务。这个专业需要对家庭管理和家政服务有兴趣。女生比较适合。就业稳定，薪资中等。随着生活水平提高，高端家政需求增长。",
        "yearly_courses": {"大一": ["社会学概论", "家政学概论", "营养学", "生理学"], "大二": ["家庭管理学", "家庭教育学", "家庭理财", "心理学"], "大三": ["家庭保健", "居室设计", "儿童保育", "老人护理"], "大四": ["家政公司实习"]},
        "top_universities": {"domestic": ["吉林农业大学", "中华女子学院", "北京师范大学", "南京师范大学", "四川师范大学"], "international": ["Cornell", "Pennsylvania", "Ohio State", "Michigan State"]}
    },
    {
        "code": "030306T",
        "name": "社会政策",
        "category": "03 法学",
        "category_icon": "📋",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "社会政策是研究社会政策制定和实施的学科，培养从事社会政策工作的专业人才。",
        "what_you_learn": "社会政策概论、社会保障、社会福利、社会政策分析、社会政策评估、社会发展、公共政策",
        "suitable_for": "对社会政策和公共管理感兴趣的学生。",
        "career_outlook": "社会政策重要，就业在民政部门、政策研究机构、NGO等。",
        "xuefeng_comment": "社会政策是社会学类的专业，研究社会政策。就业在民政部门、政策研究机构、NGO、社会保障部门。这个专业需要对社会政策和公共管理有兴趣。就业稳定，薪资中等。考公务员有优势。读研有利于发展。",
        "yearly_courses": {"大一": ["社会学概论", "社会政策概论", "社会保障", "管理学原理"], "大二": ["社会福利", "社会政策分析", "社会政策评估", "统计学"], "大三": ["社会发展", "公共政策", "社会救助", "社会政策实务"], "大四": ["民政部门或政策研究机构实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "南京大学", "上海大学"], "international": ["Oxford", "LSE", "Cambridge", "University of Essex"]}
    },
    {
        "code": "030504T",
        "name": "马克思主义理论",
        "category": "03 法学",
        "category_icon": "🔴",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "马克思主义理论是研究马克思主义理论的学科，培养从事马克思主义理论研究和教学的专门人才。",
        "what_you_learn": "马克思主义基本原理、马克思主义发展史、马克思主义中国化研究、思想政治教育、中共党史、中国近代史纲要",
        "suitable_for": "对马克思主义理论和思想政治教育感兴趣的学生。",
        "career_outlook": "思政工作重要，就业在高校思政课、中小学政治课、党政机关等。",
        "xuefeng_comment": "马克思主义理论是马克思主义理论类的专业，培养思政人才。就业在高校思政课、中小学政治课、党政机关、党校。这个专业需要对马克思主义理论和思想政治教育有兴趣。考公务员有优势。就业稳定，发展前景好。",
        "yearly_courses": {"大一": ["马克思主义基本原理", "马克思主义发展史", "中共党史", "政治经济学"], "大二": ["马克思主义中国化研究", "思想政治教育学", "毛泽东思想概论", "中国特色社会主义理论"], "大三": ["马克思主义经典著作", "科学社会主义", "中国近代史纲要", "世界近现代史"], "大四": ["高校或中小学实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "清华大学", "复旦大学", "南京大学"], "international": ["Communist Party University", "Peking University"]}
    },
    {
        "code": "030617TK",
        "name": "工会学",
        "category": "03 法学",
        "category_icon": "⚒️",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "工会学是研究工会工作的学科，培养从事工会工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "工会学概论、工会工作实务、劳动法、劳动经济学、劳动社会学、工会组织建设、劳动关系协调",
        "suitable_for": "对工会工作和劳动关系感兴趣的学生。",
        "career_outlook": "工会工作重要，就业在工会组织、企业工会、劳动部门等。",
        "xuefeng_comment": "工会学是公安学类的特色专业，培养工会人才，是国家控制布点专业。就业在工会组织、企业工会、劳动部门、职工培训。这个专业需要对工会工作和劳动关系有兴趣。就业稳定，薪资中等。考公务员有优势。",
        "yearly_courses": {"大一": ["法学基础", "工会学概论", "劳动法", "劳动经济学"], "大二": ["工会工作实务", "劳动社会学", "工会组织建设", "社会学"], "大三": ["劳动关系协调", "工会财务管理", "工会宣传", "劳动争议处理"], "大四": ["工会组织实习"]},
        "top_universities": {"domestic": ["中国劳动关系学院", "中国人民大学", "中国政法大学", "吉林大学", "西南财经大学"], "international": ["Cornell ILR", "LSE", "Oxford"]}
    },
    {
        "code": "030602TK",
        "name": "侦查学",
        "category": "03 法学",
        "category_icon": "🔍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "侦查学是研究侦查工作的学科，培养从事侦查工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "侦查学、刑事侦查、犯罪学、刑事诉讼法、物证技术、法医学、侦查讯问",
        "suitable_for": "对公安工作和侦查感兴趣、有责任感的学生。",
        "career_outlook": "公安工作重要，就业在公安机关侦查部门。",
        "xuefeng_comment": "侦查学是公安学类的专业，培养侦查人才，是国家控制布点专业。就业在公安机关侦查部门。这个专业需要责任感和纪律性。适合对公安工作和侦查感兴趣的学生。就业稳定，工作有一定的危险性和挑战性。对身体素质有要求。",
        "yearly_courses": {"大一": ["法学基础", "侦查学、犯罪学", "刑法学"], "大二": ["刑事侦查", "刑事诉讼法", "物证技术", "法医学"], "大三": ["侦查讯问", "犯罪现场勘查", "侦查措施", "刑事技术"], "大四": ["公安机关实习"]},
        "top_universities": {"domestic": ["中国人民公安大学", "中国刑事警察学院", "西南政法大学", "华东政法大学", "西北政法大学"], "international": ["FBI Academy", "Scotland Yard", "Interpol", "RCMP"]}
    },
    {
        "code": "030604TK",
        "name": "禁毒学",
        "category": "03 法学",
        "category_icon": "🚫",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "禁毒学是研究禁毒工作的学科，培养从事禁毒工作的专门人才，是国家控制布点专业。",
        "what_you_learn": "禁毒学、禁毒法、毒品与成瘾、犯罪学、刑事侦查、禁毒实务、禁毒教育",
        "suitable_for": "对禁毒工作感兴趣、有责任感的学生。",
        "career_outlook": "禁毒工作重要，就业在公安机关禁毒部门、禁毒办等。",
        "xuefeng_comment": "禁毒学是公安学类的专业，培养禁毒人才，是国家控制布点专业。就业在公安机关禁毒部门、禁毒办。这个专业需要责任感和奉献精神。适合对禁毒工作感兴趣的学生。就业稳定，工作有一定的危险性和挑战性。对身体素质有要求。",
        "yearly_courses": {"大一": ["法学基础", "禁毒学", "禁毒法", "刑法学"], "大二": ["毒品与成瘾", "犯罪学", "刑事侦查", "社会学"], "大三": ["禁毒实务", "禁毒教育", "禁毒社会工作", "禁毒国际合作"], "大四": ["公安机关禁毒部门实习"]},
        "top_universities": {"domestic": ["中国人民公安大学", "中国刑事警察学院", "云南警官学院", "西南政法大学", "华东政法大学"], "international": ["DEA Academy", "UNODC", "Europol", "RCMP"]}
    }
]

def main():
    print("=" * 70)
    print("⚖️ 开始导入法学类专业（第二批）...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in law_majors_2:
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
