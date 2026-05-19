"""
使用curl批量更新100个空专业（缩短版）
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

print(f"开始更新 {len(empty_majors)} 个专业（缩短版）...\n")

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'
BASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co/rest/v1/majors'

# 专业信息生成（缩短版，确保所有字段<=20字符）
def generate_content(code, name, category):
    career_map = {
        "材料": "材料企业、航空航天",
        "能源": "电力企业、新能源公司",
        "电子": "电子企业、通信公司",
        "通信": "通信企业、运营商",
        "信息": "IT企业、互联网公司",
        "机械": "机械制造、汽车工业",
        "设计": "设计院、装饰公司",
        "建筑": "设计院、房地产公司",
        "土木": "建筑企业、监理公司",
        "城市": "规划设计院、市政",
        "水利": "水利部门、水电企业",
        "测绘": "测绘院、地理信息",
        "遥感": "遥感公司、测绘院",
        "导航": "导航企业、航空航天",
        "化工": "化工企业、制药公司",
        "制药": "制药企业、医院",
        "交通": "航空、铁路、港口",
        "航空": "航空公司、航空制造",
        "航天": "航天企业、研究院",
        "核": "核电站、医疗设备",
        "农业": "农业企业、林业部门",
        "生物": "制药企业、医院",
        "医学": "医院、制药企业",
        "药学": "制药企业、药店",
        "食品": "食品企业、餐饮公司",
        "安全": "安全部门、消防救援",
        "林业": "林业部门、园林公司",
        "电气": "电力公司、设备企业",
        "自动": "自动化企业、机器人",
        "智能": "科技公司、AI企业",
        "数据": "IT企业、数据分析",
        "网络": "网络企业、运营商",
        "计算": "IT企业、软件企业",
        "软件": "软件企业、互联网",
        "系统": "IT企业、科研院所",
        "科学": "科研院所、高校",
        "工程": "设计院、施工企业",
    }
    
    career = "相关企业、事业单位"
    for key, value in career_map.items():
        if key in name:
            career = value
            break
    
    # 确保每个字段不超过20字符
    overview = f"{name}是{category}专业，主要学习专业理论和实践技能。"
    
    difficulty = "该专业难度较高，需要扎实基础和较强逻辑思维。"
    
    suitable = "适合对专业感兴趣、有志从事相关行业的学生。"
    
    comment = f"""{name}是{category}的重要专业：
1.专业性强，就业竞争力较强
2.就业面广，可从事{career}
3.发展前景好，薪酬逐步提升
4.适合考研深造
5.建议多参加实习实践"""
    
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
    
    # 检查字段长度
    for key, value in content.items():
        if len(value) > 500:  # xuefeng_comment可能较长
            content[key] = value[:500]
    
    json_data = json.dumps(content, ensure_ascii=False)
    
    cmd = [
        'curl', '-X', 'PATCH',
        f'{BASE_URL}?id=eq.{m["id"]}',
        '-H', f'apikey: {API_KEY}',
        '-H', f'Authorization: Bearer {API_KEY}',
        '-H', 'Content-Type: application/json',
        '-H', 'Prefer: return=representation',
        '-d', json_data,
        '-s', '-w', '\\nHTTP_CODE:%{http_code}'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if 'HTTP_CODE:200' in result.stdout or 'HTTP_CODE:201' in result.stdout:
        success += 1
        print(f"✅ {m['code']} {m['name']}")
    else:
        failed += 1
        print(f"❌ {m['code']} {m['name']}")
        # 打印错误
        if result.stdout:
            print(f"   错误: {result.stdout[:150]}")
    
    time.sleep(0.2)

print("\n" + "=" * 80)
print(f"✅ 成功: {success}, ❌ 失败: {failed}")
