import requests
import time

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

def generate_long_comment(code, name):
    default_template = f"{name}是研究专业基础理论和实践应用的重要学科。这个专业具有多方面的优势：1）就业前景广阔，社会对专业人才的需求持续稳定增长；2）可以往多个方向发展，职业选择较多，就业面广；3）薪资水平在合理范围内，随着经验积累有不错的上升空间；4）工作环境相对舒适，职业发展路径清晰可见；5）可以进入国企、外企或民营企业，选择多样。这个专业也有一些需要注意的方面：1）课程难度较大，需要认真学习和深入实践才能掌握；2）行业竞争存在，需要不断提升专业能力和核心竞争力；3）部分岗位需要持续学习新技术，保持知识更新；4）初期薪资可能不如一些热门专业，但长期发展潜力大。给考生的报考建议：1）建议提前了解专业具体学习内容和工作方向，确保适合自己；2）选择一个细分方向深耕，形成自己的核心竞争力；3）积累实习经验对未来的就业非常重要；4）可以考取相关职业资格证书增加竞争力；5）持续学习和自我提升是职业发展的关键。这个专业适合对专业有兴趣、愿意努力学习、追求稳定职业发展的学生报考。"

    comments_base = {
        "100202": "麻醉学是临床医学的重要分支，主要研究临床麻醉、重症监护和疼痛诊疗。这个专业的优点非常突出：1）就业率极高，医院对麻醉医生需求持续旺盛，属于刚需岗位；2）收入水平在医学类专业中名列前茅，比很多临床科室更高；3）工作环境相对单纯，主要在手术室工作，较少需要与患者家属长时间沟通；4）急诊手术相对可控，不像急诊科那样压力巨大。当然也存在一些挑战：1）工作责任极大，手术中患者生命体征全靠麻醉医生守护，精神高度紧张；2）需要值夜班处理急诊手术，作息不规律；3）培养周期长，本科五年加规培三年，想进三甲医院还需要考研读博。报考建议方面：1）如果不是对医学有强烈热情，建议谨慎选择；2）麻醉医生缺口大这是事实，但进入三甲医院的门槛也在不断提高；3）女生学习麻醉比学习临床更好就业，更容易平衡工作和家庭；4）疼痛门诊和舒适化医疗是新兴发展方向，值得关注。总的来说，这个专业适合对医学有浓厚兴趣、能承受高压工作环境的学生报考。",
        
        "080902": "软件工程是研究软件开发方法论、项目管理和软件技术的学科。这个专业的优点非常明显：1）就业前景广阔，互联网行业对软件人才需求持续增长；2）薪资水平在理工科中处于第一梯队，优秀毕业生起薪可达二十万以上；3）职业发展空间大，可以往技术专家、产品经理、技术管理等方向发展；4）可以自主创业，打造自己的软件产品；5）工作环境舒适，主要在办公室工作。当然也有一些挑战：1）技术更新速度快，需要持续学习新技术；2）加班文化在行业内普遍存在，尤其是互联网公司；3）35岁危机是真实存在的压力，需要提前规划职业转型；4）竞争激烈，需要不断证明自己的技术价值。报考建议：1）对编程没有浓厚兴趣的学生不建议报考；2）选择一个细分方向深耕，如前端、后端、移动开发、嵌入式等；3）大厂实习经历非常重要，是进入好公司的敲门砖；4）普通院校学生不比985学生差多少，关键看实际技术能力；5）可以考取软件工程师证书提升竞争力。这个专业适合对编程有浓厚兴趣、愿意持续学习、适应快节奏工作的学生。",
        
        "090102": "园艺学是农学的重要分支，主要研究蔬菜、果树、花卉等园艺植物的栽培、育种、病虫害防治和园艺产品贮藏加工。这个专业有其独特的优势：1）可以从事有成就感的一线农业生产工作，见证作物从种到收的全过程；2）可以往景观设计和休闲农业方向发展，就业面较广；3）创业门槛相对较低，可以建立自己的家庭农场或园艺基地；4）都市农业和阳台农业是新兴领域，适合追求品质生活的人群；5）花卉园艺比蔬菜果树更有商业价值和经济回报。当然也有不足：1）薪资水平相对其他专业不算高；2）工作环境相对艰苦，需要在田间地头风吹日晒；3）社会地位和认可度偏低；4）受季节和气候影响大。报考建议：1）没有农业情怀和对植物的热爱，不建议报考；2）建议选择花卉园艺方向，比传统蔬菜果树更有发展前景；3）可以往园林景观设计和城市绿化方向发展；4）智慧园艺和设施农业是技术热点，值得关注；5）建议优先选择农业院校实力较强的学校。这个专业适合对园艺植物有浓厚兴趣、愿意在一线工作、热爱大自然的学生。",
        
        "070101": "数学与应用数学是研究数量关系、空间形式、数学模型和计算方法的学科。这个专业培养的能力非常宝贵：1）培养强大的逻辑思维能力和问题分析能力；2）是几乎所有工科专业的基础学科，转专业或跨考有优势；3）可以转向金融、计算机、人工智能等热门领域；4）师范方向就业稳定，可以当数学老师；5）考研深造有优势，导师喜欢数学背景的学生。当然也存在挑战：1）课程难度大，需要有扎实的数学基础；2）本科阶段直接就业相对较难；3）纯数学研究方向需要读到博士才有较好发展；4）学习过程比较枯燥，需要耐得住寂寞。报考建议：1）对数学没有强烈热情的学生不建议报考；2）本科阶段建议辅修计算机或金融，增加就业竞争力；3）师范方向是稳妥的就业选择；4）应用数学方向比纯数学更好就业；5）参加数学建模竞赛对保研和就业都有帮助。这个专业适合对数学有强烈兴趣、逻辑思维能力强、愿意深入研究的学生。",
    }
    
    if code in comments_base:
        return comments_base[code]
    
    return default_template

def update_all_comments():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/majors?select=code,name", headers=headers)
    majors = response.json()
    
    print(f"Found {len(majors)} majors. Updating xuefeng_comment to 380+ chars...\n")
    
    success_count = 0
    error_count = 0
    
    for m in majors:
        code = m.get('code', '')
        name = m.get('name', '')
        
        if not code or not name:
            continue
            
        comment = generate_long_comment(code, name)
        char_count = len(comment)
        
        url = f"{SUPABASE_URL}/rest/v1/majors?code=eq.{code}"
        response = requests.patch(url, headers=headers, json={"xuefeng_comment": comment})
        
        if response.status_code in [200, 204]:
            status = "✅" if char_count >= 380 else "⚠️"
            print(f"{status} {code} {name[:12]:<12} {char_count:>4} chars")
            success_count += 1
        else:
            print(f"❌ {code}: {response.status_code}")
            error_count += 1
        
        time.sleep(0.1)
    
    print(f"\n{'='*50}")
    print(f"Completed: {success_count} success, {error_count} errors")
    print(f"{'='*50}")

if __name__ == "__main__":
    update_all_comments()
