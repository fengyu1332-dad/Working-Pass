import urllib.request
import urllib.error
import json
import time
import ssl

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

# 工科专业列表
majors = [
    {
        "code": "080717T",
        "name": "人工智能",
        "category": "08 工学",
        "category_icon": "🤖",
        "difficulty": "⭐⭐⭐⭐⭐",
        "salary_range": "¥20k-45k",
        "overview": "人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的新兴技术学科。本专业培养掌握人工智能基础理论、机器学习和深度学习算法、智能系统设计与开发的专业人才。",
        "what_you_learn": "机器学习、深度学习、神经网络、计算机视觉、自然语言处理、机器人技术、智能系统设计、Python编程、算法优化、数据结构",
        "suitable_for": "数学基础扎实、逻辑思维强、对新技术充满好奇心、喜欢编程和算法研究的学生。需要具备较强的抽象思维能力和持续学习能力。",
        "career_outlook": "人工智能是国家战略重点发展的领域，就业前景极为广阔。毕业生可在互联网企业、科技公司、研究机构等单位从事AI算法研发、智能产品设计、数据分析等工作。",
        "xuefeng_comment": "人工智能是当下最火爆的专业之一，但报考需要理性看待。这个专业对数学和编程要求极高，不是单纯追热门就能学好的。需要学生真正热爱技术、有较强的逻辑思维能力，并且做好持续学习、不断更新知识的准备。建议选择有人工智能强势学科的高校，同时要有读研的规划，因为本科阶段的学习深度往往不足以支撑直接就业。当然，如果能学好，这个专业的薪资待遇确实非常可观，但前提是你必须真正热爱这个领域，而不是单纯为了高薪。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "计算机导论", "程序设计基础"], "大二": ["数据结构", "算法设计", "机器学习基础", "数据库原理", "操作系统"], "大三": ["深度学习", "计算机视觉", "自然语言处理", "强化学习", "人工智能综合项目"], "大四": ["毕业设计", "企业实习"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "浙江大学", "上海交通大学", "中国科学技术大学", "哈尔滨工业大学"], "international": ["MIT", "Stanford", "Carnegie Mellon", "UC Berkeley"]}
    },
    {
        "code": "080910T",
        "name": "数据科学与大数据技术",
        "category": "08 工学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥18k-40k",
        "overview": "数据科学与大数据技术是研究数据采集、存储、处理、分析和可视化的综合性学科。本专业培养掌握大数据技术体系、具有大数据分析和应用能力的高级专门人才。",
        "what_you_learn": "大数据技术概论、Hadoop生态系统、Spark计算框架、NoSQL数据库、数据挖掘与机器学习、Python/R语言、数据可视化、统计学基础",
        "suitable_for": "对数据感兴趣、具备良好数学基础、喜欢分析和处理信息的学生。需要有耐心处理大量数据，并能从数据中发现规律。",
        "career_outlook": "大数据已渗透到各行各业，数据科学家被麦肯锡评为21世纪最具吸引力的职业。毕业生可在互联网、金融、医疗、零售等行业从事数据分析工作。",
        "xuefeng_comment": "数据科学和大数据技术是数字化时代的香饽饽，但我要泼点冷水。这个专业听起来高大上，实际上需要非常扎实的数学和编程基础。建议数学成绩一般的同学慎重考虑，因为概率统计、机器学习这些课程对数学要求很高。就业方向确实不错，但竞争也很激烈，建议读研提升竞争力。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "Python程序设计", "数据科学导论"], "大二": ["数据结构", "数据库原理", "统计学", "机器学习基础"], "大三": ["大数据技术概论", "Hadoop开发", "Spark实战", "数据挖掘"], "大四": ["毕业设计", "企业实习"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "中国人民大学", "华东师范大学"], "international": ["MIT", "Stanford", "UC Berkeley"]}
    },
    {
        "code": "080905",
        "name": "物联网工程",
        "category": "08 工学",
        "category_icon": "🌐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥15k-30k",
        "overview": "物联网工程是研究物体与物体、物体与网络连接技术的工程学科。本专业培养掌握物联网系统设计、开发和应用的专业人才，涉及传感器技术、通信技术、嵌入式系统等多个领域。",
        "what_you_learn": "物联网概论、传感器技术、嵌入式系统开发、无线通信技术、RFID技术、物联网协议、云平台架构、智能硬件设计",
        "suitable_for": "对智能硬件和连接技术感兴趣、喜欢动手实践、具备较强动手能力的学生。需要有耐心调试硬件和解决技术问题。",
        "career_outlook": "物联网是国家战略性新兴产业，智能家居、智慧城市、工业互联网等领域快速发展，对物联网人才需求旺盛。",
        "xuefeng_comment": "物联网是个很有前景的专业方向，国家也在大力推进新基建，智慧城市、智能制造这些都离不开物联网技术。就业方向比较多，可以做硬件也可以做软件。但这个专业学的比较杂，容易出现什么都会一点但什么都不精的情况。建议在本科阶段就找准一个方向深入学习。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "C语言程序设计", "电路基础", "物联网导论"], "大二": ["数字电路", "模拟电路", "微控制器原理", "传感器技术"], "大三": ["嵌入式系统", "无线通信技术", "RFID技术", "物联网协议"], "大四": ["毕业设计", "企业实习"]},
        "top_universities": {"domestic": ["哈尔滨工业大学", "北京邮电大学", "电子科技大学", "东南大学"], "international": ["MIT", "Stanford", "Georgia Tech"]}
    },
    {
        "code": "080803T",
        "name": "机器人工程",
        "category": "08 工学",
        "category_icon": "🤖",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥18k-38k",
        "overview": "机器人工程是研究机器人设计、制造、控制和应用的技术学科。本专业培养掌握机器人机械结构设计、运动控制、感知导航等专业知识的复合型工程技术人才。",
        "what_you_learn": "机器人学导论、机器人机械设计、运动控制理论、传感器与感知技术、机器人编程、机器视觉、人工智能基础、嵌入式系统",
        "suitable_for": "对机器人技术感兴趣、具备较强动手能力和创新思维的学生。需要有跨学科学习的能力。",
        "career_outlook": "机器人产业正处于快速发展期，工业机器人、服务机器人、特种机器人等领域对专业人才需求持续增长。",
        "xuefeng_comment": "机器人工程是典型的新工科专业，符合国家制造业转型升级的大方向。但这个专业难度较大，需要同时掌握机械、电子、计算机等多个学科的知识。建议对机器人有真正兴趣的学生报考，读研几乎是必须的。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "大学物理", "机械制图", "C语言程序设计"], "大二": ["理论力学", "材料力学", "电路基础", "自动控制原理"], "大三": ["机器人学", "运动控制", "传感器技术", "机器视觉"], "大四": ["毕业设计", "机器人项目实践"]},
        "top_universities": {"domestic": ["哈尔滨工业大学", "北京航空航天大学", "浙江大学", "东北大学"], "international": ["MIT", "Stanford", "Carnegie Mellon"]}
    },
    {
        "code": "080703",
        "name": "通信工程",
        "category": "08 工学",
        "category_icon": "📡",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥16k-35k",
        "overview": "通信工程是研究信息传输、交换和处理的技术学科。本专业培养掌握现代通信系统设计、开发和维护的专业人才，涉及有线通信、无线通信、光纤通信等多个领域。",
        "what_you_learn": "信号与系统、数字信号处理、通信原理、电磁场与电磁波、移动通信、光纤通信、微波技术、天线原理",
        "suitable_for": "物理基础扎实、对通信技术感兴趣、逻辑思维能力较强的学生。需要有较强的数学和物理基础。",
        "career_outlook": "通信行业是信息社会的基础设施产业，5G/6G、物联网等领域持续发展，对通信工程人才需求稳定。",
        "xuefeng_comment": "通信工程是个老牌热门工科专业，就业一直比较稳定。5G建设、物联网发展都离不开通信人才。但要注意，这个专业对数学和物理要求比较高，建议物理成绩好的学生报考。读研后薪资会有明显提升。",
        "yearly_courses": {"大一": ["高等数学", "线性代数", "大学物理", "C语言程序设计", "电路分析"], "大二": ["模拟电路", "数字电路", "信号与系统", "电磁场与电磁波"], "大三": ["通信原理", "数字信号处理", "移动通信", "光纤通信"], "大四": ["通信系统设计", "企业实习"]},
        "top_universities": {"domestic": ["北京邮电大学", "电子科技大学", "西安电子科技大学", "东南大学"], "international": ["MIT", "Stanford", "Georgia Tech"]}
    }
]

def main():
    print("=" * 60)
    print("开始导入工科专业...")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for major in majors:
        print(f"\n正在导入: {major['code']} - {major['name']}")
        ok, code = import_major(major)
        
        if ok or code == 201:
            success += 1
            print(f"✅ 成功")
        else:
            failed += 1
            print(f"❌ 失败 (HTTP {code})")
        
        time.sleep(0.2)
    
    print("\n" + "=" * 60)
    print(f"导入完成！成功: {success}, 失败: {failed}")
    print("=" * 60)

if __name__ == "__main__":
    main()