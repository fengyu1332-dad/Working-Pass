#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 最终版 - 完整专业数据 + 温暖学院风UI + 搜索功能 + 名校推荐
"""

import re
from typing import Dict, List, Any

# 高校推荐数据
UNIVERSITY_RECOMMENDATIONS = {
    "哲学": {"chinese": ["北京大学", "复旦大学", "中国人民大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
    "经济学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Harvard", "London School of Economics"]},
    "财政学": {"chinese": ["北京大学", "中国人民大学", "中央财经大学"], "foreign": ["Harvard", "LSE", "Columbia"]},
    "金融学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["Wharton", "Harvard Business School", "LSE"]},
    "法学": {"chinese": ["中国人民大学", "北京大学", "中国政法大学"], "foreign": ["Harvard Law", "Yale Law", "Oxford Law"]},
    "社会学": {"chinese": ["北京大学", "中国人民大学", "南京大学"], "foreign": ["Harvard", "Oxford", "Cambridge"]},
    "教育学": {"chinese": ["北京师范大学", "华东师范大学", "南京师范大学"], "foreign": ["Harvard GSE", "Stanford GSE", "UCL"]},
    "体育教育": {"chinese": ["北京体育大学", "上海体育学院", "华东师范大学"], "foreign": [" Loughborough", "USC", "University of Michigan"]},
    "汉语言文学": {"chinese": ["北京大学", "复旦大学", "南京大学"], "foreign": ["Harvard", "Oxford", "Yale"]},
    "英语": {"chinese": ["北京大学", "北京外国语大学", "上海外国语大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
    "新闻学": {"chinese": ["中国人民大学", "复旦大学", "中国传媒大学"], "foreign": ["Columbia Journalism", "NYU", "USC"]},
    "历史学": {"chinese": ["北京大学", "复旦大学", "南开大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
    "数学与应用数学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Princeton", "Harvard"]},
    "物理学": {"chinese": ["北京大学", "清华大学", "南京大学"], "foreign": ["MIT", "Stanford", "Princeton"]},
    "生物科学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Stanford", "Harvard"]},
    "统计学": {"chinese": ["北京大学", "中国人民大学", "复旦大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "计算机科学与技术": {"chinese": ["清华大学", "北京大学", "浙江大学"], "foreign": ["MIT", "Stanford", "CMU"]},
    "软件工程": {"chinese": ["清华大学", "浙江大学", "国防科技大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "人工智能": {"chinese": ["清华大学", "北京大学", "上海交通大学"], "foreign": ["MIT", "Stanford", "CMU"]},
    "电子信息工程": {"chinese": ["清华大学", "浙江大学", "东南大学"], "foreign": ["MIT", "Stanford", "ETH Zurich"]},
    "通信工程": {"chinese": ["北京邮电大学", "电子科技大学", "清华大学"], "foreign": ["MIT", "Stanford", "Caltech"]},
    "自动化": {"chinese": ["清华大学", "浙江大学", "东北大学"], "foreign": ["MIT", "Stanford", "Carnegie Mellon"]},
    "土木工程": {"chinese": ["同济大学", "东南大学", "清华大学"], "foreign": ["MIT", "UC Berkeley", "Imperial College"]},
    "机械设计制造及其自动化": {"chinese": ["清华大学", "上海交通大学", "浙江大学"], "foreign": ["MIT", "Stanford", "ETH Zurich"]},
    "电气工程及其自动化": {"chinese": ["清华大学", "西安交通大学", "华北电力大学"], "foreign": ["MIT", "Stanford", "Georgia Tech"]},
    "车辆工程": {"chinese": ["清华大学", "吉林大学", "同济大学"], "foreign": ["MIT", "Stanford", "University of Michigan"]},
    "建筑学": {"chinese": ["清华大学", "东南大学", "同济大学"], "foreign": ["MIT", "Harvard GSD", "Bartlett"]},
    "航空航天工程": {"chinese": ["北京航空航天大学", "西北工业大学", "哈尔滨工业大学"], "foreign": ["MIT", "Stanford", "Georgia Tech"]},
    "临床医学": {"chinese": ["北京协和医学院", "北京大学医学部", "复旦大学上海医学院"], "foreign": ["Johns Hopkins", "Harvard", "Mayo Clinic"]},
    "口腔医学": {"chinese": ["北京大学口腔医学院", "四川大学华西口腔医学院", "上海交通大学口腔医学院"], "foreign": ["Harvard Dental", "UCSF", "King's College London"]},
    "护理学": {"chinese": ["北京协和医学院", "复旦大学护理学院", "中山大学护理学院"], "foreign": ["Johns Hopkins", "University of Pennsylvania", "King's College London"]},
    "药学": {"chinese": ["北京大学药学院", "复旦大学药学院", "中国药科大学"], "foreign": ["Harvard", "MIT", "UCSF"]},
    "农学": {"chinese": ["中国农业大学", "浙江大学", "南京农业大学"], "foreign": ["Wageningen", "UC Davis", "Cornell"]},
    "园艺": {"chinese": ["浙江大学", "南京农业大学", "华中农业大学"], "foreign": ["Wageningen", "UC Davis", "Cornell"]},
    "动物医学": {"chinese": ["中国农业大学", "华中农业大学", "南京农业大学"], "foreign": ["UC Davis", "Cornell", "Royal Veterinary College"]},
    "园林": {"chinese": ["北京林业大学", "同济大学", "南京林业大学"], "foreign": ["Harvard GSD", "University of Sheffield", "UC Berkeley"]},
    "林学": {"chinese": ["北京林业大学", "东北林业大学", "南京林业大学"], "foreign": ["Yale School of the Environment", "UC Berkeley", "University of Michigan"]},
    "会计学": {"chinese": ["厦门大学", "中国人民大学", "上海财经大学"], "foreign": ["Wharton", "Chicago Booth", "LSE"]},
    "工商管理": {"chinese": ["清华大学", "北京大学", "复旦大学"], "foreign": ["Harvard Business School", "Wharton", "INSEAD"]},
    "市场营销": {"chinese": ["北京大学", "中国人民大学", "复旦大学"], "foreign": ["Harvard Business School", "Wharton", "Kellogg"]},
    "电子商务": {"chinese": ["北京大学", "浙江大学", "对外经济贸易大学"], "foreign": ["MIT", "Stanford", "University of Pennsylvania"]},
    "物流管理": {"chinese": ["北京交通大学", "同济大学", "上海海事大学"], "foreign": ["MIT", "Stanford", "Michigan State"]},
    "视觉传达设计": {"chinese": ["中央美术学院", "清华大学美术学院", "中国美术学院"], "foreign": ["Royal College of Art", "Parsons", "RISD"]},
    "数字媒体艺术": {"chinese": ["中国传媒大学", "北京电影学院", "浙江大学"], "foreign": ["NYU Tisch", "USC", "CalArts"]},
    "音乐表演": {"chinese": ["中央音乐学院", "上海音乐学院", "中国音乐学院"], "foreign": ["Juilliard", "Berklee", "Royal Academy of Music"]},
    "播音与主持艺术": {"chinese": ["中国传媒大学", "中央戏剧学院", "上海戏剧学院"], "foreign": ["NYU Tisch", "Columbia", "Royal Academy of Dramatic Art"]},
    "动画": {"chinese": ["北京电影学院", "中国传媒大学", "四川美术学院"], "foreign": ["CalArts", "Gobelins", "USC"]},
    "政治学与行政学": {"chinese": ["北京大学", "中国人民大学", "复旦大学"], "foreign": ["Harvard", "Oxford", "Princeton"]},
    "国际经济与贸易": {"chinese": ["对外经济贸易大学", "北京大学", "复旦大学"], "foreign": ["LSE", "Wharton", "Harvard"]},
    "金融工程": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Princeton", "Baruch"]},
    "数据科学与大数据技术": {"chinese": ["北京大学", "清华大学", "浙江大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "网络工程": {"chinese": ["电子科技大学", "北京邮电大学", "西安电子科技大学"], "foreign": ["MIT", "Stanford", "Georgia Tech"]},
    "物联网工程": {"chinese": ["东南大学", "电子科技大学", "北京邮电大学"], "foreign": ["MIT", "Stanford", "Georgia Tech"]},
    "信息安全": {"chinese": ["电子科技大学", "武汉大学", "北京邮电大学"], "foreign": ["MIT", "Stanford", "Carnegie Mellon"]},
    "化学": {"chinese": ["北京大学", "清华大学", "南京大学"], "foreign": ["MIT", "Harvard", "UC Berkeley"]},
    "应用化学": {"chinese": ["北京大学", "复旦大学", "南开大学"], "foreign": ["MIT", "Harvard", "Stanford"]},
    "材料科学与工程": {"chinese": ["清华大学", "北京航空航天大学", "上海交通大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "生物医学工程": {"chinese": ["东南大学", "清华大学", "上海交通大学"], "foreign": ["MIT", "Johns Hopkins", "Georgia Tech"]},
    "环境工程": {"chinese": ["清华大学", "同济大学", "北京大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "食品科学与工程": {"chinese": ["江南大学", "中国农业大学", "华南理工大学"], "foreign": ["MIT", "Cornell", "UC Davis"]},
    "交通运输": {"chinese": ["北京交通大学", "同济大学", "东南大学"], "foreign": ["MIT", "Stanford", "University of Michigan"]},
    "工程管理": {"chinese": ["清华大学", "同济大学", "天津大学"], "foreign": ["MIT", "Stanford", "Imperial College"]},
    "光电信息科学与工程": {"chinese": ["华中科技大学", "天津大学", "浙江大学"], "foreign": ["MIT", "Stanford", "Caltech"]},
    "仪器科学与技术": {"chinese": ["北京航空航天大学", "清华大学", "天津大学"], "foreign": ["MIT", "Stanford", "Georgia Tech"]},
    "城乡规划": {"chinese": ["清华大学", "同济大学", "东南大学"], "foreign": ["MIT", "Harvard GSD", "UCL"]},
    "风景园林": {"chinese": ["北京林业大学", "同济大学", "华南理工大学"], "foreign": ["Harvard GSD", "University of Sheffield", "UC Berkeley"]},
    "人力资源管理": {"chinese": ["中国人民大学", "北京大学", "南京大学"], "foreign": ["Harvard", "Wharton", "London Business School"]},
    "财务管理": {"chinese": ["厦门大学", "中国人民大学", "上海财经大学"], "foreign": ["Wharton", "Chicago Booth", "LSE"]},
    "行政管理": {"chinese": ["北京大学", "中国人民大学", "复旦大学"], "foreign": ["Harvard", "Oxford", "Princeton"]},
    "环境科学": {"chinese": ["北京大学", "南京大学", "浙江大学"], "foreign": ["MIT", "Stanford", "Yale"]},
}

def get_default_recommendations(name):
    """根据专业名称获取默认高校推荐"""
    if "医学" in name:
        return {"chinese": ["北京协和医学院", "北京大学医学部", "复旦大学上海医学院"], "foreign": ["Harvard", "Johns Hopkins", "Mayo Clinic"]}
    elif "工程" in name or "技术" in name or "机械" in name or "电气" in name:
        return {"chinese": ["清华大学", "上海交通大学", "浙江大学"], "foreign": ["MIT", "Stanford", "ETH Zurich"]}
    elif "经济" in name or "金融" in name:
        return {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["Harvard", "MIT", "LSE"]}
    elif "管理" in name:
        return {"chinese": ["清华大学", "北京大学", "中国人民大学"], "foreign": ["Harvard", "Wharton", "INSEAD"]}
    elif "设计" in name or "艺术" in name or "美术" in name:
        return {"chinese": ["中央美术学院", "清华大学美术学院", "中国美术学院"], "foreign": ["Parsons", "RCA", "RISD"]}
    elif "文学" in name or "语言" in name:
        return {"chinese": ["北京大学", "复旦大学", "南京大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]}
    elif "法律" in name or "法学" in name:
        return {"chinese": ["中国人民大学", "北京大学", "中国政法大学"], "foreign": ["Harvard Law", "Yale Law", "Oxford"]}
    elif "教育" in name:
        return {"chinese": ["北京师范大学", "华东师范大学", "南京师范大学"], "foreign": ["Harvard GSE", "Stanford GSE", "UCL"]}
    elif "物理" in name:
        return {"chinese": ["北京大学", "清华大学", "南京大学"], "foreign": ["MIT", "Stanford", "Princeton"]}
    elif "数学" in name:
        return {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Princeton", "Harvard"]}
    elif "生物" in name:
        return {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Harvard", "Stanford"]}
    elif "化学" in name:
        return {"chinese": ["北京大学", "清华大学", "南京大学"], "foreign": ["MIT", "Harvard", "UC Berkeley"]}
    elif "农学" in name or "园艺" in name or "林学" in name:
        return {"chinese": ["中国农业大学", "浙江大学", "南京农业大学"], "foreign": ["Wageningen", "UC Davis", "Cornell"]}
    elif "计算机" in name or "软件" in name or "人工智能" in name:
        return {"chinese": ["清华大学", "北京大学", "浙江大学"], "foreign": ["MIT", "Stanford", "CMU"]}
    elif "建筑" in name:
        return {"chinese": ["清华大学", "东南大学", "同济大学"], "foreign": ["MIT", "Harvard GSD", "Bartlett"]}
    elif "土木" in name:
        return {"chinese": ["同济大学", "东南大学", "清华大学"], "foreign": ["MIT", "UC Berkeley", "Imperial"]}
    elif "医学" in name:
        return {"chinese": ["北京协和医学院", "北京大学医学部", "复旦大学上海医学院"], "foreign": ["Johns Hopkins", "Harvard", "Mayo Clinic"]}
    elif "护理" in name:
        return {"chinese": ["北京协和医学院", "复旦大学护理学院", "中山大学护理学院"], "foreign": ["Johns Hopkins", "UPenn", "Kings College"]}
    else:
        return {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["Harvard", "MIT", "Oxford"]}


# 从 v2 版本提取的专业数据
MAJORS_DATA = [
    # 01 哲学类
    {
        "code": "010101",
        "name": "哲学",
        "category": "01 哲学",
        "category_icon": "🎓",
        "difficulty": 4,
        "popularity": 2,
        "salary": {"description": "起薪约5000-8000元，学术路线前期收入较低", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率中等，对口就业率较低", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "哲学专业学习如何思考、推理和论证", "year1": "中国哲学史、西方哲学史、逻辑学入门", "year2": "马克思主义哲学、伦理学、美学", "year3": "宗教学、科学技术哲学、专业原著选读", "year4": "毕业论文写作、哲学专题研讨"},
        "suitable_for": {"traits": ["喜欢深度思考", "对人生意义感兴趣", "耐得住寂寞"], "skills": ["阅读理解能力（大量原著）", "写作表达能力", "逻辑推理能力"], "warning": "需要长期积累，短期难以见成效"},
        "prospects": {"trend": "就业面较窄但稳定，哲学思维在管理咨询、公共政策等领域受重视", "hot": "公务员、编辑、教师", "developing": "智库研究员、文化产业"},
        "career_advice": {"immediate": "尽早确定方向：学术/教育/其他", "certifications": "教师资格证（想当老师必考）", "timeline": "大三开始准备考研或考公"},
        "learning_path": {"freshman": "读经典原著：论语、道德经、柏拉图对话录", "sophomore": "建立知识框架，写读书笔记", "junior": "参加读书会，尝试写学术论文", "senior": "确定方向：考研/考公/就业"},
        "zhang_reviews": {"pros": ["培养批判性思维：哲学训练逻辑推理能力，让人看问题更深刻", "考公优势明显：行测逻辑题和申论写作有天然优势", "能看透事物本质：哲学训练抽象思维能力", "学术地位独特：哲学家在学术界有崇高地位", "跨领域适应性强：思维方式迁移到各行各业"], "cons": ["对口工作稀少：纯哲学对口岗位非常有限", "起薪普遍较低：学术路线前期收入不高", "必须持续深造：本科就业竞争力弱，硕博是常态", "社会认可度有限：家长和雇主可能不理解哲学价值", "见效慢周期长：思维能力的提升需要长期积累"], "summary": "哲学专业适合真正热爱思考、对人生意义有追问的人。如果你想赚快钱、追求短期回报，哲学不适合你；但如果你愿意用四年时间培养批判性思维和深度思考能力，哲学是很好的通识教育。关键是要主动把哲学思维应用到实际问题上，而不是死读书。选学校时优先考虑综合性大学，师范类大学的哲学系往往偏教育方向。"}
    },
    
    # 02 经济学类
    {
        "code": "020101",
        "name": "经济学",
        "category": "02 经济学",
        "category_icon": "📊",
        "difficulty": 5,
        "popularity": 5,
        "salary": {"description": "起薪约6000-15000元，取决于院校和城市", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，对口率高", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "研究资源配置、经济发展和市场运行规律", "year1": "微积分、线性代数、政治经济学、微观经济学", "year2": "宏观经济学、统计学、概率论、计量经济学基础", "year3": "国际金融、货币银行学、财政学、计量经济学应用", "year4": "毕业论文、专业方向选修（如发展经济学、环境经济学）"},
        "suitable_for": {"traits": ["数学基础好", "对经济现象感兴趣", "逻辑思维强"], "skills": ["数学（微积分、概率统计必须精通）", "数据分析能力", "英语（看英文文献）"], "warning": "数学不好慎选，计量经济学需要较强数学基础"},
        "prospects": {"trend": "2024年经济形势复杂，但经济专业人才需求稳定", "hot": "银行、证券、咨询公司、四大", "developing": "数据分析、量化投资、公共政策"},
        "career_advice": {"immediate": "必须掌握Python或Stata进行数据分析", "certifications": "CFA（美国特许金融分析师）、CPA", "timeline": "大三暑假前拿到实习，大四准备秋招"},
        "learning_path": {"freshman": "学好数学和英语，了解经济学基本框架", "sophomore": "开始学计量经济学和数据分析工具", "junior": "参加数学建模竞赛，找第一份实习", "senior": "秋招/考研，简历突出实习和项目经验"},
        "zhang_reviews": {"pros": ["就业面极广：银行、证券、基金、咨询、四大都可以去", "金融行业认可度高：经济金融知识是入行必备", "培养商业思维：理解市场运行规律和经济现象", "考研/出国有优势：经济学是商科申请的基础学科", "考公热门专业：经济学考公岗位多，选择余地大"], "cons": ["数学要求极高：微积分、概率论、计量经济学都是难关", "竞争极其激烈：好岗位往往需要985/211背景", "顶尖岗位门槛高：投行、券商核心岗位需要研究生学历", "证书要求高：CFA、CPA等证书是加分项或必选项", "学习内容宽泛：什么都学但什么都不精"], "summary": "经济学是万金油专业，就业面广但竞争激烈。数学好是必要条件，数学不好的人学起来会很痛苦。选校很重要，985/211的经济学毕业生才有竞争力，普通院校的经济学就业一般。想进金融核心岗位的同学，必须提前规划：刷GPA、考证书、找实习、准备考研/出国，四手都要抓。建议大二就开始准备CFA一级。"}
    },
    
    {
        "code": "020201",
        "name": "财政学",
        "category": "02 经济学",
        "category_icon": "💰",
        "difficulty": 4,
        "popularity": 4,
        "salary": {"description": "体制内就业为主，起薪约5000-10000元", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，体制内比例高", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习政府理财、公共支出和税收的理论与实践", "year1": "政治经济学、财政学基础、税收概论", "year2": "中国税制、预算管理、政府会计", "year3": "国有资产管理、地方政府财政、国际税收", "year4": "毕业论文、专业实习"},
        "suitable_for": {"traits": ["有家国情怀", "愿意服务公共事务", "文字功底好"], "skills": ["财务分析能力", "政策理解能力", "公文写作能力"], "warning": "如果只想赚钱不建议选这条路"},
        "prospects": {"trend": "财政专业人才稳定需求，公务员考试有优势", "hot": "税务局、财政局、审计局、政府部门", "developing": "PPP项目、财政绩效评价"},
        "career_advice": {"immediate": "关注公务员考试，提早准备行测申论", "certifications": "税务师、会计师", "timeline": "大三开始备考公务员"},
        "learning_path": {"freshman": "了解财政体制，看政府工作报告", "sophomore": "学税收实务，关注财政政策", "junior": "找财税类实习，备考税务师", "senior": "国考/省考，简历突出财务分析能力"},
        "zhang_reviews": {"pros": ["考公优势极其明显：财政学毕业生是税务局、财政局的最爱", "工作稳定体面：体制内工作稳定，社会地位高", "专业壁垒强：财税知识有专业门槛，不是谁都能做", "福利待遇好：五险一金、年终奖、带薪休假齐全", "越老越值钱：财税经验随着年龄增长价值增加"], "cons": ["薪资天花板较低：体制内薪资增长缓慢，发不了大财", "晋升周期漫长：论资排辈现象存在，晋升需要时间", "工作内容重复：日常事务性工作多，缺乏创造性", "考试竞争激烈：国考省考竞争比例常常上百比一", "地域限制明显：好岗位集中在地市级以上城市"], "summary": "财政学是考公最热门的专业之一，非常适合追求稳定生活的人。毕业后进税务局、财政局、审计局是主要出路，体制内福利好、稳定体面，但薪资增长有限。如果你想快速致富，财政学不适合你；但如果你追求稳定、愿意从基层做起，财政学是个好选择。建议大三开始全力备考公务员，同时准备税务师考试增加竞争力。"}
    },
    
    # 03 法学类
    {
        "code": "030101",
        "name": "法学",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": 5,
        "popularity": 5,
        "salary": {"description": "前期收入低（3000-6000元），后期差距大", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率较高，但对口率低（法考是门槛）", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习法律知识和法律思维", "year1": "法理学、宪法学、中国法制史、民法总论", "year2": "物权法、合同法、侵权责任法、民事诉讼法", "year3": "刑法、刑事诉讼法、行政法与行政诉讼法", "year4": "商法、经济法、知识产权法、国际法、毕业论文"},
        "suitable_for": {"traits": ["记忆力好（背法条）", "逻辑思维强（分析案情）", "文字表达好（写诉状）"], "skills": ["记忆力（大量法条需要记忆）", "逻辑推理能力", "表达能力"], "warning": "法考通过率仅12%，没通过的很难从事法律工作"},
        "prospects": {"trend": "2024年法律行业竞争激烈，红圈所门槛极高", "hot": "律所、法院、检察院、企业法务", "developing": "合规业务、涉外法律、数据合规"},
        "career_advice": {"immediate": "大学期间必须过法考，否则就业困难", "certifications": "法律职业资格证（必考）、律师执业证", "timeline": "大四第一学期考法考，考研/就业同步准备"},
        "learning_path": {"freshman": "培养法律思维，读《西窗法雨》等入门书", "sophomore": "开始系统学习民法刑法，练习案例分析", "junior": "准备法考（至少复习6个月），找律所实习", "senior": "过法考！过法考！过法考！"},
        "zhang_reviews": {"pros": ["社会地位极高：律师、法官、检察官都是受人尊敬的职业", "越老越吃香：法律经验随时间积累，50岁正是黄金期", "能帮人解决实际问题：法律工作有强烈的社会价值", "收入上限极高：顶尖律师年薪百万不是梦", "职业发展清晰：律师→高级律师→合伙人路径明确"], "cons": ["法考难度地狱级：通过率仅12%，没通过约等于失业", "前期收入极低：律所实习期工资可能只有3000元", "工作强度极大：加班写诉状、查案例是常态", "竞争极其激烈：红圈所门槛高，需要名校+法考+实习", "培养周期长：本科+司考+律所培养期+可能的考研"], "summary": "法学是典型的\"先苦后甜\"专业。毕业前必须通过法考，这是硬门槛，否则很难从事法律工作。前期收入低、工作强度大是常态，但熬过前几年后，职业发展会越来越顺。建议在校期间就去律所实习，积累经验比什么都重要。法考复习至少需要6个月全职备考，不要掉以轻心。选校时优先五院四系，普通院校法学就业较难。"}
    },
    
    # 04 教育学类
    {
        "code": "040101",
        "name": "教育学",
        "category": "04 教育学",
        "category_icon": "📚",
        "difficulty": 3,
        "popularity": 4,
        "salary": {"description": "教师编制内稳定，薪资与地区职称挂钩", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，教师岗位需求稳定", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习教育理论和教育实践", "year1": "教育学概论、教育心理学、教育史", "year2": "课程与教学论、教育研究方法、教育评价", "year3": "教育管理学、教育政策学、比较教育", "year4": "教育实习、毕业论文"},
        "suitable_for": {"traits": ["有爱心", "善于表达", "耐心"], "skills": ["表达能力", "组织协调能力", "抗压能力"], "warning": "想当老师必须考教师资格证和编制"},
        "prospects": {"trend": "2024年教师编制竞争激烈，好学校门槛高", "hot": "中小学教师、教育培训机构、教育管理", "developing": "在线教育、教育科技、教育咨询"},
        "career_advice": {"immediate": "必须考教师资格证，大三开始准备考编", "certifications": "教师资格证（必考）、普通话证书", "timeline": "大三上学期拿教资，大三下开始备考编制"},
        "learning_path": {"freshman": "考普通话证书，了解教育行业", "sophomore": "参加教学实践，试讲练习", "junior": "考教资，准备教师编制考试", "senior": "参加教师招聘考试"},
        "zhang_reviews": {"pros": ["稳定体面：教师是受人尊敬的职业，社会地位高", "带薪寒暑假：每年三个月假期是其他行业羡慕不来的", "工作稳定：教师编制稳定，不受经济周期影响", "人际关系简单：学校环境相对单纯，勾心斗角少", "利于家庭：有利于子女教育，有充足时间陪伴家人"], "cons": ["薪资增长缓慢：体制内薪资与职称挂钩，增长有限", "编制竞争激烈：好的中小学编制竞争非常激烈", "教学压力大：升学率、考核、评职称压力并存", "家长沟通难：部分家长不理解教育，投诉多", "职业倦怠感强：重复性工作容易产生厌倦情绪"], "summary": "教育学是追求稳定生活的人的好选择，尤其是女生。教师工作稳定、假期充足、社会地位高，但薪资增长有限，而且编制竞争越来越激烈。想当老师的同学，建议直接报师范类院校的师范专业，而不是教育学专业。教育学偏理论，想当老师最好读学科教学类专业。另外，教师资格证是入门必备，越早考越好。"}
    },
    
    # 05 文学类
    {
        "code": "050101",
        "name": "汉语言文学",
        "category": "05 文学",
        "category_icon": "📖",
        "difficulty": 3,
        "popularity": 5,
        "salary": {"description": "起薪约5000-9000元，稳定型收入", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，体制内岗位多", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习汉语语言知识和文学鉴赏创作能力", "year1": "现代汉语、古代汉语、文学概论、中国现代文学", "year2": "中国古代文学、外国文学、写作学", "year3": "文学批评、语言学概论、比较文学", "year4": "毕业论文、选修方向深化"},
        "suitable_for": {"traits": ["热爱阅读", "文字敏感", "善于表达"], "skills": ["写作能力（各种文体）", "阅读理解能力", "文字功底"], "warning": "纯文学创作需要天赋，不是每个人都适合"},
        "prospects": {"trend": "考公考编热门专业，新媒体行业需求增加", "hot": "语文老师、编辑、记者、公务员", "developing": "新媒体运营、内容编辑、文案策划"},
        "career_advice": {"immediate": "多练写作，建立作品集", "certifications": "教师资格证（想当老师）、出版专业资格证", "timeline": "大三确定方向，准备考公或考编"},
        "learning_path": {"freshman": "大量阅读经典文学作品，开始写读书笔记", "sophomore": "练习各种文体写作，尝试投稿", "junior": "确定方向（教育/出版/新媒体），针对性准备", "senior": "积累作品集，准备秋招"},
        "zhang_reviews": {"pros": ["考公考编优势大：中文专业是考公最热门的专业之一", "文字能力出众：写作、编辑、文案能力是核心竞争力", "文化底蕴深厚：对中国传统文化有系统了解", "教师需求稳定：语文老师是刚需，需求量大", "新媒体有优势：内容创作时代需要文字功底深厚的人"], "cons": ["薪资天花板有限：纯文字工作起薪不高", "纯文字工作竞争激烈：作家、编辑岗位竞争很激烈", "需要持续积累：文字能力需要长期练习才能提升", "创造性要求高：想脱颖而出需要真正的写作才华", "部分岗位被AI冲击：基础文案工作可能被AI替代"], "summary": "汉语言文学是考公考编的热门专业，就业稳定但不意味着高收入。如果你热爱文学、喜欢写作，这个专业可以让你如鱼得水；如果只是冲着考公去，可能会学得很痛苦。建议大学期间多写东西，建立自己的作品集，这对就业非常重要。另外，新媒体时代，内容创作者稀缺，有文字功底的人可以考虑往内容运营方向发展。"}
    },
    
    {
        "code": "050201",
        "name": "英语",
        "category": "05 文学",
        "category_icon": "🌍",
        "difficulty": 4,
        "popularity": 5,
        "salary": {"description": "差距极大，翻译和教育类5000-20000元不等", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，但竞争激烈", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习英语语言技能和文化知识", "year1": "综合英语、听力、口语、语音", "year2": "阅读、写作、翻译入门、语言学概论", "year3": "高级翻译、英美文学、商务英语/旅游英语", "year4": "毕业论文、专业实习"},
        "suitable_for": {"traits": ["对语言有天赋", "刻苦努力", "敢于开口"], "skills": ["听说读写译（全方位）", "跨文化交际能力", "学习能力"], "warning": "必须过专八，否则没有竞争力"},
        "prospects": {"trend": "AI翻译冲击基础翻译岗位，高端翻译仍有需求", "hot": "英语老师、翻译、外贸、涉外工作", "developing": "跨境电商、国际旅游、语言培训"},
        "career_advice": {"immediate": "必须过专八，最好有CATTI证书", "certifications": "专八（必须）、CATTI、雅思7.0+", "timeline": "大二下学期开始准备专八"},
        "learning_path": {"freshman": "打好基础，每天练习听说读写", "sophomore": "过四六级专四，找外教聊天", "junior": "准备专八，考CATTI三级", "senior": "确定方向，积累专业领域英语"},
        "zhang_reviews": {"pros": ["国际视野开阔：学习英语让你了解西方文化和社会", "留学申请有优势：英语专业是留学的天然优势专业", "就业面广：翻译、外贸、教育、涉外工作都能做", "跨境电商机会多：跨境电商需要大量英语人才", "思维更开放：掌握英语让你接触更多一手信息"], "cons": ["AI翻译冲击大：基础翻译工作正在被AI替代", "竞争极其激烈：英语专业毕业生太多，同质化严重", "必须持续学习：英语退步很快，需要每天坚持", "专八必须过：专八不过，基本没有竞争力", "纯英语工作薪资不高：基础翻译、老师薪资有限"], "summary": "英语是工具，不是专业。英语专业最大的问题是：学生四年学的是语言本身，而不是用英语做某个具体领域的工作。建议英语专业学生尽早确定方向：翻译、教育、跨境电商、国际贸易等，并学习相应技能。专八必须过，否则没有竞争力。另外，口语一定要练好，这是英语专业学生的核心竞争力。不要把时间花在研究语法上，语言是用来交流的。"}
    },
    
    {
        "code": "050303",
        "name": "新闻学",
        "category": "05 文学",
        "category_icon": "📰",
        "difficulty": 3,
        "popularity": 4,
        "salary": {"description": "传统媒体低（约5000-8000元），新媒体高", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，但行业变革快", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习新闻采写编评和传播技能", "year1": "新闻学概论、传播学概论、采访写作", "year2": "新闻编辑、新闻摄影、电视摄像", "year3": "深度报道、新闻评论、新媒体运营", "year4": "毕业实习、毕业论文"},
        "suitable_for": {"traits": ["好奇心强", "善于交际", "反应快"], "skills": ["写作能力", "人际沟通能力", "抗压能力"], "warning": "媒体工作强度大，加班是常态"},
        "prospects": {"trend": "传统媒体衰落，新媒体和短视频崛起", "hot": "新媒体运营、记者、编辑、内容创作", "developing": "短视频制作、直播运营、品牌公关"},
        "career_advice": {"immediate": "运营自己的自媒体账号，建立作品集", "certifications": "记者证（想当记者必考）", "timeline": "大三开始实习积累作品"},
        "learning_path": {"freshman": "关注新闻热点，开始写稿投稿", "sophomore": "学新媒体技能，做自己的账号", "junior": "找媒体实习，积累作品", "senior": "确定方向，准备秋招"},
        "zhang_reviews": {"pros": ["接触社会各层面：记者可以接触各行各业的人", "成长速度快：新闻工作锻炼快速学习和表达能力", "有社会价值：舆论监督、揭露真相、帮助弱势群体", "文字能力提升：新闻写作训练让人快速成长", "人脉资源广：记者能积累大量人脉资源"], "cons": ["工作强度大：截稿压力、突发事件是常态", "薪资不稳定：传统媒体薪资偏低，新媒体好一些", "行业变革剧烈：传统媒体衰落，新媒体崛起", "职业风险增加：舆论环境复杂，新闻报道有风险", "晋升通道有限：传统媒体晋升慢，新媒体不稳定"], "summary": "新闻学适合有新闻理想、想从事媒体工作的人。传统媒体（报纸、电视）衰落明显，薪资偏低；新媒体、短视频是新的发展方向。建议在校期间就运营自己的自媒体账号，积累作品和粉丝。新闻学对写作能力要求很高，需要多练习。另外，记者证是进入正规媒体的敲门砖，越早考越好。没有作品集寸步难行，建议大二就开始积累作品。"}
    },
    
    # 07 理学类
    {
        "code": "070101",
        "name": "数学与应用数学",
        "category": "07 理学",
        "category_icon": "🔢",
        "difficulty": 5,
        "popularity": 4,
        "salary": {"description": "起薪约6000-20000元，取决于行业", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，跨行业能力强", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习数学理论、应用数学和计算方法", "year1": "数学分析、高等代数、解析几何", "year2": "常微分方程、概率论、数理统计", "year3": "实变函数、泛函分析、数值分析", "year4": "毕业论文、专业方向选修"},
        "suitable_for": {"traits": ["数学天赋", "逻辑思维强", "耐得住寂寞"], "skills": ["数学分析能力", "抽象思维能力", "编程能力（Python/MATLAB）"], "warning": "数学难，必须是真的喜欢，否则坚持不下去"},
        "prospects": {"trend": "数据科学AI火热，数学人才需求大增", "hot": "数据分析、算法工程师、金融量化", "developing": "人工智能、密码学、生物统计"},
        "career_advice": {"immediate": "学Python和机器学习，数学+编程是王炸组合", "certifications": "教师资格证（想当老师）、计算机等级证书", "timeline": "大二确定方向，开始针对性学习"},
        "learning_path": {"freshman": "学好数分高代，打好基础", "sophomore": "学编程，开始接触机器学习", "junior": "参加数学建模竞赛，找实习", "senior": "确定方向：读研/就业"},
        "zhang_reviews": {"pros": ["基础学科，跨专业容易：数学是AI、金融、统计的基础", "薪资潜力大：算法工程师、数据科学岗位薪资极高", "培养逻辑思维：数学训练让人思维严密", "考研有优势：数学专业考研上岸率高", "公考有优势：行测数量关系题对数学专业是送分题"], "cons": ["课程难度极大：数学分析、高等代数让很多人挂科", "必须持续深造：本科数学就业竞争力一般", "需要真正热爱：不喜欢数学的人学起来很痛苦", "与高中数学不同：大学数学更抽象，很多人不适应", "编程能力要自己培养：纯数学不教编程"], "summary": "数学专业是万金油专业，可以转向金融、计算机、统计等方向。但前提是你真的喜欢数学，能够承受高难度的课程。如果数学是你的短板，这个专业会让你痛苦四年。建议数学专业的同学大二就开始学Python和机器学习，这是增加就业竞争力的关键。数学+编程是王炸组合，在AI时代非常吃香。"}
    },
    
    {
        "code": "070201",
        "name": "物理学",
        "category": "07 理学",
        "category_icon": "⚛️",
        "difficulty": 5,
        "popularity": 3,
        "salary": {"description": "基础学科收入一般，但跨行能力强", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率较高，但大部分需要读研读博", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习物质运动规律和基本结构", "year1": "力学、热学、电磁学，光学", "year2": "理论力学、量子力学、电动力学、热力学与统计物理", "year3": "固体物理、计算物理、实验物理", "year4": "毕业论文、毕业设计"},
        "suitable_for": {"traits": ["好奇心强", "逻辑思维强", "动手能力好"], "skills": ["数学物理方法", "实验技能", "编程能力"], "warning": "纯物理路线需要读博才能有成就"},
        "prospects": {"trend": "半导体、新能源等产业带动物理人才需求", "hot": "半导体、光电、新能源、科研", "developing": "量子计算、光电子、新材料"},
        "career_advice": {"immediate": "尽早确定方向：学术/工业界", "certifications": "教师资格证（想当老师）", "timeline": "大二开始进实验室"},
        "learning_path": {"freshman": "学好四大力学基础，数学要扎实", "sophomore": "进实验室参与科研，学编程", "junior": "参加科研项目，发论文", "senior": "确定方向：读研/就业"},
        "zhang_reviews": {"pros": ["培养科学思维：物理学训练严谨的科学方法论", "跨行业能力强：物理背景在很多行业都受欢迎", "社会尊重度高：科学家在社会上有崇高地位", "半导体/光电行业需求大：芯片产业带动物理人才需求", "培养解决问题的能力：物理思维让人善于分析复杂问题"], "cons": ["学习难度极大：四大力学让很多人望而却步", "学术路线周期长：想有成就必须读博，时间成本高", "就业面相对窄：主要方向是科研和教育", "薪资起步偏低：基础研究岗位起薪不高", "需要扎实的数学基础：数学不好的学起来很吃力"], "summary": "物理学是基础学科中的基础学科，适合真正热爱物理、想搞科研的人。纯物理路线必须读博，而且学术圈竞争激烈。如果想本科就业，物理专业比较吃亏，需要及早转向半导体、光电、新能源等应用方向。物理专业最大的价值是培养解决问题的能力，这个能力在各行各业都受用。建议大二就确定方向：学术路线要进实验室发论文，工业界路线要学编程和行业知识。"}
    },
    
    {
        "code": "071001",
        "name": "生物科学",
        "category": "07 理学",
        "category_icon": "🧬",
        "difficulty": 4,
        "popularity": 3,
        "salary": {"description": "起薪约5000-10000元，需读研才有好发展", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率一般，科研路线需要高学历", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习生命科学的基础理论和实验技术", "year1": "普通生物学、生物化学、细胞生物学", "year2": "遗传学、微生物学、分子生物学", "year3": "植物学、动物学、生理学", "year4": "毕业论文、毕业实习"},
        "suitable_for": {"traits": ["热爱生命科学", "动手能力强", "有耐心"], "skills": ["实验操作能力", "观察能力", "数据分析能力"], "warning": "生物行业就业竞争激烈，必须读研"},
        "prospects": {"trend": "生物医药行业发展，生物专业就业有所改善", "hot": "生物医药、医疗器械、环保", "developing": "基因编辑、生物信息、合成生物学"},
        "career_advice": {"immediate": "必须读研究生，最好读博", "certifications": "教师资格证（想当老师）", "timeline": "大三开始准备考研"},
        "learning_path": {"freshman": "基础课程学好，进实验室参观", "sophomore": "进实验室参与科研项目", "junior": "参加科研竞赛，发论文", "senior": "准备考研/出国"},
        "zhang_reviews": {"pros": ["生物医药前景好：生物医药是国家战略新兴产业", "培养科研能力：实验室训练为科研打基础", "跨领域机会多：生物+AI、生物+医学是热点", "社会价值大：生物研究可以改善人类健康", "考研出国容易：生物专业出国读研相对容易"], "cons": ["必须读研读博：本科就业很难找到对口工作", "就业竞争激烈：生物毕业生太多，岗位有限", "薪资起步偏低：生物行业起薪不高", "科研周期长：出成果需要很长时间", "实验重复性高：很多实验是重复性的工作"], "summary": "生物科学是典型的\"高风险高回报\"专业。本科就业很难，必须读研读博。生物医药行业正在快速发展，基因编辑、细胞治疗等新领域给生物专业带来了新希望。如果你真的热爱生物科学，愿意长期投入，生物专业可以有很好的发展；如果只是想找个好工作，生物专业可能让你失望。建议在校期间进实验室参与科研，发论文对考研出国很重要。"}
    },
]


def add_university_recommendations():
    """为所有专业补充高校推荐信息"""
    for major in MAJORS_DATA:
        name = major['name']
        if name in UNIVERSITY_RECOMMENDATIONS:
            rec = UNIVERSITY_RECOMMENDATIONS[name]
        else:
            rec = get_default_recommendations(name)
        
        major['chinese_top_universities'] = rec['chinese']
        major['foreign_top_universities'] = rec['foreign']


def generate_major_card(major: Dict[str, Any]) -> str:
    code = major['code']
    name = major['name']
    category = major['category']
    icon = major['category_icon']
    difficulty = '★' * major['difficulty'] + '☆' * (5 - major['difficulty'])
    
    salary_desc = major['salary']['description']
    salary_source = major['salary']['source']
    employment_desc = major['employment_rate']['description']
    
    what_learn = major['what_you_learn']
    suitable = major['suitable_for']
    prospects = major['prospects']
    career = major['career_advice']
    learning = major['learning_path']
    reviews = major['zhang_reviews']
    chinese_unis = major.get('chinese_top_universities', [])
    foreign_unis = major.get('foreign_top_universities', [])
    
    skills_html = ''.join([f'<span class="skill-tag">{s}</span>' for s in suitable.get('skills', [])])
    pros_list = ''.join([f'<li>{p}</li>' for p in reviews.get('pros', [])])
    cons_list = ''.join([f'<li>{c}</li>' for c in reviews.get('cons', [])])
    chinese_unis_html = ''.join([f'<span class="uni-tag chinese">{u}</span>' for u in chinese_unis])
    foreign_unis_html = ''.join([f'<span class="uni-tag foreign">{u}</span>' for u in foreign_unis])
    
    return f'''
        <div class="major-card" id="card-{code}" data-category="{category}" data-name="{name}" onclick="toggleCard('{code}')">
            <div class="card-header">
                <span class="category-icon">{icon}</span>
                <div>
                    <div class="major-name">{name}</div>
                    <div class="major-code">{code}</div>
                    <div class="difficulty-stars">难度：{difficulty}</div>
                </div>
            </div>
            
            <div class="salary-tag">💰 {salary_desc}</div>
            <span class="data-source-tag">{salary_source}</span>
            
            <p class="employment-desc">就业形势：{employment_desc}</p>
            
            <div class="detail-section hidden">
                <div class="detail-title">📖 学什么</div>
                <div class="detail-content">{what_learn.get('summary', '')}</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{what_learn.get('year1', '')}</li>
                    <li><strong>大二：</strong>{what_learn.get('year2', '')}</li>
                    <li><strong>大三：</strong>{what_learn.get('year3', '')}</li>
                    <li><strong>大四：</strong>{what_learn.get('year4', '')}</li>
                </ul>
                
                <div class="detail-title">👤 适合人群</div>
                <div class="detail-content"><strong>特质：</strong>{'、'.join(suitable.get('traits', []))}</div>
                <div class="detail-content"><strong>技能要求：</strong></div>
                <div class="skill-tags">{skills_html}</div>
                <div class="detail-content warning">⚠️ {suitable.get('warning', '')}</div>
                
                <div class="detail-title">📈 前景展望</div>
                <div class="detail-content"><strong>趋势：</strong>{prospects.get('trend', '')}</div>
                <div class="detail-content"><strong>热门去向：</strong>{prospects.get('hot', '')}</div>
                <div class="detail-content"><strong>新兴方向：</strong>{prospects.get('developing', '')}</div>
                
                <div class="detail-title">💼 就业建议</div>
                <div class="detail-content"><strong>立即行动：</strong>{career.get('immediate', '')}</div>
                <div class="detail-content"><strong>证书建议：</strong>{career.get('certifications', '')}</div>
                <div class="detail-content"><strong>时间线：</strong>{career.get('timeline', '')}</div>
                
                <div class="detail-title">🛤️ 学习路径</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{learning.get('freshman', '')}</li>
                    <li><strong>大二：</strong>{learning.get('sophomore', '')}</li>
                    <li><strong>大三：</strong>{learning.get('junior', '')}</li>
                    <li><strong>大四：</strong>{learning.get('senior', '')}</li>
                </ul>
                
                <div class="detail-title">🎓 名校推荐</div>
                <div class="uni-section">
                    <strong class="uni-label">🇨🇳 国内TOP3：</strong>
                    <div class="uni-tags">{chinese_unis_html}</div>
                </div>
                <div class="uni-section">
                    <strong class="uni-label">🌍 国外TOP3：</strong>
                    <div class="uni-tags">{foreign_unis_html}</div>
                </div>
                
                <div class="detail-title">⭐ 雪峰点评</div>
                <div class="pros-cons">
                    <div class="pros-box">
                        <strong class="pros-title">✅ 优势分析：</strong>
                        <ul class="pros-cons-list">{pros_list}</ul>
                    </div>
                    <div class="cons-box">
                        <strong class="cons-title">❌ 劣势分析：</strong>
                        <ul class="pros-cons-list">{cons_list}</ul>
                    </div>
                </div>
                <div class="summary-box">
                    💬 总结：{reviews.get('summary', '')}
                </div>
            </div>
        </div>
    '''


def generate_filter_buttons(majors: List[Dict[str, Any]]) -> str:
    categories = sorted(set([m['category'] for m in majors]))
    return '\n'.join([
        f'<button class="filter-btn" data-filter="{cat}">{next((m["category_icon"] for m in majors if m["category"] == cat), "📚")} {cat}</button>'
        for cat in categories
    ])


CSS = """
:root {
    --surface: #FFF8F5;
    --surface-dim: #E9D6CC;
    --surface-container: #FFFFFF;
    --surface-container-low: #FFF1EA;
    --primary: #E67E22;
    --primary-container: #FAD7B2;
    --on-primary: #FFFFFF;
    --secondary: #705A49;
    --secondary-container: #EBE0D6;
    --on-surface: #2C2621;
    --on-surface-variant: #8B7E74;
    --outline: #DED0C6;
    --shadow: rgba(112, 90, 73, 0.05);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--surface);
    min-height: 100vh;
    color: var(--on-surface);
    line-height: 1.8;
}

.container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }

header {
    text-align: center;
    padding: 48px 40px;
    background: var(--surface-container);
    border-radius: 24px;
    margin-bottom: 40px;
    box-shadow: 0 4px 24px var(--shadow);
}

header h1 {
    font-family: "Literata", serif;
    font-size: 40px;
    font-weight: 700;
    color: var(--secondary);
    margin-bottom: 16px;
}

header p { font-size: 16px; color: var(--on-surface-variant); max-width: 800px; margin: 0 auto; }

.stats-banner { display: flex; justify-content: center; gap: 64px; margin: 40px 0 24px; flex-wrap: wrap; }
.stat-item { text-align: center; }
.stat-number { font-family: "Literata", serif; font-size: 40px; font-weight: 700; color: var(--primary); line-height: 1.2; }
.stat-label { color: var(--on-surface-variant); font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }

.search-section {
    background: var(--surface-container);
    padding: 24px 32px;
    border-radius: 20px;
    margin-bottom: 24px;
    box-shadow: 0 4px 24px var(--shadow);
}

.search-box { display: flex; gap: 12px; align-items: center; }
.search-input {
    flex: 1;
    padding: 14px 20px;
    border: 2px solid var(--outline);
    border-radius: 16px;
    font-size: 16px;
    font-family: inherit;
    outline: none;
    transition: all 0.3s;
    background: var(--surface-container-low);
}
.search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.1); }
.search-icon { font-size: 24px; color: var(--secondary); }

.filter-section {
    background: var(--surface-container);
    padding: 28px 32px;
    border-radius: 20px;
    margin-bottom: 32px;
    box-shadow: 0 4px 24px var(--shadow);
}

.filter-title { font-family: "Literata", serif; font-size: 20px; font-weight: 600; margin-bottom: 16px; color: var(--secondary); }
.filter-buttons { display: flex; flex-wrap: wrap; gap: 10px; }

.filter-btn {
    padding: 10px 20px;
    border: 2px solid var(--outline);
    border-radius: 9999px;
    background: transparent;
    color: var(--secondary);
    cursor: pointer;
    transition: all 0.3s;
    font-size: 14px;
    font-weight: 500;
}
.filter-btn:hover { background: var(--secondary-container); transform: translateY(-2px); }
.filter-btn.active { background: var(--primary); color: var(--on-primary); border-color: var(--primary); }

.majors-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }

.major-card {
    background: var(--surface-container);
    border-radius: 20px;
    padding: 28px;
    transition: all 0.3s;
    cursor: pointer;
    border: 2px solid var(--outline);
    box-shadow: 0 4px 24px var(--shadow);
}
.major-card:hover { transform: translateY(-4px); box-shadow: 0 8px 40px var(--shadow); border-color: var(--primary); }

.card-header { display: flex; align-items: center; gap: 16px; margin-bottom: 18px; }
.category-icon {
    font-size: 32px;
    background: var(--primary-container);
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
}
.major-name { font-family: "Literata", serif; font-size: 24px; font-weight: 600; color: var(--secondary); }
.major-code { font-size: 12px; color: var(--on-surface-variant); font-weight: 500; margin-top: 4px; }
.difficulty-stars { margin-top: 8px; color: var(--primary); font-size: 14px; }

.salary-tag { display: inline-block; background: var(--primary-container); color: var(--secondary); padding: 6px 16px; border-radius: 9999px; font-size: 13px; font-weight: 500; margin: 12px 0; }
.data-source-tag { display: inline-block; background: var(--secondary-container); color: var(--secondary); padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 500; margin-left: 10px; }
.employment-desc { margin-top: 10px; font-size: 0.9em; color: var(--on-surface-variant); }

.detail-section { margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--outline); }
.detail-title { font-family: "Literata", serif; font-size: 18px; font-weight: 600; color: var(--secondary); margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.detail-content { font-size: 15px; color: var(--on-surface); margin-bottom: 10px; }

.year-list { list-style: none; padding-left: 0; }
.year-list li { margin: 8px 0; position: relative; padding-left: 24px; font-size: 14px; color: var(--on-surface-variant); }
.year-list li::before { content: "•"; position: absolute; left: 0; color: var(--primary); font-weight: bold; font-size: 18px; }

.pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }
.pros-box, .cons-box { padding: 16px; border-radius: 16px; font-size: 14px; }
.pros-box { background: #e8f5e9; border-left: 4px solid #43a047; }
.cons-box { background: #ffebee; border-left: 4px solid #e53935; }
.pros-title { color: #2e7d32; }
.cons-title { color: #c62828; }
.pros-cons-list { padding-left: 20px; margin-top: 8px; }

.summary-box { background: var(--secondary-container); padding: 20px; border-radius: 16px; margin-top: 20px; font-style: normal; color: var(--on-surface); font-size: 14px; line-height: 1.8; }

.skill-tags, .uni-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.skill-tag, .uni-tag { padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 500; }
.skill-tag { background: var(--secondary-container); color: var(--secondary); }
.uni-tag.chinese { background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }
.uni-tag.foreign { background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }
.uni-section { margin-bottom: 12px; }
.uni-label { color: var(--secondary); }
.warning { color: #c05621 !important; }

.hidden { display: none; }

footer { text-align: center; padding: 48px 20px; color: var(--on-surface-variant); font-size: 14px; margin-top: 48px; border-top: 1px solid var(--outline); }

@media (max-width: 768px) {
    .majors-grid { grid-template-columns: 1fr; }
    header { padding: 32px 24px; }
    header h1 { font-size: 28px; }
    .stats-banner { gap: 40px; }
    .container { padding: 20px; }
    .pros-cons { grid-template-columns: 1fr; }
}
"""


JAVASCRIPT = """
let expandedCards = new Set();

function toggleCard(code) {
    const card = document.getElementById('card-' + code);
    if (expandedCards.has(code)) {
        expandedCards.delete(code);
        card.classList.remove('expanded');
        const detail = card.querySelector('.detail-section');
        if (detail) detail.classList.add('hidden');
    } else {
        expandedCards.add(code);
        card.classList.add('expanded');
        const detail = card.querySelector('.detail-section');
        if (detail) detail.classList.remove('hidden');
    }
}

function filterMajors(category) {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === category) {
            btn.classList.add('active');
        }
    });
    
    document.querySelectorAll('.major-card').forEach(card => {
        const cardCategory = card.dataset.category;
        if (category === 'all' || cardCategory === category) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

function searchMajors(query) {
    const searchTerm = query.toLowerCase().trim();
    document.querySelectorAll('.major-card').forEach(card => {
        const name = card.dataset.name.toLowerCase();
        const category = card.dataset.category.toLowerCase();
        if (name.includes(searchTerm) || category.includes(searchTerm)) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.getElementById('searchInput').value = '';
        filterMajors(btn.dataset.filter);
    });
});

document.getElementById('searchInput').addEventListener('input', (e) => {
    searchMajors(e.target.value);
});
"""


def generate_html() -> str:
    total = len(MAJORS_DATA)
    categories = len(set([m['category'] for m in MAJORS_DATA]))
    filter_buttons = generate_filter_buttons(MAJORS_DATA)
    major_cards = ''.join([generate_major_card(m) for m in MAJORS_DATA])
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>专业星图 - 温暖、专业的大学专业选择指南</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>专业星图</h1>
            <p>温暖、专业的大学专业选择指南 · 帮助你找到最适合的专业<br>
            <span style="font-size:0.85em;">⚠️ 本网站数据均为参考，建议结合自身情况选择</span></p>
            
            <div class="stats-banner">
                <div class="stat-item">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">专业收录</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{categories}</div>
                    <div class="stat-label">学科门类</div>
                </div>
            </div>
        </header>
        
        <section class="search-section">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" id="searchInput" placeholder="搜索专业名称、学科门类...">
            </div>
        </section>
        
        <section class="filter-section">
            <div class="filter-title">📚 按学科筛选</div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">📖 全部专业</button>
                {filter_buttons}
            </div>
        </section>
        
        <div class="majors-grid" id="majorsGrid">
            {major_cards}
        </div>
        
        <footer>
            <p>专业星图 · 温暖的专业指南</p>
            <p style="margin-top:8px;font-size:13px;">数据仅供参考 · 请结合自身情况选择</p>
        </footer>
    </div>
    
    <script>{JAVASCRIPT}</script>
</body>
</html>'''


def main():
    add_university_recommendations()
    html = generate_html()
    
    output_path = '/workspace/major_starmap_final.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 专业星图 最终版 生成完成！")
    print(f"📊 共生成 {len(MAJORS_DATA)} 个专业")
    print(f"🎓 每个专业都包含国内外TOP3名校推荐")
    print(f"🔍 新增搜索功能，快速找到目标专业")
    print(f"🎨 温暖学院风UI，更好的视觉体验")
    print(f"📁 输出文件：{output_path}")


if __name__ == '__main__':
    main()
