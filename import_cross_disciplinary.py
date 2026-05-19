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

cross_disciplinary_majors = [
    {
        "code": "082601T",
        "name": "生物医学工程",
        "category": "08 工学",
        "category_icon": "💉🧬",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥16k-35k",
        "overview": "生物医学工程是工程学、生物学和医学的交叉学科，研究医学影像、医疗器械、生物材料等。",
        "what_you_learn": "生物医学信号处理、医学成像技术、医用材料学、生物力学、康复工程、医疗仪器设计",
        "suitable_for": "对医学和工程都感兴趣、动手能力强的学生。",
        "career_outlook": "医疗健康行业快速发展，生物医学工程师需求增长。就业在医疗器械公司、医院设备科、研究所等。",
        "xuefeng_comment": "生物医学工程是典型的交叉学科，需要学生既懂工程又懂医学。这个专业方向很好，医疗健康是永恒的朝阳行业。就业主要在医疗器械公司，如GE医疗、迈瑞等。读研读博能有更好的发展，很多学生会去海外深造。可以做医疗器械研发、医学图像处理等工作。女生也很适合报考，工作环境比较好。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "普通生物学", "工程制图"], "大二": ["生物化学", "生理学", "解剖学", "电路原理"], "大三": ["生物医学信号处理", "医学成像技术", "医用材料学"], "大四": ["医疗器械企业实习"]},
        "top_universities": {"domestic": ["东南大学", "上海交通大学", "清华大学", "四川大学", "西安交通大学"], "international": ["MIT", "Stanford", "Johns Hopkins", "Imperial College London"]}
    },
    {
        "code": "082801T",
        "name": "农业工程",
        "category": "08 工学",
        "category_icon": "🌾",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-22k",
        "overview": "农业工程是将工程技术应用于农业生产的学科，研究农业机械、农田水利、农产品加工等。",
        "what_you_learn": "农业机械学、农田水利学、农产品加工工程、设施农业工程、农业电气化与自动化",
        "suitable_for": "对农业现代化和工程技术感兴趣的学生。",
        "career_outlook": "乡村振兴和农业现代化，农业工程人才需求稳定。就业在农业机械企业、农业科技公司等。",
        "xuefeng_comment": "农业工程是比较传统但很重要的专业。国家重视乡村振兴和农业现代化，这个专业的就业还是比较稳定的。但薪资水平可能不如热门工科专业。很多毕业生去农业机械企业，如农机厂、农业科技公司等。工作环境可能需要去农村或农业基地。适合对农业有兴趣、愿意为农业现代化做贡献的学生报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "普通生物学"], "大二": ["机械设计基础", "理论力学", "材料力学", "土壤学"], "大三": ["农业机械学", "农田水利学", "农产品加工工程"], "大四": ["农业企业实习"]},
        "top_universities": {"domestic": ["中国农业大学", "浙江大学", "吉林大学", "南京农业大学", "华南农业大学"], "international": ["Cornell", "University of California Davis", "Wageningen University"]}
    },
    {
        "code": "120414T",
        "name": "健康服务与管理",
        "category": "12 管理学",
        "category_icon": "🏥",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-18k",
        "overview": "健康服务与管理是研究健康评估、健康干预和健康管理的新兴交叉学科。",
        "what_you_learn": "健康管理学、预防医学、健康评估、营养学、慢性病管理、健康数据分析",
        "suitable_for": "对健康管理和公共卫生感兴趣的学生。",
        "career_outlook": "健康中国战略推进，健康管理产业快速发展。就业在健康管理公司、体检中心、社区卫生服务中心等。",
        "xuefeng_comment": "健康服务与管理是新兴专业，随着健康中国战略和老龄化社会，这个专业的需求会持续增长。但目前这个专业还在发展阶段，培养体系还在完善中。就业方向主要是健康管理公司、体检中心、社区服务中心等。薪资水平一般，工作压力相对较小。适合女生报考，工作环境比较稳定。建议报考前了解清楚各校的课程设置。",
        "yearly_courses": {"大一": ["管理学原理", "经济学原理", "基础医学概论", "临床医学概论"], "大二": ["预防医学", "营养学", "健康管理学", "心理学"], "大三": ["健康评估", "慢性病管理", "健康数据分析", "健康保险"], "大四": ["健康管理机构实习"]},
        "top_universities": {"domestic": ["北京中医药大学", "南京医科大学", "南方医科大学", "四川大学"], "international": ["Harvard T.H. Chan", "Johns Hopkins", "UCL"]}
    },
    {
        "code": "120115T",
        "name": "应急管理",
        "category": "12 管理学",
        "category_icon": "🚨",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "应急管理是研究突发事件预防、应急响应和灾后恢复的新兴交叉学科。",
        "what_you_learn": "应急管理概论、应急决策与指挥、应急预案编制、危机公关、应急救援技术",
        "suitable_for": "对公共安全和应急管理感兴趣的学生。",
        "career_outlook": "公共安全体系建设，应急管理人才需求增长。就业在政府应急管理部门、消防、企业安全管理等。",
        "xuefeng_comment": "应急管理是新兴的公共管理类专业，国家越来越重视公共安全。这个专业就业方向主要是政府应急管理部门、消防系统、企业安全管理等。工作相对稳定，但需要有责任心和应急处置能力。部分岗位可能需要值班或应对突发事件。适合对公共安全有兴趣、有组织协调能力的学生报考。考公务员是这个专业的重要出路之一。",
        "yearly_courses": {"大一": ["管理学原理", "法学概论", "公共政策分析", "社会学"], "大二": ["应急管理概论", "风险评估与管理", "突发事件应对法"], "大三": ["应急决策与指挥", "应急预案编制", "危机公关", "应急救援技术"], "大四": ["应急管理部门实习"]},
        "top_universities": {"domestic": ["中国矿业大学", "河南理工大学", "中国地质大学", "南京工业大学"], "international": ["Harvard Kennedy School", "LSE", "University of Michigan"]}
    },
    {
        "code": "130508T",
        "name": "数字媒体艺术",
        "category": "13 艺术学",
        "category_icon": "🎬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "数字媒体艺术是艺术设计与计算机技术的交叉学科，研究数字动画、游戏设计、交互设计等。",
        "what_you_learn": "数字绘画、动画设计、游戏设计、交互设计、影视特效、UI设计、虚拟现实",
        "suitable_for": "对艺术创作和计算机技术都感兴趣的学生。",
        "career_outlook": "数字文化产业发展迅速，数字媒体人才需求旺盛。就业在互联网公司、游戏公司、影视传媒等。",
        "xuefeng_comment": "数字媒体艺术是艺术与技术的结合，是一个比较热门的新兴专业。就业在互联网公司、游戏公司、影视传媒等，方向很多，收入差距也比较大。需要学生有一定的美术基础和审美能力，同时还要学会使用各种设计软件。这个专业比较适合有艺术天赋、对游戏动画感兴趣的学生。工作压力相对较大，但收入也不错，在艺术类专业中属于比较好的。",
        "yearly_courses": {"大一": ["艺术概论", "素描色彩", "计算机基础", "设计概论"], "大二": ["数字绘画、Photoshop", "三维建模、3ds Max"], "大三": ["动画设计、游戏设计", "交互设计、UI设计", "影视特效"], "大四": ["设计公司实习"]},
        "top_universities": {"domestic": ["中国传媒大学", "北京电影学院", "中央美术学院", "广州美术学院"], "international": ["NYU Tisch", "RISD", "USC", "Central Saint Martins"]}
    }
]

def main():
    print("=" * 70)
    print("🎯 开始导入新兴交叉学科专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in cross_disciplinary_majors:
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
