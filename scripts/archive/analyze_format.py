"""
详细分析：代码格式不统一问题
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

# 解析清单中的代码（包含K、T、TK后缀）
ministry_codes = set()
for match in re.finditer(r'"(\d{6}[A-Z]{0,2})":', ministry_text):
    ministry_codes.add(match.group(1))

print("=" * 80)
print("发现核心问题：专业代码格式不统一！")
print("=" * 80)

# 获取数据库中的专业
SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(f'{SUPABASE_URL}/rest/v1/majors?select=code,name')
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    majors = json.loads(response.read().decode('utf-8'))

# 分析格式差异
format_issues = []
for m in majors:
    code = m['code']
    
    # 提取基本代码（前6位）和后缀
    if len(code) >= 6:
        base_code = code[:6]
        suffix = code[6:] if len(code) > 6 else ''
        
        # 检查是否格式不一致
        # 情况1：数据库有TK，但清单只有K
        # 情况2：数据库没有后缀，但清单有K/T
        # 情况3：数据库有后缀，但清单没有
        
        if base_code in ['020201', '030101', '040201', '100101', '100201', '100301', '100401', '100501', '100601', '100701', '100801', '120201', '120901']:
            # 这些在清单中是K或TK结尾
            if suffix not in ['K', 'TK', 'T'] and f"{base_code}K" in ministry_codes:
                format_issues.append((code, m['name'], f"{base_code}K"))
            elif suffix in ['K', 'T'] and f"{base_code}TK" in ministry_codes:
                format_issues.append((code, m['name'], f"{base_code}TK"))
            elif suffix == '' and f"{base_code}K" in ministry_codes:
                format_issues.append((code, m['name'], f"{base_code}K"))

print(f"\n发现格式不一致的专业：{len(format_issues)}个\n")

if format_issues:
    print("示例（前20个）：")
    for db_code, name, expected_code in format_issues[:20]:
        print(f"  {db_code:15s} {name:20s} → 应为 {expected_code}")

print("\n" + "=" * 80)
print("问题根源分析")
print("=" * 80)
print("""
核心问题：数据库中的专业代码格式与教育部清单不一致！

教育部专业代码体系：
- 基本代码：6位数字（如 030101）
- 后缀含义：
  - K：国家控制布点专业
  - T：特设专业
  - TK：国家控制布点的特设专业

实际情况：
- 数据库有些专业没有后缀（如 030101 法学）
- 教育部清单中是 030101K 法学（带K）
- 缺少K/T/TK后缀导致系统认为是不同专业

这就解释了为什么：
✅ 数据库有869个专业
❌ 但还有大量"缺失"的专业
原因：代码格式不一致，同一个专业被重复添加或无法匹配！
""")

print("\n" + "=" * 80)
print("解决方案")
print("=" * 80)
print("""
方案：统一代码格式

步骤：
1. 更新数据库中所有专业的代码，补上缺失的后缀
2. 例如：
   - 030101 法学 → 030101K 法学
   - 100101 临床医学 → 100101K 临床医学
   - 020101 经济学 → 020101K 财政学 (注意：020101是经济学，020201才是财政学)

3. 对于无法确定后缀的，保留现状或根据专业性质添加

这样就可以：
✅ 消除"重复"的专业
✅ 正确匹配教育部清单
✅ 准确统计覆盖率
""")
