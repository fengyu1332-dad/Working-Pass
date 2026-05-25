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

literature_majors_1 = [
    {
        "code": "050103",
        "name": "古典文献学",
        "category": "05 文学",
        "category_icon": "📚",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "古典文献学是研究中国古代文献的学科，培养从事古典文献整理和研究的专门人才。",
        "what_you_learn": "古典文献学、目录学、校勘学、版本学、文字学、音韵学、训诂学、中国古代文学史",
        "suitable_for": "对中国古典文献和传统文化感兴趣的学生。",
        "career_outlook": "传统文化复兴，就业在古籍研究所、图书馆、出版社、博物馆等。",
        "xuefeng_comment": "古典文献学是中国语言文学类的专业，研究古典文献。就业在古籍研究所、图书馆、出版社、博物馆。这个专业需要对中国古典文献和传统文化有兴趣。适合坐得住、爱读书的学生。就业面相对窄但很稳定。读研比例高。",
        "yearly_courses": {"大一": ["古典文献学", "目录学", "校勘学", "中国古代文学史"], "大二": ["版本学", "文字学", "音韵学", "训诂学"], "大三": ["古籍整理", "经学研究", "史学研究", "文献检索"], "大四": ["古籍研究所或图书馆实习"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "浙江大学", "武汉大学"], "international": ["Harvard", "Oxford", "Cambridge", "SOAS"]}
    },
    {
        "code": "050104T",
        "name": "中国少数民族语言文学",
        "category": "05 文学",
        "category_icon": "🌈",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "中国少数民族语言文学是研究中国少数民族语言文学的学科，培养从事少数民族语言文学研究和教学的专门人才。",
        "what_you_learn": "民族语言学、少数民族文学、民族学、民族政策、少数民族文化、民族史",
        "suitable_for": "对中国少数民族语言文学和文化感兴趣的学生。",
        "career_outlook": "民族事业发展，就业在民委、民族院校、出版社、文化部门等。",
        "xuefeng_comment": "中国少数民族语言文学是中国语言文学类的专业，研究少数民族语言文学。就业在民委、民族院校、出版社、文化部门。这个专业需要对中国少数民族语言文学和文化有兴趣。就业稳定，适合有语言天赋的学生。",
        "yearly_courses": {"大一": ["民族语言学", "少数民族文学", "民族学", "民族政策"], "大二": ["少数民族文化", "民族史", "语言学概论", "中国文学史"], "大三": ["少数民族作家作品研究", "文化人类学", "民俗学", "翻译理论与实践"], "大四": ["民族院校或文化部门实习"]},
        "top_universities": {"domestic": ["中央民族大学", "云南大学", "西南民族大学", "内蒙古大学", "新疆大学"], "international": ["SOAS", "University of California", "University of Michigan", "University of Washington"]}
    },
    {
        "code": "050106T",
        "name": "应用语言学",
        "category": "05 文学",
        "category_icon": "💬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "应用语言学是研究语言学应用的学科，培养从事语言教学、语言测试、语言处理等工作的专业人才。",
        "what_you_learn": "语言学概论、应用语言学、语言教学法、语言测试、计算语言学、社会语言学",
        "suitable_for": "对语言学应用感兴趣的学生。",
        "career_outlook": "语言应用领域广，就业在语言教学、语言测试、语言处理、媒体等。",
        "xuefeng_comment": "应用语言学是中国语言文学类的专业，研究语言学应用。就业在语言教学、语言测试、语言处理、媒体。这个专业需要对语言学应用有兴趣。就业面广，薪资中等。适合对语言教学、语言处理感兴趣的学生。",
        "yearly_courses": {"大一": ["语言学概论", "应用语言学", "普通语音学", "语法学"], "大二": ["语言教学法", "语言测试", "计算语言学", "社会语言学"], "大三": ["心理语言学", "话语分析", "语言规划", "计算语言学"], "大四": ["语言教学或语言处理机构实习"]},
        "top_universities": {"domestic": ["北京语言大学", "北京大学", "复旦大学", "南京大学", "上海交通大学"], "international": ["MIT", "Stanford", "Oxford", "Cambridge"]}
    },
    {
        "code": "050107T",
        "name": "秘书学",
        "category": "05 文学",
        "category_icon": "📋",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "秘书学是培养秘书人才的学科，培养从事秘书工作和行政管理的专业人才。",
        "what_you_learn": "秘书学概论、文书学、档案学、行政管理、办公自动化、应用写作、公共关系学",
        "suitable_for": "对秘书工作和行政管理感兴趣的学生。",
        "career_outlook": "企事业单位都需要，就业在企业、政府部门、事业单位等。",
        "xuefeng_comment": "秘书学是中国语言文学类的专业，培养秘书人才。就业在企业、政府部门、事业单位。这个专业需要细致、耐心，沟通能力强。适合对秘书工作和行政管理感兴趣的学生。就业稳定，薪资中等。",
        "yearly_courses": {"大一": ["秘书学概论", "文书学", "档案学", "行政管理"], "大二": ["办公自动化", "应用写作", "公共关系学", "管理学"], "大三": ["秘书实务", "公文写作", "会议组织", "商务礼仪"], "大四": ["企业或政府部门实习"]},
        "top_universities": {"domestic": ["中国人民大学", "北京大学", "复旦大学", "上海交通大学", "南京大学"], "international": ["Harvard", "Stanford", "Wharton", "Columbia"]}
    },
    {
        "code": "050109T",
        "name": "中国语言与文化",
        "category": "05 文学",
        "category_icon": "🎎",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "中国语言与文化是研究中国语言与文化的学科，培养从事中国语言文化推广和研究的专门人才。",
        "what_you_learn": "中国语言学、中国文化概论、中国文学史、中国思想史、文化人类学、文化传播学",
        "suitable_for": "对中国语言与文化感兴趣的学生。",
        "career_outlook": "文化传播发展，就业在文化机构、媒体、出版社、孔子学院等。",
        "xuefeng_comment": "中国语言与文化是中国语言文学类的专业，研究中国语言与文化。就业在文化机构、媒体、出版社、孔子学院。这个专业需要对中国语言与文化有兴趣。适合对文化传播感兴趣的学生。就业稳定，发展前景好。",
        "yearly_courses": {"大一": ["中国语言学", "中国文化概论", "中国文学史", "中国思想史"], "大二": ["文化人类学", "文化传播学", "中国哲学史", "中国艺术史"], "大三": ["中国文化专题研究", "文化产业管理", "文化政策", "跨文化交际"], "大四": ["文化机构或孔子学院实习"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "中国人民大学", "北京师范大学"], "international": ["Harvard", "Oxford", "Cambridge", "SOAS"]}
    },
    {
        "code": "050110T",
        "name": "国际中文教育",
        "category": "05 文学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "国际中文教育是培养国际中文教师的学科，培养从事国际中文教育的专门人才。",
        "what_you_learn": "汉语国际教育、对外汉语教学法、第二语言习得、跨文化交际、中国文化、教育学、语言学",
        "suitable_for": "英语好、对国际中文教育感兴趣的学生。",
        "career_outlook": "国际中文教育需求增长，就业在孔子学院、国际学校、国际中文教育机构等。",
        "xuefeng_comment": "国际中文教育是中国语言文学类的专业，培养国际中文教师。就业在孔子学院、国际学校、国际中文教育机构。这个专业需要英语好，有跨文化交际能力。适合对国际中文教育感兴趣的学生。就业前景好，有机会到海外工作。",
        "yearly_courses": {"大一": ["汉语国际教育", "对外汉语教学法", "第二语言习得", "语言学"], "大二": ["跨文化交际", "中国文化", "教育学", "心理学"], "大三": ["对外汉语教材编写", "对外汉语测试", "课堂教学技能", "中国现代文学"], "大四": ["孔子学院或国际学校实习"]},
        "top_universities": {"domestic": ["北京语言大学", "北京大学", "复旦大学", "华东师范大学", "北京师范大学"], "international": ["Harvard", "Stanford", "Oxford", "Cambridge"]}
    },
    {
        "code": "050302",
        "name": "广播电视学",
        "category": "05 文学",
        "category_icon": "📺",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "广播电视学是研究广播电视的学科，培养从事广播电视采编工作的专门人才。",
        "what_you_learn": "广播电视学概论、广播电视采访、广播电视写作、广播电视编辑、电视摄像、非线性编辑",
        "suitable_for": "对广播电视工作感兴趣的学生。",
        "career_outlook": "媒体行业发展，就业在广播电视台、新媒体公司、影视公司等。",
        "xuefeng_comment": "广播电视学是新闻传播学类的专业，培养广播电视人才。就业在广播电视台、新媒体公司、影视公司。这个专业需要对广播电视工作有兴趣。适合有创造力、表达能力强的学生。就业稳定，薪资中等。竞争比较激烈。",
        "yearly_courses": {"大一": ["广播电视学概论", "传播学概论", "新闻学概论", "广播电视史"], "大二": ["广播电视采访", "广播电视写作", "广播电视编辑", "电视摄像"], "大三": ["非线性编辑", "广播电视节目策划", "广播电视评论", "媒介经营管理"], "大四": ["广播电视台或新媒体公司实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "复旦大学", "中国人民大学", "武汉大学", "浙江大学"], "international": ["USC Annenberg", "Columbia Journalism", "Northwestern", "NYU Tisch"]}
    },
    {
        "code": "050303",
        "name": "广告学",
        "category": "05 文学",
        "category_icon": "📢",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-26k",
        "overview": "广告学是研究广告的学科，培养从事广告策划和创作的专门人才。",
        "what_you_learn": "广告学概论、广告策划、广告创意、广告文案、广告设计、市场调查、传播学",
        "suitable_for": "对广告和营销感兴趣的学生。",
        "career_outlook": "广告行业发展，就业在广告公司、企业营销部门、媒体等。",
        "xuefeng_comment": "广告学是新闻传播学类的专业，培养广告人才。就业在广告公司、企业营销部门、媒体。这个专业需要对广告和营销有兴趣，有创意。适合有创造力、沟通能力强的学生。就业面广，薪资中等偏上。",
        "yearly_courses": {"大一": ["广告学概论", "传播学概论", "市场营销学", "市场调查"], "大二": ["广告策划", "广告创意", "广告文案", "广告设计"], "大三": ["媒介策划", "品牌管理", "广告效果研究", "消费者行为"], "大四": ["广告公司或企业营销部门实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "复旦大学", "中国人民大学", "武汉大学", "北京大学"], "international": ["NYU", "USC", "Northwestern", "University of Texas"]}
    },
    {
        "code": "050304",
        "name": "传播学",
        "category": "05 文学",
        "category_icon": "📡",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "传播学是研究传播现象的学科，培养从事传播研究和媒体工作的专门人才。",
        "what_you_learn": "传播学概论、传播理论、传播研究方法、媒介社会学、媒介心理学、网络传播、媒体政策",
        "suitable_for": "对传播学和媒体感兴趣的学生。",
        "career_outlook": "媒体行业发展，就业在媒体、互联网公司、公关公司、政府部门等。",
        "xuefeng_comment": "传播学是新闻传播学类的专业，研究传播现象。就业在媒体、互联网公司、公关公司、政府部门。这个专业需要对传播学和媒体有兴趣。就业面广，薪资中等。读研比例高。",
        "yearly_courses": {"大一": ["传播学概论", "传播理论", "新闻学概论", "社会学"], "大二": ["传播研究方法", "媒介社会学", "媒介心理学", "统计学"], "大三": ["网络传播", "媒体政策", "传播学史", "媒介经济学"], "大四": ["媒体或互联网公司实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "复旦大学", "中国人民大学", "北京大学", "武汉大学"], "international": ["USC Annenberg", "Columbia", "Northwestern", "University of Pennsylvania"]}
    },
    {
        "code": "050305T",
        "name": "编辑出版学",
        "category": "05 文学",
        "category_icon": "📖",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "编辑出版学是研究编辑出版的学科，培养从事编辑出版工作的专门人才。",
        "what_you_learn": "编辑学、出版学、出版经营管理、选题策划、书稿编辑、校对、装帧设计",
        "suitable_for": "对编辑出版工作感兴趣的学生。",
        "career_outlook": "出版行业发展，就业在出版社、期刊社、文化公司、新媒体等。",
        "xuefeng_comment": "编辑出版学是新闻传播学类的专业，培养编辑出版人才。就业在出版社、期刊社、文化公司、新媒体。这个专业需要对编辑出版工作有兴趣，文字功底好。适合爱读书、文字好的学生。就业稳定，薪资中等。",
        "yearly_courses": {"大一": ["编辑学、出版学", "传播学概论", "中国文学史", "现代汉语"], "大二": ["出版经营管理", "选题策划", "书稿编辑", "校对"], "大三": ["装帧设计", "出版法规", "数字出版", "媒体营销"], "大四": ["出版社或文化公司实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "复旦大学", "武汉大学", "北京大学", "南京大学"], "international": ["Columbia Journalism", "NYU", "Northwestern", "University of Texas"]}
    },
    {
        "code": "050306T",
        "name": "网络与新媒体",
        "category": "05 文学",
        "category_icon": "💻",
        "difficulty": "⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "网络与新媒体是研究网络和新媒体的学科，培养从事新媒体工作的专门人才。",
        "what_you_learn": "新媒体概论、网络传播学、新媒体编辑、新媒体策划、新媒体技术、数字营销、数据分析",
        "suitable_for": "对网络和新媒体感兴趣的学生。",
        "career_outlook": "新媒体行业爆发，就业在互联网公司、新媒体公司、媒体、企业等。",
        "xuefeng_comment": "网络与新媒体是新闻传播学类的专业，培养新媒体人才。就业在互联网公司、新媒体公司、媒体、企业。这个专业需要对网络和新媒体有兴趣，有一定的技术能力。适合对新技术敏感的学生。就业前景好，薪资较高。",
        "yearly_courses": {"大一": ["新媒体概论", "网络传播学", "传播学概论", "新闻学概论"], "大二": ["新媒体编辑", "新媒体策划", "新媒体技术", "网络文化"], "大三": ["数字营销", "数据分析", "新媒体运营", "媒介经营管理"], "大四": ["互联网公司或新媒体公司实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "复旦大学", "中国人民大学", "浙江大学", "清华大学"], "international": ["USC Annenberg", "Columbia", "NYU", "Northwestern"]}
    },
    {
        "code": "050307T",
        "name": "数字出版",
        "category": "05 文学",
        "category_icon": "📱",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "数字出版是研究数字出版的学科，培养从事数字出版工作的专门人才。",
        "what_you_learn": "数字出版概论、出版学、数字编辑、数字营销、数字出版技术、新媒体编辑、数字内容管理",
        "suitable_for": "对数字出版工作感兴趣的学生。",
        "career_outlook": "数字出版发展，就业在出版社数字出版部门、新媒体公司、互联网公司等。",
        "xuefeng_comment": "数字出版是新闻传播学类的专业，培养数字出版人才。就业在出版社数字出版部门、新媒体公司、互联网公司。这个专业需要对数字出版工作有兴趣，有一定的技术能力。适合对新技术敏感的学生。就业前景好，薪资中等。",
        "yearly_courses": {"大一": ["数字出版概论", "出版学", "传播学概论", "计算机基础"], "大二": ["数字编辑", "数字营销", "数字出版技术", "新媒体编辑"], "大三": ["数字内容管理", "电子出版", "移动出版", "数字版权"], "大四": ["出版社或互联网公司实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "复旦大学", "武汉大学", "南京大学", "北京印刷学院"], "international": ["Columbia", "NYU", "MIT", "Stanford"]}
    },
    {
        "code": "050308T",
        "name": "时尚传播",
        "category": "05 文学",
        "category_icon": "👗",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "时尚传播是研究时尚传播的学科，培养从事时尚传播工作的专门人才。",
        "what_you_learn": "时尚传播概论、传播学概论、时尚史、时尚产业、时尚营销、时尚摄影、时尚编辑",
        "suitable_for": "对时尚和传播感兴趣的学生。",
        "career_outlook": "时尚产业发展，就业在时尚媒体、时尚品牌、公关公司、营销公司等。",
        "xuefeng_comment": "时尚传播是新闻传播学类的新兴专业，培养时尚传播人才。就业在时尚媒体、时尚品牌、公关公司、营销公司。这个专业需要对时尚和传播有兴趣，有时尚敏感度。适合喜欢时尚的学生。就业前景好，薪资中等。",
        "yearly_courses": {"大一": ["时尚传播概论", "传播学概论", "时尚史", "时尚产业"], "大二": ["时尚营销", "时尚摄影", "时尚编辑", "品牌管理"], "大三": ["时尚公关", "时尚媒体策划", "时尚评论", "跨文化时尚"], "大四": ["时尚媒体或时尚品牌实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "东华大学", "上海视觉艺术学院", "北京服装学院", "中央美术学院"], "international": ["Parsons", "FIT", "Central Saint Martins", "NYU"]}
    }
]

def main():
    print("=" * 70)
    print("📚 开始导入文学类专业（第一批）...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in literature_majors_1:
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
