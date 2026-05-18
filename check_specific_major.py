import requests

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

response = requests.get(f"{SUPABASE_URL}/rest/v1/majors?code=eq.100202&select=code,name,xuefeng_comment", headers=headers)
majors = response.json()

for m in majors:
    comment = m.get('xuefeng_comment', '')
    print(f"Code: {m['code']}")
    print(f"Name: {m['name']}")
    print(f"Comment length: {len(comment)}")
    print(f"Comment preview (first 200 chars): {comment[:200]}")
    print("-" * 50)
