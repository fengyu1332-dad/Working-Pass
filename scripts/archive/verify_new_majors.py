import requests

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

# 检查几个新增的代表性专业
sample_codes = ['080201', '080905', '082001', '083201T', '081008T', '081808TK']

print("检查新增专业的详细信息...\n")
for code in sample_codes:
    response = requests.get(f"{SUPABASE_URL}/rest/v1/majors?code=eq.{code}", headers=headers)
    majors = response.json()
    if majors:
        m = majors[0]
        comment_length = len(m.get('xuefeng_comment', ''))
        print(f"{m['code']} - {m['name']}")
        print(f"  学科: {m['category']}")
        print(f"  难度: {m['difficulty']}")
        print(f"  薪资: {m['salary_range']}")
        print(f"  点评长度: {comment_length} 字符")
        print(f"  点评预览: {m.get('xuefeng_comment', '')[:80]}...")
        print()
