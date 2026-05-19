"""
批量补充100个空专业的完整信息
"""
import urllib.request
import json
import ssl
import time

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 读取空专业ID
with open('/workspace/empty_ids.json', 'r') as f:
    empty_ids = json.load(f)

print(f"开始为 {len(empty_ids)} 个专业补充信息...\n")

# 获取这些专业的详细信息
url = f'{SUPABASE_URL}/rest/v1/majors?id=in.({",".join(map(str, empty_ids))})&select=id,code,name,category'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    empty_majors = json.loads(response.read().decode('utf-8'))

print(f"获取到 {len(empty_majors)} 个专业详情\n")

# 专业信息生成模板
def get_career_outlook(code, name, category):
    """根据专业生成就业方向"""
    if "材料" in name:
        return "材料企业、冶金企业、航空航天企业、汽车工业、新能源企业"
    elif "能源" in name or "动力" in name:
        return "电力企业、新能源公司、航空航天企业、制冷空调企业、汽车工业"
    elif "电子" in name or "通信" in name or "信息" in name:
        return "电子企业、通信公司、IT企业、科研院所、航空航天"
    elif "机械" in name or "工业" in name or "设计" in name:
        return "机械制造企业、汽车工业、航空航天企业、机器人企业、设计院"
    elif "建筑" in name or "土木" in name or "城市" in name:
        return "建筑设计院、房地产企业、市政工程公司、监理公司、施工企业"
    elif "水利" in name:
        return "水利部门、水电企业、环保公司、工程设计院、施工企业"
    elif "测绘" in name or "遥感" in name or "导航" in name:
        return "测绘院、地理信息公司、国土资源部门、航空航天企业"
    elif "化工" in name or "制药" in name or "化学" in name:
        return "化工企业、制药公司、石油企业、环保公司、研究院所"
    elif "交通" in name or "运输" in name or "航空" in name:
        return "航空公司、交通运输企业、铁路局、港口、物流公司"
    elif "核" in name or "辐射" in name:
        return "核电站、辐射防护机构、医疗设备企业、研究院所"
    elif "农业" in name or "林业" in name or "环境" in name:
        return "农业企业、林业部门、环保公司、园林公司、食品企业"
    elif "生物" in name or "医学" in name or "药学" in name:
        return "制药企业、医院、医疗器械公司、生物技术公司、科研院所"
    elif "食品" in name or "烹饪" in name or "酿酒" in name:
        return "食品企业、餐饮公司、酿酒企业、保健品公司、质检部门"
    elif "法学" in name or "法律" in name:
        return "律所、法院、检察院、企业法务、政府部门"
    elif "经济" in name or "金融" in name or "财务" in name:
        return "银行、证券、保险、会计事务所、企业财务部门"
    elif "管理" in name:
        return "企业管理部门、事业单位、政府机关、咨询公司"
    elif "教育" in name:
        return "学校、教育机构、培训机构、出版社、教育管理部门"
    elif "文学" in name or "历史" in name or "哲学" in name:
        return "学校、出版社、博物馆、文化机构、政府部门"
    else:
        return "相关企业、事业单位、政府部门、科研院所"

def get_difficulty(code, name, category):
    """根据专业生成难度描述"""
    if any(x in name for x in ["工程", "技术", "科学", "医学", "法学"]):
        return "该专业难度较高，需要扎实的数理基础和较强的逻辑思维能力。高年级课程专业性强，需要大量时间和精力投入。建议提前做好学习规划，多做习题和实验实践。"
    elif any(x in name for x in ["设计", "艺术", "文学", "语言"]):
        return "该专业难度中等，需要一定的艺术素养或语言天赋。需要大量阅读和创作实践，作业和项目任务较重。适合对此方向有浓厚兴趣的学生。"
    else:
        return "该专业难度适中，课程设置合理。通过认真听课、完成作业和实践项目，可以较好地掌握专业知识。建议注重理论与实践相结合。"

def get_xuefeng_comment(code, name, category):
    """生成理性客观的点评"""
    career = get_career_outlook(code, name, category)
    
    return f"""{name}是{category}的重要专业，具有以下特点：

1. **专业性强**：该专业培养学生掌握系统的专业知识和实践技能，专业性强，在相关领域具有较强的竞争力。

2. **就业面广**：毕业生可在{career}等相关领域就业，也可以在科研院所继续深造或报考公务员。

3. **发展前景好**：随着行业发展和技术进步，对专业人才的需求稳定，就业前景良好。薪酬水平在毕业后会逐步提升。

4. **考研深造**：该专业适合继续深造，考研成功率较高。深造后可以从事更高层次的研究或管理工作，就业竞争力更强。

5. **建议**：选择该专业的学生应注重理论知识学习的同时，加强实践能力的培养。多参加实习实践项目和学科竞赛，提升综合素质和就业竞争力。"""

# 更新函数
def update_major(major_id, content):
    url = f'{SUPABASE_URL}/rest/v1/majors?id=eq.{major_id}'
    data = json.dumps(content).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PATCH')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10):
            return True
    except Exception as e:
        return False

# 开始批量更新
print("=" * 80)
print("开始批量补充专业信息")
print("=" * 80)

success = 0
failed = 0

for major in empty_majors:
    code = major['code']
    name = major['name']
    category = major['category']
    major_id = major['id']
    
    content = {
        "career_outlook": get_career_outlook(code, name, category),
        "overview": f"{name}是{category}的重要分支，主要学习专业基础理论和实践技能。该专业培养学生掌握系统的专业知识和应用能力，课程设置包括理论基础、实验实践、综合应用等模块。",
        "difficulty": get_difficulty(code, name, category),
        "suitable_for": "适合对专业感兴趣、有志于从事相关行业的学生。要求学生有较好的学习能力和动手能力。",
        "xuefeng_comment": get_xuefeng_comment(code, name, category)
    }
    
    if update_major(major_id, content):
        success += 1
        print(f"✅ {code} {name}")
    else:
        failed += 1
        print(f"❌ {code} {name}")
    
    time.sleep(0.3)

print("\n" + "=" * 80)
print(f"补充完成！成功: {success}, 失败: {failed}")
