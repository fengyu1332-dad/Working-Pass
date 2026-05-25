"""
测试数据库插入并获取错误详情
"""
import urllib.request
import urllib.error
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 测试插入一个专业
test_major = {
    "code": "100101K",
    "name": "临床医学",
    "category": "医学",
    "description": "培养具备临床诊疗能力的医学人才",
    "tags": ["教育部2024清单"],
    "salary_score": 50,
    "difficulty_score": 80,
    "prospects_score": 80,
    "hot_score": 90
}

url = f'{SUPABASE_URL}/rest/v1/majors'
data = json.dumps(test_major).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
req.add_header('Content-Type', 'application/json')
req.add_header('Prefer', 'return=representation')

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
        print(f"✅ Success: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error: {e.code}")
    print(f"Error Body: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"❌ Error: {e}")
