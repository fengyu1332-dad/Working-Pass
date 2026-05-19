"""
全面检查611个专业的信息质量和完整性
"""
import urllib.request
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 获取所有专业完整信息
print("正在获取数据库中的所有专业信息...")
url = f'{SUPABASE_URL}/rest/v1/majors?select=id,code,name,category,career_outlook,overview,difficulty,suitable_for,xuefeng_comment,status'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    majors = json.loads(response.read().decode('utf-8'))

print(f"已获取 {len(majors)} 个专业的信息\n")

# 定义检查标准
REQUIRED_FIELDS = ['code', 'name', 'category']
CONTENT_FIELDS = ['career_outlook', 'overview', 'difficulty', 'suitable_for', 'xuefeng_comment']

# 检查结果分类
issues = {
    'missing_required': [],      # 缺少必填字段
    'missing_content': [],       # 缺少内容字段
    'empty_content': [],         # 内容字段为空
    'short_content': [],         # 内容过短（可能质量低）
    'long_content': [],          # 内容过长
}

# 详细检查每个专业
print("=" * 80)
print("开始全面检查专业信息质量")
print("=" * 80)

for major in majors:
    code = major.get('code', '')
    name = major.get('name', '')
    category = major.get('category', '')
    
    # 1. 检查必填字段
    for field in REQUIRED_FIELDS:
        if not major.get(field):
            issues['missing_required'].append({
                'code': code,
                'name': name,
                'field': field,
                'value': major.get(field)
            })
    
    # 2. 检查内容完整性
    missing_fields = []
    empty_fields = []
    short_fields = []
    long_fields = []
    
    for field in CONTENT_FIELDS:
        content = major.get(field, '')
        if content is None or content == '':
            empty_fields.append(field)
        elif len(str(content)) < 10:
            short_fields.append(f"{field}({len(str(content))}字)")
        elif len(str(content)) > 500:
            long_fields.append(f"{field}({len(str(content))}字)")
    
    if missing_fields:
        issues['missing_content'].append({
            'code': code,
            'name': name,
            'missing': missing_fields
        })
    if empty_fields:
        issues['empty_content'].append({
            'code': code,
            'name': name,
            'empty': empty_fields
        })
    if short_fields:
        issues['short_content'].append({
            'code': code,
            'name': name,
            'short': short_fields
        })
    if long_fields:
        issues['long_content'].append({
            'code': code,
            'name': name,
            'long': long_fields
        })

# 输出检查结果
print("\n" + "=" * 80)
print("检查结果统计")
print("=" * 80)

print(f"\n1. 缺少必填字段: {len(issues['missing_required'])} 个")
if issues['missing_required']:
    for item in issues['missing_required'][:10]:
        print(f"   - {item['code']} {item['name']}: 缺少 {item['field']}")

print(f"\n2. 缺少内容字段: {len(issues['missing_content'])} 个")
if issues['missing_content']:
    for item in issues['missing_content'][:10]:
        print(f"   - {item['code']} {item['name']}: 缺少 {', '.join(item['missing'])}")

print(f"\n3. 内容字段为空: {len(issues['empty_content'])} 个")
if issues['empty_content']:
    print("   示例（前20个）：")
    for item in issues['empty_content'][:20]:
        print(f"   - {item['code']} {item['name']}: {', '.join(item['empty'])}")

print(f"\n4. 内容过短(可能质量低): {len(issues['short_content'])} 个")
if issues['short_content']:
    print("   示例（前20个）：")
    for item in issues['short_content'][:20]:
        print(f"   - {item['code']} {item['name']}: {', '.join(item['short'])}")

print(f"\n5. 内容过长: {len(issues['long_content'])} 个")
if issues['long_content']:
    print("   示例（前10个）：")
    for item in issues['long_content'][:10]:
        print(f"   - {item['code']} {item['name']}: {', '.join(item['long'])}")

# 统计总体质量
total_issues = (
    len(issues['missing_required']) +
    len(issues['missing_content']) +
    len(issues['empty_content']) +
    len(issues['short_content']) +
    len(issues['long_content'])
)

print("\n" + "=" * 80)
print("总体质量评估")
print("=" * 80)

perfect_count = len(majors) - len(set(
    [item['code'] for item in issues['empty_content']] + 
    [item['code'] for item in issues['short_content']]
))

print(f"\n总专业数: {len(majors)}")
print(f"信息完整(无空内容): {len(majors) - len(issues['empty_content'])} ({len(majors) - len(issues['empty_content'])/len(majors)*100:.1f}%)")
print(f"内容充实(无过短): {len(majors) - len(issues['short_content'])} ({len(majors) - len(issues['short_content'])/len(majors)*100:.1f}%)")
print(f"内容合理(无过长): {len(majors) - len(issues['long_content'])} ({len(majors) - len(issues['long_content'])/len(majors)*100:.1f}%)")

print(f"\n总问题数: {total_issues}")
