import requests
import json

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

response = requests.get(f"{SUPABASE_URL}/rest/v1/majors?select=code,name,category", headers=headers)
majors = response.json()

print(f"Total majors: {len(majors)}\n")

# 按类别分组
categories = {}
for major in majors:
    cat = major.get('category', '未分类')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(f"{major['code']} - {major['name']}")

print("按学科类别分布：")
for cat, items in sorted(categories.items()):
    print(f"\n{cat} ({len(items)}):")
    for item in items:
        print(f"  {item}")
