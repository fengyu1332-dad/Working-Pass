import urllib.request
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

law_majors = [
    {
        "code": "030101K",
        "name": "法学",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "法学是研究法律现象和法律规律的学科，培养掌握法律知识和法律实务技能的专业人才。",
        "what_you_learn": "法理学、宪法学、民法学、刑法学、商法学、民事诉讼法、刑事诉讼法、行政法与行政诉讼法",
        "suitable_for": "逻辑思维强、语言表达能力好、对法律感兴趣的学生。",
        "career_outlook": "法律人才需求稳定，就业方向包括律师、法官、检察官、企业法务、公务员等。",
        "xuefeng_comment": "法学是比较热门的文科专业，就业方向明确。但要提醒大家，法学专业门槛越来越高，司考改革后需要法律职业资格证。就业竞争激烈，顶尖律所对学校背景要求很高。建议报考五院四系等法学强校。如果想做律师，建议读研读博，并尽早实习积累经验。这个专业适合逻辑思维强、语言表达能力好的学生。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "中国法制史", "法律英语"], "大二": ["民法学", "刑法学", "行政法", "民事诉讼法"], "大三": ["刑事诉讼法", "商法学", "知识产权法", "国际法"], "大四": ["律所实习", "司法考试准备"]},
        "top_universities": {"domestic": ["中国政法大学", "北京大学", "中国人民大学", "武汉大学", "华东政法大学"], "international": ["Harvard Law", "Yale Law", "Stanford Law", "Oxford"]}
    },
    {
        "code": "030102K",
        "name": "知识产权",
        "category": "03 法学",
        "category_icon": "©️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "知识产权专业培养掌握专利、商标、著作权等知识产权法律知识和实务技能的专业人才。",
        "what_you_learn": "知识产权法、专利法、商标法、著作权法、知识产权实务、知识产权管理、科技法",
        "suitable_for": "对知识产权保护和科技法律感兴趣、有理工科背景的学生。",
        "career_outlook": "科技创新推动知识产权保护需求增长，就业在知识产权律所、专利事务所、科技企业法务等。",
        "xuefeng_comment": "知识产权是比较有前景的法律专业方向，随着科技创新和知识产权保护意识提高，这个领域需求增长。就业方向包括知识产权律所、专利事务所、科技企业法务、知识产权局等。建议有理工科背景的学生报考，这样在处理专利等事务时更有优势。薪资待遇不错，但需要不断学习新的科技知识。",
        "yearly_courses": {"大一": ["法理学", "宪法学", "民法", "知识产权导论"], "大二": ["专利法", "商标法", "著作权法", "民诉法"], "大三": ["知识产权实务", "知识产权管理", "科技法", "国际知识产权法"], "大四": ["知识产权机构实习"]},
        "top_universities": {"domestic": ["中国政法大学", "北京大学", "华东政法大学", "西南政法大学", "上海大学"], "international": ["Harvard Law", "Stanford Law", "LSE", "University of Melbourne"]}
    },
    {
        "code": "030201",
        "name": "政治学与行政学",
        "category": "03 法学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "政治学与行政学是研究政治现象和行政管理的学科，培养从事公共管理和政策研究的人才。",
        "what_you_learn": "政治学原理、行政管理学、公共政策分析、中外政治制度、行政法学、公共经济学",
        "suitable_for": "对政治和公共事务感兴趣、有社会责任感的学生。",
        "career_outlook": "政府机构、事业单位、公共政策研究机构等需要政治学人才，就业相对稳定。",
        "xuefeng_comment": "政治学与行政学是比较传统的文科专业，就业主要在政府机构、事业单位、公共政策研究机构等。工作相对稳定，但薪资水平一般。这个专业适合对政治和公共事务感兴趣、有社会责任感的学生。考公务员是这个专业的重要出路之一。建议读研读博提升竞争力，未来可以去高校或研究机构工作。",
        "yearly_courses": {"大一": ["政治学原理", "管理学原理", "法学概论", "社会学"], "大二": ["行政管理学", "公共政策分析", "中外政治制度", "行政法学"], "大三": ["公共经济学", "组织行为学", "公共部门人力资源管理"], "大四": ["政府部门实习"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "中国人民大学", "清华大学", "南开大学"], "international": ["Harvard", "Stanford", "Oxford", "Cambridge"]}
    },
    {
        "code": "030302",
        "name": "社会工作",
        "category": "03 法学",
        "category_icon": "🤝",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "社会工作是研究社会问题解决和社会服务的学科，培养从事社会服务和社会管理的专业人才。",
        "what_you_learn": "社会工作概论、社会学概论、社会心理学、个案工作、小组工作、社区工作、社会政策",
        "suitable_for": "有爱心、有耐心、善于与人沟通、关注社会问题的学生。",
        "career_outlook": "社会服务需求增长，社会工作人才在社区、民政部门、公益组织等有稳定需求。",
        "xuefeng_comment": "社会工作是比较特殊的专业，强调社会服务和助人自助。就业主要在社区服务中心、民政部门、公益组织、社会工作机构等。工作相对稳定，但薪资水平不高。这个专业需要有爱心、有耐心、善于与人沟通的学生。适合关注社会问题、想为社会做出贡献的学生。可以考取社会工作师职业资格证。",
        "yearly_courses": {"大一": ["社会学概论", "社会工作概论", "社会心理学", "管理学原理"], "大二": ["个案工作", "小组工作", "社区工作", "社会调查研究方法"], "大三": ["社会政策", "社会保障", "社会工作实务", "社会工作伦理"], "大四": ["社会工作机构实习"]},
        "top_universities": {"domestic": ["北京大学", "中国人民大学", "复旦大学", "华东师范大学", "中山大学"], "international": ["Columbia", "NYU", "University of Chicago", "LSE"]}
    },
    {
        "code": "030601",
        "name": "治安学",
        "category": "03 法学",
        "category_icon": "👮",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "治安学是研究社会治安管理和安全防范的学科，培养从事公安工作和安全管理的专业人才。",
        "what_you_learn": "治安管理学、公安学基础理论、犯罪学、治安案件查处、安全防范技术、公安法规",
        "suitable_for": "对公安工作和安全管理感兴趣、有正义感的学生。",
        "career_outlook": "公安机关、国家安全部门、企事业单位安全管理等需要治安学人才，就业稳定。",
        "xuefeng_comment": "治安学是公安类专业，就业主要在公安机关、国家安全部门、企事业单位安全管理等。工作相对稳定，但可能需要轮班或值夜班。对体能有一定要求。这个专业适合有正义感、愿意为社会安全做出贡献的学生。需要通过招警考试进入公安系统。工作有一定危险性，需要有心理准备。",
        "yearly_courses": {"大一": ["公安学基础理论", "法学概论", "刑法学", "刑事诉讼法"], "大二": ["治安管理学", "犯罪学", "治安案件查处", "公安法规"], "大三": ["安全防范技术", "公安情报学", "户政管理", "交通管理"], "大四": ["公安实习"]},
        "top_universities": {"domestic": ["中国人民公安大学", "中国刑事警察学院", "中国人民警察大学", "西南政法大学", "华东政法大学"], "international": ["FBI Academy", "Met Police College", "Australian Federal Police College"]}
    }
]

def main():
    print("=" * 70)
    print("⚖️ 开始导入法学专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in law_majors:
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
