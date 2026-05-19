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
        error_body = e.read().decode('utf-8')
        if 'duplicate key' in error_body or 'already exists' in error_body:
            return False, 409
        return False, e.code

medical_majors = [
    {
        "code": "100205TK",
        "name": "精神医学",
        "category": "10 医学",
        "category_icon": "🧠",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥15k-30k",
        "overview": "精神医学是研究精神障碍的病因、发病机制、临床表现、诊断、治疗和预防的医学学科。本专业培养掌握精神疾病诊疗、心理治疗等专业知识的临床医学人才。",
        "what_you_learn": "精神障碍诊断与治疗学、心理学导论、临床精神病学、心理治疗技术、精神药理学、心理咨询与治疗、儿童青少年精神病学、老年精神病学、精神疾病预防",
        "suitable_for": "对心理健康和精神疾病感兴趣、善于沟通和倾听、有同理心的学生。精神科医生需要良好的心理素质和沟通能力。",
        "career_outlook": "心理健康日益受到重视，精神医学专业人才需求增长。毕业生可在精神卫生中心、综合医院精神科、心理卫生机构等从事诊疗和心理治疗工作。",
        "xuefeng_comment": "精神医学是比较特殊的医学专业，随着社会发展，心理健康问题越来越受重视，这个专业的发展前景是很好的。但要提醒大家，精神科医生需要面对特殊的患者群体，工作压力和心理负担不小。建议真正对精神心理领域有兴趣的学生报考。另外，医患关系方面，精神科相对其他科室可能要特殊一些，需要有心理准备。就业方向主要是精神卫生中心、综合性医院精神科等。读研读博几乎是必须的。",
        "yearly_courses": {"大一": ["人体解剖学", "组织学与胚胎学", "生物化学", "生理学", "医学心理学"], "大二": ["病理学", "药理学", "诊断学", "内科学", "外科学"], "大三": ["精神病学基础", "精神障碍诊断学", "精神药理学", "心理治疗技术"], "大四": ["精神科临床实习", "心理治疗实践"]},
        "top_universors": {"domestic": ["北京大学", "上海交通大学", "中南大学", "四川大学", "首都医科大学"], "international": ["Harvard Medical", "Johns Hopkins", "UCL", " King's College London"]}
    },
    {
        "code": "100207TK",
        "name": "儿科学",
        "category": "10 医学",
        "category_icon": "👶",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥15k-32k",
        "overview": "儿科学是研究小儿生长发育、卫生保健和疾病防治的医学学科。本专业培养掌握儿科常见病、多发病诊疗等专业知识的临床医学人才。",
        "what_you_learn": "小儿内科学、小儿外科学、新生儿学、小儿传染病学、小儿急救医学、儿童保健学、小儿诊断学、儿科护理学",
        "suitable_for": "喜欢孩子、有耐心、善于与儿童沟通的学生。儿科医生需要较强的沟通能力和应变能力，因为患儿往往不能准确描述病情。",
        "career_outlook": "国家鼓励生育，儿科医生需求持续增长。但儿科医生工作压力大、薪资相对低，是医疗行业的热门但又紧缺的岗位。",
        "xuefeng_comment": "儿科学是国家急需的专业，儿科医生缺口很大。但我要提醒大家，儿科医生工作强度大、压力大、收入相对不高，是典型的'钱少事多'岗位。给孩子看病需要和家长充分沟通，医患矛盾在儿科可能更突出。建议真正喜欢孩子、有耐心、沟通能力强的学生报考。如果你对儿科有热情，还是值得选择的，因为就业相对容易。如果只是为了稳定而选择儿科，可能需要慎重考虑。",
        "yearly_courses": {"大一": ["人体解剖学", "组织学与胚胎学", "生物化学", "生理学", "儿科学导论"], "大二": ["病理学", "药理学", "诊断学", "内科学基础"], "大三": ["小儿内科学", "小儿外科学", "新生儿学", "儿童保健学"], "大四": ["儿科临床实习"]},
        "top_universities": {"domestic": ["上海交通大学", "北京大学", "复旦大学", "浙江大学", "首都医科大学"], "international": ["Harvard Medical", "Stanford", "UCL", "Imperial College"]}
    },
    {
        "code": "101003T",
        "name": "医学影像技术",
        "category": "10 医学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-25k",
        "overview": "医学影像技术是研究医学影像设备操作、图像获取和处理的技术学科。本专业培养掌握X线、CT、MRI、超声等医学影像技术操作的专业技术人才。",
        "what_you_learn": "人体解剖学、影像物理学、X线检查技术、CT检查技术、MRI检查技术、超声检查技术、介入放射学、医学影像诊断学、放射防护",
        "suitable_for": "对医学影像技术感兴趣、动手能力强的学生。影像技术人员需要熟练操作各种影像设备，耐心细致。",
        "career_outlook": "医学影像技术是临床诊断的重要支撑，影像检查需求持续增长。毕业生可在医院影像科、体检中心、医疗器械公司等从事技术操作和设备维护工作。",
        "xuefeng_comment": "医学影像技术是医技类专业，不需要考执业医师资格证，是医学类中性价比较高的专业。就业主要在医院的影像科，操作X光机、CT、MRI等设备。工作相对稳定，不需要值夜班（或者夜班强度低于临床科室）。薪资水平在医技类中属于中等。不需要与患者过多沟通，工作压力相对小一些。适合女生报考。这个专业是理学学位，不是医学学位，这一点需要注意。",
        "yearly_courses": {"大一": ["人体解剖学", "影像物理学", "电子学基础", "计算机基础"], "大二": ["X线检查技术", "CT检查技术", "医学影像设备学"], "大三": ["MRI检查技术", "超声检查技术", "医学影像诊断学"], "大四": ["影像科实习"]},
        "top_universities": {"domestic": ["华中科技大学", "四川大学", "中南大学", "南方医科大学", "天津医科大学"], "international": ["MIT", "Johns Hopkins", "Imperial College", "University of Toronto"]}
    },
    {
        "code": "101005T",
        "name": "康复治疗学",
        "category": "10 医学",
        "category_icon": "💪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-25k",
        "overview": "康复治疗学是研究功能障碍的评估、治疗和训练的医学技术学科。本专业培养掌握物理治疗、作业治疗、言语治疗等康复治疗技术的专业技术人才。",
        "what_you_learn": "人体解剖学、康复评定学、物理治疗学、作业治疗学、言语治疗学、康复工程学、中国传统康复治疗学、临床康复学",
        "suitable_for": "对康复医学感兴趣、动手能力强、有耐心的学生。康复治疗师需要与患者长期接触，建立良好的医患关系。",
        "career_outlook": "老龄化社会推动康复医疗需求增长，康复治疗师缺口大。毕业生可在康复医院、综合医院康复科、养老机构、体育运动队等从事康复治疗工作。",
        "xuefeng_comment": "康复治疗学是朝阳专业，随着老龄化加剧和人们对生活质量要求提高，康复医疗需求快速增长。这个专业是理学学位，不需要考执业医师资格证。就业方向主要是康复医院、综合医院康复科、养老机构等。工作相对稳定，薪资水平中等。适合女生报考，工作环境比临床科室轻松一些。可以考虑考取康复治疗师资格证，提升职业竞争力。",
        "yearly_courses": {"大一": ["人体解剖学", "生理学", "运动学基础", "康复医学概论"], "大二": ["康复评定学", "物理治疗学", "作业治疗学"], "大三": ["言语治疗学", "康复工程学", "中国传统康复治疗学"], "大四": ["康复科实习"]},
        "top_universities": {"domestic": ["中山大学", "四川大学", "华中科技大学", "首都医科大学", "南京医科大学"], "international": ["University of Pittsburgh", "University of Toronto", "King's College London", "Sydney University"]}
    },
    {
        "code": "100401T",
        "name": "预防医学",
        "category": "10 医学",
        "category_icon": "🦠",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-25k",
        "overview": "预防医学是研究预防和控制疾病、促进健康的医学学科。本专业培养掌握疾病预防控制、流行病学调查、卫生监测等专业知识的公共卫生人才。",
        "what_you_learn": "流行病学、卫生统计学、劳动卫生与职业病学、环境卫生学、营养与食品卫生学、儿少卫生学、卫生事业管理、传染病学、公共卫生监测",
        "suitable_for": "对公共卫生和疾病预防感兴趣、关注人群健康的学生。预防医学专业培养的是公共卫生领域的专业人才。",
        "career_outlook": "新冠疫情后，国家高度重视公共卫生体系建设，预防医学专业人才需求增长。毕业生可在疾控中心、卫健委、医院防保科、海关检验检疫等机构工作。",
        "xuefeng_comment": "预防医学是公共卫生体系的重要组成部分。新冠疫情让大家认识到公共卫生的重要性，这个专业的发展前景明显提升。就业方向包括疾控中心、卫健委、医院、海关等。工作相对稳定，但薪资水平不如临床医生。考公务员是这个专业的一个重要出路。这个专业是五年制，毕业后可获得医学学位。可以考取公共卫生执业医师资格证。适合对公共卫生管理有兴趣的学生报考。",
        "yearly_courses": {"大一": ["人体解剖学", "生物化学", "生理学", "预防医学导论"], "大二": ["流行病学", "卫生统计学", "劳动卫生学", "环境卫生学"], "大三": ["营养与食品卫生学", "儿少卫生学", "传染病学"], "大四": ["疾控中心实习", "卫生监督所实习"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "华中科技大学", "中山大学", "南京医科大学"], "international": ["Harvard T.H. Chan", "Johns Hopkins", "Imperial College", "UCL"]}
    }
]

def main():
    print("=" * 60)
    print("开始导入医学专业...")
    print("=" * 60)
    
    success = 0
    failed = 0
    skipped = 0
    
    for major in medical_majors:
        print(f"\n正在导入: {major['code']} - {major['name']}")
        ok, code = import_major(major)
        
        if ok or code in [200, 201]:
            success += 1
            print(f"✅ 成功")
        elif code == 409:
            skipped += 1
            print(f"⏭️ 已存在，跳过")
        else:
            failed += 1
            print(f"❌ 失败 (HTTP {code})")
        
        time.sleep(0.2)
    
    print("\n" + "=" * 60)
    print(f"导入完成！成功: {success}, 已存在: {skipped}, 失败: {failed}")
    print("=" * 60)

if __name__ == "__main__":
    main()