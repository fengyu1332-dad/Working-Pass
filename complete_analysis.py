"""
完整分析数据库与教育部清单的对比
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
end_idx = content.find('\ndef ', start_idx)
ministry_text = content[start_idx:end_idx]

# 解析清单中的代码
ministry_codes = {}
for match in re.finditer(r'"(\d{6}[A-Z]{0,2})":\s*"([^"]+)"', ministry_text):
    code = match.group(1)
    name = match.group(2)
    ministry_codes[code] = name

print("=" * 80)
print("数据库 vs 教育部清单 完整对比")
print("=" * 80)

# 获取数据库中的专业
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

# 按代码分组
db_by_code = {}
for m in majors:
    db_by_code[m['code']] = m

print(f"\n📊 统计：")
print(f"   教育部清单专业数: {len(ministry_codes)}")
print(f"   数据库专业数: {len(db_by_code)}")

# 1. 找出格式差异（基代码相同但后缀不同）
format_diffs = []
for db_code, db_info in db_by_code.items():
    if len(db_code) == 6:  # 无后缀
        # 查找可能的带后缀版本
        possible_variants = [
            db_code + 'K',
            db_code + 'T', 
            db_code + 'TK'
        ]
        for variant in possible_variants:
            if variant in ministry_codes:
                format_diffs.append({
                    'db_code': db_code,
                    'db_name': db_info['name'],
                    'expected_code': variant,
                    'expected_name': ministry_codes[variant]
                })
                break

print(f"\n📝 格式差异（数据库无后缀，清单有后缀）: {len(format_diffs)}个")

# 2. 找出真正的重复（同一代码在数据库多次出现）
from collections import Counter
code_counter = Counter(m['code'] for m in majors)
real_duplicates = {code: count for code, count in code_counter.items() if count > 1}

print(f"\n🔄 真正的重复（同一代码多次）: {len(real_duplicates)}个")

# 3. 超出清单的专业（代码不在清单中）
extra_in_db = [db_code for db_code in db_by_code.keys() if db_code not in ministry_codes]
print(f"\n📦 超出清单的专业: {len(extra_in_db)}个")

# 4. 缺失的专业（清单有但数据库没有）
missing_from_db = [code for code in ministry_codes.keys() if code not in db_by_code]
print(f"\n❌ 缺失的专业: {len(missing_from_db)}个")

print("\n" + "=" * 80)
print("示例：格式差异的专业")
print("=" * 80)
if format_diffs:
    print("\n这些专业在数据库中缺少K/T/TK后缀：\n")
    for item in format_diffs[:10]:
        print(f"  数据库: {item['db_code']:10s} {item['db_name']:20s}")
        print(f"  清单应为: {item['expected_code']:10s} {item['expected_name']:20s}")
        print()

print("\n" + "=" * 80)
print("解决方案")
print("=" * 80)
print("""
针对以上问题，建议采用以下方案：

1️⃣ 处理重复（如果有的话）
   - 方案A：删除重复，保留内容最完整的
   - 方案B：保留所有（专业星图可能需要）
   
2️⃣ 处理格式差异（统一代码格式）
   - 将数据库中的代码补上缺失的后缀
   - 例如：030101 → 030101K
   
3️⃣ 补充缺失的专业
   - 将清单中有但数据库没有的专业补充进来
   
4️⃣ 保留超出清单的专业
   - 对于有价值的新兴专业（如人工智能等），可以保留
   - 这些专业虽然不在教育部清单中，但有实际需求

✅ 推荐处理流程：
   1. 先统一代码格式（消除"假重复"）
   2. 删除或合并真正的重复
   3. 补充缺失的清单专业
   4. 评估超出清单的专业，决定是否保留

您希望我执行哪个方案？
""")
