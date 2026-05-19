import urllib.request
import urllib.error
import json
import ssl
from collections import defaultdict

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_majors():
    url = f"{SUPABASE_URL}/rest/v1/majors?select=*"
    req = urllib.request.Request(url)
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"请求失败: {e}")
        return []

def analyze_majors():
    majors = fetch_majors()
    if not majors:
        print("未能获取数据")
        return
    
    print("=" * 80)
    print("📊 当前数据库专业分布分析")
    print("=" * 80)
    print(f"\n✅ 数据库专业总数: {len(majors)}")
    
    # 按学科分类
    categories = defaultdict(list)
    for m in majors:
        cat = m['category']
        categories[cat].append(m)
    
    print("\n" + "=" * 80)
    print("📚 各学科门类专业分布")
    print("=" * 80)
    
    sorted_cats = sorted(categories.items(), key=lambda x: x[0])
    for cat, ms in sorted_cats:
        print(f"\n{cat}: {len(ms)}个专业")
        # 按专业代码排序
        ms_sorted = sorted(ms, key=lambda x: x['code'])
        for m in ms_sorted:
            print(f"  {m['code']:<12} - {m['name']}")
    
    print("\n" + "=" * 80)
    print("📈 学科门类统计")
    print("=" * 80)
    
    total_by_cat = {}
    for cat, ms in sorted_cats:
        total_by_cat[cat] = len(ms)
    
    # 显示柱状图
    max_count = max(total_by_cat.values())
    for cat, count in sorted(total_by_cat.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(count / max_count * 30)
        print(f"{cat}: {count:3d} {bar}")
    
    print("\n" + "=" * 80)
    print("🎯 重点学科详细分析")
    print("=" * 80)
    
    # 08 工学详细分析
    if '08 工学' in categories:
        print("\n🔧 08 工学（112个）详细分类:")
        print("=" * 80)
        
        # 按专业类细分
        sub_cats = defaultdict(list)
        for m in categories['08 工学']:
            code = m['code']
            if len(code) >= 5:
                sub_cat = code[:5]  # 取前5位
                sub_cats[sub_cat].append(m)
        
        for sub_cat, sub_majors in sorted(sub_cats.items()):
            print(f"\n{sub_cat}x: {len(sub_majors)}个专业")
            for m in sorted(sub_majors, key=lambda x: x['code']):
                print(f"  {m['code']:<12} - {m['name']}")

if __name__ == "__main__":
    analyze_majors()
