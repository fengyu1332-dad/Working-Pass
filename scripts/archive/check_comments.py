"""
检查点评内容的理性客观性
"""
import urllib.request
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 获取有点评的专业
url = f'{SUPABASE_URL}/rest/v1/majors?select=code,name,category,xuefeng_comment&xuefeng_comment=not.is.null'
req = urllib.request.Request(url)
req.add_header('apikey', SUPABASE_KEY)
req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')

with urllib.request.urlopen(req, context=ctx) as response:
    majors = json.loads(response.read().decode('utf-8'))

print(f"有点评内容的专业: {len(majors)} 个\n")

# 定义可能不当的词汇
bad_words = [
    # 绝对化表述
    ['最好', '最差', '最烂', '最坑', '最赚钱', '最容易', '最难', '最简单的', '最难的'],
    # 极端贬低
    ['天坑', '坑爹', '垃圾专业', '别学', '后悔', '劝退', '千万别', '千万不要'],
    # 夸大其词
    ['年薪百万', '一夜暴富', '毕业就有工作', '保证就业'],
    # 不当比喻
    ['搬砖', '码农', '程序猿'],
    # 其他不当表述
    ['有关系', '靠背景', '潜规则', '走后门']
]

# 检查结果
problematic = []

for major in majors:
    comment = major.get('xuefeng_comment', '')
    if not comment:
        continue
    
    # 检查是否包含不当词汇
    for words in bad_words:
        for word in words:
            if word in comment:
                problematic.append({
                    'code': major['code'],
                    'name': major['name'],
                    'word': word,
                    'comment': comment[:100]  # 只显示前100字
                })
                break

print("=" * 80)
print("检查点评内容的理性客观性")
print("=" * 80)

if problematic:
    print(f"\n发现 {len(problematic)} 处可能不当的表述：\n")
    
    # 按词汇分类
    by_word = {}
    for item in problematic:
        word = item['word']
        if word not in by_word:
            by_word[word] = []
        by_word[word].append(item)
    
    for word, items in sorted(by_word.items(), key=lambda x: -len(x[1])):
        print(f"\n【{word}】出现 {len(items)} 次：")
        for item in items[:3]:  # 每个显示3个示例
            print(f"  - {item['code']} {item['name']}")
            print(f"    点评: {item['comment']}...")
else:
    print("\n✅ 未发现明显不当的表述！")

# 显示一些典型的理性客观点评示例
print("\n" + "=" * 80)
print("理性客观的点评示例")
print("=" * 80)

good_examples = [m for m in majors if m.get('xuefeng_comment') and len(m['xuefeng_comment']) > 50]
if good_examples:
    for major in good_examples[:10]:
        print(f"\n{major['code']} {major['name']}:")
        print(f"  {major['xuefeng_comment'][:150]}...")
