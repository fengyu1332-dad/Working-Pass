"""
补充最后几个缺失专业
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

def import_major(major):
    url = f'{SUPABASE_URL}/rest/v1/majors'
    data = json.dumps(major).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Prefer', 'return=representation')
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            return True, 'created'
    except Exception as e:
        if 'duplicate' in str(e).lower():
            return False, 'already_exists'
        return False, str(e)

def create_major(code, name, category, career_outlook="", overview="", difficulty="", suitable_for="", xuefeng_comment=""):
    return {
        "code": code,
        "name": name,
        "category": category,
        "career_outlook": career_outlook,
        "overview": overview,
        "difficulty": difficulty,
        "suitable_for": suitable_for,
        "xuefeng_comment": xuefeng_comment,
        "status": "active",
        "view_count": 0,
        "salary_range": "面议",
        "top_universities": {},
        "yearly_courses": {},
        "category_icon": "📚",
        "what_you_learn": ""
    }

last_majors = [
    ("070904T", "生态学", "理学", "环保部门、科研院所、生态修复企业", "研究生态系统结构、功能与保护", "较高", "对生态环境保护感兴趣的学生", "生态文明建设需要专业人才。"),
    ("101005", "康复治疗学", "医学", "康复中心、养老机构、医院康复科、残联", "研究康复治疗的理论与技术", "较高", "有爱心、动手能力强的学生", "老龄化社会带动康复治疗需求。"),
    ("130412T", "艺术设计学", "艺术学", "设计公司、美术学院、研究机构", "研究艺术设计理论与历史", "中等", "设计基础好、有学术兴趣的学生", "艺术设计学偏理论。"),
]

print("补充最后几个缺失专业...")
print("=" * 60)

success_count = 0
skip_count = 0

for code, name, category, career_outlook, overview, difficulty, suitable_for, xuefeng_comment in last_majors:
    m = create_major(code, name, category, career_outlook, overview, difficulty, suitable_for, xuefeng_comment)
    success, result = import_major(m)
    
    if success:
        print(f"✅ {code} - {name}")
        success_count += 1
    else:
        if result == 'already_exists':
            print(f"⏭️ {code} - {name} (已存在)")
            skip_count += 1
        else:
            print(f"❌ {code} - {name} (失败: {result})")
    
    time.sleep(0.3)

print("\n" + "=" * 60)
print(f"✅ 成功添加 {success_count} 个专业")
print(f"⏭️ 跳过 {skip_count} 个(已存在)")
