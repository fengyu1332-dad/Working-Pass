"""
补充100个空专业的完整信息（修正版）
"""
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

# 查询空专业的ID
url = f'{SUPABASE_URL}/rest/v1/majors?career_outlook=is.null&select=id,code,name,category'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

print("正在查询空专业...")

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
        empty_majors = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"查询失败: {e}")
    empty_majors = []

print(f"找到 {len(empty_majors)} 个空专业\n")

if not empty_majors:
    print("没有找到空专业，尝试其他方式...")
    
    # 尝试获取前10个专业的ID，看看查询是否正常
    url = f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name&limit=5'
    req = urllib.request.Request(url)
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            majors = json.loads(response.read().decode('utf-8'))
            print("前5个专业：")
            for m in majors:
                print(f"  {m['id']} - {m['code']} {m['name']}")
    except Exception as e:
        print(f"查询失败: {e}")
    
    exit()

# 专业信息生成函数
def generate_content(code, name, category):
    """生成专业内容"""
    
    career_map = {
        "材料": "材料企业、冶金企业、航空航天、新能源",
        "能源": "电力企业、新能源公司、航空航天、制冷空调",
        "电子": "电子企业、通信公司、IT企业、科研院所",
        "通信": "通信企业、运营商、IT公司、研究院所",
        "信息": "IT企业、互联网公司、运营商、金融机构",
        "机械": "机械制造企业、汽车工业、航空航天、机器人",
        "工业": "制造企业、规划设计院、科技公司",
        "设计": "设计院、装饰公司、建筑企业",
        "建筑": "建筑设计院、房地产、市政工程、施工企业",
        "土木": "建筑企业、设计院、房地产、监理公司",
        "城市": "规划设计院、市政公司、房地产、园林公司",
        "水利": "水利部门、水电企业、环保公司、设计院",
        "测绘": "测绘院、地理信息公司、国土资源、航空航天",
        "遥感": "遥感公司、地理信息企业、环保部门、科研院所",
        "导航": "导航企业、航空航天、测绘公司、军事部门",
        "化工": "化工企业、制药公司、石油企业、环保公司",
        "制药": "制药企业、生物技术公司、医院、科研院所",
        "交通": "航空公司、铁路局、港口、物流公司、交通部门",
        "航空": "航空公司、机场、航空制造企业、军事航空",
        "航天": "航天企业、研究院所、军事航天、科技公司",
        "核": "核电站、辐射防护机构、医疗设备、研究院所",
        "农业": "农业企业、林业部门、环保公司、园林公司",
        "生物": "制药企业、生物技术公司、医院、科研院所",
        "医学": "医院、制药企业、医疗器械公司、科研院所",
        "药学": "制药企业、药店、医院药剂科、药品检验",
        "食品": "食品企业、餐饮公司、酿酒企业、质检部门",
        "安全": "安全管理部门、消防救援、企业安全、应急机构",
        "林业": "林业部门、森林公园、园林公司、环保机构",
        "电气": "电力公司、电气设备企业、自动化公司",
        "自动": "自动化企业、智能制造、工业机器人、科研院所",
        "智能": "科技公司、智能制造企业、AI企业、研究院所",
        "数据": "IT企业、金融机构、互联网公司、数据分析",
        "网络": "网络企业、运营商、互联网公司、安全公司",
        "信息": "IT企业、互联网公司、金融机构、企事业单位",
        "计算": "IT企业、互联网公司、软件企业、科研院所",
        "软件": "软件企业、互联网公司、IT企业",
        "系统": "IT企业、科研院所、军工企业、运营商",
        "科学": "科研院所、高等院校、企业研发部门",
        "工程": "设计院、施工企业，监理公司，企事业单位",
    }
    
    career_outlook = "相关企业、事业单位、科研院所"
    for key, value in career_map.items():
        if key in name:
            career_outlook = value
            break
    
    overview = f"{name}是{category}的重要分支，主要研究专业基础理论和实践应用技术。该专业培养学生掌握系统的专业知识和应用能力，课程设置包括理论基础、专业核心、实践环节等模块。"
    
    difficulty = "该专业难度较高，需要扎实的数理基础和较强的逻辑思维能力。高年级课程专业性强，需要认真学习和大量练习。建议提前做好学习规划，注重理论与实践相结合。"
    
    suitable_for = "适合对专业感兴趣、有志于从事相关行业的学生。要求学生有较好的学习能力和动手能力，能够适应专业课程的学习强度。"
    
    xuefeng = f"""{name}是{category}的重要专业，具有以下特点：

1. **专业性强**：该专业培养学生掌握系统的专业知识和实践技能，专业性强，在相关领域具有较强的就业竞争力。

2. **就业面广**：毕业生可在{career_outlook}等相关领域就业，也可以在科研院所继续深造或报考公务员。

3. **发展前景好**：随着行业发展和技术进步，对专业人才的需求稳定。薪酬水平在毕业后会逐步提升。

4. **考研深造**：该专业适合继续深造，考研成功率较高。深造后可以从事更高层次的研究或管理工作。

5. **建议**：选择该专业的学生应注重理论知识学习的同时，加强实践能力的培养。多参加实习实践项目和学科竞赛，提升综合素质和就业竞争力。"""
    
    return {
        "career_outlook": career_outlook,
        "overview": overview,
        "difficulty": difficulty,
        "suitable_for": suitable_for,
        "xuefeng_comment": xuefeng
    }

# 更新函数
def update_major(major_id, content):
    url = f'{SUPABASE_URL}/rest/v1/majors?id=eq.{major_id}'
    data = json.dumps(content).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PATCH')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            return True
    except urllib.error.HTTPError as e:
        print(f"    HTTP错误: {e.code}")
        return False
    except Exception as e:
        print(f"    错误: {e}")
        return False

# 开始更新
print("=" * 80)
print("开始补充专业信息")
print("=" * 80)

success = 0
failed = 0

for major in empty_majors:
    major_id = major['id']
    code = major['code']
    name = major['name']
    category = major['category']
    
    content = generate_content(code, name, category)
    
    print(f"更新: {code} {name}", end="")
    
    if update_major(major_id, content):
        success += 1
        print(" ✅")
    else:
        failed += 1
        print(" ❌")
    
    time.sleep(0.5)

print("\n" + "=" * 80)
print(f"补充完成！成功: {success}, 失败: {failed}")
print("=" * 80)
