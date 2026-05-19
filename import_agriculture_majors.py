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

agriculture_majors = [
    {
        "code": "090101",
        "name": "农学",
        "category": "09 农学",
        "category_icon": "🌾",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "农学是研究农作物生产和农业技术的学科，培养从事作物栽培、育种和农业管理的专业人才。",
        "what_you_learn": "作物栽培学、作物育种学、植物生理学、土壤学、农业生态学、农业经济学",
        "suitable_for": "对农业生产和植物科学感兴趣、愿意从事农业工作的学生。",
        "career_outlook": "农业现代化和乡村振兴，农学人才需求稳定。就业在农业科研机构、农业企业、农业技术推广部门等。",
        "xuefeng_comment": "农学是比较传统的农业类专业，就业主要在农业科研机构、农业企业、农业技术推广部门等。工作相对稳定，但薪资水平一般。需要经常去田间地头，工作环境相对艰苦。男生比较适合报考。可以考取农业技术员资格证。随着乡村振兴，这个专业的重要性会越来越突出。",
        "yearly_courses": {"大一": ["植物学", "植物生理学", "土壤学", "农业气象学"], "大二": ["作物栽培学", "作物育种学", "农业生态学", "遗传学"], "大三": ["农业经济学", "农业推广学", "作物病虫害防治", "农业机械化"], "大四": ["农业生产实习"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "浙江大学", "华中农业大学", "山东农业大学"], "international": ["Cornell", "University of California Davis", "Wageningen University", "University of Illinois"]}
    },
    {
        "code": "090301",
        "name": "动物科学",
        "category": "09 农学",
        "category_icon": "🐄",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "动物科学是研究动物生产和动物生物技术的学科，培养从事动物养殖、育种和动物营养的专业人才。",
        "what_you_learn": "动物生理学、动物营养学、动物繁殖学、动物育种学、畜牧生产学、动物行为学",
        "suitable_for": "对动物养殖和动物科学感兴趣、不怕脏不怕累的学生。",
        "career_outlook": "畜牧业发展和食品安全，动物科学人才需求稳定。就业在养殖场、饲料企业、畜牧科研机构等。",
        "xuefeng_comment": "动物科学是比较有特色的农业类专业，就业主要在养殖场、饲料企业、畜牧科研机构等。工作相对稳定，但工作环境可能比较艰苦，需要和动物打交道。男生比较适合报考。可以考取畜牧师资格证。随着人们对食品安全的关注，这个专业的重要性会越来越突出。",
        "yearly_courses": {"大一": ["动物解剖学", "动物生理学", "动物生物化学", "微生物学"], "大二": ["动物营养学", "动物繁殖学", "动物育种学", "遗传学"], "大三": ["畜牧生产学", "动物行为学", "饲料科学", "动物疫病防治"], "大四": ["畜牧企业实习"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "华中农业大学", "四川农业大学", "东北农业大学"], "international": ["Cornell", "University of California Davis", "Texas A&M", "University of Guelph"]}
    },
    {
        "code": "090401",
        "name": "动物医学",
        "category": "09 农学",
        "category_icon": "🩺",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "动物医学是研究动物疾病诊断和治疗的学科，培养从事动物医疗和兽医工作的专业人才。",
        "what_you_learn": "动物解剖学、动物生理学、动物病理学、兽医药理学、兽医临床诊断学、兽医外科学",
        "suitable_for": "对动物医疗感兴趣、不怕脏不怕累、有爱心的学生。",
        "career_outlook": "宠物经济和畜牧业发展，兽医人才需求增长。就业在宠物医院、养殖场、兽医科研机构等。",
        "xuefeng_comment": "动物医学是比较热门的农业类专业，就业主要在宠物医院、养殖场、兽医科研机构等。工作相对稳定，薪资水平中等。需要有爱心、不怕脏不怕累。男生女生都适合报考。可以考取执业兽医资格证。随着宠物经济的发展，这个专业的前景越来越广阔。",
        "yearly_courses": {"大一": ["动物解剖学", "动物生理学", "动物生物化学", "微生物学"], "大二": ["动物病理学", "兽医药理学", "兽医免疫学", "兽医临床诊断学"], "大三": ["兽医外科学", "兽医内科学", "兽医传染病学", "兽医产科学"], "大四": ["兽医临床实习"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "华中农业大学", "华南农业大学", "四川农业大学"], "international": ["Cornell", "University of California Davis", "Texas A&M", "University of Guelph"]}
    },
    {
        "code": "090501",
        "name": "林学",
        "category": "09 农学",
        "category_icon": "🌲",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "林学是研究森林培育和森林资源管理的学科，培养从事林业生产和森林保护的专业人才。",
        "what_you_learn": "森林培育学、森林生态学、林木遗传育种学、森林保护学、森林经理学、测树学",
        "suitable_for": "对林业和环境保护感兴趣、愿意在户外工作的学生。",
        "career_outlook": "生态文明建设和林业发展，林学人才需求稳定。就业在林业部门、林场、林业科研机构等。",
        "xuefeng_comment": "林学是比较传统的林业类专业，就业主要在林业部门、林场、林业科研机构等。工作相对稳定，但工作环境可能比较艰苦，需要经常在户外工作。男生比较适合报考。可以考取林业工程师资格证。随着生态文明建设，这个专业的重要性会越来越突出。",
        "yearly_courses": {"大一": ["植物学", "植物生理学", "土壤学", "气象学"], "大二": ["森林生态学", "林木遗传育种学", "森林培育学", "测量学"], "大三": ["森林保护学", "森林经理学", "测树学", "林业经济管理"], "大四": ["林场实习"]},
        "top_universities": {"domestic": ["北京林业大学", "南京林业大学", "东北林业大学", "西南林业大学", "浙江农林大学"], "international": ["University of British Columbia", "University of Washington", "University of Freiburg", "University of Helsinki"]}
    },
    {
        "code": "090801",
        "name": "水产养殖学",
        "category": "09 农学",
        "category_icon": "🐟",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "水产养殖学是研究水产动物养殖和水产资源保护的学科，培养从事水产养殖和渔业管理的专业人才。",
        "what_you_learn": "水产动物生理学、水产动物营养学、水产养殖学、水产动物疾病防治、渔业资源学、水产工程",
        "suitable_for": "对水产养殖和海洋生物感兴趣、愿意在水边工作的学生。",
        "career_outlook": "水产养殖业发展和海洋资源保护，水产养殖人才需求稳定。就业在水产养殖场、渔业部门、水产科研机构等。",
        "xuefeng_comment": "水产养殖学是比较有特色的农业类专业，就业主要在水产养殖场、渔业部门、水产科研机构等。工作相对稳定，但工作环境可能比较艰苦，需要在水边工作。男生比较适合报考。可以考取水产养殖技术员资格证。随着人们对水产品需求的增长，这个专业的前景不错。",
        "yearly_courses": {"大一": ["水生生物学", "水产动物生理学", "化学", "微生物学"], "大二": ["水产动物营养学", "水产养殖学", "遗传学", "水化学"], "大三": ["水产动物疾病防治", "渔业资源学", "水产工程", "水产经济管理"], "大四": ["水产养殖场实习"]},
        "top_universities": {"domestic": ["中国海洋大学", "上海海洋大学", "华中农业大学", "大连海洋大学", "广东海洋大学"], "international": ["University of British Columbia", "University of Florida", "Wageningen University", "Tokyo University of Marine Science"]}
    }
]

def main():
    print("=" * 70)
    print("🌾 开始导入农学专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in agriculture_majors:
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
