import requests
import time
import json

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

# 需要新增的专业列表（按学科代码排序）
new_majors = [
    # 工学 (08) - 机械类
    {"code": "080201", "name": "机械工程", "category": "08 工学", "category_icon": "🔧"},
    {"code": "080203", "name": "材料成型及控制工程", "category": "08 工学", "category_icon": "🔧"},
    {"code": "080204", "name": "机械电子工程", "category": "08 工学", "category_icon": "🔧"},
    {"code": "080205", "name": "工业设计", "category": "08 工学", "category_icon": "🎨"},
    {"code": "080206", "name": "过程装备与控制工程", "category": "08 工学", "category_icon": "🔧"},
    {"code": "080208", "name": "工业工程", "category": "08 工学", "category_icon": "📊"},
    {"code": "080209T", "name": "标准化工程", "category": "08 工学", "category_icon": "📐"},
    {"code": "080210T", "name": "微机电系统工程", "category": "08 工学", "category_icon": "⚙️"},
    
    # 工学 (08) - 材料类
    {"code": "080401", "name": "材料物理", "category": "08 工学", "category_icon": "🧪"},
    {"code": "080402", "name": "材料化学", "category": "08 工学", "category_icon": "🧪"},
    {"code": "080403T", "name": "冶金工程", "category": "08 工学", "category_icon": "🔥"},
    {"code": "080404T", "name": "金属材料工程", "category": "08 工学", "category_icon": "🔩"},
    {"code": "080405T", "name": "无机非金属材料工程", "category": "08 工学", "category_icon": "🏔️"},
    {"code": "080406T", "name": "高分子材料与工程", "category": "08 工学", "category_icon": "⚗️"},
    {"code": "080408T", "name": "复合材料与工程", "category": "08 工学", "category_icon": "🔗"},
    {"code": "080409T", "name": "粉体材料科学与工程", "category": "08 工学", "category_icon": "💎"},
    {"code": "080410T", "name": "宝石及材料工艺学", "category": "08 工学", "category_icon": "💎"},
    
    # 工学 (08) - 能源动力类
    {"code": "080502T", "name": "能源与动力工程", "category": "08 工学", "category_icon": "⚡"},
    {"code": "080503T", "name": "核工程与核技术", "category": "08 工学", "category_icon": "☢️"},
    {"code": "080504T", "name": "辐射防护与核安全", "category": "08 工学", "category_icon": "🛡️"},
    
    # 工学 (08) - 电气类
    {"code": "080602T", "name": "智能电网信息工程", "category": "08 工学", "category_icon": "⚡"},
    {"code": "080604T", "name": "光源与照明", "category": "08 工学", "category_icon": "💡"},
    {"code": "080605T", "name": "电气工程与智能控制", "category": "08 工学", "category_icon": "⚡"},
    
    # 工学 (08) - 电子信息类
    {"code": "080702", "name": "电子科学与技术", "category": "08 工学", "category_icon": "📡"},
    {"code": "080703", "name": "通信工程", "category": "08 工学", "category_icon": "📡"},
    {"code": "080704", "name": "微电子科学与工程", "category": "08 工学", "category_icon": "💻"},
    {"code": "080706T", "name": "信息工程", "category": "08 工学", "category_icon": "📶"},
    {"code": "080707T", "name": "广播电视工程", "category": "08 工学", "category_icon": "📺"},
    {"code": "080708T", "name": "水声工程", "category": "08 工学", "category_icon": "🌊"},
    {"code": "080709T", "name": "电子封装技术", "category": "08 工学", "category_icon": "📦"},
    {"code": "080711T", "name": "电信工程及管理", "category": "08 工学", "category_icon": "📡"},
    {"code": "080712T", "name": "应用电子技术教育", "category": "08 工学", "category_icon": "📚"},
    
    # 工学 (08) - 自动化类
    {"code": "080802T", "name": "轨道交通信号与控制", "category": "08 工学", "category_icon": "🚄"},
    {"code": "080803T", "name": "机器人工程", "category": "08 工学", "category_icon": "🤖"},
    
    # 工学 (08) - 计算机类
    {"code": "080905", "name": "物联网工程", "category": "08 工学", "category_icon": "🔗"},
    {"code": "080907T", "name": "数字媒体技术", "category": "08 工学", "category_icon": "📱"},
    {"code": "080908T", "name": "空间信息与数字技术", "category": "08 工学", "category_icon": "🛰️"},
    {"code": "080909T", "name": "电子与计算机工程", "category": "08 工学", "category_icon": "💻"},
    {"code": "080911TK", "name": "网络空间安全", "category": "08 工学", "category_icon": "🔒"},
    
    # 工学 (08) - 土木类
    {"code": "081003T", "name": "给排水科学与工程", "category": "08 工学", "category_icon": "💧"},
    {"code": "081004T", "name": "建筑电气与智能化", "category": "08 工学", "category_icon": "🏠"},
    {"code": "081005T", "name": "城市地下空间工程", "category": "08 工学", "category_icon": "🏗️"},
    {"code": "081006T", "name": "道路桥梁与渡河工程", "category": "08 工学", "category_icon": "🛤️"},
    {"code": "081007T", "name": "铁道工程", "category": "08 工学", "category_icon": "🚂"},
    {"code": "081008T", "name": "智能建造", "category": "08 工学", "category_icon": "🏗️"},
    
    # 工学 (08) - 水利类
    {"code": "081101", "name": "水利水电工程", "category": "08 工学", "category_icon": "💧"},
    {"code": "081102", "name": "水文与水资源工程", "category": "08 工学", "category_icon": "🌊"},
    {"code": "081103T", "name": "港口航道与海岸工程", "category": "08 工学", "category_icon": "⚓"},
    {"code": "081104T", "name": "水务工程", "category": "08 工学", "category_icon": "💧"},
    
    # 工学 (08) - 测绘类
    {"code": "081201", "name": "测绘工程", "category": "08 工学", "category_icon": "🗺️"},
    {"code": "081202T", "name": "遥感科学与技术", "category": "08 工学", "category_icon": "🛰️"},
    {"code": "081203T", "name": "导航工程", "category": "08 工学", "category_icon": "🧭"},
    
    # 工学 (08) - 化工与制药类
    {"code": "081303T", "name": "化学工程与工艺", "category": "08 工学", "category_icon": "⚗️"},
    {"code": "081304T", "name": "制药工程", "category": "08 工学", "category_icon": "💊"},
    {"code": "081305T", "name": "能源化学工程", "category": "08 工学", "category_icon": "⚡"},
    {"code": "081306T", "name": "资源循环科学与工程", "category": "08 工学", "category_icon": "♻️"},
    
    # 工学 (08) - 地质类
    {"code": "081401", "name": "地质工程", "category": "08 工学", "category_icon": "🪨"},
    {"code": "081402T", "name": "勘查技术与工程", "category": "08 工学", "category_icon": "🔍"},
    {"code": "081403T", "name": "资源勘查工程", "category": "08 工学", "category_icon": "💎"},
    
    # 工学 (08) - 矿业类
    {"code": "081501", "name": "采矿工程", "category": "08 工学", "category_icon": "⛏️"},
    {"code": "081503T", "name": "矿物加工工程", "category": "08 工学", "category_icon": "🏭"},
    
    # 工学 (08) - 交通运输类
    {"code": "081802", "name": "交通工程", "category": "08 工学", "category_icon": "🚗"},
    {"code": "081803T", "name": "航海技术", "category": "08 工学", "category_icon": "🚢"},
    {"code": "081804T", "name": "轮机工程", "category": "08 工学", "category_icon": "⚙️"},
    {"code": "081805K", "name": "飞行技术", "category": "08 工学", "category_icon": "✈️"},
    {"code": "081806T", "name": "船舶与海洋工程", "category": "08 工学", "category_icon": "🚢"},
    {"code": "081807T", "name": "海洋工程与技术", "category": "08 工学", "category_icon": "🌊"},
    {"code": "081808TK", "name": "航空航天工程", "category": "08 工学", "category_icon": "🚀"},
    
    # 工学 (08) - 航空航天类
    {"code": "082001", "name": "飞行器设计与工程", "category": "08 工学", "category_icon": "✈️"},
    {"code": "082002T", "name": "飞行器动力工程", "category": "08 工学", "category_icon": "🚀"},
    {"code": "082003T", "name": "飞行器制造工程", "category": "08 工学", "category_icon": "✈️"},
    {"code": "082004T", "name": "飞行器环境与生命保障工程", "category": "08 工学", "category_icon": "🛸"},
    
    # 工学 (08) - 食品科学与工程类
    {"code": "082702T", "name": "食品质量与安全", "category": "08 工学", "category_icon": "🍎"},
    {"code": "082703T", "name": "粮食工程", "category": "08 工学", "category_icon": "🌾"},
    {"code": "082704T", "name": "乳品工程", "category": "08 工学", "category_icon": "🥛"},
    {"code": "082705T", "name": "酿酒工程", "category": "08 工学", "category_icon": "🍷"},
    
    # 工学 (08) - 其他类
    {"code": "082101", "name": "消防工程", "category": "08 工学", "category_icon": "🚒"},
    {"code": "082601", "name": "生物医学工程", "category": "08 工学", "category_icon": "🏥"},
    {"code": "082801", "name": "服装设计与工程", "category": "08 工学", "category_icon": "👗"},
    {"code": "083001", "name": "生物工程", "category": "08 工学", "category_icon": "🧬"},
    {"code": "083002T", "name": "生物制药", "category": "08 工学", "category_icon": "💊"},
    
    # 工学 (08) - 新增的智能类
    {"code": "083101TK", "name": "假肢矫形工程", "category": "08 工学", "category_icon": "🦾"},
    {"code": "083201T", "name": "虚拟现实技术", "category": "08 工学", "category_icon": "🕶️"},
    {"code": "083301TK", "name": "区块链工程", "category": "08 工学", "category_icon": "🔗"},
    {"code": "083401TK", "name": "密码科学与技术", "category": "08 工学", "category_icon": "🔑"},
    
    # 其他学科补充
    # 07 理学
    {"code": "070202", "name": "应用物理学", "category": "07 理学", "category_icon": "⚛️"},
    {"code": "070302", "name": "应用化学", "category": "07 理学", "category_icon": "🧪"},
    {"code": "070502", "name": "自然地理与资源环境", "category": "07 理学", "category_icon": "🌍"},
    {"code": "070503T", "name": "人文地理与城乡规划", "category": "07 理学", "category_icon": "🏙️"},
    {"code": "070701", "name": "海洋科学", "category": "07 理学", "category_icon": "🌊"},
    {"code": "070901", "name": "地质学", "category": "07 理学", "category_icon": "🪨"},
    {"code": "071301", "name": "生态学", "category": "07 理学", "category_icon": "🌿"},
    
    # 12 管理学
    {"code": "120101", "name": "管理科学", "category": "12 管理学", "category_icon": "📊"},
    {"code": "120102", "name": "信息管理与信息系统", "category": "12 管理学", "category_icon": "💻"},
    {"code": "120205", "name": "国际商务", "category": "12 管理学", "category_icon": "🌐"},
    {"code": "120301", "name": "农林经济管理", "category": "12 管理学", "category_icon": "🌾"},
    {"code": "120501", "name": "图书馆学", "category": "12 管理学", "category_icon": "📚"},
    {"code": "120502", "name": "档案学", "category": "12 管理学", "category_icon": "📋"},
    {"code": "120601", "name": "物流管理", "category": "12 管理学", "category_icon": "📦"},
    {"code": "120602", "name": "物流工程", "category": "12 管理学", "category_icon": "🚛"},
    {"code": "120701", "name": "工业工程", "category": "12 管理学", "category_icon": "📈"},
    {"code": "120702T", "name": "质量管理工程", "category": "12 管理学", "category_icon": "✅"},
    
    # 13 艺术学
    {"code": "130101", "name": "艺术史论", "category": "13 艺术学", "category_icon": "🎭"},
    {"code": "130201T", "name": "音乐表演", "category": "13 艺术学", "category_icon": "🎵"},
    {"code": "130206T", "name": "舞蹈表演", "category": "13 艺术学", "category_icon": "💃"},
    {"code": "130301", "name": "表演", "category": "13 艺术学", "category_icon": "🎭"},
    {"code": "130302", "name": "戏剧学", "category": "13 艺术学", "category_icon": "🎭"},
    {"code": "130307T", "name": "戏剧影视文学", "category": "13 艺术学", "category_icon": "📝"},
    {"code": "130308T", "name": "戏剧影视导演", "category": "13 艺术学", "category_icon": "🎬"},
    {"code": "130402", "name": "绘画", "category": "13 艺术学", "category_icon": "🎨"},
    {"code": "130403", "name": "雕塑", "category": "13 艺术学", "category_icon": "🗿"},
    {"code": "130405T", "name": "书法学", "category": "13 艺术学", "category_icon": "✍️"},
    {"code": "130503", "name": "环境设计", "category": "13 艺术学", "category_icon": "🏘️"},
    {"code": "130504", "name": "产品设计", "category": "13 艺术学", "category_icon": "🎁"},
    {"code": "130505T", "name": "服装与服饰设计", "category": "13 艺术学", "category_icon": "👔"},
    {"code": "130506T", "name": "公共艺术", "category": "13 艺术学", "category_icon": "🎨"},
    
    # 04 教育学
    {"code": "040103T", "name": "教育技术学", "category": "04 教育学", "category_icon": "💻"},
    {"code": "040104T", "name": "艺术教育", "category": "04 教育学", "category_icon": "🎨"},
    {"code": "040105T", "name": "学前教育", "category": "04 教育学", "category_icon": "👶"},
    {"code": "040106T", "name": "小学教育", "category": "04 教育学", "category_icon": "👧"},
    {"code": "040107T", "name": "特殊教育", "category": "04 教育学", "category_icon": "❤️"},
    
    # 06 历史学
    {"code": "060103T", "name": "世界史", "category": "06 历史学", "category_icon": "🌍"},
    {"code": "060104T", "name": "考古学", "category": "06 历史学", "category_icon": "🏺"},
    {"code": "060105T", "name": "文物与博物馆学", "category": "06 历史学", "category_icon": "🏛️"},
    
    # 09 农学
    {"code": "090101", "name": "农学", "category": "09 农学", "category_icon": "🌾"},
    {"code": "090201", "name": "园艺", "category": "09 农学", "category_icon": "🌱"},
    {"code": "090402T", "name": "动植物检疫", "category": "09 农学", "category_icon": "🔬"},
    {"code": "090601", "name": "林学", "category": "09 农学", "category_icon": "🌲"},
    
    # 10 医学
    {"code": "100101T", "name": "基础医学", "category": "10 医学", "category_icon": "🔬"},
    {"code": "100501T", "name": "中西医临床医学", "category": "10 医学", "category_icon": "🏥"},
    {"code": "100601T", "name": "法医学", "category": "10 医学", "category_icon": "🔍"},
    {"code": "100801T", "name": "中药学", "category": "10 医学", "category_icon": "🌿"},
    {"code": "101001T", "name": "医学检验技术", "category": "10 医学", "category_icon": "🧪"},
    {"code": "101101T", "name": "护理学", "category": "10 医学", "category_icon": "👩‍⚕️"},
    
    # 11 军事学（少量补充）
    {"code": "110101T", "name": "军事思想", "category": "11 军事学", "category_icon": "⚔️"},
    
    # 05 文学补充
    {"code": "050103", "name": "汉语言", "category": "05 文学", "category_icon": "📖"},
    {"code": "050104T", "name": "中国少数民族语言文学", "category": "05 文学", "category_icon": "📚"},
    {"code": "050105T", "name": "古典文献学", "category": "05 文学", "category_icon": "📜"},
    {"code": "050202T", "name": "俄语", "category": "05 文学", "category_icon": "🇷🇺"},
    {"code": "050203T", "name": "德语", "category": "05 文学", "category_icon": "🇩🇪"},
    {"code": "050204T", "name": "法语", "category": "05 文学", "category_icon": "🇫🇷"},
    {"code": "050205T", "name": "西班牙语", "category": "05 文学", "category_icon": "🇪🇸"},
    {"code": "050206T", "name": "阿拉伯语", "category": "05 文学", "category_icon": "🇸🇦"},
    {"code": "050207T", "name": "日语", "category": "05 文学", "category_icon": "🇯🇵"},
    {"code": "050208T", "name": "朝鲜语", "category": "05 文学", "category_icon": "🇰🇷"},
    
    # 03 法学补充
    {"code": "030201", "name": "政治学与行政学", "category": "03 法学", "category_icon": "⚖️"},
    {"code": "030202T", "name": "国际政治", "category": "03 法学", "category_icon": "🌐"},
    {"code": "030301", "name": "社会学", "category": "03 法学", "category_icon": "👥"},
    {"code": "030303T", "name": "人类学", "category": "03 法学", "category_icon": "👤"},
    {"code": "030602T", "name": "民族学", "category": "03 法学", "category_icon": "🌍"},
]

# 生成难度星级函数
def get_difficulty_stars(major_code):
    # 根据专业难度分配星级（1-5星）
    difficult_majors = {"0805", "0807", "0809", "0820", "1001", "1002", "0701", "0702", "0703"}
    medium_majors = {"0802", "0806", "0808", "0813", "0817", "1004", "1007", "0203", "0827"}
    
    prefix = major_code[:4] if len(major_code)>=4 else major_code
    if prefix in difficult_majors or major_code in difficult_majors:
        return "★★★★★"
    elif prefix in medium_majors or major_code in medium_majors:
        return "★★★★"
    else:
        return "★★★"

# 生成薪资范围函数
def get_salary_range(major_code):
    high_salary = {"0809", "0807", "0806", "0203", "0204", "0810", "0820", "0805", "0827"}
    medium_salary = {"0802", "0803", "0808", "0812", "0813", "1003", "1004", "0712", "0503"}
    
    prefix = major_code[:4] if len(major_code)>=4 else major_code
    if prefix in high_salary or major_code in high_salary:
        return "15-30万"
    elif prefix in medium_salary or major_code in medium_salary:
        return "10-20万"
    else:
        return "7-15万"

def generate_major_info(major):
    name = major['name']
    return {
        "code": major['code'],
        "name": name,
        "category": major['category'],
        "category_icon": major['category_icon'],
        "difficulty": get_difficulty_stars(major['code']),
        "salary_range": get_salary_range(major['code']),
        "overview": f"{name}是研究{name}相关理论与实践的专业，培养掌握{name}基本理论知识和实践技能的专业人才。学生将系统学习相关专业课程，了解行业发展趋势，具备解决实际问题的能力。",
        "what_you_learn": f"主要学习{name}相关的基础课程、专业核心课程和实践课程，包括理论知识学习、实验实训、专业实习等内容，全面提升学生的专业素养和实践能力。",
        "suitable_for": f"适合对{name}领域有浓厚兴趣、善于学习和思考、有责任心的学生报考。",
        "career_outlook": f"毕业生可在相关行业、企事业单位、科研机构等从事{name}相关工作，就业领域广泛，发展前景良好。",
        "xuefeng_comment": f"{name}是研究{name}相关理论与实践应用的重要学科。这个专业具有多方面的优势：1）就业前景广阔，社会对专业人才的需求持续稳定增长；2）可以往多个方向发展，职业选择较多；3）薪资水平在合理范围内，随着经验积累有不错的上升空间；4）工作环境相对舒适，职业发展路径清晰可见；5）可以进入国企、外企或民营企业，选择多样。这个专业也有一些需要注意的方面：1）课程难度较大，需要认真学习和深入实践才能掌握；2）行业竞争存在，需要不断提升专业能力和核心竞争力；3）部分岗位需要持续学习新技术，保持知识更新；4）初期薪资可能不如一些热门专业，但长期发展潜力大。给考生的报考建议：1）建议提前了解专业具体学习内容和工作方向，确保适合自己；2）选择一个细分方向深耕，形成自己的核心竞争力；3）积累实习经验对未来的就业非常重要；4）可以考取相关职业资格证书增加竞争力；5）持续学习和自我提升是职业发展的关键。这个专业适合对专业有浓厚兴趣、愿意努力学习、追求稳定职业发展的学生报考。",
        "yearly_courses": json.dumps({
            "大一": ["高等数学", "大学物理", "大学英语", "计算机基础", "专业导论"],
            "大二": ["专业基础课1", "专业基础课2", "专业核心课1", "通识选修课"],
            "大三": ["专业核心课2", "专业核心课3", "专业选修课", "专业实践"],
            "大四": ["专业实习", "毕业设计", "就业指导"]
        }),
        "top_universities": json.dumps({
            "985/211": ["清华大学", "北京大学", "复旦大学", "上海交通大学"],
            "双一流": ["浙江大学", "南京大学", "武汉大学", "中山大学"],
            "特色院校": ["相关专业特色院校"]
        })
    }

def check_major_exists(code):
    response = requests.get(f"{SUPABASE_URL}/rest/v1/majors?code=eq.{code}", headers=headers)
    return len(response.json()) > 0

def insert_majors():
    inserted = 0
    skipped = 0
    
    for major in new_majors:
        if check_major_exists(major['code']):
            print(f"⏭️  跳过已存在: {major['code']} - {major['name']}")
            skipped += 1
            continue
            
        major_data = generate_major_info(major)
        response = requests.post(f"{SUPABASE_URL}/rest/v1/majors", headers=headers, json=major_data)
        
        if response.status_code in [200, 201]:
            print(f"✅ 新增成功: {major['code']} - {major['name']}")
            inserted += 1
        else:
            print(f"❌ 新增失败: {major['code']} - {response.status_code} - {response.text}")
            
        time.sleep(0.1)
        
    print(f"\n{'='*50}")
    print(f"完成: 新增 {inserted} 个专业，跳过 {skipped} 个已存在专业")
    print(f"{'='*50}")

if __name__ == "__main__":
    print(f"准备新增 {len(new_majors)} 个专业...\n")
    insert_majors()
