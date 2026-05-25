"""
测试curl PATCH请求
"""
import subprocess
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'
BASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co/rest/v1/majors'

# 测试一条记录
content = {
    "career_outlook": "测试就业方向",
    "overview": "测试概述内容",
    "difficulty": "测试难度描述",
    "suitable_for": "测试适合人群",
    "xuefeng_comment": "测试点评"
}
json_data = json.dumps(content, ensure_ascii=False)

cmd = [
    'curl', '-X', 'PATCH',
    f'{BASE_URL}?id=eq.1191',
    '-H', f'apikey: {API_KEY}',
    '-H', f'Authorization: Bearer {API_KEY}',
    '-H', 'Content-Type: application/json',
    '-H', 'Prefer: return=representation',
    '-d', json_data,
    '-s', '-w', '\\nHTTP_CODE:%{http_code}'
]

print("执行curl命令...")
result = subprocess.run(cmd, capture_output=True, text=True)

print(f"返回码: {result.returncode}")
print(f"stdout:\n{result.stdout}")
print(f"stderr:\n{result.stderr}")

# 检查是否成功
if '"id"' in result.stdout:
    print("\n✅ 成功！")
else:
    print("\n❌ 失败！")
