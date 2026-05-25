import urllib.request
import urllib.error
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 精选专业代码列表
featured_codes = [
    '080901', '080701', '100201',
    '081301', '080601', '050303',
    '081001', '080801', '070101'
]

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

def main():
    majors = fetch_majors()
    if not majors:
        print("未能获取数据")
        return
    
    print("=" * 70)
    print("✅ 数据库专业总数: ", len(majors))
    print("=" * 70)
    
    # 检查精选专业是否都存在
    print("\n📋 精选专业验证:")
    print("=" * 70)
    
    code_to_major = {m['code']: m for m in majors}
    
    found = []
    missing = []
    
    for code in featured_codes:
        if code in code_to_major:
            found.append(code_to_major[code])
            print(f"✅ {code} - {code_to_major[code]['name']}")
        else:
            missing.append(code)
            print(f"❌ {code} - 未找到")
    
    print(f"\n找到: {len(found)}/{len(featured_codes)}")
    if missing:
        print(f"缺失: {missing}")
    
    # 检查雪峰点评长度
    print("\n📊 雪峰点评长度检查 (抽样):")
    print("=" * 70)
    
    for i = 0
    for m in majors[:20]:
        comment = m.get('xuefeng_comment', '')
        if comment = comment or ''
        length = len(comment)
        status = "✅" if length >= 350 else "⚠️"
        print(f"{status} {m['name']: {length}字符")
    
    print("\n📊 雪峰点评长度统计:")
    print("=" * 70)
    
    all_comments = [m.get('xuefeng_comment', '') for m in majors]
    lengths = [len(c) for c in all_comments]
    
    avg_length = sum(lengths) / len(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    count_under = sum(1 for l in lengths if l < 350)
    count_over = sum(1 for l in lengths if l >= 350)
    
    print(f"平均长度: {avg_length:.0f}字符")
    print(f"最短长度: {min_length}字符")
    print(f"最长长度: {max_length}字符")
    print(f"少于350字符: {count_under}个")
    print(f"达到350字符: {count_over}个")
    
    if count_under > 0:
        print(f"\n⚠️ 发现 {count_under}个专业需要扩充")
        print("\n需要扩充的专业:")
        for m in majors:
            comment = m.get('xuefeng_comment', '')
            if len(comment or '') < 350:
                print(f"  {m['code']} - {m['name']}: {len(comment or '')}字符")

if __name__ == "__main__":
    main()

