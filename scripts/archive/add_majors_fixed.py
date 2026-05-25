
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

majors_to_add = [
    {
        "code": "070603",
        "name": "应用气象学",
        "category": "07 理学",
        "category_icon": "🌤️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "应用气象学专业培养掌握气象学理论和应用技能的人才，能在气象、民航、农业等部门从事相关工作。",
        "what_you_learn": "大气科学、气象学、气候学、大气探测、天气学原理、应用气象学、农业气象学、民航气象",
        "suitable_for": "对气象科学有兴趣、有志于气象事业的学生。",
        "career_outlook": "气象部门、环保、民航、农业等领域对应用气象人才需求稳定。",
        "xuefeng_comment": "应用气象学专业实用性强，就业领域广，工作稳定。可以在气象局、民航、农业部门等工作。建议对气象科学有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "大气科学概论", "计算机基础"], "大二": ["气象学", "气候学", "大气探测", "天气学原理"], "大三": ["应用气象学", "农业气象学", "民航气象", "气象统计"], "大四": ["毕业实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京信息工程大学", "成都信息工程大学", "南京大学", "兰州大学"], "international": ["MIT", "Stanford", "Cambridge"]}
    },
    {
        "code": "070401",
        "name": "天文学",
        "category": "07 理学",
        "category_icon": "🔭",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "天文学专业培养掌握天文学理论和观测技能的人才，从事天文研究和科普工作。",
        "what_you_learn": "天体物理学、天体力学、天文观测、宇宙学、天文学史、射电天文学",
        "suitable_for": "对宇宙星空有浓厚兴趣、有志于天文研究的学生。",
        "career_outlook": "科研院所、天文台、高校、科普机构等对天文学人才有需求。",
        "xuefeng_comment": "天文学是基础前沿学科，适合热爱科学研究的学生。建议继续深造，未来可在科研机构、高校工作。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "天文学导论", "计算机基础"], "大二": ["天体物理学", "天体力学", "光学", "原子物理"], "大三": ["天文观测、宇宙学", "射电天文学", "天文学史"], "大四": ["天文台实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京大学", "北京大学", "中国科学技术大学", "北京师范大学"], "international": ["MIT", "Caltech", "Harvard"]}
    },
    {
        "code": "070702",
        "name": "海洋技术",
        "category": "07 理学",
        "category_icon": "🌊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-23k",
        "overview": "海洋技术专业培养掌握海洋技术理论和实践技能的人才，从事海洋探测、海洋工程等工作。",
        "what_you_learn": "海洋学、海洋探测、海洋技术装备、海洋环境保护、物理海洋学、海洋遥感",
        "suitable_for": "对海洋科学有兴趣、有志于海洋事业的学生。",
        "career_outlook": "海洋战略是国家战略，海洋技术人才需求持续增长。",
        "xuefeng_comment": "海洋技术专业应用前景好，可在海洋部门、科研院所、涉海企业工作。建议对海洋有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "海洋学导论", "计算机基础"], "大二": ["物理海洋学", "海洋探测、海洋化学", "海洋生物学"], "大三": ["海洋技术装备", "海洋环境保护", "海洋遥感", "海洋信息处理"], "大四": ["海洋机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国海洋大学", "厦门大学", "上海海洋大学", "同济大学"], "international": ["MIT", "Woods Hole", "Scripps"]}
    },
    {
        "code": "030603TK",
        "name": "边防管理",
        "category": "03 法学",
        "category_icon": "🛂",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "边防管理专业培养从事边防管理工作的专门人才，保障国门安全。",
        "what_you_learn": "边防管理、边防检查、边境管理、边防法学、涉外警务",
        "suitable_for": "有志于公安边防事业的学生。",
        "career_outlook": "公安边防部门对边防管理人才有稳定需求。",
        "xuefeng_comment": "边防管理专业就业定向明确，工作稳定，待遇好。建议有志于公安边防事业的同学报考。",
        "yearly_courses": {"大一": ["法学基础", "边防管理概论", "管理学基础", "大学英语"], "大二": ["边防检查", "边境管理", "边防法学", "涉外警务"], "大三": ["边防情报", "边防战术", "边防指挥", "边境涉外工作"], "大四": ["边防部队实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民公安大学", "中国人民警察大学", "武警警官学院"], "international": []}
    },
    {
        "code": "030606TK",
        "name": "经济犯罪侦查",
        "category": "03 法学",
        "category_icon": "💰",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "经济犯罪侦查专业培养从事经济犯罪侦查工作的专门人才，打击各类经济犯罪活动。",
        "what_you_learn": "经济犯罪侦查、司法会计、经济法学、刑事侦查学、刑法学",
        "suitable_for": "有志于公安经侦事业的学生。",
        "career_outlook": "公安经济犯罪侦查部门对经侦人才有稳定需求。",
        "xuefeng_comment": "经济犯罪侦查专业实用性强，在打击经济犯罪中发挥重要作用。建议有志于公安经侦事业的同学报考。",
        "yearly_courses": {"大一": ["法学基础", "刑法学", "刑事诉讼法", "管理学基础"], "大二": ["刑事侦查学", "司法会计", "经济法学", "民法学"], "大三": ["经济犯罪侦查、金融犯罪侦查", "涉税犯罪侦查", "走私犯罪侦查"], "大四": ["公安经侦部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民公安大学", "中国刑事警察学院", "西南政法大学"], "international": []}
    },
    {
        "code": "100802",
        "name": "中药资源与开发",
        "category": "10 医学",
        "category_icon": "🌿",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "中药资源与开发专业培养中药资源保护开发的专门人才，从事中药资源调查、开发和利用工作。",
        "what_you_learn": "中药学、药用植物学、中药资源学、中药鉴定学、中药栽培学、中药炮制学",
        "suitable_for": "对中医药有兴趣的学生。",
        "career_outlook": "中医药复兴，中药资源专业前景好。",
        "xuefeng_comment": "中药资源与开发是中医药类专业，可在中药企业、药检所、科研院所工作。建议对中医药有兴趣的同学报考。",
        "yearly_courses": {"大一": ["中医学基础", "中药学", "药用植物学", "有机化学"], "大二": ["中药资源学", "中药鉴定学", "中药栽培学", "方剂学"], "大三": ["中药炮制学", "天然药物化学", "中药药理学", "中药材加工"], "大四": ["中药企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京中医药大学", "中国药科大学", "北京中医药大学", "广州中医药大学"], "international": []}
    },
    {
        "code": "101004",
        "name": "眼视光学",
        "category": "10 医学",
        "category_icon": "👁️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "眼视光学专业培养眼视光医疗保健专门人才，从事视力矫正、眼病防治等工作。",
        "what_you_learn": "眼科学、视光学、眼镜学、角膜接触镜学、斜视弱视、视觉训练",
        "suitable_for": "对眼视光有兴趣的学生。",
        "career_outlook": "医院眼科、视光中心、眼镜企业等对眼视光人才有需求。",
        "xuefeng_comment": "眼视光学专业就业好，创业机会多。可以在医院、视光中心工作，也可以自己创业。建议对眼视光有兴趣的同学报考。",
        "yearly_courses": {"大一": ["人体解剖学", "生理学", "眼科学基础", "大学物理"], "大二": ["眼科学", "视光学", "眼镜学", "角膜接触镜学"], "大三": ["斜视弱视、视觉训练", "低视力康复", "眼视光器械学"], "大四": ["医院眼科实习", "毕业论文"]},
        "top_universities": {"domestic": ["温州医科大学", "天津医科大学", "南京医科大学", "中山大学"], "international": ["UC Berkeley", "University of Melbourne"]}
    },
    {
        "code": "120603",
        "name": "采购管理",
        "category": "12 管理学",
        "category_icon": "🛒",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "采购管理专业培养采购与供应链管理人才，从事企业采购、供应链优化等工作。",
        "what_you_learn": "采购管理、供应链管理、物流管理、谈判学、供应商管理、成本控制",
        "suitable_for": "对采购供应链有兴趣的学生。",
        "career_outlook": "采购与供应链管理日益重要，专才需求大。",
        "xuefeng_comment": "采购管理专业实用性强，可在工商企业、物流企业、政府采购部门工作。建议对采购供应链有兴趣的同学报考。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "物流学基础", "商务英语"], "大二": ["采购管理、供应链管理", "物流管理", "市场营销"], "大三": ["谈判学", "供应商管理", "成本控制", "采购法务"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京物资学院", "浙江工商大学", "上海海事大学", "天津理工大学"], "international": ["MIT", "Michigan State", "INSEAD"]}
    },
    {
        "code": "090103",
        "name": "植物保护",
        "category": "09 农学",
        "category_icon": "🌱",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "植物保护专业培养植物病虫害防治技术人才，从事农业生产中的病虫害防治工作。",
        "what_you_learn": "植物病理学、昆虫学、农药学、植物化学保护、植物检疫、杂草学",
        "suitable_for": "对农业和植物保护有兴趣的学生。",
        "career_outlook": "植物保护是农业生产的重要保障，专业性强。",
        "xuefeng_comment": "植物保护专业是农学类专业，可在农业部门、农技推广、农药企业工作。建议对农业有兴趣的同学报考。",
        "yearly_courses": {"大一": ["植物学、生物化学", "微生物学、农业气象学"], "大二": ["植物病理学、昆虫学", "农业生态学，化学"], "大三": ["农药学、植物化学保护", "植物检疫、杂草学"], "大四": ["农业部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "西北农林科技大学", "浙江大学"], "international": ["Cornell", "UC Davis", "Wageningen"]}
    },
    {
        "code": "090202",
        "name": "茶学",
        "category": "09 农学",
        "category_icon": "🍵",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "茶学专业培养茶叶生产加工和茶文化专业人才，从事茶叶生产、加工、审评和营销工作。",
        "what_you_learn": "茶树栽培学、茶叶加工学、茶叶审评、茶文化、茶叶化学、茶叶营销",
        "suitable_for": "对茶文化和茶产业有兴趣的学生。",
        "career_outlook": "茶学专业特色鲜明，中国茶文化底蕴深厚。",
        "xuefeng_comment": "茶学专业特色鲜明，可在茶企业、茶场、茶叶研究所工作，也可以从事茶文化传播。建议对茶文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["植物学、生物化学", "食品化学", "茶学概论"], "大二": ["茶树栽培学、茶叶加工学", "茶叶审评、茶文化"], "大三": ["茶叶化学、茶叶营销", "茶叶深加工、茶叶机械"], "大四": ["茶企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["安徽农业大学", "浙江大学", "湖南农业大学", "福建农林大学"], "international": []}
    },
    {
        "code": "050238",
        "name": "荷兰语",
        "category": "05 文学",
        "category_icon": "🇳🇱",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "荷兰语专业培养掌握荷兰语语言文学的复合型人才，从事荷兰语翻译、教学和研究工作。",
        "what_you_learn": "荷兰语语音、语法、口语、阅读、写作、文学、文化、跨文化交际",
        "suitable_for": "对荷兰及北欧语言文化有兴趣的学生。",
        "career_outlook": "外事、经贸、教育、文化、旅游等领域对荷兰语人才有需求。",
        "xuefeng_comment": "荷兰语虽是小语种，但在国际贸易和文化交流中很实用。建议对荷兰文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["荷兰语语音、基础荷兰语", "荷兰文化概况", "英语"], "大二": ["荷兰语语法、中级荷兰语", "荷兰文学选读", "荷兰社会"], "大三": ["高级荷兰语、翻译理论与实践", "荷兰史", "经贸荷兰语"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "广东外语外贸大学"], "international": ["Leiden University", "Amsterdam University"]}
    },
    {
        "code": "050240",
        "name": "瑞典语",
        "category": "05 文学",
        "category_icon": "🇸🇪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "瑞典语专业培养掌握瑞典语语言文学的专门人才，从事瑞典语翻译、教学和研究工作。",
        "what_you_learn": "瑞典语语音、语法、口语、阅读、写作、文学、文化、跨文化交际",
        "suitable_for": "对瑞典及北欧语言文化有兴趣的学生。",
        "career_outlook": "外事、经贸、教育、文化、旅游等领域对瑞典语人才有需求。",
        "xuefeng_comment": "瑞典是创新强国，瑞典语人才在相关领域很有价值。建议对瑞典文化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["瑞典语语音、基础瑞典语", "瑞典文化概况", "英语"], "大二": ["瑞典语语法、中级瑞典语", "瑞典文学选读", "瑞典社会"], "大三": ["高级瑞典语、翻译理论与实践", "瑞典史", "经贸瑞典语"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学"], "international": ["Stockholm University", "Lund University"]}
    }
]

def main():
    print("=" * 70)
    print("📊 开始补充专业数据...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in majors_to_add:
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
