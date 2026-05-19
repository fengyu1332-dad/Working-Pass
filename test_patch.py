"""
测试PATCH更新
"""
import urllib.request
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 获取一个空专业的ID
url = f'{SUPABASE_URL}/rest/v1/majors?career_outlook=is.null&select=id&limit=1'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    result = json.loads(response.read().decode('utf-8'))

if result:
    test_id = result[0]['id']
    print(f"测试更新ID: {test_id}")
    
    # 测试PATCH
    url = f'{SUPABASE_URL}/rest/v1/majors?id=eq.{test_id}'
    data = json.dumps({"career_outlook": "测试就业方向"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PATCH')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            print(f"成功！状态码: {response.status}")
            print(f"响应: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code}")
        print(f"错误信息: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"错误: {e}")
else:
    print("没有找到空专业")
