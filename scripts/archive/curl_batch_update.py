"""
使用curl批量更新100个空专业
"""
import subprocess
import time
import json

# 读取空专业信息
empty_majors = []
with open('/workspace/empty_ids.txt', 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) == 4:
            empty_majors.append({
                'id': parts[0],
                'code': parts[1],
                'name': parts[2],
                'category': parts[3]
            })

print(f"开始使用curl更新 {len(empty_majors)} 个专业...\n")

# API密钥
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'
BASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co/rest/v1/majors'

# 专业信息生成
def generate_content(code, name, category):
    career_map = {
        "材料": "材料企业、冶金企业、航空航天、新能源",
        "能源": "电力企业、新能源公司、航空航天、制冷空调",
        "电子": "电子企业、通信公司、IT企业、科研院所",
        "通信": "通信企业、运营商、IT公司",
        "信息": "IT企业、互联网公司、金融机构",
        "机械": "机械制造企业、汽车工业、航空航天、机器人",
        "工业": "制造企业、规划设计院、科技公司",
        "设计": "设计院、装饰公司、建筑企业",
        "建筑": "建筑设计院、房地产、市政工程",
        "土木": "建筑企业、设计院、房地产、监理公司",
        "城市": "规划设计院、市政公司、园林公司",
        "水利": "水利部门、水电企业、环保公司",
        "测绘": "测绘院、地理信息公司、国土资源",
        "遥感": "遥感公司、地理信息企业、环保部门",
        "导航": "导航企业、航空航天、测绘公司",
        "化工": "化工企业、制药公司、石油企业",
        "制药": "制药企业、生物技术公司、医院",
        "交通": "航空公司、铁路局、港口、物流公司",
        "航空": "航空公司、航空制造企业、军事航空",
        "航天": "航天企业、研究院所、军事航天",
        "核": "核电站、辐射防护机构、医疗设备",
        "农业": "农业企业、林业部门、环保公司",
        "生物": "制药企业、生物技术公司、医院",
        "医学": "医院、制药企业、医疗器械公司",
        "药学": "制药企业、药店、医院药剂科",
        "食品": "食品企业、餐饮公司、酿酒企业",
        "安全": "安全管理部门、消防救援、企业安全",
        "林业": "林业部门、森林公园、园林公司",
        "电气": "电力公司、电气设备企业",
        "自动": "自动化企业、智能制造、工业机器人",
        "智能": "科技公司、智能制造企业、AI企业",
        "数据": "IT企业、金融机构、数据分析公司",
        "网络": "网络企业、运营商、互联网公司",
        "计算": "IT企业、互联网公司、软件企业",
        "软件": "软件企业、互联网公司、IT企业",
        "系统": "IT企业、科研院所、军工企业",
        "科学": "科研院所、高等院校、企业研发",
        "工程": "设计院、施工企业、监理公司",
    }
    
    career = "相关企业、事业单位、科研院所"
    for key, value in career_map.items():
        if key in name:
            career = value
            break
    
    overview = f"{name}是{category}的重要分支，主要研究专业基础理论和实践应用技术。课程包括理论基础、专业核心、实践环节等模块。"
    
    difficulty = "该专业难度较高，需要扎实的数理基础和较强的逻辑思维能力。高年级课程专业性强，需要认真学习和大量练习。"
    
    suitable = "适合对专业感兴趣、有志于从事相关行业的学生。要求有较好的学习能力和动手能力。"
    
    comment = f"""{name}是{category}的重要专业：

1. **专业性强**：培养系统专业知识和实践技能，就业竞争力较强。

2. **就业面广**：毕业生可在{career}等相关领域就业。

3. **发展前景好**：行业需求稳定，薪酬水平会逐步提升。

4. **考研深造**：适合继续深造，深造后就业竞争力更强。

5. **建议**：注重理论学习的同时加强实践，多参加实习和项目实践。"""
    
    return {
        "career_outlook": career,
        "overview": overview,
        "difficulty": difficulty,
        "suitable_for": suitable,
        "xuefeng_comment": comment
    }

# 批量更新
print("=" * 80)
success = 0
failed = 0

for m in empty_majors:
    content = generate_content(m['code'], m['name'], m['category'])
    json_data = json.dumps(content, ensure_ascii=False)
    
    cmd = [
        'curl', '-X', 'PATCH',
        f'{BASE_URL}?id=eq.{m["id"]}',
        '-H', f'apikey: {API_KEY}',
        '-H', f'Authorization: Bearer {API_KEY}',
        '-H', 'Content-Type: application/json',
        '-H', 'Prefer: return=representation',
        '-d', json_data,
        '-s'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and 'id' in result.stdout:
        success += 1
        print(f"✅ {m['code']} {m['name']}")
    else:
        failed += 1
        print(f"❌ {m['code']} {m['name']} - {result.stderr[:50] if result.stderr else 'unknown error'}")
    
    time.sleep(0.2)

print("\n" + "=" * 80)
print(f"✅ 成功: {success}, ❌ 失败: {failed}")
