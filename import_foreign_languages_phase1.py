import urllib.request
import urllib.error
import json
import ssl
import time

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def import_major(major):
    url = f"{SUPABASE_URL}/rest/v1/majors"
    data = json.dumps(major).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Prefer', 'return=minimal')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return True, response.status
    except urllib.error.HTTPError as e:
        return False, e.code

foreign_languages_majors = [
    {
        "code": "050202",
        "name": "俄语",
        "category": "05 文学",
        "category_icon": "🇷🇺",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "俄语专业是培养俄语人才的学科，培养从事俄语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础俄语、高级俄语、俄语语法、俄语阅读、俄语写作、俄语口语、俄罗斯文学史、俄罗斯文化",
        "suitable_for": "对俄语和俄罗斯文化感兴趣的学生。",
        "career_outlook": "中俄交流发展，就业在俄资企业、外贸公司、翻译公司、学校等。",
        "xuefeng_comment": "俄语是外国语言文学类的专业，培养俄语人才。就业在俄资企业、外贸公司、翻译公司、学校。这个专业需要对俄语和俄罗斯文化有兴趣。适合有语言天赋的学生。就业稳定，薪资中等。中俄关系好的时候就业机会多。",
        "yearly_courses": {"大一": ["基础俄语", "俄语语法", "俄语阅读", "俄罗斯概况"], "大二": ["高级俄语", "俄语写作", "俄语口语", "俄罗斯文学史"], "大三": ["俄语翻译理论与实践", "俄罗斯文化", "俄语视听说", "俄语报刊选读"], "大四": ["俄资企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "黑龙江大学", "北京大学", "北京师范大学"], "international": ["Moscow State University", "Saint Petersburg State University"]}
    },
    {
        "code": "050203",
        "name": "德语",
        "category": "05 文学",
        "category_icon": "🇩🇪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "德语专业是培养德语人才的学科，培养从事德语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础德语、高级德语、德语语法、德语阅读、德语写作、德语口语、德国文学史、德国文化",
        "suitable_for": "对德语和德国文化感兴趣的学生。",
        "career_outlook": "中德交流发展，就业在德资企业、外贸公司、翻译公司、学校等。",
        "xuefeng_comment": "德语是外国语言文学类的专业，培养德语人才。就业在德资企业、外贸公司、翻译公司、学校。这个专业需要对德语和德国文化有兴趣。适合有语言天赋的学生。就业稳定，薪资中等。德国企业在中国多，就业机会不错。",
        "yearly_courses": {"大一": ["基础德语", "德语语法", "德语阅读", "德国概况"], "大二": ["高级德语", "德语写作", "德语口语", "德国文学史"], "大三": ["德语翻译理论与实践", "德国文化", "德语视听说", "德语报刊选读"], "大四": ["德资企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "同济大学", "北京大学", "南京大学"], "international": ["Ludwig Maximilian University", "Technical University Munich"]}
    },
    {
        "code": "050204",
        "name": "法语",
        "category": "05 文学",
        "category_icon": "🇫🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-26k",
        "overview": "法语专业是培养法语人才的学科，培养从事法语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础法语、高级法语、法语语法、法语阅读、法语写作、法语口语、法国文学史、法国文化",
        "suitable_for": "对法语和法国文化感兴趣的学生。",
        "career_outlook": "中法交流发展，就业在法资企业、外贸公司、翻译公司、学校等。",
        "xuefeng_comment": "法语是外国语言文学类的专业，培养法语人才。就业在法资企业、外贸公司、翻译公司、学校。这个专业需要对法语和法国文化有兴趣。适合有语言天赋的学生。就业稳定，薪资中等。法语是国际语言，就业面广。",
        "yearly_courses": {"大一": ["基础法语", "法语语法", "法语阅读", "法国概况"], "大二": ["高级法语", "法语写作", "法语口语", "法国文学史"], "大三": ["法语翻译理论与实践", "法国文化", "法语视听说", "法语报刊选读"], "大四": ["法资企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "南京大学", "北京大学", "武汉大学"], "international": ["Sorbonne", "Sciences Po", "Paris Dauphine"]}
    },
    {
        "code": "050205",
        "name": "西班牙语",
        "category": "05 文学",
        "category_icon": "🇪🇸",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "西班牙语专业是培养西班牙语人才的学科，培养从事西班牙语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础西班牙语、高级西班牙语、西班牙语语法、西班牙语阅读、西班牙语写作、西班牙语口语、西班牙文学史、西班牙文化",
        "suitable_for": "对西班牙语和西班牙文化感兴趣的学生。",
        "career_outlook": "中拉交流发展，就业在西资企业、外贸公司、翻译公司、学校等。",
        "xuefeng_comment": "西班牙语是外国语言文学类的专业，培养西班牙语人才。就业在西资企业、外贸公司、翻译公司、学校。这个专业需要对西班牙语和西班牙文化有兴趣。适合有语言天赋的学生。就业前景好，西班牙语使用国家多，就业面广。",
        "yearly_courses": {"大一": ["基础西班牙语", "西班牙语语法", "西班牙语阅读", "西班牙概况"], "大二": ["高级西班牙语", "西班牙语写作", "西班牙语口语", "西班牙文学史"], "大三": ["西班牙语翻译理论与实践", "西班牙文化", "西班牙语视听说", "西班牙语报刊选读"], "大四": ["西资企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "南京大学", "对外经济贸易大学"], "international": ["Complutense University", "University of Barcelona"]}
    },
    {
        "code": "050206",
        "name": "阿拉伯语",
        "category": "05 文学",
        "category_icon": "🇸🇦",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥12k-30k",
        "overview": "阿拉伯语专业是培养阿拉伯语人才的学科，培养从事阿拉伯语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础阿拉伯语、高级阿拉伯语、阿拉伯语语法、阿拉伯语阅读、阿拉伯语写作、阿拉伯语口语、阿拉伯文学史、阿拉伯文化",
        "suitable_for": "对阿拉伯语和阿拉伯文化感兴趣的学生。",
        "career_outlook": "中阿交流发展，就业在阿拉伯企业、外贸公司、翻译公司、政府部门等。",
        "xuefeng_comment": "阿拉伯语是外国语言文学类的专业，培养阿拉伯语人才。就业在阿拉伯企业、外贸公司、翻译公司、政府部门。这个专业需要对阿拉伯语和阿拉伯文化有兴趣，学习难度较大。适合有语言天赋、能吃苦的学生。就业前景好，阿拉伯语人才稀缺。",
        "yearly_courses": {"大一": ["基础阿拉伯语", "阿拉伯语语法", "阿拉伯语阅读", "阿拉伯概况"], "大二": ["高级阿拉伯语", "阿拉伯语写作", "阿拉伯语口语", "阿拉伯文学史"], "大三": ["阿拉伯语翻译理论与实践", "阿拉伯文化", "阿拉伯语视听说", "阿拉伯语报刊选读"], "大四": ["阿拉伯企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "北京语言大学", "对外经济贸易大学"], "international": ["American University in Cairo", "Cairo University"]}
    },
    {
        "code": "050207",
        "name": "日语",
        "category": "05 文学",
        "category_icon": "🇯🇵",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "日语专业是培养日语人才的学科，培养从事日语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础日语、高级日语、日语语法、日语阅读、日语写作、日语口语、日本文学史、日本文化",
        "suitable_for": "对日语和日本文化感兴趣的学生。",
        "career_outlook": "中日交流发展，就业在日资企业、外贸公司、翻译公司、学校等。",
        "xuefeng_comment": "日语是外国语言文学类的专业，培养日语人才。就业在日资企业、外贸公司、翻译公司、学校。这个专业需要对日语和日本文化有兴趣。适合有语言天赋的学生。就业稳定，薪资中等。日资企业在中国很多，就业机会多。",
        "yearly_courses": {"大一": ["基础日语", "日语语法", "日语阅读", "日本概况"], "大二": ["高级日语", "日语写作", "日语口语", "日本文学史"], "大三": ["日语翻译理论与实践", "日本文化", "日语视听说", "日语报刊选读"], "大四": ["日资企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "吉林大学", "东北师范大学"], "international": ["University of Tokyo", "Waseda University"]}
    },
    {
        "code": "050208",
        "name": "波斯语",
        "category": "05 文学",
        "category_icon": "🇮🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-26k",
        "overview": "波斯语专业是培养波斯语人才的学科，培养从事波斯语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础波斯语、高级波斯语、波斯语语法、波斯语阅读、波斯语写作、波斯语口语、波斯文学史、波斯文化",
        "suitable_for": "对波斯语和波斯文化感兴趣的学生。",
        "career_outlook": "中伊交流发展，就业在伊朗企业、外贸公司、翻译公司、政府部门等。",
        "xuefeng_comment": "波斯语是外国语言文学类的专业，培养波斯语人才。就业在伊朗企业、外贸公司、翻译公司、政府部门。这个专业需要对波斯语和波斯文化有兴趣。波斯语人才比较稀缺，就业前景好。适合有语言天赋的学生。",
        "yearly_courses": {"大一": ["基础波斯语", "波斯语语法", "波斯语阅读", "波斯概况"], "大二": ["高级波斯语", "波斯语写作", "波斯语口语", "波斯文学史"], "大三": ["波斯语翻译理论与实践", "波斯文化", "波斯语视听说", "波斯语报刊选读"], "大四": ["伊朗企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "北京语言大学"], "international": ["University of Tehran", "Sharif University"]}
    },
    {
        "code": "050209",
        "name": "朝鲜语",
        "category": "05 文学",
        "category_icon": "🇰🇷",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "朝鲜语专业是培养朝鲜语人才的学科，培养从事朝鲜语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础朝鲜语、高级朝鲜语、朝鲜语语法、朝鲜语阅读、朝鲜语写作、朝鲜语口语、朝鲜文学史、朝鲜文化",
        "suitable_for": "对朝鲜语和韩国文化感兴趣的学生。",
        "career_outlook": "中韩交流发展，就业在韩资企业、外贸公司、翻译公司、学校等。",
        "xuefeng_comment": "朝鲜语是外国语言文学类的专业，培养朝鲜语人才。就业在韩资企业、外贸公司、翻译公司、学校。这个专业需要对朝鲜语和韩国文化有兴趣。适合有语言天赋的学生。就业稳定，薪资中等。韩资企业在中国很多，就业机会多。",
        "yearly_courses": {"大一": ["基础朝鲜语", "朝鲜语语法", "朝鲜语阅读", "韩国概况"], "大二": ["高级朝鲜语", "朝鲜语写作", "朝鲜语口语", "朝鲜文学史"], "大三": ["朝鲜语翻译理论与实践", "韩国文化", "朝鲜语视听说", "朝鲜语报刊选读"], "大四": ["韩资企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "延边大学", "北京大学", "复旦大学"], "international": ["Seoul National University", "Korea University"]}
    },
    {
        "code": "050210",
        "name": "菲律宾语",
        "category": "05 文学",
        "category_icon": "🇵🇭",
        "difficulty": "⭐⭐",
        "salary_range": "¥9k-22k",
        "overview": "菲律宾语专业是培养菲律宾语人才的学科，培养从事菲律宾语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础菲律宾语、高级菲律宾语、菲律宾语语法、菲律宾语阅读、菲律宾语写作、菲律宾语口语、菲律宾文学史、菲律宾文化",
        "suitable_for": "对菲律宾语和菲律宾文化感兴趣的学生。",
        "career_outlook": "中菲交流发展，就业在菲律宾企业、外贸公司、翻译公司等。",
        "xuefeng_comment": "菲律宾语是外国语言文学类的专业，培养菲律宾语人才。就业在菲律宾企业、外贸公司、翻译公司。这个专业需要对菲律宾语和菲律宾文化有兴趣。菲律宾语人才比较稀缺，就业稳定。适合有语言天赋的学生。",
        "yearly_courses": {"大一": ["基础菲律宾语", "菲律宾语语法", "菲律宾语阅读", "菲律宾概况"], "大二": ["高级菲律宾语", "菲律宾语写作", "菲律宾语口语", "菲律宾文学史"], "大三": ["菲律宾语翻译理论与实践", "菲律宾文化", "菲律宾语视听说", "菲律宾语报刊选读"], "大四": ["菲律宾企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学"], "international": ["University of the Philippines", "Ateneo de Manila"]}
    },
    {
        "code": "050211",
        "name": "梵语巴利语",
        "category": "05 文学",
        "category_icon": "🕉️",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥10k-24k",
        "overview": "梵语巴利语专业是研究梵语巴利语的学科，培养从事宗教研究、文化研究、翻译等工作的专门人才。",
        "what_you_learn": "梵语、巴利语、印度文化、佛教史、印度哲学史、语言学、校勘学",
        "suitable_for": "对梵语巴利语和印度文化感兴趣的学生。",
        "career_outlook": "文化研究领域，就业在高校、研究机构、宗教机构、出版社等。",
        "xuefeng_comment": "梵语巴利语是外国语言文学类的专业，研究梵语巴利语。就业在高校、研究机构、宗教机构、出版社。这个专业需要对梵语巴利语和印度文化有兴趣，学习难度较大。适合有语言天赋、对文化研究感兴趣的学生。就业面相对窄但很稳定。读研比例很高。",
        "yearly_courses": {"大一": ["梵语入门", "巴利语入门", "印度概况", "语言学概论"], "大二": ["梵语中级", "巴利语中级", "印度文化", "佛教史"], "大三": ["梵语高级", "巴利语高级", "印度哲学史", "校勘学"], "大四": ["研究机构或高校实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "四川大学"], "international": ["Harvard", "Oxford", "Cambridge", "Sorbonne"]}
    },
    {
        "code": "050212",
        "name": "印地语",
        "category": "05 文学",
        "category_icon": "🇮🇳",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-24k",
        "overview": "印地语专业是培养印地语人才的学科，培养从事印地语翻译、教学、国际贸易等工作的专业人才。",
        "what_you_learn": "基础印地语、高级印地语、印地语语法、印地语阅读、印地语写作、印地语口语、印度文学史、印度文化",
        "suitable_for": "对印地语和印度文化感兴趣的学生。",
        "career_outlook": "中印交流发展，就业在印度企业、外贸公司、翻译公司、政府部门等。",
        "xuefeng_comment": "印地语是外国语言文学类的专业，培养印地语人才。就业在印度企业、外贸公司、翻译公司、政府部门。这个专业需要对印地语和印度文化有兴趣。印度发展快，中印交流多，就业前景好。适合有语言天赋的学生。",
        "yearly_courses": {"大一": ["基础印地语", "印地语语法", "印地语阅读", "印度概况"], "大二": ["高级印地语", "印地语写作", "印地语口语", "印度文学史"], "大三": ["印地语翻译理论与实践", "印度文化", "印地语视听说", "印地语报刊选读"], "大四": ["印度企业或翻译公司实习"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "上海外国语大学", "北京语言大学"], "international": ["University of Delhi", "JNU"]}
    }
]

def main():
    print("=" * 70)
    print("🌍 开始导入外国语言文学类专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in foreign_languages_majors:
        print(f"\n正在导入: {major['code']} - {major['name']}")
        ok, code = import_major(major)
        if ok or code in [200, 201]:
            success += 1
            print(f"✅ 成功")
        elif code == 409:
            skipped += 1
            print(f"⏭️ 已存在")
        else:
            failed += 1
            print(f"❌ 失败 (HTTP {code})")
        time.sleep(0.2)
    
    print(f"\n导入完成！成功: {success}, 跳过: {skipped}, 失败: {failed}")

if __name__ == "__main__":
    main()
