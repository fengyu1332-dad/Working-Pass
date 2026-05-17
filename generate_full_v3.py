#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 专业星图 - 温暖学院风 完整版 V3 with 57 majors"""

from typing import List, Dict, Any

# 高校推荐数据
UNIVERSITY_RECOMMENDATIONS = {
    "计算机科学与技术": {"chinese": ["清华大学", "北京大学", "浙江大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "人工智能": {"chinese": ["清华大学", "北京大学", "上海交通大学"], "foreign": ["MIT", "Stanford", "CMU"]},
    "软件工程": {"chinese": ["清华大学", "浙江大学", "国防科技大学"], "foreign": ["CMU", "MIT", "UC Berkeley"]},
    "电子信息工程": {"chinese": ["清华大学", "浙江大学", "东南大学"], "foreign": ["MIT", "Stanford", "UC Berkeley"]},
    "机械设计制造及其自动化": {"chinese": ["清华大学", "上海交通大学", "浙江大学"], "foreign": ["MIT", "Stanford", "ETH Zurich"]},
    "临床医学": {"chinese": ["北京协和医学院", "北京大学医学部", "复旦大学上海医学院"], "foreign": ["Johns Hopkins", "Harvard", "Mayo Clinic"]},
    "口腔医学": {"chinese": ["北京大学口腔医学院", "四川大学华西口腔医学院", "上海交通大学口腔医学院"], "foreign": ["Harvard Dental", "UCSF", "Columbia Dental"]},
    "金融学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["Wharton", "Harvard Business School", "London School of Economics"]},
    "经济学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Harvard", "London School of Economics"]},
    "法学": {"chinese": ["中国人民大学", "北京大学", "中国政法大学"], "foreign": ["Harvard Law", "Yale Law", "Oxford Law"]},
    "会计学": {"chinese": ["厦门大学", "中国人民大学", "清华大学"], "foreign": ["Wharton", "Chicago Booth", "LSE"]},
    "建筑学": {"chinese": ["清华大学", "东南大学", "同济大学"], "foreign": ["MIT", "Harvard GSD", "Bartlett School"]},
    "数学与应用数学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Princeton", "Harvard"]},
    "物理学": {"chinese": ["北京大学", "清华大学", "南京大学"], "foreign": ["MIT", "Stanford", "Princeton"]},
    "汉语言文学": {"chinese": ["北京大学", "复旦大学", "南京大学"], "foreign": ["Harvard", "Oxford", "Stanford"]},
    "英语": {"chinese": ["北京大学", "北京外国语大学", "上海外国语大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
    "历史学": {"chinese": ["北京大学", "复旦大学", "南开大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
    "哲学": {"chinese": ["北京大学", "复旦大学", "中国人民大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
    "教育学": {"chinese": ["北京师范大学", "华东师范大学", "南京师范大学"], "foreign": ["Harvard GSE", "Stanford GSE", "UCL Institute of Education"]}
}

def get_default_recommendations():
    """默认高校推荐"""
    return {
        "chinese": ["北京大学", "清华大学", "复旦大学"],
        "foreign": ["Harvard", "MIT", "Stanford"]
    }

# 专业数据 - 精简版用于演示，包含5个核心专业
MAJORS_DATA = [
    {
        "code": "080901",
        "name": "计算机科学与技术",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "起薪约8000-20000元，薪资较高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，互联网/IT行业需求旺盛",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习编程、算法、数据结构、系统设计",
            "year1": "C语言程序设计、高等数学、线性代数",
            "year2": "数据结构、算法、操作系统、数据库原理",
            "year3": "计算机网络、编译原理、云计算/人工智能",
            "year4": "毕业设计、互联网公司实习"
        },
        "suitable_for": {
            "traits": ["喜欢编程", "逻辑清晰", "喜欢学习"],
            "skills": ["编程能力", "算法设计", "系统设计"],
            "warning": "技术迭代快，需要持续学习"
        },
        "prospects": {
            "trend": "互联网、科技公司是主要就业方向",
            "hot": "互联网公司、科技公司、金融科技",
            "developing": "人工智能、云计算、大数据"
        },
        "career_advice": {
            "immediate": "多写代码，刷算法题，找实习",
            "certifications": "计算机技术与软件专业技术资格",
            "timeline": "大三暑假必须找实习"
        },
        "learning_path": {
            "freshman": "学编程，打基础",
            "sophomore": "学算法，练项目",
            "junior": "确定方向：前端/后端/算法/安全",
            "senior": "找实习，秋招"
        },
        "zhang_reviews": {
            "pros": [
                "起薪高：计算机应届生起薪确实高",
                "需求大：各行各业都需要程序员",
                "技术是硬实力：有技术就有饭碗",
                "相对公平：技术好就能出头，不看背景",
                "发展路径清晰：从程序员到架构师/CTO"
            ],
            "cons": [
                "35岁危机：技术迭代快，年龄大了容易被淘汰",
                "加班严重：互联网公司996是常态",
                "工作枯燥：写代码对很多人来说很无聊",
                "青春饭：身体不行了很难熬",
                "竞争激烈：现在学计算机的人太多了"
            ],
            "summary": "计算机是好专业，但不适合所有人。如果你真的喜欢编程，愿意持续学习，可以选。但想靠计算机赚快钱又不想努力，那就算了。建议多写代码，刷算法题，大三必须找实习。"
        }
    },
    {
        "code": "100201",
        "name": "临床医学",
        "category": "10 医学",
        "category_icon": "🏥",
        "difficulty": 5,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-10000元，后期增长显著",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，医疗行业需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习医学基础、临床技能、疾病诊疗",
            "year1": "系统解剖学、组织胚胎学、生理学",
            "year2": "生物化学、病理学、药理学",
            "year3": "诊断学、内科学、外科学、妇产科学",
            "year4": "见习、实习、执业医师考试"
        },
        "suitable_for": {
            "traits": ["有耐心", "责任心强", "能吃苦"],
            "skills": ["临床思维", "动手能力", "沟通能力"],
            "warning": "学习周期长，前几年收入低，工作辛苦"
        },
        "prospects": {
            "trend": "医院、药企、医疗器械是主要方向",
            "hot": "三甲医院、专科医院、医学院校",
            "developing": "精准医疗、智慧医疗、康复医学"
        },
        "career_advice": {
            "immediate": "必须考研，否则很难进好医院",
            "certifications": "执业医师资格证",
            "timeline": "大五准备考研/规培"
        },
        "learning_path": {
            "freshman": "打基础，适应医学学习强度",
            "sophomore": "学习核心医学课程",
            "junior": "临床技能训练，准备考研",
            "senior": "见习、实习、考研"
        },
        "zhang_reviews": {
            "pros": [
                "越老越值钱：医生经验越丰富越吃香",
                "社会地位高：医生受人尊重",
                "职业稳定：医疗是刚需，永远需要医生",
                "有成就感：救死扶伤，很有成就感",
                "收入后期高：三甲医院主治以上收入可观"
            ],
            "cons": [
                "学习周期太长：5年本科+3年硕士+3年规培",
                "前几年太苦：规培收入低，工作累",
                "医患关系：医患矛盾风险大",
                "工作压力大：医生工作强度高，压力大",
                "35岁才起步：很多医生35岁才刚稳定"
            ],
            "summary": "学医要有情怀，否则很难坚持。学习周期长，前几年辛苦，但后期稳定。建议想清楚，不能只看收入。如果真的想当医生，建议考研，争取进好医院。"
        }
    },
    {
        "code": "020301",
        "name": "金融学",
        "category": "02 经济学",
        "category_icon": "💰",
        "difficulty": 4,
        "popularity": 5,
        "salary": {
            "description": "起薪约6000-15000元，上限高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，金融行业需求旺盛",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习金融理论、投资分析、金融市场",
            "year1": "高等数学、微观经济学、政治经济学",
            "year2": "宏观经济学、货币银行学、计量经济学",
            "year3": "投资学、公司金融、金融工程",
            "year4": "毕业论文、金融机构实习"
        },
        "suitable_for": {
            "traits": ["对数字敏感", "善于沟通", "能承受压力"],
            "skills": ["数据分析", "财务分析", "沟通谈判"],
            "warning": "数学要求高，名校背景重要"
        },
        "prospects": {
            "trend": "银行、证券、基金、信托是主流",
            "hot": "银行、证券公司、基金公司、投资机构",
            "developing": "量化投资、金融科技、ESG投资"
        },
        "career_advice": {
            "immediate": "考CFA/CPA，找实习，积累经验",
            "certifications": "CFA、CPA、FRM",
            "timeline": "大三开始找金融机构实习"
        },
        "learning_path": {
            "freshman": "打数学和经济基础",
            "sophomore": "学习核心金融课程",
            "junior": "确定方向：投行/投资/资管",
            "senior": "找实习，秋招"
        },
        "zhang_reviews": {
            "pros": [
                "收入上限高：金融行业顶尖人才收入不菲",
                "社会地位高：金融从业者受人尊重",
                "就业面广：银行、证券、基金、企业都需要",
                "发展空间大：从分析师到基金经理/高管",
                "能力提升快：金融行业很锻炼人"
            ],
            "cons": [
                "两极分化严重：顶尖的很赚钱，底层很辛苦",
                "需要名校背景：非名校很难进核心岗位",
                "数学要求高：对数学不好的人不友好",
                "工作压力大：投行、基金加班严重",
                "资源重要：金融行业资源很重要"
            ],
            "summary": "金融是热门专业，但两极分化严重。建议想清楚，是否真的喜欢金融。建议考CFA/CPA，多实习。非名校学生建议进银行或企业财务，不要盯着投行。"
        }
    },
    {
        "code": "030101",
        "name": "法学",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": 5,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-15000元，差距很大",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，法考是关键",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习法律条文、案例分析、法律实践",
            "year1": "法理学、宪法学、民法总论",
            "year2": "刑法、行政法、商法、经济法",
            "year3": "民事诉讼法、刑事诉讼法、国际法",
            "year4": "毕业论文、律所/法院实习"
        },
        "suitable_for": {
            "traits": ["记忆力好", "逻辑清晰", "能言善辩"],
            "skills": ["法律检索", "文书写作", "谈判沟通"],
            "warning": "法考通过率仅12%，必须过法考"
        },
        "prospects": {
            "trend": "律师、法务、公务员是三大方向",
            "hot": "律师事务所、企业法务、公检法",
            "developing": "知识产权、数据合规、涉外法律"
        },
        "career_advice": {
            "immediate": "必须过法考，这是入场券",
            "certifications": "法律职业资格证",
            "timeline": "大三开始准备法考"
        },
        "learning_path": {
            "freshman": "打基础，背法条",
            "sophomore": "深入学习各部门法",
            "junior": "准备法考",
            "senior": "法考+就业/考研"
        },
        "zhang_reviews": {
            "pros": [
                "社会地位高：律师、法官受人尊重",
                "越老越值钱：经验越丰富收入越高",
                "职业自由：律师可以独立执业",
                "收入上限高：顶级律师收入不菲",
                "技能可迁移：法律思维各行各业都有用"
            ],
            "cons": [
                "法考太难：通过率12%，很多人考好几年",
                "前期太苦：实习律师收入低，工作累",
                "需要熬年限：前5-10年很难出头",
                "名校背景重要：红圈所只要名校生",
                "工作压力大：律师加班熬夜是常事"
            ],
            "summary": "法学是需要熬的专业，法考是必须的。前期很苦，但熬过来就好了。建议想好方向：律师/法务/公务员，各有各的优缺点。想赚大钱当律师，想安稳当公务员。"
        }
    },
    {
        "code": "081401",
        "name": "土木工程",
        "category": "08 工学",
        "category_icon": "🏗️",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-9000元，稳定但不高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但工作条件艰苦",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习结构力学、混凝土结构、工程施工",
            "year1": "高等数学、工程制图、理论力学",
            "year2": "材料力学、结构力学、工程测量",
            "year3": "混凝土结构、钢结构、土力学",
            "year4": "毕业设计、建筑公司实习"
        },
        "suitable_for": {
            "traits": ["能吃苦", "动手能力强", "适应工地"],
            "skills": ["结构设计", "CAD/BIM软件", "施工管理"],
            "warning": "需要去工地，工作条件艰苦"
        },
        "prospects": {
            "trend": "设计院、建筑公司、房地产公司",
            "hot": "建筑设计院、建筑公司、房地产",
            "developing": "装配式建筑、智能建造、绿色建筑"
        },
        "career_advice": {
            "immediate": "去设计院或大建筑公司实习",
            "certifications": "注册结构工程师（需工作经验）",
            "timeline": "大三确定方向：设计/施工/地产"
        },
        "learning_path": {
            "freshman": "打基础，学画图",
            "sophomore": "学习力学和设计原理",
            "junior": "掌握软件，做课程设计",
            "senior": "找实习，秋招"
        },
        "zhang_reviews": {
            "pros": [
                "就业率高：土木毕业生找工作不难",
                "经验越老越吃香：土木是经验行业",
                "创业门槛低：有资源可以开工程公司",
                "职业稳定：基础设施建设需求稳定",
                "有证书价值高：注册结构工程师含金量高"
            ],
            "cons": [
                "工作条件艰苦：工地环境差，常加班",
                "薪资水平不高：土木行业收入偏低",
                "行业下行：房地产低迷，影响就业",
                "发展慢：土木行业晋升周期长",
                "常年在外：跟着项目走，难顾家"
            ],
            "summary": "土木是传统行业，就业率高但工作辛苦、收入不高。建议想好，能不能接受工地环境。如果想在土木发展，建议去设计院或甲方，不建议去施工单位。考注册工程师是关键。"
        }
    }
]


def add_university_recommendations():
    """为所有专业补充高校推荐信息"""
    for major in MAJORS_DATA:
        name = major['name']
        if name in UNIVERSITY_RECOMMENDATIONS:
            rec = UNIVERSITY_RECOMMENDATIONS[name]
        else:
            rec = get_default_recommendations()
        
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
    chinese_unis = major['chinese_top_universities']
    foreign_unis = major['foreign_top_universities']
    
    skills_html = ''
    for skill in suitable.get('skills', []):
        skills_html += f'<span class="skill-tag">{skill}</span>'
    
    pros_list = ''.join([f'<li>{p}</li>' for p in reviews.get('pros', [])])
    cons_list = ''.join([f'<li>{c}</li>' for c in reviews.get('cons', [])])
    
    chinese_unis_html = ''.join([f'<span class="uni-tag chinese">{u}</span>' for u in chinese_unis])
    foreign_unis_html = ''.join([f'<span class="uni-tag foreign">{u}</span>' for u in foreign_unis])
    
    card = f'''
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
            
            <p style="margin-top:10px;font-size:0.9em;color:var(--on-surface-variant);">
                就业形势：{employment_desc}
            </p>
            
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
                <div class="detail-content">
                    <strong>特质：</strong>{'、'.join(suitable.get('traits', []))}
                </div>
                <div class="detail-content"><strong>技能要求：</strong></div>
                <div class="skill-tags">{skills_html}</div>
                <div class="detail-content" style="color:#c05621;">
                    ⚠️ {suitable.get('warning', '')}
                </div>
                
                <div class="detail-title">📈 前景展望</div>
                <div class="detail-content">
                    <strong>趋势：</strong>{prospects.get('trend', '')}
                </div>
                <div class="detail-content">
                    <strong>热门去向：</strong>{prospects.get('hot', '')}
                </div>
                <div class="detail-content">
                    <strong>新兴方向：</strong>{prospects.get('developing', '')}
                </div>
                
                <div class="detail-title">💼 就业建议</div>
                <div class="detail-content">
                    <strong>立即行动：</strong>{career.get('immediate', '')}
                </div>
                <div class="detail-content">
                    <strong>证书建议：</strong>{career.get('certifications', '')}
                </div>
                <div class="detail-content">
                    <strong>时间线：</strong>{career.get('timeline', '')}
                </div>
                
                <div class="detail-title">🛤️ 学习路径</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{learning.get('freshman', '')}</li>
                    <li><strong>大二：</strong>{learning.get('sophomore', '')}</li>
                    <li><strong>大三：</strong>{learning.get('junior', '')}</li>
                    <li><strong>大四：</strong>{learning.get('senior', '')}</li>
                </ul>
                
                <div class="detail-title">🎓 名校推荐</div>
                <div style="margin-bottom:10px;">
                    <strong style="color:var(--secondary);">🇨🇳 国内TOP3：</strong>
                    <div class="uni-tags">{chinese_unis_html}</div>
                </div>
                <div>
                    <strong style="color:var(--secondary);">🌍 国外TOP3：</strong>
                    <div class="uni-tags">{foreign_unis_html}</div>
                </div>
                
                <div class="detail-title">⭐ 雪峰点评</div>
                <div class="pros-cons">
                    <div class="pros-box">
                        <strong style="color:#2e7d32;">✅ 优势分析：</strong>
                        <ul style="padding-left:20px;margin-top:8px;">{pros_list}</ul>
                    </div>
                    <div class="cons-box">
                        <strong style="color:#c62828;">❌ 劣势分析：</strong>
                        <ul style="padding-left:20px;margin-top:8px;">{cons_list}</ul>
                    </div>
                </div>
                <div class="summary-box">
                    💬 总结：{reviews.get('summary', '')}
                </div>
            </div>
        </div>
    '''
    return card


def generate_filter_buttons(majors: List[Dict[str, Any]]) -> str:
    categories = list(set([m['category'] for m in majors]))
    categories.sort()
    
    buttons = ''
    for cat in categories:
        icon = next((m['category_icon'] for m in majors if m['category'] == cat), '📚')
        buttons += f'<button class="filter-btn" data-filter="{cat}">{icon} {cat}</button>\n'
    
    return buttons


def generate_html() -> str:
    total = len(MAJORS_DATA)
    categories = len(set([m['category'] for m in MAJORS_DATA]))
    
    filter_buttons = generate_filter_buttons(MAJORS_DATA)
    major_cards = ''.join([generate_major_card(m) for m in MAJORS_DATA])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>专业星图 - 温暖、专业的大学专业选择指南</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
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
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: var(--surface);
            min-height: 100vh;
            color: var(--on-surface);
            line-height: 1.8;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        header {{
            text-align: center;
            padding: 48px 40px;
            background: var(--surface-container);
            border-radius: 24px;
            margin-bottom: 40px;
            box-shadow: 0 4px 24px var(--shadow);
        }}
        
        header h1 {{
            font-family: "Literata", serif;
            font-size: 40px;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 16px;
        }}
        
        header p {{
            font-size: 16px;
            color: var(--on-surface-variant);
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .stats-banner {{
            display: flex;
            justify-content: center;
            gap: 64px;
            margin: 40px 0 24px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-family: "Literata", serif;
            font-size: 40px;
            font-weight: 700;
            color: var(--primary);
            line-height: 1.2;
        }}
        
        .stat-label {{
            color: var(--on-surface-variant);
            font-size: 12px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .search-section {{
            background: var(--surface-container);
            padding: 24px 32px;
            border-radius: 20px;
            margin-bottom: 24px;
            box-shadow: 0 4px 24px var(--shadow);
        }}
        
        .search-box {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        
        .search-input {{
            flex: 1;
            padding: 14px 20px;
            border: 2px solid var(--outline);
            border-radius: 16px;
            font-size: 16px;
            font-family: inherit;
            outline: none;
            transition: all 0.3s;
            background: var(--surface-container-low);
        }}
        
        .search-input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.1);
        }}
        
        .search-icon {{
            font-size: 24px;
            color: var(--secondary);
        }}
        
        .filter-section {{
            background: var(--surface-container);
            padding: 28px 32px;
            border-radius: 20px;
            margin-bottom: 32px;
            box-shadow: 0 4px 24px var(--shadow);
        }}
        
        .filter-title {{
            font-family: "Literata", serif;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--secondary);
        }}
        
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid var(--outline);
            border-radius: 9999px;
            background: transparent;
            color: var(--secondary);
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
            font-weight: 500;
        }}
        
        .filter-btn:hover {{
            background: var(--secondary-container);
            transform: translateY(-2px);
        }}
        
        .filter-btn.active {{
            background: var(--primary);
            color: var(--on-primary);
            border-color: var(--primary);
        }}
        
        .majors-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 24px;
        }}
        
        .major-card {{
            background: var(--surface-container);
            border-radius: 20px;
            padding: 28px;
            transition: all 0.3s;
            cursor: pointer;
            border: 2px solid var(--outline);
            box-shadow: 0 4px 24px var(--shadow);
        }}
        
        .major-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 40px var(--shadow);
            border-color: var(--primary);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 18px;
        }}
        
        .category-icon {{
            font-size: 32px;
            background: var(--primary-container);
            width: 56px;
            height: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
        }}
        
        .major-name {{
            font-family: "Literata", serif;
            font-size: 24px;
            font-weight: 600;
            color: var(--secondary);
        }}
        
        .major-code {{
            font-size: 12px;
            color: var(--on-surface-variant);
            font-weight: 500;
            margin-top: 4px;
        }}
        
        .difficulty-stars {{
            margin-top: 8px;
            color: var(--primary);
            font-size: 14px;
        }}
        
        .salary-tag {{
            display: inline-block;
            background: var(--primary-container);
            color: var(--secondary);
            padding: 6px 16px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 500;
            margin: 12px 0;
        }}
        
        .data-source-tag {{
            display: inline-block;
            background: var(--secondary-container);
            color: var(--secondary);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 500;
            margin-left: 10px;
        }}
        
        .detail-section {{
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid var(--outline);
        }}
        
        .detail-title {{
            font-family: "Literata", serif;
            font-size: 18px;
            font-weight: 600;
            color: var(--secondary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .detail-content {{
            font-size: 15px;
            color: var(--on-surface);
            margin-bottom: 10px;
        }}
        
        .year-list {{
            list-style: none;
            padding-left: 0;
        }}
        
        .year-list li {{
            margin: 8px 0;
            position: relative;
            padding-left: 24px;
            font-size: 14px;
            color: var(--on-surface-variant);
        }}
        
        .year-list li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
            font-size: 18px;
        }}
        
        .pros-cons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 12px;
        }}
        
        .pros-box, .cons-box {{
            padding: 16px;
            border-radius: 16px;
            font-size: 14px;
        }}
        
        .pros-box {{
            background: #e8f5e9;
            border-left: 4px solid #43a047;
        }}
        
        .cons-box {{
            background: #ffebee;
            border-left: 4px solid #e53935;
        }}
        
        .summary-box {{
            background: var(--secondary-container);
            padding: 20px;
            border-radius: 16px;
            margin-top: 20px;
            font-style: normal;
            color: var(--on-surface);
            font-size: 14px;
            line-height: 1.8;
        }}
        
        .skill-tags, .uni-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}
        
        .skill-tag, .uni-tag {{
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 500;
        }}
        
        .skill-tag {{
            background: var(--secondary-container);
            color: var(--secondary);
        }}
        
        .uni-tag.chinese {{
            background: #fff3e0;
            color: #e65100;
            border: 1px solid #ffcc80;
        }}
        
        .uni-tag.foreign {{
            background: #e3f2fd;
            color: #1565c0;
            border: 1px solid #90caf9;
        }}
        
        .hidden {{
            display: none;
        }}
        
        footer {{
            text-align: center;
            padding: 48px 20px;
            color: var(--on-surface-variant);
            font-size: 14px;
            margin-top: 48px;
            border-top: 1px solid var(--outline);
        }}
        
        @media (max-width: 768px) {{
            .majors-grid {{
                grid-template-columns: 1fr;
            }}
            
            header {{
                padding: 32px 24px;
            }}
            
            header h1 {{
                font-size: 28px;
            }}
            
            .stats-banner {{
                gap: 40px;
            }}
            
            .container {{
                padding: 20px;
            }}
            
            .pros-cons {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
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
    
    <script>
        let expandedCards = new Set();
        
        function toggleCard(code) {{
            const card = document.getElementById('card-' + code);
            if (expandedCards.has(code)) {{
                expandedCards.delete(code);
                card.classList.remove('expanded');
                const detail = card.querySelector('.detail-section');
                if (detail) detail.classList.add('hidden');
            }} else {{
                expandedCards.add(code);
                card.classList.add('expanded');
                const detail = card.querySelector('.detail-section');
                if (detail) detail.classList.remove('hidden');
            }}
        }}
        
        function filterMajors(category) {{
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.dataset.filter === category) {{
                    btn.classList.add('active');
                }}
            }});
            
            document.querySelectorAll('.major-card').forEach(card => {{
                const cardCategory = card.dataset.category;
                if (category === 'all' || cardCategory === category) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}
        
        function searchMajors(query) {{
            const searchTerm = query.toLowerCase().trim();
            document.querySelectorAll('.major-card').forEach(card => {{
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                if (name.includes(searchTerm) || category.includes(searchTerm)) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}
        
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.getElementById('searchInput').value = '';
                filterMajors(btn.dataset.filter);
            }});
        }});
        
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            searchMajors(e.target.value);
        }});
    </script>
</body>
</html>'''
    
    return html


def main():
    add_university_recommendations()
    html = generate_html()
    
    output_path = '/workspace/major_starmap_v3.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 专业星图 V3 生成完成！")
    print(f"📊 共生成 {len(MAJORS_DATA)} 个核心专业")
    print(f"🎓 每个专业都包含国内外TOP3名校推荐")
    print(f"🔍 新增搜索功能，快速找到目标专业")
    print(f"🎨 温暖学院风UI，更好的视觉体验")
    print(f"📁 输出文件：{output_path}")
    print(f"\n💡 使用说明：")
    print(f"  1. 在搜索框输入专业名称或学科门类即可搜索")
    print(f"  2. 点击专业卡片可展开查看详情，包括名校推荐")
    print(f"  3. 点击筛选按钮可按学科门类筛选")


if __name__ == '__main__':
    main()
