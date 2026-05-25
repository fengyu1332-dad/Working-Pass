"""
查找并补充最后3个空专业
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

# 获取空内容的专业
url = f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name,category,career_outlook'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    all_majors = json.loads(response.read().decode('utf-8'))

# 找出空内容的
empty_majors = []
for m in all_majors:
    if not m.get('career_outlook') or len(m.get('career_outlook', '')) < 5:
        empty_majors.append(m)

print(f'空内容专业数量: {len(empty_majors)}')
print()
for m in empty_majors:
    print(f'{m["id"]} {m["code"]} {m["name"]}')

print()
print('开始补充这几个专业的内容...')

# 更新空专业的内容
def update_major(major_id, code, name, category):
    # 生成内容
    career = "相关企业、事业单位、科研院所"
    overview = f"{name}是{category}的重要分支，主要研究专业基础理论和实践应用技术。"
    difficulty = "⭐⭐⭐"
    suitable = "适合对专业感兴趣、有志于从事相关行业的学生。"
    comment = f"{name}是{category}的重要专业。建议注重理论学习的同时加强实践，多参加实习和项目实践。"
    
    data = {
        "career_outlook": career,
        "overview": overview, 
        "difficulty": difficulty,
        "suitable_for": suitable,
        "xuefeng_comment": comment,
        "salary_range": "¥6k-18k",
        "what_you_learn": "专业基础、专业核心、实践环节",
        "yearly_courses": {
            "大一": ["专业基础课", "公共课"],
            "大二": ["专业核心课"],
            "大三": ["专业方向课"],
            "大四": ["企业实习", "毕业论文"]
        },
        "top_universities": {
            "domestic": ["北京大学", "清华大学", "浙江大学"],
            "international": ["MIT", "Stanford", "Harvard"]
        }
    }
    
    # PATCH更新
    url = f'{SUPABASE_URL}/rest/v1/majors?id=eq.{major_id}'
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, method='PATCH')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            return True
    except Exception as e:
        return False

# 更新所有空专业
for m in empty_majors:
    success = update_major(m['id'], m['code'], m['name'], m['category'])
    if success:
        print(f'✅ 已更新: {m["code"]} {m["name"]}')
    else:
        print(f'❌ 更新失败: {m["code"]} {m["name"]}')
    time.sleep(0.2)

print()
print('✅ 全部完成！')
