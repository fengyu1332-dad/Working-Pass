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
        if e.code == 409:
            return False, 409
        return False, e.code

more_medical = [
    {
        "code": "100102T",
        "name": "生物育种科学",
        "category": "10 医学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-20k",
        "overview": "医学检验技术是研究临床标本检验方法和技术的技术学科。本专业培养掌握血液学、临床生化、免疫学、微生物学检验等专业技能的检验技师。",
        "what_you_learn": "临床基础检验学、临床血液学检验、临床生化检验、临床免疫学检验、临床微生物学检验、分子诊断学、实验室管理学",
        "suitable_for": "动手能力强、细心耐心的学生。检验科工作需要高度细心，避免出错。",
        "career_outlook": "医学检验是医院的重要辅助科室，检验项目日益增多。毕业生可在医院检验科、第三方检验机构、疾控中心、血站等从事检验工作。",
        "xuefeng_comment": "医学检验技术是医技类专业中的热门方向，就业主要在医院的检验科或第三方检验机构。工作相对稳定，不需要值夜班（多数情况），也不需要与患者过多接触。薪资水平在医技类中属于中等偏上。这个专业是理学学位，不需要考执业医师资格证。适合追求稳定工作环境的女生报考。可以考取检验技师资格证，提升职业发展空间。",
        "yearly_courses": {"大一": ["生物化学", "生理学", "病理学", "医学检验导论"], "大二": ["临床基础检验学", "临床血液学检验", "临床生化检验"], "大三": ["临床免疫学检验", "临床微生物学检验", "分子诊断学"], "大四": ["检验科实习"]},
        "top_universities": {"domestic": ["上海交通大学", "华中科技大学", "四川大学", "温州医科大学"], "international": ["Johns Hopkins", "University of Toronto", " King's College London"]}
    },
    {
        "code": "100302T",
        "name": "麻醉学",
        "category": "10 医学",
        "category_icon": "💉",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥18k-40k",
        "overview": "麻醉学是研究临床麻醉、重症监测治疗和疼痛诊疗的医学学科。本专业培养掌握麻醉学理论知识和临床技能的专业医学人才。",
        "what_you_learn": "麻醉解剖学、麻醉生理学、麻醉药理学、临床麻醉学、重症监测治疗学、疼痛诊疗学、麻醉设备学、急救复苏学",
        "suitable_for": "心理素质好、应急能力强、对麻醉学感兴趣的学生。麻醉医生责任重大，需要在手术中保持高度警觉。",
        "career_outlook": "麻醉医生缺口大，是医院最紧缺的人才之一。手术量持续增长，对麻醉医生需求旺盛。就业主要在各级医院麻醉科、ICU、疼痛科。",
        "xuefeng_comment": "麻醉学是医学类中的黄金专业之一，就业率极高，薪资待遇也好。但我要提醒大家，麻醉医生工作压力大、责任大，一台手术的成功与否，麻醉医生功不可没。工作需要高度专注，术中患者的一切生命体征都靠麻醉医生维护。需要有强大的心理素质和应急能力。就业确实不愁，但工作强度不小。读研读博能去更好的医院。适合对医学有热情、能承受工作压力的学生。",
        "yearly_courses": {"大一": ["人体解剖学", "生物化学", "生理学", "麻醉学导论"], "大二": ["病理学", "药理学", "诊断学", "内科学"], "大四": ["临床麻醉学", "重症监测治疗学", "疼痛诊疗学"], "大五": ["麻醉科实习"]},
        "top_universities": {"domestic": ["华中科技大学", "上海交通大学", "四川大学", "中南大学", "首都医科大学"], "international": ["Harvard Medical", "Johns Hopkins", "UCL", "Stanford"]}
    },
    {
        "code": "100601T",
        "name": "法医学",
        "category": "10 医学",
        "category_icon": "🔍",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-25k",
        "overview": "法医学是应用医学、生物学及其他自然科学理论和技术解决法律问题的医学学科。本专业培养掌握法医学鉴定、检验等专业知识的专业人才。",
        "what_you_learn": "法医病理学、法医临床学、法医物证学、法医毒理学、法医精神病学、法医人类学、司法鉴定学",
        "suitable_for": "对法医学感兴趣、心理素质好、能面对各种案件现场的学生。法医工作需要严谨细致，有强大的心理承受能力。",
        "career_outlook": "司法鉴定需求增长，法医学专业人才需求稳定。毕业生可在公安、检察院、法院、司法鉴定机构、保险理赔部门等从事法医学鉴定工作。",
        "xuefeng_comment": "法医学是比较特殊的医学专业，就业方向比较明确，主要是公检法系统和司法鉴定机构。工作相对稳定，但薪资水平不如临床医生。这个专业需要面对各种案件现场和遗体，对心理素质要求很高。另外，部分岗位可能需要值夜班或随时待命。如果立志成为法医，建议提前了解这个职业的真实工作状态。读研读博能去更好的鉴定机构或高校任教。适合对法律和医学都有兴趣的学生报考。",
        "yearly_courses": {"大一": ["人体解剖学", "生物化学", "生理学", "法医学导论"], "大二": ["病理学", "药理学", "内科学", "外科学"], "大三": ["法医病理学", "法医临床学", "法医物证学", "法医毒理学"], "大四": ["法医鉴定实习"]},
        "top_universities": {"domestic": ["华中科技大学", "四川大学", "山西医科大学", "中国医科大学", "西安交通大学"], "international": ["University of Pennsylvania", "University of Montreal", "University of Sydney"]}
    }
]

def main():
    print("=" * 60)
    print("继续导入医学专业...")
    print("=" * 60)
    
    success = failed = skipped = 0
    
    for major in more_medical:
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