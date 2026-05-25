import requests
import json

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

response = requests.get(f"{SUPABASE_URL}/rest/v1/majors?select=code,name,xuefeng_comment&order=name", headers=headers)
majors = response.json()

print(f"Total majors: {len(majors)}")
print("\n" + "="*60)
print("Checking xuefeng_comment length (sorted by length desc):")
print("="*60)

# Sort by comment length
majors_with_length = []
for m in majors:
    comment = m.get('xuefeng_comment', '') or ''
    length = len(comment)
    majors_with_length.append({
        'code': m.get('code', ''),
        'name': m.get('name', ''),
        'length': length,
        'comment_preview': comment[:100] if comment else '(empty)'
    })

# Sort by length descending
majors_with_length.sort(key=lambda x: x['length'], reverse=True)

short_count = 0
for m in majors_with_length:
    status = "🔴 SHORT" if m['length'] < 350 else "✅ OK"
    print(f"{status} | {m['code']} | {m['name'][:15]:<15} | {m['length']:>4} chars")
    if m['length'] < 350:
        short_count += 1

print("\n" + "="*60)
print(f"Summary: {short_count}/{len(majors)} majors have comments < 350 chars")
print("="*60)
