import urllib.request
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
        return False, e.code if e.code != 409 else 409

language_majors = [
    {
        "code": "050207",
        "name": "日语",
        "category": "05 文学",
        "category_icon": "🇯🇵",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "日语专业培养掌握日语语言文学基础知识和专业技能的复合型人才。",
        "what_you_learn": "日语精读、日语听力、日语口语、日语写作、日本文学、日本文化、翻译理论与实践",
        "suitable_for": "对日本文化和语言感兴趣的学生。",
        "career_outlook": "中日经贸文化交流频繁，日语人才需求稳定。就业在日企、外贸、翻译、教育等领域。",
        "xuefeng_comment": "日语是比较热门的小语种专业。日企在中国很多，日语人才需求比较稳定。就业方向包括日企、外贸公司、翻译机构、日语教育等。但要注意，纯日语专业的就业竞争力可能不如复合型人才，建议辅修其他专业或技能。这个专业女生报考较多，工作环境相对较好。如果能去日本留学，会更有竞争力。",
        "yearly_courses": {"大一": ["日语精读、日语听力", "日语入门", "日本概况"], "大二": ["日语口语、日语写作", "日本文化", "日本历史"], "大三": ["日本文学、高级日语", "翻译理论与实践", "商务日语"], "大四": ["日语专业实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "复旦大学", "广东外语外贸大学"], "international": ["University of Tokyo", "Waseda", "Osaka University"]}
    },
    {
        "code": "050209",
        "name": "朝鲜语",
        "category": "05 文学",
        "category_icon": "🇰🇷",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "朝鲜语专业培养掌握韩国语（朝鲜语）语言文化知识的专业人才。",
        "what_you_learn": "朝鲜语精读、朝鲜语听力、朝鲜语口语、朝鲜语写作、韩国文学、韩国文化、翻译",
        "suitable_for": "对韩国文化和语言感兴趣的学生。",
        "career_outlook": "中韩经贸文化交流频繁，韩国企业在中国有大量投资，朝鲜语人才需求稳定。",
        "xuefeng_comment": "朝鲜语专业，也就是韩语专业。韩流文化和韩国企业在中国影响力不小，韩语人才有一定需求。就业方向包括韩企、外贸、翻译、韩语教育等。和日语类似，纯语言专业建议辅修其他技能。女生报考较多。韩国留学也比较方便，对语言提升有帮助。但要注意，韩半岛的政治局势可能有影响。",
        "yearly_courses": {"大一": ["朝鲜语精读、听力", "韩语入门", "韩国概况"], "大二": ["韩语口语、写作", "韩国文化", "韩国历史"], "大三": ["韩国文学、高级韩语", "翻译理论与实践", "商务韩语"], "大四": ["朝鲜语专业实习"]},
        "top_universities": {"domestic": ["延边大学", "北京外国语大学", "上海外国语大学", "复旦大学", "广东外语外贸大学"], "international": ["Seoul National University", "Yonsei University", "Korea University"]}
    },
    {
        "code": "050205",
        "name": "西班牙语",
        "category": "05 文学",
        "category_icon": "🇪🇸",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "西班牙语专业培养掌握西语语言文化，能从事翻译、外贸、教育等工作的人才。",
        "what_you_learn": "西语精读、西语听力、西语口语、西语写作、西语文学、西语国家概况、翻译",
        "suitable_for": "对西班牙语和拉丁美洲文化感兴趣的学生。",
        "career_outlook": "西语是联合国官方语言，20多个国家使用，中国与拉美经贸合作加强，需求持续增长。",
        "xuefeng_comment": "西班牙语是很有前景的小语种专业。西班牙语是世界第二大语言，使用人口众多。中国与拉丁美洲的经贸合作越来越多，西语人才缺口较大。就业方向包括外贸、外交、翻译、教育、媒体等。但小语种专业都面临一个问题，就是就业面相对较窄，建议辅修其他专业。这个专业女生也比较多，建议有兴趣的学生报考。",
        "yearly_courses": {"大一": ["西班牙语精读、听力", "西语入门", "西语国家概况"], "大二": ["西语口语、写作", "西班牙文化", "拉美文化"], "大三": ["西语文学、高级西语", "翻译理论与实践", "商务西语"], "大四": ["西班牙语专业实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "南京大学", "广东外语外贸大学"], "international": ["Complutense University of Madrid", "University of Barcelona", "Sorbonne"]}
    },
    {
        "code": "050204",
        "name": "法语",
        "category": "05 文学",
        "category_icon": "🇫🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-25k",
        "overview": "法语专业培养掌握法语语言文化，能从事翻译、外交、教育等工作的专业人才。",
        "what_you_learn": "法语精读、法语听力、法语口语、法语写作、法国文学、法国文化、翻译理论与实践",
        "suitable_for": "对法国文化和法语感兴趣的学生。",
        "career_outlook": "法语是联合国官方语言，中国与法语国家交流合作广泛，法语人才需求稳定。",
        "xuefeng_comment": "法语是比较经典的小语种专业，被誉为世界上最优美的语言。法语是联合国、欧盟等组织的官方语言。就业方向包括外交、外贸、翻译、教育、媒体、旅游等。法语学习有一定难度，但就业质量不错。建议辅修国际关系、经济等专业，提升竞争力。法国留学也是一个很好的选择。女生报考较多。",
        "yearly_courses": {"大一": ["法语精读、听力", "法语入门", "法国概况"], "大二": ["法语口语、写作", "法国文化", "法国历史"], "大三": ["法国文学、高级法语", "翻译理论与实践", "商务法语"], "大四": ["法语专业实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "南京大学", "武汉大学"], "international": ["Sorbonne", "Sciences Po", "LSE", "University of Geneva"]}
    },
    {
        "code": "050203",
        "name": "德语",
        "category": "05 文学",
        "category_icon": "🇩🇪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-24k",
        "overview": "德语专业培养掌握德语语言文化，能从事翻译、外贸、教育等工作的人才。",
        "what_you_learn": "德语精读、德语听力、德语口语、德语写作、德国文学、德国文化、翻译理论",
        "suitable_for": "对德国文化和德语感兴趣的学生。",
        "career_outlook": "德国是制造业强国，中德经贸合作密切，德语人才在机械、汽车等行业有稳定需求。",
        "xuefeng_comment": "德语专业比较扎实。德国是制造业强国，中德经贸合作密切，德语人才在机械、汽车等行业很受欢迎。就业方向包括外贸、德企、翻译、教育等。但德语学习难度比较大，语法复杂。建议辅修机械、汽车、经济等专业，提升就业竞争力。德国留学费用低、教育质量高，是个不错的选择。",
        "yearly_courses": {"大一": ["德语精读、听力", "德语入门", "德国概况"], "大二": ["德语口语、写作", "德国文化", "德国历史"], "大三": ["德国文学、高级德语", "翻译理论与实践", "商务德语"], "大四": ["德语专业实习"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "南京大学", "同济大学"], "international": ["LMU Munich", "Heidelberg", "Berlin", "TU Munich"]}
    }
]

def main():
    print("=" * 70)
    print("🌍 开始导入外语类专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in language_majors:
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
