#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 最终版 - 完整专业数据 + 新UI + 星座背景
"""

from typing import List, Dict, Any

# 专业数据（包含57个专业）
MAJORS_DATA = [
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
        "zhang_reviews": {"pros": ["培养批判性思维", "考公优势明显", "能看透事物本质", "学术地位独特", "跨领域适应性强"], "cons": ["对口工作稀少", "起薪普遍较低", "必须持续深造", "社会认可度有限", "见效慢周期长"], "summary": "哲学专业适合真正热爱思考的人。"}
    },
    {
        "code": "020101",
        "name": "经济学",
        "category": "02 经济学",
        "category_icon": "📊",
        "difficulty": 5,
        "popularity": 5,
        "salary": {"description": "起薪约6000-15000元，取决于院校和城市", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，对口率高", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "研究资源配置、经济发展和市场运行规律", "year1": "微积分、线性代数、政治经济学、微观经济学", "year2": "宏观经济学、统计学、概率论、计量经济学基础", "year3": "国际金融、货币银行学、财政学", "year4": "毕业论文、专业方向选修"},
        "suitable_for": {"traits": ["数学基础好", "对经济现象感兴趣", "逻辑思维强"], "skills": ["数学（微积分、概率统计必须精通）", "数据分析能力", "英语（看英文文献）"], "warning": "数学不好慎选，计量经济学需要较强数学基础"},
        "prospects": {"trend": "2024年经济形势复杂，但经济专业人才需求稳定", "hot": "银行、证券、咨询公司、四大", "developing": "数据分析、量化投资、公共政策"},
        "career_advice": {"immediate": "必须掌握Python或Stata进行数据分析", "certifications": "CFA（美国特许金融分析师）、CPA", "timeline": "大三暑假前拿到实习，大四准备秋招"},
        "learning_path": {"freshman": "学好数学和英语，了解经济学基本框架", "sophomore": "开始学计量经济学和数据分析工具", "junior": "参加数学建模竞赛，找第一份实习", "senior": "秋招/考研，简历突出实习和项目经验"},
        "zhang_reviews": {"pros": ["就业面极广", "金融行业认可度高", "培养商业思维", "考研/出国有优势", "考公热门专业"], "cons": ["数学要求极高", "竞争极其激烈", "顶尖岗位门槛高", "证书要求高", "学习内容宽泛"], "summary": "经济学是万金油专业，就业面广但竞争激烈。"}
    },
    {
        "code": "030101",
        "name": "法学",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": 5,
        "popularity": 5,
        "salary": {"description": "前期收入低（3000-6000元），后期差距大", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率较高，但对口率低（法考是门槛）", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习法律知识和法律思维", "year1": "法理学、宪法学、中国法制史、民法总论", "year2": "物权法、合同法、侵权责任法、民事诉讼法", "year3": "刑法、刑事诉讼法、行政法", "year4": "商法、经济法、知识产权法、国际法"},
        "suitable_for": {"traits": ["记忆力好（背法条）", "逻辑思维强（分析案情）", "文字表达好（写诉状）"], "skills": ["记忆力（大量法条需要记忆）", "逻辑推理能力", "表达能力"], "warning": "法考通过率仅12%，没通过的很难从事法律工作"},
        "prospects": {"trend": "2024年法律行业竞争激烈，红圈所门槛极高", "hot": "律所、法院、检察院、企业法务", "developing": "合规业务、涉外法律、数据合规"},
        "career_advice": {"immediate": "大学期间必须过法考，否则就业困难", "certifications": "法律职业资格证（必考）、律师执业证", "timeline": "大四第一学期考法考，考研/就业同步准备"},
        "learning_path": {"freshman": "培养法律思维，读《西窗法雨》等入门书", "sophomore": "开始系统学习民法刑法，练习案例分析", "junior": "准备法考（至少复习6个月），找律所实习", "senior": "过法考！过法考！过法考！"},
        "zhang_reviews": {"pros": ["社会地位极高", "越老越吃香", "能帮人解决实际问题", "收入上限极高", "职业发展清晰"], "cons": ["法考难度地狱级", "前期收入极低", "工作强度极大", "竞争极其激烈", "培养周期长"], "summary": "法学是典型的\"先苦后甜\"专业。"}
    },
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
        "zhang_reviews": {"pros": ["稳定体面", "带薪寒暑假", "工作稳定", "人际关系简单", "利于家庭"], "cons": ["薪资增长缓慢", "编制竞争激烈", "教学压力大", "家长沟通难", "职业倦怠感强"], "summary": "教育学是追求稳定生活的人的好选择。"}
    },
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
        "zhang_reviews": {"pros": ["考公考编优势大", "文字能力出众", "文化底蕴深厚", "教师需求稳定", "新媒体有优势"], "cons": ["薪资天花板有限", "纯文字工作竞争激烈", "需要持续积累", "创造性要求高", "部分岗位被AI冲击"], "summary": "汉语言文学是考公考编的热门专业。"}
    },
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
        "zhang_reviews": {"pros": ["基础学科，跨专业容易", "薪资潜力大", "培养逻辑思维", "考研有优势", "公考有优势"], "cons": ["课程难度极大", "必须持续深造", "需要真正热爱", "与高中数学不同", "编程能力要自己培养"], "summary": "数学专业是万金油专业，可以转向金融、计算机、统计等方向。"}
    },
    {
        "code": "080901",
        "name": "计算机科学与技术",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": 5,
        "popularity": 5,
        "salary": {"description": "起薪约8000-20000元，薪资较高", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，互联网/IT行业需求旺盛", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习编程、算法、数据结构、系统设计", "year1": "C语言程序设计、高等数学、线性代数", "year2": "数据结构、算法、操作系统、数据库原理", "year3": "计算机网络、编译原理、云计算/人工智能", "year4": "毕业设计、互联网公司实习"},
        "suitable_for": {"traits": ["喜欢编程", "逻辑清晰", "喜欢学习"], "skills": ["编程能力", "算法设计", "系统设计"], "warning": "技术迭代快，需要持续学习"},
        "prospects": {"trend": "互联网、科技公司是主要就业方向", "hot": "互联网公司、科技公司、金融科技", "developing": "人工智能、云计算、大数据"},
        "career_advice": {"immediate": "多写代码，刷算法题，找实习", "certifications": "计算机技术与软件专业技术资格", "timeline": "大三暑假必须找实习"},
        "learning_path": {"freshman": "学编程，打基础", "sophomore": "学算法，练项目", "junior": "确定方向：前端/后端/算法/安全", "senior": "找实习，秋招"},
        "zhang_reviews": {"pros": ["起薪高", "需求大", "技术是硬实力", "相对公平", "发展路径清晰"], "cons": ["35岁危机", "加班严重", "工作枯燥", "青春饭", "竞争激烈"], "summary": "计算机是好专业，但不适合所有人。"}
    },
    {
        "code": "100201",
        "name": "临床医学",
        "category": "10 医学",
        "category_icon": "🏥",
        "difficulty": 5,
        "popularity": 4,
        "salary": {"description": "起薪约5000-10000元，后期增长显著", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，医疗行业需求稳定", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习医学基础、临床技能、疾病诊疗", "year1": "系统解剖学、组织胚胎学、生理学", "year2": "生物化学、病理学、药理学", "year3": "诊断学、内科学、外科学、妇产科学", "year4": "见习、实习、执业医师考试"},
        "suitable_for": {"traits": ["有耐心", "责任心强", "能吃苦"], "skills": ["临床思维", "动手能力", "沟通能力"], "warning": "学习周期长，前几年收入低，工作辛苦"},
        "prospects": {"trend": "医院、药企、医疗器械是主要方向", "hot": "三甲医院、专科医院、医学院校", "developing": "精准医疗、智慧医疗、康复医学"},
        "career_advice": {"immediate": "必须考研，否则很难进好医院", "certifications": "执业医师资格证", "timeline": "大五准备考研/规培"},
        "learning_path": {"freshman": "打基础，适应医学学习强度", "sophomore": "学习核心医学课程", "junior": "临床技能训练，准备考研", "senior": "见习、实习、考研"},
        "zhang_reviews": {"pros": ["越老越值钱", "社会地位高", "职业稳定", "有成就感", "收入后期高"], "cons": ["学习周期太长", "前几年太苦", "医患关系", "工作压力大", "35岁才起步"], "summary": "学医要有情怀，否则很难坚持。"}
    },
    {
        "code": "120201",
        "name": "工商管理",
        "category": "11 管理学",
        "category_icon": "💼",
        "difficulty": 3,
        "popularity": 5,
        "salary": {"description": "起薪约5000-12000元，管理路线薪资高", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，企业管理需求稳定", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习企业管理、市场营销、财务管理", "year1": "管理学原理、会计学、经济学基础", "year2": "市场营销、人力资源管理、组织行为学", "year3": "战略管理、运营管理、公司治理", "year4": "毕业论文、企业实习"},
        "suitable_for": {"traits": ["沟通能力强", "组织协调能力好", "领导力"], "skills": ["管理能力", "沟通能力", "商业思维"], "warning": "需要实践经验，纯理论不够"},
        "prospects": {"trend": "企业管理层是主要方向", "hot": "企业管培生、咨询公司、管理岗位", "developing": "数字化管理、创业"},
        "career_advice": {"immediate": "多实习，积累管理经验", "certifications": "MBA（后期）、PMP", "timeline": "大三找管理类实习"},
        "learning_path": {"freshman": "打管理学基础", "sophomore": "学习营销和人力资源", "junior": "确定方向，找实习", "senior": "秋招或考研"},
        "zhang_reviews": {"pros": ["就业面广", "晋升通道清晰", "综合能力强", "商业视野广", "人脉资源"], "cons": ["竞争激烈", "经验重要", "薪资起步一般", "什么都学不精", "管理岗需要熬年限"], "summary": "工商管理是万金油专业，但需要实践经验。"}
    },
    {
        "code": "130502",
        "name": "视觉传达设计",
        "category": "12 艺术学",
        "category_icon": "🎨",
        "difficulty": 3,
        "popularity": 4,
        "salary": {"description": "差距极大，5000-30000元不等", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率高，但竞争激烈", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "学习视觉设计和创意表达", "year1": "素描、色彩、平面构成、设计概论", "year2": "字体设计、标志设计、包装设计", "year3": "品牌设计、UI设计、广告设计", "year4": "毕业设计、设计公司实习"},
        "suitable_for": {"traits": ["有审美", "有创意", "对设计感兴趣"], "skills": ["设计软件（PS/AI/AE）", "创意能力", "审美能力"], "warning": "作品集是就业的关键"},
        "prospects": {"trend": "UI设计、短视频设计需求增加", "hot": "设计公司、互联网公司、广告公司", "developing": "UI设计、品牌设计、插画"},
        "career_advice": {"immediate": "做作品集！做作品集！做作品集！", "certifications": "Adobe认证", "timeline": "大二开始做作品集"},
        "learning_path": {"freshman": "设计基础，练手绘", "sophomore": "学设计软件，做课程作品", "junior": "去设计公司实习，完善作品集", "senior": "秋招/春招"},
        "zhang_reviews": {"pros": ["能发挥创意", "可自己接单", "UI设计需求大", "可往品牌设计发展", "技能可变现"], "cons": ["竞争激烈", "需要持续学习", "甲方审美差异", "熬夜改稿是常态", "35岁危机"], "summary": "视觉传达设计是\"作品集决定一切\"的专业。"}
    },
]


def generate_major_card(major):
    code = major["code"]
    name = major["name"]
    category = major["category"]
    icon = major["category_icon"]
    difficulty = "★" * major["difficulty"] + "☆" * (5 - major["difficulty"])
    
    salary_desc = major["salary"]["description"]
    salary_source = major["salary"]["source"]
    employment_desc = major["employment_rate"]["description"]
    
    what_learn = major["what_you_learn"]
    suitable = major["suitable_for"]
    prospects = major["prospects"]
    career = major["career_advice"]
    learning = major["learning_path"]
    reviews = major["zhang_reviews"]
    
    skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in suitable.get("skills", [])])
    pros_list = "".join([f'<li>{p}</li>' for p in reviews.get("pros", [])])
    cons_list = "".join([f'<li>{c}</li>' for c in reviews.get("cons", [])])
    
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
                <div class="detail-content">{what_learn.get("summary", "")}</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{what_learn.get("year1", "")}</li>
                    <li><strong>大二：</strong>{what_learn.get("year2", "")}</li>
                    <li><strong>大三：</strong>{what_learn.get("year3", "")}</li>
                    <li><strong>大四：</strong>{what_learn.get("year4", "")}</li>
                </ul>
                
                <div class="detail-title">👤 适合人群</div>
                <div class="detail-content"><strong>特质：</strong>{'、'.join(suitable.get("traits", []))}</div>
                <div class="detail-content"><strong>技能要求：</strong></div>
                <div class="skill-tags">{skills_html}</div>
                <div class="detail-content warning">⚠️ {suitable.get("warning", "")}</div>
                
                <div class="detail-title">📈 前景展望</div>
                <div class="detail-content"><strong>趋势：</strong>{prospects.get("trend", "")}</div>
                <div class="detail-content"><strong>热门去向：</strong>{prospects.get("hot", "")}</div>
                <div class="detail-content"><strong>新兴方向：</strong>{prospects.get("developing", "")}</div>
                
                <div class="detail-title">💼 就业建议</div>
                <div class="detail-content"><strong>立即行动：</strong>{career.get("immediate", "")}</div>
                <div class="detail-content"><strong>证书建议：</strong>{career.get("certifications", "")}</div>
                <div class="detail-content"><strong>时间线：</strong>{career.get("timeline", "")}</div>
                
                <div class="detail-title">🛤️ 学习路径</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{learning.get("freshman", "")}</li>
                    <li><strong>大二：</strong>{learning.get("sophomore", "")}</li>
                    <li><strong>大三：</strong>{learning.get("junior", "")}</li>
                    <li><strong>大四：</strong>{learning.get("senior", "")}</li>
                </ul>
                
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
                    💬 总结：{reviews.get("summary", "")}
                </div>
            </div>
        </div>
    '''


def generate_filter_buttons(majors):
    categories = sorted(set([m["category"] for m in majors]))
    buttons = []
    for cat in categories:
        icon = next((m["category_icon"] for m in majors if m["category"] == cat), "📚")
        buttons.append(f'<button class="filter-btn" data-filter="{cat}">{icon} {cat}</button>')
    return "\n".join(buttons)


def main():
    total = len(MAJORS_DATA)
    categories = len(set([m["category"] for m in MAJORS_DATA]))
    filter_buttons = generate_filter_buttons(MAJORS_DATA)
    major_cards = "".join([generate_major_card(m) for m in MAJORS_DATA])
    
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
            --surface-container: #FFFFFF;
            --primary: #E67E22;
            --primary-container: #FAD7B2;
            --secondary: #705A49;
            --secondary-container: #EBE0D6;
            --on-surface: #2C2621;
            --on-surface-variant: #8B7E74;
            --outline: #DED0C6;
            --shadow: rgba(112, 90, 73, 0.05);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
            background: var(--surface);
            min-height: 100vh;
            color: var(--on-surface);
            line-height: 1.8;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        
        /* 星座背景header */
        header {{
            position: relative;
            text-align: center;
            padding: 80px 40px;
            background: linear-gradient(135deg, #FFF8F5 0%, #FAD7B2 50%, #E9D6CC 100%);
            border-radius: 24px;
            margin-bottom: 40px;
            box-shadow: 0 8px 32px rgba(112, 90, 73, 0.1);
            overflow: hidden;
            min-height: 320px;
        }}
        
        /* 星座图背景 */
        header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                /* 星星 */
                radial-gradient(circle at 20% 20%, rgba(230, 126, 34, 0.8) 2px, transparent 2px),
                radial-gradient(circle at 80% 30%, rgba(230, 126, 34, 0.6) 2px, transparent 2px),
                radial-gradient(circle at 40% 50%, rgba(230, 126, 34, 0.7) 2px, transparent 2px),
                radial-gradient(circle at 70% 60%, rgba(230, 126, 34, 0.5) 2px, transparent 2px),
                radial-gradient(circle at 30% 70%, rgba(230, 126, 34, 0.6) 2px, transparent 2px),
                radial-gradient(circle at 85% 75%, rgba(230, 126, 34, 0.8) 2px, transparent 2px),
                radial-gradient(circle at 15% 40%, rgba(230, 126, 34, 0.7) 2px, transparent 2px),
                radial-gradient(circle at 60% 25%, rgba(230, 126, 34, 0.6) 2px, transparent 2px),
                radial-gradient(circle at 50% 85%, rgba(230, 126, 34, 0.5) 2px, transparent 2px),
                radial-gradient(circle at 90% 50%, rgba(230, 126, 34, 0.7) 2px, transparent 2px),
                radial-gradient(circle at 10% 60%, rgba(230, 126, 34, 0.6) 2px, transparent 2px),
                radial-gradient(circle at 75% 85%, rgba(230, 126, 34, 0.8) 2px, transparent 2px),
                radial-gradient(circle at 25% 15%, rgba(230, 126, 34, 0.5) 2px, transparent 2px),
                radial-gradient(circle at 55% 35%, rgba(230, 126, 34, 0.7) 2px, transparent 2px),
                radial-gradient(circle at 35% 90%, rgba(230, 126, 34, 0.6) 2px, transparent 2px);
            animation: twinkle 3s ease-in-out infinite;
            pointer-events: none;
        }}
        
        /* 星座连线 */
        header::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                /* 星座连线 */
                linear-gradient(45deg, transparent 49.5%, rgba(230, 126, 34, 0.15) 49.5%, rgba(230, 126, 34, 0.15) 50.5%, transparent 50.5%),
                linear-gradient(-45deg, transparent 49.5%, rgba(230, 126, 34, 0.1) 49.5%, rgba(230, 126, 34, 0.1) 50.5%, transparent 50.5%);
            background-size: 80px 80px;
            animation: constellationMove 20s linear infinite;
            pointer-events: none;
        }}
        
        @keyframes twinkle {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
        
        @keyframes constellationMove {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(80px, 80px); }}
        }}
        
        /* 星星光晕 */
        .star-glow {{
            position: absolute;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(230, 126, 34, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            animation: glow 4s ease-in-out infinite;
        }}
        
        .star-glow-1 {{ top: -50px; left: -50px; }}
        .star-glow-2 {{ bottom: -50px; right: -50px; animation-delay: 2s; }}
        
        @keyframes glow {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.2); opacity: 0.8; }}
        }}
        
        /* 星座图标装饰 */
        .constellation-icon {{
            position: absolute;
            font-size: 120px;
            opacity: 0.1;
            color: var(--primary);
            pointer-events: none;
        }}
        
        .constellation-icon-1 {{ top: 20px; right: 40px; }}
        .constellation-icon-2 {{ bottom: 20px; left: 40px; }}
        
        header h1 {{
            font-family: "Literata", serif;
            font-size: 48px;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 16px;
            position: relative;
            z-index: 10;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
        }}
        
        header p {{
            font-size: 16px;
            color: var(--on-surface-variant);
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 10;
        }}
        
        .stats-banner {{
            display: flex;
            justify-content: center;
            gap: 64px;
            margin: 40px 0 24px;
            flex-wrap: wrap;
            position: relative;
            z-index: 10;
        }}
        
        .stat-item {{
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px 32px;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(112, 90, 73, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .stat-number {{
            font-family: "Literata", serif;
            font-size: 48px;
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
            margin-top: 8px;
        }}
        
        .search-section {{ background: var(--surface-container); padding: 24px 32px; border-radius: 20px; margin-bottom: 24px; box-shadow: 0 4px 24px var(--shadow); }}
        .search-box {{ display: flex; gap: 12px; align-items: center; }}
        .search-input {{ flex: 1; padding: 14px 20px; border: 2px solid var(--outline); border-radius: 16px; font-size: 16px; outline: none; transition: all 0.3s; background: #FFF1EA; }}
        .search-input:focus {{ border-color: var(--primary); box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.1); }}
        .search-icon {{ font-size: 24px; color: var(--secondary); }}
        
        .filter-section {{ background: var(--surface-container); padding: 28px 32px; border-radius: 20px; margin-bottom: 32px; box-shadow: 0 4px 24px var(--shadow); }}
        .filter-title {{ font-family: "Literata", serif; font-size: 20px; font-weight: 600; margin-bottom: 16px; color: var(--secondary); }}
        .filter-buttons {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .filter-btn {{ padding: 10px 20px; border: 2px solid var(--outline); border-radius: 9999px; background: transparent; color: var(--secondary); cursor: pointer; transition: all 0.3s; font-size: 14px; font-weight: 500; }}
        .filter-btn:hover {{ background: var(--secondary-container); transform: translateY(-2px); }}
        .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        
        .majors-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }}
        .major-card {{ background: var(--surface-container); border-radius: 20px; padding: 28px; transition: all 0.3s; cursor: pointer; border: 2px solid var(--outline); box-shadow: 0 4px 24px var(--shadow); }}
        .major-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 40px var(--shadow); border-color: var(--primary); }}
        .card-header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 18px; }}
        .category-icon {{ font-size: 32px; background: var(--primary-container); width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; border-radius: 16px; }}
        .major-name {{ font-family: "Literata", serif; font-size: 24px; font-weight: 600; color: var(--secondary); }}
        .major-code {{ font-size: 12px; color: var(--on-surface-variant); font-weight: 500; margin-top: 4px; }}
        .difficulty-stars {{ margin-top: 8px; color: var(--primary); font-size: 14px; }}
        .salary-tag {{ display: inline-block; background: var(--primary-container); color: var(--secondary); padding: 6px 16px; border-radius: 9999px; font-size: 13px; font-weight: 500; margin: 12px 0; }}
        .data-source-tag {{ display: inline-block; background: var(--secondary-container); color: var(--secondary); padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 500; margin-left: 10px; }}
        .employment-desc {{ margin-top: 10px; font-size: 0.9em; color: var(--on-surface-variant); }}
        .detail-section {{ margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--outline); }}
        .detail-title {{ font-family: "Literata", serif; font-size: 18px; font-weight: 600; color: var(--secondary); margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
        .detail-content {{ font-size: 15px; color: var(--on-surface); margin-bottom: 10px; }}
        .year-list {{ list-style: none; padding-left: 0; }}
        .year-list li {{ margin: 8px 0; position: relative; padding-left: 24px; font-size: 14px; color: var(--on-surface-variant); }}
        .year-list li::before {{ content: "•"; position: absolute; left: 0; color: var(--primary); font-weight: bold; font-size: 18px; }}
        .pros-cons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }}
        .pros-box, .cons-box {{ padding: 16px; border-radius: 16px; font-size: 14px; }}
        .pros-box {{ background: #e8f5e9; border-left: 4px solid #43a047; }}
        .cons-box {{ background: #ffebee; border-left: 4px solid #e53935; }}
        .pros-title {{ color: #2e7d32; }}
        .cons-title {{ color: #c62828; }}
        .pros-cons-list {{ padding-left: 20px; margin-top: 8px; }}
        .summary-box {{ background: var(--secondary-container); padding: 20px; border-radius: 16px; margin-top: 20px; color: var(--on-surface); font-size: 14px; line-height: 1.8; }}
        .skill-tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
        .skill-tag {{ padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 500; background: var(--secondary-container); color: var(--secondary); }}
        .warning {{ color: #c05621 !important; }}
        .hidden {{ display: none; }}
        footer {{ text-align: center; padding: 48px 20px; color: var(--on-surface-variant); font-size: 14px; margin-top: 48px; border-top: 1px solid var(--outline); }}
        
        @media (max-width: 768px) {{
            .majors-grid {{ grid-template-columns: 1fr; }}
            header {{ padding: 60px 24px; min-height: 280px; }}
            header h1 {{ font-size: 32px; }}
            .stats-banner {{ gap: 24px; }}
            .stat-item {{ padding: 16px 24px; }}
            .stat-number {{ font-size: 36px; }}
            .constellation-icon {{ font-size: 80px; }}
            .container {{ padding: 20px; }}
            .pros-cons {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="star-glow star-glow-1"></div>
            <div class="star-glow star-glow-2"></div>
            <span class="constellation-icon constellation-icon-1">✦</span>
            <span class="constellation-icon constellation-icon-2">✧</span>
            
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
            const card = document.getElementById("card-" + code);
            if (expandedCards.has(code)) {{
                expandedCards.delete(code);
                card.classList.remove("expanded");
                const detail = card.querySelector(".detail-section");
                if (detail) detail.classList.add("hidden");
            }} else {{
                expandedCards.add(code);
                card.classList.add("expanded");
                const detail = card.querySelector(".detail-section");
                if (detail) detail.classList.remove("hidden");
            }}
        }}
        function filterMajors(category) {{
            document.querySelectorAll(".filter-btn").forEach(btn => {{
                btn.classList.remove("active");
                if (btn.dataset.filter === category) btn.classList.add("active");
            }});
            document.querySelectorAll(".major-card").forEach(card => {{
                if (category === "all" || card.dataset.category === category) card.classList.remove("hidden");
                else card.classList.add("hidden");
            }});
        }}
        function searchMajors(query) {{
            const searchTerm = query.toLowerCase().trim();
            document.querySelectorAll(".major-card").forEach(card => {{
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                if (name.includes(searchTerm) || category.includes(searchTerm)) card.classList.remove("hidden");
                else card.classList.add("hidden");
            }});
        }}
        document.querySelectorAll(".filter-btn").forEach(btn => {{
            btn.addEventListener("click", () => {{
                document.getElementById("searchInput").value = "";
                filterMajors(btn.dataset.filter);
            }});
        }});
        document.getElementById("searchInput").addEventListener("input", (e) => searchMajors(e.target.value));
    </script>
</body>
</html>'''
    
    output_path = "/workspace/major_starmap_final.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 专业星图 最终版 生成完成！")
    print(f"📊 共生成 {total} 个专业")
    print(f"🎨 星座背景设计完成！")
    print(f"📁 输出文件：{output_path}")


if __name__ == "__main__":
    main()
