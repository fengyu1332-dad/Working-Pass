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

education_majors = [
    {
        "code": "040103",
        "name": "特殊教育",
        "category": "04 教育学",
        "category_icon": "🧑‍🦯",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-16k",
        "overview": "特殊教育是研究特殊儿童教育规律和方法的学科，培养从事特殊教育教学和研究的专业人才。",
        "what_you_learn": "特殊教育学、特殊儿童心理学、特殊教育课程与教学、行为矫正、手语、康复训练",
        "suitable_for": "有爱心、有耐心、善于与特殊儿童沟通、关注特殊教育事业的学生。",
        "career_outlook": "特殊教育事业发展，特殊教育教师需求增长。就业在特殊教育学校、康复机构、残联等。",
        "xuefeng_comment": "特殊教育是比较有意义的专业，需要有爱心和耐心。就业主要在特殊教育学校、康复机构、残联等。工作相对稳定，但薪资水平不高。这个专业适合有爱心、愿意为特殊儿童教育事业做出贡献的学生。女生比较适合报考。可以考取特殊教育教师资格证。",
        "yearly_courses": {"大一": ["教育学原理", "普通心理学", "特殊教育导论", "教育心理学"], "大二": ["特殊教育学", "特殊儿童心理学", "发展心理学", "手语"], "大三": ["特殊教育课程与教学", "行为矫正", "康复训练", "融合教育"], "大四": ["特殊教育学校实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "华中师范大学", "西南大学", "陕西师范大学"], "international": ["University of Birmingham", "University of Manchester", "UCLA", "University of Toronto"]}
    },
    {
        "code": "040105",
        "name": "学前教育",
        "category": "04 教育学",
        "category_icon": "👶",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-15k",
        "overview": "学前教育是研究幼儿教育规律和方法的学科，培养从事幼儿园教育教学和管理的专业人才。",
        "what_you_learn": "学前教育学、学前儿童心理学、幼儿园课程与教学、幼儿游戏、幼儿卫生保健、幼儿文学",
        "suitable_for": "喜欢孩子、有耐心、有爱心、善于与幼儿沟通的学生。",
        "career_outlook": "学前教育普及，幼儿园教师需求持续增长。就业在幼儿园、早教机构、学前教育研究机构等。",
        "xuefeng_comment": "学前教育是非常适合女生的专业，就业主要在幼儿园、早教机构等。工作相对稳定，但薪资水平不高。需要有耐心、有爱心、喜欢孩子。可以考取幼儿园教师资格证。随着二胎三胎政策，学前教育需求增长。但工作压力也不小，需要不断学习和提升自己。",
        "yearly_courses": {"大一": ["教育学原理", "普通心理学", "学前教育导论", "乐理与视唱"], "大二": ["学前教育学", "学前儿童心理学", "幼儿卫生保健", "舞蹈基础"], "大三": ["幼儿园课程与教学", "幼儿游戏", "幼儿文学", "美术基础"], "大四": ["幼儿园实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "南京师范大学", "西南大学", "东北师范大学"], "international": ["University of California Berkeley", "Stanford", "University of Cambridge", "University of Melbourne"]}
    },
    {
        "code": "040106",
        "name": "艺术教育",
        "category": "04 教育学",
        "category_icon": "🎨",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "艺术教育是研究艺术教育规律和方法的学科，培养从事学校艺术教育和艺术活动组织的专业人才。",
        "what_you_learn": "艺术教育学、音乐基础、美术基础、舞蹈基础、戏剧基础、艺术课程与教学",
        "suitable_for": "有艺术特长、喜欢艺术教育、善于与学生沟通的学生。",
        "career_outlook": "素质教育推进，艺术教育教师需求增长。就业在中小学、艺术培训机构、文化馆等。",
        "xuefeng_comment": "艺术教育是结合艺术和教育的专业，适合有艺术特长的学生。就业主要在中小学、艺术培训机构、文化馆等。工作相对稳定，但薪资水平中等。需要有一定的艺术功底，如音乐、美术、舞蹈等。女生比较适合报考。可以考取教师资格证。",
        "yearly_courses": {"大一": ["教育学原理", "普通心理学", "艺术概论", "音乐基础"], "大二": ["艺术教育学", "美术基础", "舞蹈基础", "教育心理学"], "大三": ["艺术课程与教学", "戏剧基础", "艺术鉴赏", "艺术实践"], "大四": ["艺术教育实习"]},
        "top_universities": {"domestic": ["北京师范大学", "华东师范大学", "南京师范大学", "中央音乐学院", "中国美术学院"], "international": ["Juilliard", "Royal Academy of Music", "Central Saint Martins", "Parsons"]}
    },
    {
        "code": "040203",
        "name": "社会体育指导与管理",
        "category": "04 教育学",
        "category_icon": "⚽",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-20k",
        "overview": "社会体育指导与管理是研究社会体育活动组织和指导的学科，培养从事群众体育指导和管理的专业人才。",
        "what_you_learn": "社会体育学、体育管理学、体育经济学、运动训练学、全民健身概论、体育赛事策划",
        "suitable_for": "热爱体育、身体健康、善于组织和指导体育活动的学生。",
        "career_outlook": "全民健身普及，社会体育指导人才需求增长。就业在体育场馆、健身俱乐部、社区体育中心等。",
        "xuefeng_comment": "社会体育指导与管理是体育类专业，适合热爱体育的学生。就业主要在体育场馆、健身俱乐部、社区体育中心等。工作相对灵活，但薪资水平一般。需要有较好的身体素质和体育技能。男生女生都适合报考。可以考取社会体育指导员资格证。",
        "yearly_courses": {"大一": ["体育概论", "运动解剖学", "运动生理学", "体育社会学"], "大二": ["社会体育学", "体育管理学", "体育经济学", "运动训练学"], "大三": ["全民健身概论", "体育赛事策划", "体育市场营销", "体育保健"], "大四": ["社会体育实践"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育学院", "武汉体育学院", "成都体育学院", "沈阳体育学院"], "international": ["Loughborough University", "University of Birmingham", "University of Oregon", "University of Texas"]}
    },
    {
        "code": "040204",
        "name": "武术与民族传统体育",
        "category": "04 教育学",
        "category_icon": "🥋",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "武术与民族传统体育是研究武术和民族传统体育的学科，培养从事武术教学和研究的专业人才。",
        "what_you_learn": "武术基础、武术套路、散打、传统体育养生、武术理论、武术教学法",
        "suitable_for": "热爱武术、身体健康、有一定武术基础或对传统体育感兴趣的学生。",
        "career_outlook": "武术推广和传统文化复兴，武术人才需求稳定。就业在学校、武术馆校、体育部门等。",
        "xuefeng_comment": "武术与民族传统体育是比较有特色的专业，适合热爱武术的学生。就业主要在学校、武术馆校、体育部门等。工作相对稳定，但薪资水平一般。需要有较好的身体素质和武术功底。男生比较适合报考。可以考取武术段位和教师资格证。",
        "yearly_courses": {"大一": ["体育概论", "运动解剖学", "运动生理学", "武术基础"], "大二": ["武术套路", "散打", "传统体育养生", "武术理论"], "大三": ["武术教学法", "武术训练学", "民族传统体育", "体育赛事组织"], "大四": ["武术教学实习"]},
        "top_universities": {"domestic": ["北京体育大学", "上海体育学院", "武汉体育学院", "成都体育学院", "河南大学"], "international": ["Shanghai University of Sport", "Beijing Sport University"]}
    }
]

def main():
    print("=" * 70)
    print("📚 开始导入教育学专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in education_majors:
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
