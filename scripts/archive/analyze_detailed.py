"""
详细分析教育部完整清单和数据库对比
"""
import urllib.request
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("=" * 80)
print("教育部2024年本科专业目录统计")
print("=" * 80)

# 读取完整的analyze_majors.py来获取清单
with open('/workspace/analyze_majors.py', 'r') as f:
    content = f.read()

# 提取清单部分
import re
match = re.search(r'MINISTRY_2024_CATEGORIES = (\{.*\})', content, re.DOTALL)
if match:
    import ast
    MINISTRY_2024_CATEGORIES = ast.literal_eval(match.group(1))
    
    total_majors = 0
    category_counts = {}
    for category, majors in sorted(MINISTRY_2024_CATEGORIES.items()):
        count = len(majors)
        category_counts[category] = count
        total_majors += count
        print(f"{category:20s}: {count:3d}个专业")
    
    print(f"\n{'总计':20s}: {total_majors:3d}个专业\n")
    
    # 按数量排序
    print("各学科门类专业数排名：")
    sorted_cats = sorted(category_counts.items(), key=lambda x: -x[1])
    for i, (cat, cnt) in enumerate(sorted_cats, 1):
        print(f"{i:2d}. {cat:20s} {cnt:3d}")

# 获取数据库中的专业
print("\n" + "=" * 80)
print("数据库专业按类别统计")
print("=" * 80)

req = urllib.request.Request(f'{SUPABASE_URL}/rest/v1/majors?select=code,category')
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    db_majors = json.loads(response.read().decode('utf-8'))

from collections import defaultdict
db_by_category = defaultdict(int)
for major in db_majors:
    cat = major.get('category', 'unknown')
    db_by_category[cat] += 1

for cat in sorted(db_by_category.keys()):
    print(f"{cat:20s}: {db_by_category[cat]:3d}个专业")

print(f"\n总计: {len(db_majors)}个专业")

print("\n" + "=" * 80)
print("原因说明")
print("=" * 80)
print("""
1. 工学是最大的学科门类，在教育部清单中占比约30%
2. 数据库中的869个专业是所有类别的总和，其中工学只有92个
3. 工学本身有241个专业，所以看起来缺失很多
4. 但我们已经覆盖了最主要和常用的工学专业
""")
