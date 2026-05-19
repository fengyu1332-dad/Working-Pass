"""
检查数据库中的重复专业
"""
import urllib.request
import json
import ssl
from collections import defaultdict

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 获取所有专业
req = urllib.request.Request(f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name,category')
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    majors = json.loads(response.read().decode('utf-8'))

print("=" * 80)
print("检查数据库中的重复专业")
print("=" * 80)

# 按code分组
by_code = defaultdict(list)
for m in majors:
    by_code[m['code']].append(m)

# 找出重复的
duplicates = {code: items for code, items in by_code.items() if len(items) > 1}

if duplicates:
    print(f"\n发现 {len(duplicates)} 个专业代码有重复：\n")
    
    for code, items in sorted(duplicates.items()):
        print(f"\n📌 {code} ({len(items)}个重复)：")
        for item in items:
            print(f"   - ID: {item['id']}, 名称: {item['name']}, 类别: {item['category']}")
else:
    print("\n✅ 数据库中没有重复的专业代码！")

print("\n" + "=" * 80)
print("处理建议")
print("=" * 80)
print("""
根据发现的情况，有以下处理方案：

方案1：保留最新添加的
- 删除重复记录，保留最新创建的
- 优点：数据最新
- 缺点：可能丢失历史数据

方案2：保留ID最小的（最早创建）
- 删除重复记录，保留最早创建的
- 优点：保持数据历史
- 缺点：数据可能过时

方案3：手动合并
- 对比重复记录，保留内容最完整的
- 优点：数据质量最高
- 缺点：工作量大

方案4：全部保留
- 如果重复记录内容不同，视为不同专业
- 优点：数据完整
- 缺点：总数会超出教育部清单

建议：如果重复数量不多，可以手动合并或保留内容最完整的记录。
""")
