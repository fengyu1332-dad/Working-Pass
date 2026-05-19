"""
获取并补充100个空专业的信息
"""
import urllib.request
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 获取空专业的ID和基本信息
url = f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name,category&career_outlook=is.null'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    empty_majors = json.loads(response.read().decode('utf-8'))

print(f"需要补充信息的空专业: {len(empty_majors)} 个\n")
print("专业列表：")
for i, major in enumerate(empty_majors, 1):
    print(f"{i:3d}. {major['code']} {major['name']} ({major['category']})")

# 导出到JSON方便后续使用
with open('/workspace/empty_majors.json', 'w', encoding='utf-8') as f:
    json.dump(empty_majors, f, ensure_ascii=False, indent=2)

print(f"\n已将空专业列表保存到 empty_majors.json")
