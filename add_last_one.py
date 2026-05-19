
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

def import_major(major):
    url = f'{SUPABASE_URL}/rest/v1/majors'
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

majors = [
    {
        "code": "080902T",
        "name": "软件工程",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-30k",
        "overview": "软件工程专业培养软件人才，能在IT企业从事软件开发工作。",
        "what_you_learn": "C语言、Java、数据结构、软件工程、数据库原理",
        "suitable_for": "对编程感兴趣的学生。",
        "career_outlook": "互联网企业、IT公司等，就业非常好！",
        "xuefeng_comment": "软件工程专业就业非常好，收入高，强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "C语言程序设计", "线性代数"], "大二": ["数据结构", "Java程序设计", "数据库原理"], "大三": ["软件工程", "软件测试", "软件设计模式"], "大四": ["IT企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "浙江大学", "上海交通大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    }
]

count = 0
skipped = 0

for major in majors:
    ok, code = import_major(major)
    if ok:
        print(f"✅ {major['code']} - {major['name']} 成功")
        count += 1
    elif code == 409:
        print(f"⏭️ {major['code']} - {major['name']} 已存在")
        skipped += 1
    else:
        print(f"❌ {major['code']} - {major['name']} 失败")
    time.sleep(0.5)

print(f"\n导入完成！成功 {count}，跳过 {skipped}")
