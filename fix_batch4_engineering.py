"""
系统性补充教育部2024年专业清单中的缺失专业
第四批：工学类（机械类、材料类、电子信息类、计算机类等）
"""
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
    url = f'{SUPABASE_URL}/rest/v1/majors'
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

majors = [
    # ========== 08工学 - 机械类 ==========
    {
        "code": "080105",
        "name": "工业设计",
        "category": "08 工学",
        "category_icon": "💡",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "工业设计专业培养掌握工业产品设计理论和技能的专门人才，能在设计机构、企业设计部门从事产品设计工作。",
        "what_you_learn": "工业设计概论、产品设计方法、人机工程学、工业设计史、材料与工艺、设计表达",
        "suitable_for": "对工业设计感兴趣，有创意和审美能力的学生。",
        "career_outlook": "设计机构、企业设计部门、制造业等。",
        "xuefeng_comment": "工业设计专业就业好，中国制造转型升级需要大量设计人才！",
        "yearly_courses": {"大一": ["工业设计概论", "设计素描", "设计色彩"], "大二": ["产品设计方法", "人机工程学", "材料与工艺"], "大三": ["设计表达", "计算机辅助设计", "设计实践"], "大四": ["设计机构/企业实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学美术学院", "北京理工大学", "上海交通大学", "浙江大学"], "international": ["艺术中心设计学院", "皇家艺术学院"]}
    },
    {
        "code": "080106",
        "name": "过程装备与控制工程",
        "category": "08 工学",
        "category_icon": "⚙️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "过程装备与控制工程专业培养掌握过程装备设计和管理的高级工程技术人才，能在化工、制药等行业从事装备设计和管理工作。",
        "what_you_learn": "化工原理、过程装备设计、过程控制工程、流体机械、过程装备制造",
        "suitable_for": "对过程装备感兴趣的学生。",
        "career_outlook": "化工企业、制药企业、装备制造企业等。",
        "xuefeng_comment": "过程装备与控制工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图"], "大二": ["理论力学", "材料力学", "化工原理"], "大三": ["过程装备设计", "过程控制工程", "流体机械"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["华东理工大学", "北京化工大学", "浙江工业大学"], "international": []}
    },
    {
        "code": "080107",
        "name": "车辆工程",
        "category": "08 工学",
        "category_icon": "🚗",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "车辆工程专业培养掌握汽车设计与制造技术的高级工程技术人才，能在汽车企业从事汽车设计、制造和管理工作。",
        "what_you_learn": "汽车构造、汽车理论、汽车设计、汽车制造工艺、汽车电子技术",
        "suitable_for": "对汽车感兴趣的学生。",
        "career_outlook": "汽车企业、汽车零部件企业、汽车研发机构等。",
        "xuefeng_comment": "车辆工程专业就业非常好，新能源汽车行业发展迅猛！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "机械设计基础"], "大二": ["汽车构造", "汽车理论", "材料力学"], "大三": ["汽车设计", "汽车制造工艺", "汽车电子技术"], "大四": ["汽车企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "上海交通大学", "同济大学", "吉林大学", "北京理工大学"], "international": ["密歇根大学", "斯坦福大学"]}
    },
    {
        "code": "080108",
        "name": "汽车服务工程",
        "category": "08 工学",
        "category_icon": "🔧",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "汽车服务工程专业培养掌握汽车服务理论和技能的专门人才，能在汽车后市场从事技术服务和管理工作。",
        "what_you_learn": "汽车构造、汽车营销、汽车维修工程、汽车保险与理赔、二手车鉴定评估",
        "suitable_for": "对汽车服务行业感兴趣的学生。",
        "career_outlook": "汽车4S店、汽车维修企业、汽车保险公司、二手车市场等。",
        "xuefeng_comment": "汽车服务工程专业就业好，汽车后市场规模庞大！",
        "yearly_courses": {"大一": ["汽车构造", "机械设计基础"], "大二": ["汽车营销", "汽车维修工程"], "大三": ["汽车保险与理赔", "二手车鉴定评估"], "大四": ["汽车服务企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["同济大学", "北京理工大学", "武汉理工大学"], "international": []}
    },
    {
        "code": "080109T",
        "name": "机械工艺技术",
        "category": "08 工学",
        "category_icon": "🔩",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "机械工艺技术专业培养掌握机械加工工艺技术的专门人才，能在制造企业从事工艺设计和技术工作。",
        "what_you_learn": "机械制造基础、数控加工技术、机械加工工艺、刀具设计、工装夹具设计",
        "suitable_for": "对机械加工感兴趣的学生。",
        "career_outlook": "制造企业、机械加工企业等。",
        "xuefeng_comment": "机械工艺技术专业就业稳定！",
        "yearly_courses": {"大一": ["机械制图", "机械设计基础"], "大二": ["机械制造基础", "金属材料"], "大三": ["数控加工技术", "机械加工工艺"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["华中科技大学", "北京理工大学"], "international": []}
    },
    {
        "code": "080110T",
        "name": "微机电系统工程",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "微机电系统工程专业培养掌握微机电系统设计和制造技术的高级专门人才，能在高科技企业从事MEMS研发工作。",
        "what_you_learn": "微机电系统概论、微电子制造技术、微机械设计、微传感器技术、微纳米技术",
        "suitable_for": "对微机电系统感兴趣的学生。",
        "career_outlook": "半导体企业、MEMS传感器企业、科研机构等。",
        "xuefeng_comment": "微机电系统工程是前沿专业，就业好！建议继续深造。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "机械设计基础"], "大二": ["微机电系统概论", "微电子制造技术"], "大三": ["微机械设计", "微传感器技术"], "大四": ["企业/研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["东南大学", "北京大学", "清华大学"], "international": []}
    },
    {
        "code": "080111T",
        "name": "机电技术教育",
        "category": "08 工学",
        "category_icon": "🏭",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "机电技术教育专业培养掌握机电技术理论和教育方法的专门人才，能在职业院校从事机电技术教学工作。",
        "what_you_learn": "机电一体化技术、电气控制技术、可编程控制器、教育学、机电教学法",
        "suitable_for": "对机电技术和教育工作感兴趣的学生。",
        "career_outlook": "职业院校、培训机构等。",
        "xuefeng_comment": "机电技术教育专业就业稳定，适合想当老师的同学！",
        "yearly_courses": {"大一": ["机械设计基础", "电工电子学"], "大二": ["机电一体化技术", "电气控制技术"], "大三": ["可编程控制器", "教育学"], "大四": ["职业院校实习", "毕业论文"]},
        "top_universities": {"domestic": ["天津职业技术师范大学", "河南师范大学"], "international": []}
    },
    
    # ========== 08工学 - 材料类 ==========
    {
        "code": "080402",
        "name": "材料物理",
        "category": "08 工学",
        "category_icon": "🔬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "材料物理专业培养掌握材料物理理论和技术的专门人才，能在材料企业和科研机构从事材料研发工作。",
        "what_you_learn": "材料物理、固体物理学、材料力学、材料分析方法、半导体材料",
        "suitable_for": "对材料科学感兴趣的学生。",
        "career_outlook": "材料企业、半导体企业、科研机构等。",
        "xuefeng_comment": "材料物理专业就业好，材料是工业基础！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "材料科学基础"], "大二": ["材料物理", "固体物理学"], "大三": ["材料力学", "材料分析方法", "半导体材料"], "大四": ["企业/研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "上海交通大学", "浙江大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080403",
        "name": "材料化学",
        "category": "08 工学",
        "category_icon": "🧪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "材料化学专业培养掌握材料化学理论和技术的专门人才，能在材料企业和科研机构从事材料研发工作。",
        "what_you_learn": "材料化学、无机非金属材料化学、高分子材料化学、材料分析测试技术",
        "suitable_for": "对材料化学感兴趣的学生。",
        "career_outlook": "材料企业、化工企业、科研机构等。",
        "xuefeng_comment": "材料化学专业就业好！",
        "yearly_courses": {"大一": ["高等数学", "大学化学", "材料科学基础"], "大二": ["材料化学", "高分子化学"], "大三": ["无机非金属材料化学", "材料分析测试技术"], "大四": ["企业/研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "复旦大学", "浙江大学"], "international": ["哈佛大学", "斯坦福大学"]}
    },
    {
        "code": "080404",
        "name": "冶金工程",
        "category": "08 工学",
        "category_icon": "🔩",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "冶金工程专业培养掌握钢铁和有色金属冶炼技术的高级工程技术人才，能在冶金企业从事技术和管理工作。",
        "what_you_learn": "冶金原理、钢铁冶金学、有色金属冶金学、冶金设备、冶金工艺",
        "suitable_for": "对冶金行业感兴趣的学生。",
        "career_outlook": "钢铁企业、有色金属企业、冶金设备企业等。",
        "xuefeng_comment": "冶金工程专业是老牌工科专业，就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图"], "大二": ["理论力学", "材料力学", "冶金原理"], "大三": ["钢铁冶金学", "有色金属冶金学", "冶金设备"], "大四": ["冶金企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京科技大学", "东北大学", "中南大学"], "international": []}
    },
    {
        "code": "080405",
        "name": "金属材料工程",
        "category": "08 工学",
        "category_icon": "🛡️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "金属材料工程专业培养掌握金属材料设计和使用技术的高级工程技术人才，能在材料企业和制造企业从事材料研发和管理工作。",
        "what_you_learn": "金属材料学、材料力学、金属材料加工、材料热处理、金属材料性能测试",
        "suitable_for": "对金属材料感兴趣的学生。",
        "career_outlook": "材料企业、航空航天企业、汽车企业等。",
        "xuefeng_comment": "金属材料工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图"], "大二": ["金属材料学", "材料力学"], "大三": ["金属材料加工", "材料热处理", "金属材料性能测试"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京科技大学", "西北工业大学", "哈尔滨工业大学"], "international": []}
    },
    {
        "code": "080406",
        "name": "无机非金属材料工程",
        "category": "08 工学",
        "category_icon": "🏺",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "无机非金属材料工程专业培养掌握无机非金属材料设计和技术的高级工程技术人才，能在材料企业从事材料研发和生产工作。",
        "what_you_learn": "无机非金属材料学、材料力学、材料热工基础、陶瓷材料工艺、水泥与混凝土工艺",
        "suitable_for": "对无机非金属材料感兴趣的学生。",
        "career_outlook": "建材企业、陶瓷企业、新材料企业等。",
        "xuefeng_comment": "无机非金属材料工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学化学", "工程制图"], "大二": ["无机非金属材料学", "材料力学"], "大三": ["材料热工基础", "陶瓷材料工艺", "水泥与混凝土工艺"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["武汉理工大学", "华南理工大学", "华东理工大学"], "international": []}
    },
    {
        "code": "080407",
        "name": "高分子材料与工程",
        "category": "08 工学",
        "category_icon": "💎",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "高分子材料与工程专业培养掌握高分子材料设计和技术的高级工程技术人才，能在材料企业和化工企业从事材料研发和生产工作。",
        "what_you_learn": "高分子化学、高分子物理、高分子材料加工、塑料成型工艺、橡胶工艺学",
        "suitable_for": "对高分子材料感兴趣的学生。",
        "career_outlook": "材料企业、化工企业、塑料制品企业等。",
        "xuefeng_comment": "高分子材料与工程专业就业好！",
        "yearly_courses": {"大一": ["高等数学", "大学化学", "工程制图"], "大二": ["高分子化学", "高分子物理"], "大三": ["高分子材料加工", "塑料成型工艺", "橡胶工艺学"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "浙江大学", "四川大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080408",
        "name": "复合材料与工程",
        "category": "08 工学",
        "category_icon": "🛡️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "复合材料与工程专业培养掌握复合材料设计和技术的高级工程技术人才，能在航空航天、新材料企业从事复合材料研发工作。",
        "what_you_learn": "复合材料力学、复合材料设计、复合材料制备技术、复合材料性能测试、航空航天复合材料",
        "suitable_for": "对复合材料感兴趣的学生。",
        "career_outlook": "航空航天企业、新材料企业、汽车企业等。",
        "xuefeng_comment": "复合材料与工程专业就业好，是国家重点发展领域！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["材料科学基础", "复合材料力学"], "大三": ["复合材料设计", "复合材料制备技术"], "大四": ["航空航天/新材料企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["西北工业大学", "哈尔滨工业大学", "南京航空航天大学"], "international": []}
    },
    
    # ========== 08工学 - 能源动力类 ==========
    {
        "code": "080501",
        "name": "能源与动力工程",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "能源与动力工程专业培养掌握能源转换和动力技术的的高级工程技术人才，能在电力企业、动力机械企业从事技术和管理工作。",
        "what_you_learn": "工程热力学、流体力学、传热学、锅炉原理、汽轮机原理、热力发电厂",
        "suitable_for": "对能源和动力感兴趣的学生。",
        "career_outlook": "电力企业、动力机械企业、空调制冷企业等。",
        "xuefeng_comment": "能源与动力工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["工程热力学", "流体力学", "传热学"], "大三": ["锅炉原理", "汽轮机原理", "热力发电厂"], "大四": ["电力/动力企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "西安交通大学", "上海交通大学", "华中科技大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080502T",
        "name": "能源与环境系统工程",
        "category": "08 工学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "能源与环境系统工程专业培养掌握能源系统优化和环境保护的高级工程技术人才，能在能源企业和环保企业从事相关工作。",
        "what_you_learn": "能源系统分析、能源与环境、节能技术、清洁能源技术、环境工程",
        "suitable_for": "对能源环保感兴趣的学生。",
        "career_outlook": "能源企业、环保企业、政府能源管理部门等。",
        "xuefeng_comment": "能源与环境系统工程是新兴交叉专业，就业好！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["工程热力学", "能源系统分析"], "大三": ["能源与环境", "清洁能源技术", "节能技术"], "大四": ["能源/环保企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "上海交通大学", "华中科技大学"], "international": []}
    },
    {
        "code": "080503T",
        "name": "新能源科学与工程",
        "category": "08 工学",
        "category_icon": "☀️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "新能源科学与工程专业培养掌握新能源开发与利用技术的高级工程技术人才，能在新能源企业从事技术研发和管理工作。",
        "what_you_learn": "太阳能利用技术、风能利用技术、生物质能技术、储能技术、新能源发电技术",
        "suitable_for": "对新能源技术感兴趣的学生。",
        "career_outlook": "新能源企业、电网公司、电力设备企业等。",
        "xuefeng_comment": "新能源科学与工程专业就业非常好，是国家战略重点！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["工程热力学", "流体力学"], "大三": ["太阳能利用技术", "风能利用技术", "储能技术"], "大四": ["新能源企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["华北电力大学", "上海交通大学", "华中科技大学", "河海大学"], "international": []}
    },
    {
        "code": "080504T",
        "name": "储能科学与工程",
        "category": "08 工学",
        "category_icon": "🔋",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "储能科学与工程专业培养掌握储能技术的高级工程技术人才，能在储能企业、新能源企业从事储能系统研发和管理工作。",
        "what_you_learn": "储能原理与技术、电池技术、储热技术、储氢技术、储能系统设计",
        "suitable_for": "对储能技术感兴趣的学生。",
        "career_outlook": "储能企业、新能源企业、电网公司等。",
        "xuefeng_comment": "储能科学与工程是新兴专业，随着新能源发展，需求爆发式增长！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["工程热力学", "电化学基础"], "大三": ["储能原理与技术", "电池技术", "储热技术"], "大四": ["储能/新能源企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["华中科技大学", "天津大学", "上海交通大学"], "international": []}
    },
    
    # ========== 08工学 - 电子信息类 ==========
    {
        "code": "080702",
        "name": "电子科学与技术",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "电子科学与技术专业培养掌握电子器件和电路设计技术的高级工程技术人才，能在电子企业和IT企业从事技术研发工作。",
        "what_you_learn": "电路分析、模拟电子技术、数字电子技术、信号与系统、微电子技术、电磁场与电磁波",
        "suitable_for": "对电子技术感兴趣的学生。",
        "career_outlook": "电子企业、半导体企业、通信企业等。",
        "xuefeng_comment": "电子科学与技术专业就业非常好！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["模拟电子技术", "数字电子技术", "信号与系统"], "大三": ["微电子技术", "电磁场与电磁波", "高频电子线路"], "大四": ["电子企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["电子科技大学", "西安电子科技大学", "北京大学", "复旦大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080703",
        "name": "通信工程",
        "category": "08 工学",
        "category_icon": "📡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "通信工程专业培养掌握通信系统和技术的高级工程技术人才，能在通信企业和IT企业从事通信系统研发和管理工作。",
        "what_you_learn": "通信原理、信号与系统、数字信号处理、通信电子线路、移动通信、光纤通信",
        "suitable_for": "对通信技术感兴趣的学生。",
        "career_outlook": "通信企业、互联网企业、电信运营商等。",
        "xuefeng_comment": "通信工程专业就业非常好！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["信号与系统", "数字信号处理", "通信电子线路"], "大三": ["通信原理", "移动通信", "光纤通信"], "大四": ["通信企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京邮电大学", "电子科技大学", "西安电子科技大学", "东南大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080704",
        "name": "微电子科学与工程",
        "category": "08 工学",
        "category_icon": "🔌",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "微电子科学与工程专业培养掌握集成电路设计和技术的高级工程技术人才，能在半导体企业和IC设计企业从事芯片研发工作。",
        "what_you_learn": "半导体物理、集成电路设计、IC制造技术、微电子器件、版图设计",
        "suitable_for": "对微电子技术感兴趣的学生。",
        "career_outlook": "半导体企业、IC设计企业、电子整机企业等。",
        "xuefeng_comment": "微电子科学与工程专业就业非常好，是卡脖子技术领域！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["半导体物理", "模拟电子技术", "数字电子技术"], "大三": ["集成电路设计", "IC制造技术", "微电子器件"], "大四": ["半导体企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "清华大学", "复旦大学", "电子科技大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080705",
        "name": "光电信息科学与工程",
        "category": "08 工学",
        "category_icon": "💡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "光电信息科学与工程专业培养掌握光电信息技术的的高级工程技术人才，能在光电企业和通信企业从事技术研发工作。",
        "what_you_learn": "物理光学、应用光学、光电子技术、光纤通信、光电检测技术、光电系统设计",
        "suitable_for": "对光电信息技术感兴趣的学生。",
        "career_outlook": "光电企业、通信企业、激光企业、显示技术企业等。",
        "xuefeng_comment": "光电信息科学与工程专业就业好！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["物理光学", "应用光学", "信号与系统"], "大三": ["光电子技术", "光纤通信", "光电检测技术"], "大四": ["光电企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["浙江大学", "华中科技大学", "天津大学", "电子科技大学"], "international": ["斯坦福大学"]}
    },
    {
        "code": "080706",
        "name": "信息工程",
        "category": "08 工学",
        "category_icon": "📊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "信息工程专业培养掌握信息系统和技术的的高级工程技术人才，能在IT企业和通信企业从事信息系统研发工作。",
        "what_you_learn": "信号与系统、数字信号处理、信息论与编码、通信原理、雷达原理、信息安全",
        "suitable_for": "对信息技术感兴趣的学生。",
        "career_outlook": "IT企业、通信企业、互联网企业等。",
        "xuefeng_comment": "信息工程专业就业非常好！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["信号与系统", "数字信号处理", "信息论与编码"], "大三": ["通信原理", "雷达原理", "信息安全"], "大四": ["IT企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["上海交通大学", "东南大学", "北京邮电大学", "电子科技大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    
    # ========== 08工学 - 自动化类 ==========
    {
        "code": "080802T",
        "name": "轨道交通信号与控制",
        "category": "08 工学",
        "category_icon": "🚂",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "轨道交通信号与控制专业培养掌握轨道交通信号和控制技术的高级工程技术人才，能在轨道交通企业从事信号系统研发和维护工作。",
        "what_you_learn": "铁路信号基础、列车运行控制系统、车站信号控制、区间信号控制、铁道信号设备",
        "suitable_for": "对轨道交通信号感兴趣的学生。",
        "career_outlook": "铁路局、城市轨道交通企业、信号设备企业等。",
        "xuefeng_comment": "轨道交通信号与控制专业就业稳定，铁路和地铁大发展需要大量人才！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["自动控制原理", "信号与系统"], "大三": ["铁路信号基础", "列车运行控制系统", "车站信号控制"], "大四": ["轨道交通企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京交通大学", "西南交通大学", "兰州交通大学"], "international": []}
    },
    {
        "code": "080803T",
        "name": "机器人工程",
        "category": "08 工学",
        "category_icon": "🤖",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "机器人工程专业培养掌握机器人设计和技术的高级工程技术人才，能在机器人企业和智能制造企业从事机器人研发工作。",
        "what_you_learn": "机器人学、机器人机构学、机器人控制技术、机器人传感技术、人工智能",
        "suitable_for": "对机器人技术感兴趣的学生。",
        "career_outlook": "机器人企业、智能制造企业、汽车企业等。",
        "xuefeng_comment": "机器人工程是新兴热门专业，就业非常好！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "机械设计基础"], "大二": ["自动控制原理", "单片机原理"], "大三": ["机器人学", "机器人机构学", "机器人控制技术"], "大四": ["机器人企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["东南大学", "北京航空航天大学", "哈尔滨工业大学", "浙江大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "080804T",
        "name": "邮政工程",
        "category": "08 工学",
        "category_icon": "📦",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "邮政工程专业培养掌握邮政技术和设备的高级工程技术人才，能在邮政企业和物流企业从事技术和管理工作。",
        "what_you_learn": "邮政技术基础、邮政设备自动化、物流技术、邮政网络规划、邮政物联网技术",
        "suitable_for": "对邮政和物流技术感兴趣的学生。",
        "career_outlook": "邮政企业、快递企业、物流企业等。",
        "xuefeng_comment": "邮政工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["自动控制原理", "物流技术"], "大三": ["邮政设备自动化", "邮政网络规划"], "大四": ["邮政/物流企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京邮电大学", "南京邮电大学"], "international": []}
    },
    
    # ========== 08工学 - 计算机类 ==========
    {
        "code": "080903",
        "name": "网络工程",
        "category": "08 工学",
        "category_icon": "🌐",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "网络工程专业培养掌握网络设计和维护技术的高级工程技术人才，能在IT企业和互联网企业从事网络工程工作。",
        "what_you_learn": "计算机网络、数据通信、网络协议、网络设备、网络安全、网络工程设计",
        "suitable_for": "对网络技术感兴趣的学生。",
        "career_outlook": "IT企业、互联网企业、电信运营商、网络设备企业等。",
        "xuefeng_comment": "网络工程专业就业非常好！",
        "yearly_courses": {"大一": ["高等数学", "程序设计基础", "计算机组成原理"], "大二": ["数据结构", "操作系统", "计算机网络"], "大三": ["数据通信", "网络协议", "网络安全"], "大四": ["IT企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["电子科技大学", "西安电子科技大学", "北京邮电大学", "东南大学"], "international": ["斯坦福大学", "麻省理工学院"]}
    },
    {
        "code": "080904K",
        "name": "信息安全",
        "category": "08 工学",
        "category_icon": "🔒",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥10k-30k",
        "overview": "信息安全专业培养掌握网络安全和信息安全技术的高级工程技术人才，能在安全企业和互联网企业从事安全研发和运维工作。",
        "what_you_learn": "网络安全基础、密码学、信息安全数学基础、网络攻防技术、安全协议、信息安全管理",
        "suitable_for": "对信息安全技术感兴趣的学生。",
        "career_outlook": "安全企业、互联网企业、金融机构、政府安全部门等。",
        "xuefeng_comment": "信息安全专业就业非常好，是国家重点发展领域！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "程序设计基础", "计算机组成原理"], "大二": ["数据结构", "操作系统", "计算机网络"], "大三": ["密码学", "网络安全基础", "网络攻防技术"], "大四": ["安全企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["武汉大学", "电子科技大学", "北京邮电大学", "四川大学"], "international": ["斯坦福大学", "麻省理工学院"]}
    },
    {
        "code": "080905",
        "name": "物联网工程",
        "category": "08 工学",
        "category_icon": "📱",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "物联网工程专业培养掌握物联网技术和应用的高级工程技术人才，能在物联网企业和IT企业从事物联网系统研发工作。",
        "what_you_learn": "物联网概论、传感器技术、嵌入式系统、通信技术、云计算、物联网应用",
        "suitable_for": "对物联网技术感兴趣的学生。",
        "career_outlook": "物联网企业、IT企业、制造业物联网部门、智慧城市相关企业等。",
        "xuefeng_comment": "物联网工程专业就业好，是国家战略重点领域！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "程序设计基础", "电路分析"], "大二": ["数据结构", "计算机网络", "传感器技术"], "大三": ["嵌入式系统", "通信技术", "云计算"], "大四": ["物联网企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["东南大学", "电子科技大学", "北京邮电大学", "华中科技大学"], "international": ["斯坦福大学"]}
    },
    {
        "code": "080906",
        "name": "数字媒体技术",
        "category": "08 工学",
        "category_icon": "🎮",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "数字媒体技术专业培养掌握数字媒体技术的高级工程技术人才，能在游戏公司、影视制作公司从事技术研发工作。",
        "what_you_learn": "数字媒体技术导论、计算机图形学、游戏开发技术、影视特效技术、虚拟现实技术、人机交互技术",
        "suitable_for": "对数字媒体技术感兴趣的学生。",
        "career_outlook": "游戏公司、影视制作公司、互联网公司、广告公司等。",
        "xuefeng_comment": "数字媒体技术专业就业非常好，游戏和影视行业发展迅猛！强烈推荐！",
        "yearly_courses": {"大一": ["高等数学", "程序设计基础", "计算机图形学"], "大二": ["数据结构", "游戏开发技术基础"], "大三": ["游戏开发技术", "影视特效技术", "虚拟现实技术"], "大四": ["游戏/影视公司实习", "毕业论文"]},
        "top_universities": {"domestic": ["浙江大学", "中国传媒大学", "北京电影学院", "电子科技大学"], "international": ["南加州大学"]}
    },
    
    # ========== 08工学 - 土木类 ==========
    {
        "code": "081002",
        "name": "建筑环境与能源应用工程",
        "category": "08 工学",
        "category_icon": "🏠",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "建筑环境与能源应用工程专业培养掌握建筑环境和能源系统设计的高级工程技术人才，能在建筑设计院和建筑企业从事暖通空调设计工作。",
        "what_you_learn": "传热传质学、建筑环境学、暖通空调设计、建筑能耗分析、燃气工程",
        "suitable_for": "对建筑环境感兴趣的学生。",
        "career_outlook": "建筑设计院、建筑企业、房地产公司、空调设备企业等。",
        "xuefeng_comment": "建筑环境与能源应用工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["传热传质学", "流体力学"], "大三": ["建筑环境学", "暖通空调设计", "建筑能耗分析"], "大四": ["设计院/企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "同济大学", "天津大学", "哈尔滨工业大学"], "international": []}
    },
    {
        "code": "081003",
        "name": "给排水科学与工程",
        "category": "08 工学",
        "category_icon": "💧",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-20k",
        "overview": "给排水科学与工程专业培养掌握给排水系统设计的高级工程技术人才，能在设计院和水务企业从事给排水工程设计和管理工作。",
        "what_you_learn": "水力学、水质工程学、给水排水管网系统、建筑给水排水工程、水处理工程",
        "suitable_for": "对给排水感兴趣的学生。",
        "career_outlook": "设计院、水务企业、建筑企业、环保企业等。",
        "xuefeng_comment": "给排水科学与工程专业就业稳定！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["水力学", "化学", "微生物学"], "大三": ["水质工程学", "给水排水管网系统", "建筑给水排水工程"], "大四": ["设计院/水务企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["同济大学", "哈尔滨工业大学", "东南大学", "重庆大学"], "international": []}
    },
    {
        "code": "081004",
        "name": "建筑电气与智能化",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "建筑电气与智能化专业培养掌握建筑电气和智能建筑系统设计的高级工程技术人才，能在设计院和建筑企业从事建筑电气设计工作。",
        "what_you_learn": "建筑电气技术、建筑智能化系统、建筑供配电、建筑自动化、智能建筑",
        "suitable_for": "对建筑电气和智能化感兴趣的学生。",
        "career_outlook": "设计院、建筑企业、房地产公司、智能化系统企业等。",
        "xuefeng_comment": "建筑电气与智能化专业就业好，智能化是趋势！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "电路分析"], "大二": ["自动控制原理", "建筑电气技术"], "大三": ["建筑智能化系统", "建筑供配电", "智能建筑"], "大四": ["设计院/企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["同济大学", "东南大学", "华南理工大学"], "international": []}
    },
    
    # ========== 08工学 - 测绘类 ==========
    {
        "code": "081203",
        "name": "导航工程",
        "category": "08 工学",
        "category_icon": "🧭",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-24k",
        "overview": "导航工程专业培养掌握导航系统和技术的高级工程技术人才，能在航空航天、测绘企业和智能交通企业从事导航系统研发工作。",
        "what_you_learn": "卫星导航原理、惯性导航原理、导航电子地图、组合导航系统、导航定位技术",
        "suitable_for": "对导航技术感兴趣的学生。",
        "career_outlook": "航空航天企业、测绘企业、智能交通企业、无人驾驶企业等。",
        "xuefeng_comment": "导航工程专业就业好，无人驾驶和智能交通发展带来大量需求！",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程力学"], "大二": ["信号与系统", "自动控制原理"], "大三": ["卫星导航原理", "惯性导航原理", "导航电子地图"], "大四": ["航空航天/测绘企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["武汉大学", "解放军信息工程大学", "北京航空航天大学"], "international": []}
    }
]

count = 0
skipped = 0

print("开始补充工学类专业...")
print("="*60)

for major in majors:
    ok, code = import_major(major)
    if ok:
        print(f"✅ {major['code']} - {major['name']}")
        count += 1
    elif code == 409:
        print(f"⏭️ {major['code']} - {major['name']} (已存在)")
        skipped += 1
    else:
        print(f"❌ {major['code']} - {major['name']}")
    time.sleep(0.3)

print("="*60)
print(f"✅ 成功添加 {count} 个专业")
print(f"⏭️ 跳过 {skipped} 个(已存在)")
