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

economics_majors = [
    {
        "code": "020303T",
        "name": "信用管理",
        "category": "02 经济学",
        "category_icon": "📋",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-25k",
        "overview": "信用管理是研究信用风险评估、信用产品设计和信用体系建设的经济学科。本专业培养掌握信用分析、风险管理等专业知识的金融人才。",
        "what_you_learn": "信用管理学、征信理论与实务、信用风险计量、信用评级、金融风险管理、信用法律法规、信用数据分析、供应链金融",
        "suitable_for": "对金融信用领域感兴趣、逻辑分析能力强的学生。",
        "career_outlook": "社会信用体系建设推进，信用管理人才需求增长。就业方向包括银行、征信机构、信用评级公司、互联网金融等。",
        "xuefeng_comment": "信用管理是比较新兴的专业，随着社会信用体系建设和互联网金融发展，这个专业的重要性日益凸显。就业方向主要包括银行信用卡部门、征信机构、信用评级公司、互联网金融企业等。薪资水平在金融类中属于中等。这个专业需要较强的数据分析能力和逻辑思维。建议数学和统计学基础好的学生报考。",
        "yearly_courses": {"大一": ["微积分", "线性代数", "概率论", "政治经济学", "会计学"], "大二": ["统计学", "金融学", "信用管理学", "征信理论与实务"], "大三": ["信用风险计量", "信用评级", "金融风险管理", "信用法律法规"], "大四": ["信用管理实习"]},
        "top_universities": {"domestic": ["中国人民大学", "上海财经大学", "对外经济贸易大学", "首都经济贸易大学"], "international": ["LSE", "University of Chicago", "NYU", "University of Toronto"]}
    },
    {
        "code": "020304T",
        "name": "投资学",
        "category": "02 经济学",
        "category_icon": "💹",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥15k-35k",
        "overview": "投资学是研究投资决策、资产配置和投资管理的经济学科。本专业培养掌握证券投资、基金管理、资产管理等专业知识的金融人才。",
        "what_you_learn": "投资学原理、公司金融、证券投资学、基金管理、资产定价理论、金融工程、投资组合管理、固定收益证券、衍生金融工具",
        "suitable_for": "对投资理财感兴趣、风险意识强的学生。",
        "career_outlook": "财富管理行业发展迅速，专业投资人才需求旺盛。就业方向包括证券公司、基金公司、资产管理公司、商业银行、私募基金等。",
        "xuefeng_comment": "投资学是金融类中的热门方向，就业主要在金融机构的投资部门或资产管理公司。薪资水平两极分化明显，顶尖人才薪资极高，但普通从业者收入一般。这个行业竞争激烈，对学校背景和学历要求较高。建议考取相关资格证书，如CFA、基金从业资格等。读研能去更好的平台。本科阶段建议尽早实习，积累实战经验。",
        "yearly_courses": {"大一": ["微积分", "线性代数", "概率论", "政治经济学", "会计学原理"], "大二": ["统计学", "金融学", "公司金融", "证券投资学"], "大三": ["基金管理", "资产定价理论", "金融工程", "投资组合管理"], "大四": ["投资机构实习"]},
        "top_universities": {"domestic": ["中央财经大学", "上海财经大学", "对外经济贸易大学", "南开大学"], "international": ["Columbia", "LSE", "Princeton", "University of Chicago"]}
    },
    {
        "code": "020306T",
        "name": "精算学",
        "category": "02 经济学",
        "category_icon": "🎯",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥20k-45k",
        "overview": "精算学是应用数学、统计学和金融学方法评估风险的专业学科。本专业培养掌握保险精算、风险管理等专业知识的精算人才。",
        "what_you_learn": "精算数学、保险精算学、利息理论、风险理论、生命 contingencies", "金融数学、数理统计、随机过程、投资与资产管理",
        "suitable_for": "数学基础极其扎实、对风险评估感兴趣的学生。",
        "career_outlook": "保险行业和金融行业发展，精算师需求稳定增长。就业主要在保险公司、精算咨询公司、银行、养老金公司等。",
        "xuefeng_comment": "精算学是数学和金融的交叉学科，被称为'金领中的金领'。但我要提醒大家，精算师考证难度极大，需要通过一系列国际精算师考试才能成为真正的精算师。这个专业对数学要求极高，不是简单算数那么简单。建议数学竞赛获奖者或数学天赋极强的学生报考。就业稳定，薪资待遇优厚，但需要持续学习和考证。",
        "yearly_courses": {"大一": ["微积分", "线性代数", "概率论", "政治经济学", "会计学"], "大二": ["数理统计", "利息理论", "金融学", "保险学原理"], "大三": ["精算数学", "风险理论", "生命 contingencies", "非寿险精算"], "大四": ["精算实习"]},
        "top_universities": {"domestic": ["对外经济贸易大学", "上海财经大学", "中央财经大学", "南开大学", "湖南大学"], "international": ["University of Waterloo", "Heriot-Watt University", "University of Michigan", "Boston University"]}
    },
    {
        "code": "020307T",
        "name": "数字经济",
        "category": "02 经济学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥14k-28k",
        "overview": "数字经济是研究数字技术驱动的经济活动和数字治理的经济学科。本专业培养掌握数字经济分析、数字产业管理等专业知识的复合型人才。",
        "what_you_learn": "数字经济学、数字技术概论、区块链与数字货币、电子商务、数据分析与挖掘、平台经济学、数字营销、网络经济学",
        "suitable_for": "对数字经济和互联网产业感兴趣的学生。",
        "career_outlook": "数字经济蓬勃发展，专业人才需求旺盛。就业方向包括互联网企业、数字经济研究机构、政府部门等。",
        "xuefeng_comment": "数字经济是新兴专业，顺应数字化发展趋势。这个专业涉及面广，既要学经济学基础，也要学数字技术。就业方向主要是互联网企业和数字经济相关领域。报考时建议关注学校的学科背景，选择计算机或经济学强势的学校更有优势。这个专业适合对互联网和新兴经济形态有兴趣的学生。",
        "yearly_courses": {"大一": ["微积分", "线性代数", "政治经济学", "数字技术概论", "会计学"], "大二": ["统计学", "金融学", "数字经济学", "数据分析基础"], "大三": ["区块链与数字货币", "平台经济学", "数字营销", "电子商务"], "大四": ["数字经济企业实习"]},
        "top_universities": {"domestic": ["中国人民大学", "复旦大学", "浙江大学", "上海对外经贸大学", "中央财经大学"], "international": ["MIT", "Stanford", "University of Cambridge", "University of Tokyo"]}
    },
    {
        "code": "120103",
        "name": "工程管理",
        "category": "12 管理学",
        "category_icon": "🏗️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥12k-26k",
        "overview": "工程管理是研究工程项目建设全过程管理的学科。本专业培养掌握工程项目决策、计划、组织、控制等专业知识的复合型管理人才。",
        "what_you_learn": "工程项目管理、工程经济学、工程造价管理、工程合同管理、施工组织设计、建筑力学、工程结构、建设法规",
        "suitable_for": "对工程项目管理感兴趣、具有较强组织协调能力的学生。",
        "career_outlook": "基础设施建设持续投入，工程管理人才需求稳定。就业方向包括建筑施工企业、房地产公司、工程咨询公司、造价事务所等。",
        "xuefeng_comment": "工程管理是建筑行业的管理类专业，就业主要集中在房地产和建筑施工行业。这个专业既学管理又学一些工程技术，知识面比较广。就业相对稳定，但薪资水平中等。工作可能需要去工地现场，环境相对艰苦。建议男生报考为主，女生可以考虑考研后去设计院或房地产公司。可以考取一级建造师、造价工程师等执业资格。",
        "yearly_courses": {"大一": ["微积分", "线性代数", "工程制图", "管理学原理", "经济学原理"], "大二": ["工程力学", "工程结构", "工程项目管理", "工程经济学"], "大三": ["工程造价管理", "工程合同管理", "施工组织设计", "建设法规"], "大四": ["工程项目实习"]},
        "top_universities": {"domestic": ["重庆大学", "西安建筑科技大学", "同济大学", "东南大学", "天津大学"], "international": ["MIT", "Imperial College London", "TU Delft", "University of Sydney"]}
    }
]

def main():
    print("=" * 60)
    print("开始导入经济管理专业...")
    print("=" * 60)
    
    success = failed = skipped = 0
    
    for major in economics_majors:
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