"""
重新检查并补充空专业
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

# 获取所有专业
url = f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name,category,career_outlook'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    all_majors = json.loads(response.read().decode('utf-8'))

print(f"总专业数: {len(all_majors)}")

# 找出career_outlook为空的
empty_majors = [m for m in all_majors if not m.get('career_outlook')]

print(f"career_outlook为空的专业: {len(empty_majors)}")

if empty_majors:
    print("\n前10个空专业：")
    for m in empty_majors[:10]:
        print(f"  {m['code']} {m['name']} ({m['category']})")
    
    # 导出ID列表
    empty_ids = [m['id'] for m in empty_majors]
    with open('/workspace/empty_ids.json', 'w') as f:
        json.dump(empty_ids, f)
    print(f"\n已保存 {len(empty_ids)} 个空专业ID到 empty_ids.json")
else:
    print("所有专业都已补充career_outlook信息！")
