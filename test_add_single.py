"""
测试添加一个专业，查看详细错误
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

# 测试数据
test_data = {
    "code": "080101",
    "name": "理论与应用力学",
    "category": "工学",
    "career_outlook": "相关企业、事业单位、科研院所",
    "overview": "这是一门专业",
    "difficulty": "较难",
    "suitable_for": "适合相关学生",
    "xuefeng_comment": "这是一个点评",
    "status": "active",
    "view_count": 0
}

print("尝试添加专业...")
print("数据:")
print(json.dumps(test_data, ensure_ascii=False, indent=2))

url = f'{SUPABASE_URL}/rest/v1/majors'
data = json.dumps(test_data).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
req.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
        print(f"✅ 成功！状态码: {response.status}")
        result = json.loads(response.read().decode('utf-8'))
        print(f"结果: {result}")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP 错误: {e.code}")
    print(f"错误信息: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"❌ 错误: {e}")
