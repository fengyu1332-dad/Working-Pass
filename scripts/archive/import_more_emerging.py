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

more_emerging_majors = [
    {
        "code": "082502T",
        "name": "环境工程",
        "category": "08 工学",
        "category_icon": "🌿",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥11k-25k",
        "overview": "环境工程是研究环境污染防治和环境质量改善的工程学科，包括水处理、大气污染控制等。",
        "what_you_learn": "环境工程原理、水处理工程、大气污染控制工程、固体废弃物处理、环境监测、环境影响评价",
        "suitable_for": "对环境保护和工程技术感兴趣的学生。",
        "career_outlook": "环保产业快速发展，环境工程人才需求持续增长。就业在环保公司、市政设计院、环境监测站等。",
        "xuefeng_comment": "环境工程是比较有前景的工科专业，随着环保意识提高和双碳战略，这个专业的重要性越来越突出。就业包括环保公司、市政设计院、环境监测站、污水处理厂等。工作相对稳定，但薪资水平中等。这个专业需要化学、生物等知识，比较适合女生报考。建议读研读博，能有更好的发展空间。考公务员也是一个不错的选择。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "普通化学", "分析化学"], "大二": ["有机化学", "物理化学", "环境科学概论", "流体力学"], "大三": ["环境工程原理", "水处理工程", "大气污染控制工程"], "大四": ["环保企业实习"]},
        "top_universities": {"domestic": ["清华大学", "同济大学", "哈尔滨工业大学", "浙江大学", "北京大学"], "international": ["MIT", "Stanford", "ETH Zurich", "University of California Berkeley"]}
    },
    {
        "code": "080911T",
        "name": "网络空间安全",
        "category": "08 工学",
        "category_icon": "🔐",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥18k-42k",
        "overview": "网络空间安全是研究网络安全、密码学、信息安全的新兴学科，保障网络空间安全。",
        "what_you_learn": "密码学、网络安全、信息安全、计算机病毒防治、网络攻防、数字取证、云安全",
        "suitable_for": "对网络安全和密码学感兴趣、计算机基础扎实的学生。",
        "career_outlook": "网络安全需求爆发增长，人才缺口巨大。就业在互联网公司、金融机构、政府部门等。",
        "xuefeng_comment": "网络空间安全是当下最热门的专业之一，网络安全人才缺口很大，就业非常好。但这个专业学习难度比较大，需要有比较好的数学和计算机基础。建议对安全技术真正感兴趣的学生报考，不要只看热门。就业方向包括安全厂商、互联网公司安全部门、金融机构、政府部门等。薪资待遇很好，但工作压力也比较大。读研读博能有更高的起点。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "计算机基础", "程序设计"], "大二": ["数据结构", "操作系统", "计算机网络", "密码学基础"], "大三": ["网络安全", "信息安全", "网络攻防", "数字取证"], "大四": ["网络安全企业实习"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "上海交通大学", "浙江大学", "西安电子科技大学"], "international": ["MIT", "Stanford", "Carnegie Mellon", "UC Berkeley"]}
    },
    {
        "code": "081204T",
        "name": "测绘工程",
        "category": "08 工学",
        "category_icon": "📐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-26k",
        "overview": "测绘工程是研究测量和绘制地球表面信息的学科，包括工程测量、遥感、地理信息系统等。",
        "what_you_learn": "测量学、工程测量、遥感概论、地理信息系统、GPS原理与应用、地籍测量",
        "suitable_for": "对测绘、地理信息感兴趣、动手能力强的学生。",
        "career_outlook": "测绘在基础设施建设、城市规划、国土资源管理中发挥重要作用，需求稳定。",
        "xuefeng_comment": "测绘工程是比较传统的工科专业，就业面比较广，包括测绘院、工程局、国土资源部门、导航与地图公司等。工作相对稳定，但可能需要外出作业，工作环境相对艰苦，女生要慎重考虑。薪资水平中等。这个专业学的内容比较实用，也容易转行到GIS或IT行业。建议读研读博，能有更好的发展。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "大学物理", "计算机基础", "测绘学概论"], "大二": ["测量学", "地图学", "地理信息系统原理", "遥感概论"], "大三": ["工程测量", "GPS原理与应用", "地籍测量", "摄影测量"], "大四": ["测绘单位实习"]},
        "top_universities": {"domestic": ["武汉大学", "中国矿业大学", "同济大学", "中南大学", "西南交通大学"], "international": ["ETH Zurich", "University of Cambridge", "MIT", "TU Delft"]}
    },
    {
        "code": "081403T",
        "name": "地质工程",
        "category": "08 工学",
        "category_icon": "⛰️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-24k",
        "overview": "地质工程是研究地质勘查、地质灾害防治、岩土工程的工程学科，应用于工程建设、资源勘查等。",
        "what_you_learn": "普通地质学、岩石学、构造地质学、工程地质学、岩土力学、地质灾害防治",
        "suitable_for": "对地质学和工程感兴趣的学生。",
        "career_outlook": "基础设施建设和矿产资源开发，地质工程人才需求稳定。就业在地质队、工程局、矿业公司等。",
        "xuefeng_comment": "地质工程是比较传统的工科专业，就业主要在地质队、工程局、矿业公司等。这个专业需要经常出野外，工作环境比较艰苦，女生要慎重考虑。薪资水平中等，但工作可能不太稳定。如果对地质真的感兴趣，建议读研读博，以后去研究所或高校。报考时要了解清楚未来的工作状态，不要盲目选择。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "普通化学", "普通地质学"], "大二": ["岩石学", "构造地质学", "矿物学", "工程力学"], "大三": ["工程地质学", "岩土力学", "地质灾害防治", "勘查技术"], "大四": ["地质单位实习"]},
        "top_universities": {"domestic": ["中国地质大学", "中国矿业大学", "吉林大学", "成都理工大学", "长安大学"], "international": ["Stanford", "ETH Zurich", "University of Cambridge", "Colorado School of Mines"]}
    },
    {
        "code": "120503T",
        "name": "图书馆学",
        "category": "12 管理学",
        "category_icon": "📚",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "图书馆学是研究文献信息资源管理、图书馆管理的学科，包括信息组织、信息检索、数字图书馆等。",
        "what_you_learn": "图书馆学概论、信息组织、信息检索、目录学、图书馆管理、数字图书馆",
        "suitable_for": "对图书资料和信息管理感兴趣的学生。",
        "career_outlook": "图书馆、档案馆、出版社、企业信息部门等需要图书情报人才，需求稳定。",
        "xuefeng_comment": "图书馆学是比较传统的管理类专业，就业主要在图书馆、档案馆、出版社、企业信息部门等。工作非常稳定，压力小，工作环境相对较好，但薪资水平不高。适合追求稳定、不太看重高薪的学生，女生比较适合。这个专业在高校扩招后，就业竞争也在加大，建议读研提升竞争力。这个专业比较适合考公务员，如档案局、文化部门等。",
        "yearly_courses": {"大一": ["图书馆学概论", "目录学", "信息资源管理", "计算机基础"], "大二": ["信息组织", "信息检索", "图书馆管理", "文献学"], "大三": ["数字图书馆", "信息分析", "图书馆学前沿", "信息服务"], "大四": ["图书馆实习"]},
        "top_universities": {"domestic": ["武汉大学", "北京大学", "中国人民大学", "南京大学", "南开大学"], "international": ["University of Michigan", "University of Texas at Austin", "LSE", "University of Toronto"]}
    },
    {
        "code": "071202T",
        "name": "应用统计学",
        "category": "07 理学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥14k-32k",
        "overview": "应用统计学是将统计学应用于实际问题的学科，包括数据分析、统计建模、机器学习等。",
        "what_you_learn": "数理统计、回归分析、多元统计分析、时间序列分析、抽样调查、应用统计软件",
        "suitable_for": "数学基础好、对数据分析感兴趣的学生。",
        "career_outlook": "数据科学时代，统计学人才需求爆发增长，就业在金融、互联网、政府部门等。",
        "xuefeng_comment": "应用统计学是当下的黄金专业之一，随着大数据和人工智能发展，统计学人才需求爆发增长。就业方向包括金融机构、互联网公司、政府部门、市场研究机构等。这个专业对数学要求很高，需要真正喜欢数学的学生报考。建议读研读博，最好去国外顶尖学校深造。薪资待遇很好，但学习压力也比较大。是很好的交叉学科基础，可转金融、计算机等方向。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "数学分析", "统计学导论"], "大二": ["数理统计", "回归分析", "多元统计分析", "Python/R编程"], "大三": ["时间序列分析", "抽样调查", "机器学习", "数据挖掘"], "大四": ["统计机构实习"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "中国人民大学", "南开大学"], "international": ["Stanford", "Harvard", "MIT", "University of California Berkeley", "University of Chicago"]}
    }
]

def main():
    print("=" * 70)
    print("🚀 继续导入更多新兴专业...")
    print("=" * 70)
    
    success = failed = skipped = 0
    
    for major in more_emerging_majors:
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
