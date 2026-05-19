import urllib.request
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def check_majors():
    url = f"{SUPABASE_URL}/rest/v1/majors?select=code,name,category"
    
    req = urllib.request.Request(url)
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    
    with urllib.request.urlopen(req, context=ctx) as response:
        majors = json.loads(response.read().decode('utf-8'))
        
        # 按类别统计
        from collections import defaultdict
        categories = defaultdict(list)
        for m in majors:
            categories[m['category']].append(m)
        
        print("=" * 70)
        print(f"📊 专业总数: {len(majors)}")
        print("=" * 70)
        
        for cat, ms in sorted(categories.items()):
            print(f"\n{cat}: {len(ms)}个专业")
            for m in ms[:5]:  # 每个类别显示前5个
                print(f"  {m['code']:<12} - {m['name']}")
            if len(ms) > 5:
                print(f"  ...还有 {len(ms)-5} 个")

check_majors()
