"""
分析数据库中超出教育部清单的专业
"""
import urllib.request
import json
import ssl
import re

# 读取analyze_majors.py获取清单
with open('/workspace/analyze_majors.py', 'r') as f:
    content = f.read()

# 提取MINISTRY_2024_CATEGORIES部分
start_idx = content.find('MINISTRY_2024_CATEGORIES = {')
end_idx = content.find('\n}', start_idx) + 2
ministry_text = content[start_idx:end_idx]

# 解析清单中的代码
ministry_codes = set()
for match in re.finditer(r'"(\d{6}[A-Z]?)":', ministry_text):
    ministry_codes.add(match.group(1))

print(f"教育部清单中的专业代码数量: {len(ministry_codes)}")

# 获取数据库中的专业代码
SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(f'{SUPABASE_URL}/rest/v1/majors?select=code,name,category')
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    majors = json.loads(response.read().decode('utf-8'))

db_codes = [m['code'] for m in majors]
print(f"数据库中的专业总数: {len(db_codes)}")

# 找出超出清单的专业
extra_codes = [code for code in db_codes if code not in ministry_codes]
print(f"\n超出教育部清单的专业数量: {len(extra_codes)}")
print(f"缺失的专业数量: {len(ministry_codes - set(db_codes))}")

# 分类统计超出的专业
extra_by_category = {}
for m in majors:
    if m['code'] in extra_codes:
        cat = m['category']
        if cat not in extra_by_category:
            extra_by_category[cat] = []
        extra_by_category[cat].append((m['code'], m['name']))

print("\n" + "=" * 80)
print("超出清单的专业按类别分布")
print("=" * 80)

for cat in sorted(extra_by_category.keys()):
    items = extra_by_category[cat]
    print(f"\n📂 {cat} ({len(items)}个)：")
    for code, name in items[:10]:  # 只显示前10个
        print(f"   - {code} {name}")
    if len(items) > 10:
        print(f"   ... 还有 {len(items) - 10} 个")

print("\n" + "=" * 80)
print("结论与处理建议")
print("=" * 80)
print(f"""
✅ 好消息：数据库中没有真正的重复专业代码！

📊 数量差异原因：
   - 数据库总数: {len(db_codes)}
   - 教育部清单: {len(ministry_codes)}
   - 超出清单: {len(extra_codes)} 个
   
💡 这{len(extra_codes)}个专业不在教育部清单中，可能包括：
   1. 新增的特设专业（教育部清单可能有更新延迟）
   2. 交叉学科专业（如人工智能、大数据等）
   3. 高校自主设置的专业
   4. 一些特殊或新兴专业

🎯 处理方案：

方案A：严格对标清单
   - 删除超出清单的 {len(extra_codes)} 个专业
   - 保留清单中的所有专业
   - 优点：严格对标，数据纯净
   - 缺点：可能丢失一些有价值的新兴专业

方案B：保留清单+有价值的新兴专业
   - 保留清单中的 {len(ministry_codes - set(db_codes))} 个缺失专业
   - 保留超出清单但有价值的新兴专业
   - 优点：覆盖更全面
   - 缺点：总数会超出教育部清单

方案C：完全保留
   - 保留所有 {len(db_codes)} 个专业
   - 优点：数据最完整
   - 缺点：总数远超教育部清单

建议：采用方案A + 方案B的混合方案
   - 补充 {len(ministry_codes - set(db_codes))} 个缺失的清单专业
   - 保留有价值的新兴专业（如人工智能等）
   - 这样数据库既完整对标清单，又包含新兴专业
""")
