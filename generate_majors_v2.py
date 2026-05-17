#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 V2 - 生成更真实、准确的专业信息网站
"""

import re
from typing import Dict, List, Any

MAJORS_DATA: List[Dict[str, Any]] = [
    # 01 哲学类
    {
        "code": "010101",
        "name": "哲学",
        "category": "01 哲学",
        "category_icon": "🎓",
        "difficulty": 4,
        "popularity": 2,
        "salary": {
            "description": "起薪约5000-8000元，学术路线前期收入较低",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，对口就业率较低",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "哲学专业学习如何思考、推理和论证",
            "year1": "中国哲学史、西方哲学史、逻辑学入门",
            "year2": "马克思主义哲学、伦理学、美学",
            "year3": "宗教学、科学技术哲学、专业原著选读",
            "year4": "毕业论文写作、哲学专题研讨"
        },
        "suitable_for": {
            "traits": ["喜欢深度思考", "对人生意义感兴趣", "耐得住寂寞"],
            "skills": ["阅读理解能力（大量原著）", "写作表达能力", "逻辑推理能力"],
            "warning": "需要长期积累，短期难以见成效"
        },
        "prospects": {
            "trend": "就业面较窄但稳定，哲学思维在管理咨询、公共政策等领域受重视",
            "hot": "公务员、编辑、教师",
            "developing": "智库研究员、文化产业"
        },
        "career_advice": {
            "immediate": "尽早确定方向：学术/教育/其他",
            "certifications": "教师资格证（想当老师必考）",
            "timeline": "大三开始准备考研或考公"
        },
        "learning_path": {
            "freshman": "读经典原著：论语、道德经、柏拉图对话录",
            "sophomore": "建立知识框架，写读书笔记",
            "junior": "参加读书会，尝试写学术论文",
            "senior": "确定方向：考研/考公/就业"
        },
        "zhang_reviews": {
            "pros": ["培养批判性思维", "考公有优势（行测逻辑题）", "能看透事物本质"],
            "cons": ["对口工作少", "起薪低", "需要持续深造"],
            "summary": "如果想赚快钱别选哲学；如果想提升思维层次，哲学是很好的通识教育"
        }
    },
    
    # 02 经济学类
    {
        "code": "020101",
        "name": "经济学",
        "category": "02 经济学",
        "category_icon": "📊",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "起薪约6000-15000元，取决于院校和城市",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，对口率高",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "研究资源配置、经济发展和市场运行规律",
            "year1": "微积分、线性代数、政治经济学、微观经济学",
            "year2": "宏观经济学、统计学、概率论、计量经济学基础",
            "year3": "国际金融、货币银行学、财政学、计量经济学应用",
            "year4": "毕业论文、专业方向选修（如发展经济学、环境经济学）"
        },
        "suitable_for": {
            "traits": ["数学基础好", "对经济现象感兴趣", "逻辑思维强"],
            "skills": ["数学（微积分、概率统计必须精通）", "数据分析能力", "英语（看英文文献）"],
            "warning": "数学不好慎选，计量经济学需要较强数学基础"
        },
        "prospects": {
            "trend": "2024年经济形势复杂，但经济专业人才需求稳定",
            "hot": "银行、证券、咨询公司、四大",
            "developing": "数据分析、量化投资、公共政策"
        },
        "career_advice": {
            "immediate": "必须掌握Python或Stata进行数据分析",
            "certifications": "CFA（美国特许金融分析师）、CPA",
            "timeline": "大三暑假前拿到实习，大四准备秋招"
        },
        "learning_path": {
            "freshman": "学好数学和英语，了解经济学基本框架",
            "sophomore": "开始学计量经济学和数据分析工具",
            "junior": "参加数学建模竞赛，找第一份实习",
            "senior": "秋招/考研，简历突出实习和项目经验"
        },
        "zhang_reviews": {
            "pros": ["就业面广", "金融行业认可度高", "培养商业思维"],
            "cons": ["数学要求高", "竞争激烈", "顶尖岗位需要研究生学历"],
            "summary": "数学好的人适合，数学不好建议选其他方向"
        }
    },
    
    {
        "code": "020201",
        "name": "财政学",
        "category": "02 经济学",
        "category_icon": "💰",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "体制内就业为主，起薪约5000-10000元",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，体制内比例高",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习政府理财、公共支出和税收的理论与实践",
            "year1": "政治经济学、财政学基础、税收概论",
            "year2": "中国税制、预算管理、政府会计",
            "year3": "国有资产管理、地方政府财政、国际税收",
            "year4": "毕业论文、专业实习"
        },
        "suitable_for": {
            "traits": ["有家国情怀", "愿意服务公共事务", "文字功底好"],
            "skills": ["财务分析能力", "政策理解能力", "公文写作能力"],
            "warning": "如果只想赚钱不建议选这条路"
        },
        "prospects": {
            "trend": "财政专业人才稳定需求，公务员考试有优势",
            "hot": "税务局、财政局、审计局、政府部门",
            "developing": "PPP项目、财政绩效评价"
        },
        "career_advice": {
            "immediate": "关注公务员考试，提早准备行测申论",
            "certifications": "税务师、会计师",
            "timeline": "大三开始备考公务员"
        },
        "learning_path": {
            "freshman": "了解财政体制，看政府工作报告",
            "sophomore": "学税收实务，关注财政政策",
            "junior": "找财税类实习，备考税务师",
            "senior": "国考/省考，简历突出财务分析能力"
        },
        "zhang_reviews": {
            "pros": ["考公优势明显", "工作稳定", "社会地位较高"],
            "cons": ["薪资天花板较低", "体制内晋升慢"],
            "summary": "想稳定生活的人适合，想快速致富的不适合"
        }
    },
    
    # 03 法学类
    {
        "code": "030101",
        "name": "法学",
        "category": "03 法学",
        "category_icon": "⚖️",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "前期收入低（3000-6000元），后期差距大",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率较高，但对口率低（法考是门槛）",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习法律知识和法律思维",
            "year1": "法理学、宪法学、中国法制史、民法总论",
            "year2": "物权法、合同法、侵权责任法、民事诉讼法",
            "year3": "刑法、刑事诉讼法、行政法与行政诉讼法",
            "year4": "商法、经济法、知识产权法、国际法、毕业论文"
        },
        "suitable_for": {
            "traits": ["记忆力好（背法条）", "逻辑思维强（分析案情）", "文字表达好（写诉状）"],
            "skills": ["记忆力（大量法条需要记忆）", "逻辑推理能力", "表达能力"],
            "warning": "法考通过率仅12%，没通过的很难从事法律工作"
        },
        "prospects": {
            "trend": "2024年法律行业竞争激烈，红圈所门槛极高",
            "hot": "律所、法院、检察院、企业法务",
            "developing": "合规业务、涉外法律、数据合规"
        },
        "career_advice": {
            "immediate": "大学期间必须过法考，否则就业困难",
            "certifications": "法律职业资格证（必考）、律师执业证",
            "timeline": "大四第一学期考法考，考研/就业同步准备"
        },
        "learning_path": {
            "freshman": "培养法律思维，读《西窗法雨》等入门书",
            "sophomore": "开始系统学习民法刑法，练习案例分析",
            "junior": "准备法考（至少复习6个月），找律所实习",
            "senior": "过法考！过法考！过法考！"
        },
        "zhang_reviews": {
            "pros": ["社会地位高", "越老越吃香", "能帮人解决实际问题"],
            "cons": ["法考难（通过率12%）", "前期收入低", "加班多"],
            "summary": "背书不行别选法学，法考是硬门槛"
        }
    },
    
    {
        "code": "030301",
        "name": "社会学",
        "category": "03 法学",
        "category_icon": "👥",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，非热门但稳定",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，适合继续深造",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "研究社会结构、社会问题和社会变迁",
            "year1": "社会学概论、社会学理论、社会研究方法",
            "year2": "社会统计学、社会调查方法、质性研究",
            "year3": "社会分层与流动、城市社会学、农村社会学",
            "year4": "社会政策、社会工作、毕业论文"
        },
        "suitable_for": {
            "traits": ["关心社会问题", "喜欢与人打交道", "有同理心"],
            "skills": ["问卷设计能力", "数据分析能力", "报告写作能力"],
            "warning": "纯学术路线需要读研读博"
        },
        "prospects": {
            "trend": "社会调研需求增加，新兴领域包括互联网用户研究",
            "hot": "市场研究公司、咨询公司、政府部门",
            "developing": "用户研究、社会企业、公共政策"
        },
        "career_advice": {
            "immediate": "掌握SPSS或R语言进行数据分析",
            "certifications": "社工证（想做社工必考）",
            "timeline": "大三确定方向：学术/市场研究/社工"
        },
        "learning_path": {
            "freshman": "读费孝通《乡土中国》等经典",
            "sophomore": "学社会调查方法，做实地调研",
            "junior": "学数据分析，找市场研究公司实习",
            "senior": "写高质量调研报告"
        },
        "zhang_reviews": {
            "pros": ["理解社会深刻", "培养调查能力", "考公有优势"],
            "cons": ["对口工作少", "薪资不高"],
            "summary": "适合做学术或市场研究，不适合想赚快钱的人"
        }
    },
    
    # 04 教育学类
    {
        "code": "040101",
        "name": "教育学",
        "category": "04 教育学",
        "category_icon": "📚",
        "difficulty": 3,
        "popularity": 4,
        "salary": {
            "description": "教师编制内稳定，薪资与地区职称挂钩",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，教师岗位需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习教育理论和教育实践",
            "year1": "教育学概论、教育心理学、教育史",
            "year2": "课程与教学论、教育研究方法、教育评价",
            "year3": "教育管理学、教育政策学、比较教育",
            "year4": "教育实习、毕业论文"
        },
        "suitable_for": {
            "traits": ["有爱心", "善于表达", "耐心"],
            "skills": ["表达能力", "组织协调能力", "抗压能力"],
            "warning": "想当老师必须考教师资格证和编制"
        },
        "prospects": {
            "trend": "2024年教师编制竞争激烈，好学校门槛高",
            "hot": "中小学教师、教育培训机构、教育管理",
            "developing": "在线教育、教育科技、教育咨询"
        },
        "career_advice": {
            "immediate": "必须考教师资格证，大三开始准备考编",
            "certifications": "教师资格证（必考）、普通话证书",
            "timeline": "大三上学期拿教资，大三下开始备考编制"
        },
        "learning_path": {
            "freshman": "考普通话证书，了解教育行业",
            "sophomore": "参加教学实践，试讲练习",
            "junior": "考教资，准备教师编制考试",
            "senior": "参加教师招聘考试"
        },
        "zhang_reviews": {
            "pros": ["稳定体面", "有寒暑假", "社会地位高"],
            "cons": ["薪资增长慢", "编制难考", "教学压力大"],
            "summary": "适合追求稳定生活的人，挣钱不是首要目标"
        }
    },
    
    {
        "code": "040201",
        "name": "体育教育",
        "category": "04 教育学",
        "category_icon": "⚽",
        "difficulty": 3,
        "popularity": 3,
        "salary": {
            "description": "教师编制内稳定，薪资与地区相关",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，体育老师需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习体育理论、运动技能和教学方法",
            "year1": "运动解剖学、体育概论、田径、篮球",
            "year2": "运动生理学、体操、武术、游泳",
            "year3": "体育教学论、运动训练学、体育游戏",
            "year4": "教育实习、毕业论文"
        },
        "suitable_for": {
            "traits": ["热爱体育", "身体素质好", "有耐心"],
            "skills": ["运动技能（至少一项专长）", "教学能力", "组织能力"],
            "warning": "运动伤病是职业风险"
        },
        "prospects": {
            "trend": "体育产业快速发展，中考高考体育地位提升",
            "hot": "中小学体育老师、健身教练、体育培训机构",
            "developing": "体育经纪、运动康复、体育管理"
        },
        "career_advice": {
            "immediate": "培养一项运动专长，考取相关证书",
            "certifications": "教师资格证、教练员证、社会体育指导员证",
            "timeline": "大三准备考编"
        },
        "learning_path": {
            "freshman": "确定运动专长方向，考取相关证书",
            "sophomore": "考教资，参加教学实习",
            "junior": "准备考编，了解体育产业",
            "senior": "参加教师招聘考试"
        },
        "zhang_reviews": {
            "pros": ["工作稳定", "有寒暑假", "适合热爱运动的人"],
            "cons": ["薪资有限", "发展空间有限"],
            "summary": "热爱体育且追求稳定的人适合"
        }
    },
    
    # 05 文学类
    {
        "code": "050101",
        "name": "汉语言文学",
        "category": "05 文学",
        "category_icon": "📖",
        "difficulty": 3,
        "popularity": 5,
        "salary": {
            "description": "起薪约5000-9000元，稳定型收入",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，体制内岗位多",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习汉语语言知识和文学鉴赏创作能力",
            "year1": "现代汉语、古代汉语、文学概论、中国现代文学",
            "year2": "中国古代文学、外国文学、写作学",
            "year3": "文学批评、语言学概论、比较文学",
            "year4": "毕业论文、选修方向深化"
        },
        "suitable_for": {
            "traits": ["热爱阅读", "文字敏感", "善于表达"],
            "skills": ["写作能力（各种文体）", "阅读理解能力", "文字功底"],
            "warning": "纯文学创作需要天赋，不是每个人都适合"
        },
        "prospects": {
            "trend": "考公考编热门专业，新媒体行业需求增加",
            "hot": "语文老师、编辑、记者、公务员",
            "developing": "新媒体运营、内容编辑、文案策划"
        },
        "career_advice": {
            "immediate": "多练写作，建立作品集",
            "certifications": "教师资格证（想当老师）、出版专业资格证",
            "timeline": "大三确定方向，准备考公或考编"
        },
        "learning_path": {
            "freshman": "大量阅读经典文学作品，开始写读书笔记",
            "sophomore": "练习各种文体写作，尝试投稿",
            "junior": "确定方向（教育/出版/新媒体），针对性准备",
            "senior": "积累作品集，准备秋招"
        },
        "zhang_reviews": {
            "pros": ["考公考编优势大", "文字能力强", "文化底蕴深"],
            "cons": ["薪资天花板有限", "纯文字工作竞争激烈"],
            "summary": "适合追求稳定、热爱文学的人"
        }
    },
    
    {
        "code": "050201",
        "name": "英语",
        "category": "05 文学",
        "category_icon": "🌍",
        "difficulty": 4,
        "popularity": 5,
        "salary": {
            "description": "差距极大，翻译和教育类5000-20000元不等",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但竞争激烈",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习英语语言技能和文化知识",
            "year1": "综合英语、听力、口语、语音",
            "year2": "阅读、写作、翻译入门、语言学概论",
            "year3": "高级翻译、英美文学、商务英语/旅游英语",
            "year4": "毕业论文、专业实习"
        },
        "suitable_for": {
            "traits": ["对语言有天赋", "刻苦努力", "敢于开口"],
            "skills": ["听说读写译（全方位）", "跨文化交际能力", "学习能力"],
            "warning": "必须过专八，否则没有竞争力"
        },
        "prospects": {
            "trend": "AI翻译冲击基础翻译岗位，高端翻译仍有需求",
            "hot": "英语老师、翻译、外贸、涉外工作",
            "developing": "跨境电商、国际旅游、语言培训"
        },
        "career_advice": {
            "immediate": "必须过专八，最好有CATTI证书",
            "certifications": "专八（必须）、CATTI、雅思7.0+",
            "timeline": "大二下学期开始准备专八"
        },
        "learning_path": {
            "freshman": "打好基础，每天练习听说读写",
            "sophomore": "过四六级专四，找外教聊天",
            "junior": "准备专八，考CATTI三级",
            "senior": "确定方向，积累专业领域英语"
        },
        "zhang_reviews": {
            "pros": ["国际视野", "就业面广", "有留学优势"],
            "cons": ["AI冲击", "竞争激烈", "需要持续学习"],
            "summary": "英语是工具而非专业，必须结合其他技能"
        }
    },
    
    {
        "code": "050303",
        "name": "新闻学",
        "category": "05 文学",
        "category_icon": "📰",
        "difficulty": 3,
        "popularity": 4,
        "salary": {
            "description": "传统媒体低（约5000-8000元），新媒体高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但行业变革快",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习新闻采写编评和传播技能",
            "year1": "新闻学概论、传播学概论、采访写作",
            "year2": "新闻编辑、新闻摄影、电视摄像",
            "year3": "深度报道、新闻评论、新媒体运营",
            "year4": "毕业实习、毕业论文"
        },
        "suitable_for": {
            "traits": ["好奇心强", "善于交际", "反应快"],
            "skills": ["写作能力", "人际沟通能力", "抗压能力"],
            "warning": "媒体工作强度大，加班是常态"
        },
        "prospects": {
            "trend": "传统媒体衰落，新媒体和短视频崛起",
            "hot": "新媒体运营、记者、编辑、内容创作",
            "developing": "短视频制作、直播运营、品牌公关"
        },
        "career_advice": {
            "immediate": "运营自己的自媒体账号，建立作品集",
            "certifications": "记者证（想当记者必考）",
            "timeline": "大三开始实习积累作品"
        },
        "learning_path": {
            "freshman": "关注新闻热点，开始写稿投稿",
            "sophomore": "学新媒体技能，做自己的账号",
            "junior": "找媒体实习，积累作品",
            "senior": "确定方向，准备秋招"
        },
        "zhang_reviews": {
            "pros": ["能接触社会各层面", "成长快", "有成就感"],
            "cons": ["工作强度大", "薪资不稳定", "行业变动大"],
            "summary": "热爱新闻的人适合，追求稳定的不适合"
        }
    },
    
    # 07 理学类
    {
        "code": "070101",
        "name": "数学与应用数学",
        "category": "07 理学",
        "category_icon": "🔢",
        "difficulty": 5,
        "popularity": 4,
        "salary": {
            "description": "起薪约6000-20000元，取决于行业",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，跨行业能力强",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习数学理论、应用数学和计算方法",
            "year1": "数学分析、高等代数、解析几何",
            "year2": "常微分方程、概率论、数理统计",
            "year3": "实变函数、泛函分析、数值分析",
            "year4": "毕业论文、专业方向选修"
        },
        "suitable_for": {
            "traits": ["数学天赋", "逻辑思维强", "耐得住寂寞"],
            "skills": ["数学分析能力", "抽象思维能力", "编程能力（Python/MATLAB）"],
            "warning": "数学难，必须是真的喜欢，否则坚持不下去"
        },
        "prospects": {
            "trend": "数据科学AI火热，数学人才需求大增",
            "hot": "数据分析、算法工程师、金融量化",
            "developing": "人工智能、密码学、生物统计"
        },
        "career_advice": {
            "immediate": "学Python和机器学习，数学+编程是王炸组合",
            "certifications": "教师资格证（想当老师）、计算机等级证书",
            "timeline": "大二确定方向，开始针对性学习"
        },
        "learning_path": {
            "freshman": "学好数分高代，打好基础",
            "sophomore": "学编程，开始接触机器学习",
            "junior": "参加数学建模竞赛，找实习",
            "senior": "确定方向：读研/就业"
        },
        "zhang_reviews": {
            "pros": ["基础学科，跨专业容易", "薪资潜力大", "培养逻辑思维"],
            "cons": ["课程很难", "需要持续深造"],
            "summary": "数学好的人选这个专业很有优势"
        }
    },
    
    {
        "code": "070201",
        "name": "物理学",
        "category": "07 理学",
        "category_icon": "⚛️",
        "difficulty": 5,
        "popularity": 3,
        "salary": {
            "description": "基础学科收入一般，但跨行能力强",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率较高，但大部分需要读研读博",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习物质运动规律和基本结构",
            "year1": "力学、热学、电磁学、光学",
            "year2": "理论力学、量子力学、电动力学、热力学与统计物理",
            "year3": "固体物理、计算物理、实验物理",
            "year4": "毕业论文、毕业设计"
        },
        "suitable_for": {
            "traits": ["好奇心强", "逻辑思维强", "动手能力好"],
            "skills": ["数学物理方法", "实验技能", "编程能力"],
            "warning": "纯物理路线需要读博才能有成就"
        },
        "prospects": {
            "trend": "半导体、新能源等产业带动物理人才需求",
            "hot": "半导体、光电、新能源、科研",
            "developing": "量子计算、光电子、新材料"
        },
        "career_advice": {
            "immediate": "尽早确定方向：学术/工业界",
            "certifications": "教师资格证（想当老师）",
            "timeline": "大二开始进实验室"
        },
        "learning_path": {
            "freshman": "学好四大力学基础，数学要扎实",
            "sophomore": "进实验室参与科研，学编程",
            "junior": "参加科研项目，发论文",
            "senior": "确定方向：读研/就业"
        },
        "zhang_reviews": {
            "pros": ["培养科学思维", "跨行业能力强", "社会尊重"],
            "cons": ["学习难度大", "学术路线周期长"],
            "summary": "真正热爱物理的人适合，想快速就业的慎选"
        }
    },
    
    {
        "code": "071001",
        "name": "生物科学",
        "category": "07 理学",
        "category_icon": "🧬",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，需读研才有好发展",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率一般，科研路线需要高学历",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习生命科学的基础理论和实验技术",
            "year1": "普通生物学、生物化学、细胞生物学",
            "year2": "遗传学、微生物学、分子生物学",
            "year3": "植物学、动物学、生理学",
            "year4": "毕业论文、毕业实习"
        },
        "suitable_for": {
            "traits": ["热爱生命科学", "动手能力强", "有耐心"],
            "skills": ["实验操作能力", "观察能力", "数据分析能力"],
            "warning": "生物行业就业竞争激烈，必须读研"
        },
        "prospects": {
            "trend": "生物医药行业发展，生物专业就业有所改善",
            "hot": "生物医药、医疗器械、环保",
            "developing": "基因编辑、生物信息、合成生物学"
        },
        "career_advice": {
            "immediate": "必须读研究生，最好读博",
            "certifications": "教师资格证（想当老师）",
            "timeline": "大三开始准备考研"
        },
        "learning_path": {
            "freshman": "基础课程学好，进实验室参观",
            "sophomore": "进实验室参与科研项目",
            "junior": "确定研究方向，准备考研",
            "senior": "考研/保研"
        },
        "zhang_reviews": {
            "pros": ["生命科学是未来方向", "科研意义大"],
            "cons": ["学习周期长", "前期收入低"],
            "summary": "必须读研读博才能有好发展，短期就业不适合"
        }
    },
    
    {
        "code": "071101",
        "name": "心理学",
        "category": "07 理学",
        "category_icon": "🧠",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-12000元，行业差距大",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，心理咨询师需要经验积累",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习心理现象规律和心理服务技术",
            "year1": "普通心理学、实验心理学、心理统计",
            "year2": "发展心理学、社会心理学、变态心理学",
            "year3": "心理咨询与治疗、心理测量、人格心理学",
            "year4": "毕业论文、心理咨询实习"
        },
        "suitable_for": {
            "traits": ["善于倾听", "同理心强", "情绪稳定"],
            "skills": ["人际沟通能力", "洞察力", "情绪管理能力"],
            "warning": "心理咨询师前期收入低，需要长期积累"
        },
        "prospects": {
            "trend": "社会压力增大，心理健康需求上升",
            "hot": "心理咨询师、用户体验研究 HR",
            "developing": "在线心理咨询、心理测评、EAP"
        },
        "career_advice": {
            "immediate": "学咨询技术，积累个案经验",
            "certifications": "心理咨询师证（取消职业资格后可考协会认证）",
            "timeline": "大三开始接个案实习"
        },
        "learning_path": {
            "freshman": "读心理学经典著作，自我成长",
            "sophomore": "学心理统计和咨询技术",
            "junior": "开始接个案实习，督导成长",
            "senior": "确定方向：咨询/用户研究/HR"
        },
        "zhang_reviews": {
            "pros": ["帮助他人", "自我成长", "行业前景好"],
            "cons": ["前期积累期长", "收入增长慢"],
            "summary": "真正热爱心理学、能承受他人痛苦的人适合"
        }
    },
    
    {
        "code": "071201",
        "name": "统计学",
        "category": "07 理学",
        "category_icon": "📈",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "数据时代起薪高，约8000-20000元",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，数据人才需求大",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习数据收集、处理和分析的理论方法",
            "year1": "数学分析、高等代数、概率论",
            "year2": "数理统计、回归分析、时间序列",
            "year3": "多元统计、抽样调查、贝叶斯统计",
            "year4": "毕业论文、数据分析项目"
        },
        "suitable_for": {
            "traits": ["数学好", "对数据敏感", "细心耐心"],
            "skills": ["统计软件（R/Python/SAS）", "数据分析能力", "业务理解能力"],
            "warning": "必须会编程，纯理论不够用"
        },
        "prospects": {
            "trend": "数据科学时代，统计人才极度稀缺",
            "hot": "数据分析师、量化分析师、精算师",
            "developing": "数据科学、AI、风险管理"
        },
        "career_advice": {
            "immediate": "必须精通Python或R，会SQL",
            "certifications": "CDA数据分析师、Python编程证书",
            "timeline": "大二开始做数据分析项目"
        },
        "learning_path": {
            "freshman": "学好数学和统计理论",
            "sophomore": "学Python/R，开始做项目",
            "junior": "参加数据竞赛，找实习",
            "senior": "秋招，准备数据分析面试"
        },
        "zhang_reviews": {
            "pros": ["就业前景好", "薪资高", "跨行业容易"],
            "cons": ["需要持续学习新技术"],
            "summary": "数学好、会编程的人选这个专业很有优势"
        }
    },
    
    {
        "code": "080901",
        "name": "计算机科学与技术",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "起薪高，应届生白菜价15K+，sp可达30K+",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，2024年因AI竞争激烈度上升",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习软件硬件理论、软件开发与系统架构",
            "year1": "C语言、数据结构与算法、计算机导论、高等数学",
            "year2": "算法、数据库、操作系统、计算机网络",
            "year3": "软件工程、编译原理、选修AI/大数据/云计算",
            "year4": "项目实战、毕业设计、实习"
        },
        "suitable_for": {
            "traits": ["逻辑思维强", "对技术感兴趣", "能持续学习"],
            "skills": ["编程能力（至少精通一门语言）", "算法功底", "自学能力"],
            "warning": "必须持续学习，技术更新快，35岁危机存在"
        },
        "prospects": {
            "trend": "2024年AI算法岗竞争激烈，约100人竞争1个岗位，但开发岗仍需求大",
            "hot": "软件开发、算法工程师、产品经理",
            "developing": "人工智能、大数据、云计算、网络安全"
        },
        "career_advice": {
            "immediate": "大二必须刷算法题，大三暑假前拿到实习offer，建议3月份开始投递",
            "certifications": "软考、阿里云认证",
            "timeline": "大二下：刷题+项目；大三：实习；大四：秋招"
        },
        "learning_path": {
            "freshman": "学C语言，打好编程基础，过四级",
            "sophomore": "学数据结构算法，刷LeetCode，准备ACM",
            "junior": "实习+项目，面试算法",
            "senior": "秋招/考研，简历突出项目经验"
        },
        "zhang_reviews": {
            "pros": ["起薪高（应届生15K+）", "需求量大（每年校招数万人）", "技术更迭带来机会"],
            "cons": ["学习难度大", "35岁危机", "竞争激烈（尤其是AI方向）"],
            "summary": "数学逻辑好、能持续学习的人适合；数学不好慎选AI方向"
        }
    },
    
    {
        "code": "080717",
        "name": "人工智能",
        "category": "08 工学",
        "category_icon": "🤖",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "顶尖人才薪资极高，硕士应届可达30-50K",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "高端人才稀缺，但门槛极高",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习机器学习、深度学习、自然语言处理等AI核心技术",
            "year1": "高等数学、线性代数、概率论、Python编程",
            "year2": "机器学习、数据挖掘、TensorFlow/PyTorch",
            "year3": "深度学习、计算机视觉、自然语言处理、强化学习",
            "year4": "AI项目实战、顶会论文（大厂方向）、毕业设计"
        },
        "suitable_for": {
            "traits": ["数学极好", "对AI有热情", "能啃硬骨头"],
            "skills": ["数学（高数线代概率必须精通）", "Python编程", "英文阅读（看paper）"],
            "warning": "必须读研究生，本科生难以胜任AI岗位"
        },
        "prospects": {
            "trend": "2024年AI方向卷出天际，顶会论文+顶会比赛经验是入场券",
            "hot": "算法工程师、AI研究员、大模型",
            "developing": "大模型、AIGC具身智能"
        },
        "career_advice": {
            "immediate": "必须读研究生，争取发顶会paper",
            "certifications": "无硬性证书，但Kaggle比赛成绩很重要",
            "timeline": "大二进实验室，大三发论文，大四保研/考研"
        },
        "learning_path": {
            "freshman": "数学基础+Python，学吴恩达课程",
            "sophomore": "机器学习，进实验室打杂",
            "junior": "做AI项目，争取发论文",
            "senior": "保研/考研到AI强校"
        },
        "zhang_reviews": {
            "pros": ["薪资天花板极高", "改变世界的机会"],
            "cons": ["难度最高的专业之一", "必须读研", "竞争极其激烈"],
            "summary": "数学极好、极度热爱AI的人适合；只想赚钱的别来"
        }
    },
    
    {
        "code": "080701",
        "name": "电子信息工程",
        "category": "08 工学",
        "category_icon": "📡",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约6000-15000元，硬件方向稳定",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，制造业和科技公司需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习电子电路、信号处理和通信技术",
            "year1": "电路分析、模拟电路、数字电路、C语言",
            "year2": "信号与系统、数字信号处理、微机原理",
            "year3": "通信原理、嵌入式系统、电磁场与电磁波",
            "year4": "电子设计项目、毕业设计、实习"
        },
        "suitable_for": {
            "traits": ["动手能力强", "对硬件感兴趣", "细心耐心"],
            "skills": ["电路设计能力", "编程能力", "仪器使用能力"],
            "warning": "硬件学习周期长，需要实践经验"
        },
        "prospects": {
            "trend": "芯片产业受重视，电子人才需求增加",
            "hot": "华为、中兴、电子制造、通信",
            "developing": "半导体、5G/6G、物联网"
        },
        "career_advice": {
            "immediate": "参加电子设计竞赛，做实际项目",
            "certifications": "电工证、嵌入式工程师认证",
            "timeline": "大二开始做项目"
        },
        "learning_path": {
            "freshman": "电路基础+编程，画PCB板",
            "sophomore": "参加电子设计竞赛",
            "junior": "找对口实习，学嵌入式开发",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["技术门槛高", "稳定不易被替代", "芯片行业受重视"],
            "cons": ["学习难度大", "薪资不如CS高"],
            "summary": "硬件爱好者适合，想赚快钱的不如选CS"
        }
    },
    
    {
        "code": "080801",
        "name": "自动化",
        "category": "08 工学",
        "category_icon": "🤖",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约6000-12000元，工业应用广",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，工业4.0带动需求",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习自动控制原理、系统设计和智能技术",
            "year1": "电路基础、C语言、微积分、线性代数",
            "year2": "自动控制原理、数字电子技术、PLC编程",
            "year3": "运动控制、过程控制、机器人技术",
            "year4": "控制系统设计、毕业设计、实习"
        },
        "suitable_for": {
            "traits": ["喜欢控制系统", "动手能力强", "逻辑思维好"],
            "skills": ["编程能力", "系统设计能力", "PLC编程"],
            "warning": "需要软硬件结合，学习面广"
        },
        "prospects": {
            "trend": "工业4.0、智能制造带动自动化需求",
            "hot": "制造业、机器人公司、智能装备",
            "developing": "工业互联网、智能工厂、无人机"
        },
        "career_advice": {
            "immediate": "学PLC和单片机，做控制系统项目",
            "certifications": "PLC工程师认证",
            "timeline": "大二开始做项目"
        },
        "learning_path": {
            "freshman": "编程基础+电路基础",
            "sophomore": "学PLC和单片机",
            "junior": "参加机器人大赛，找实习",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["就业面广", "工业需求稳定", "技术积累价值高"],
            "cons": ["学习难度较大", "薪资不如CS高"],
            "summary": "工科里面比较均衡的专业"
        }
    },
    
    {
        "code": "080902",
        "name": "软件工程",
        "category": "08 工学",
        "category_icon": "🖥️",
        "difficulty": 4,
        "popularity": 5,
        "salary": {
            "description": "与CS类似，起薪约10-20K",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，互联网公司需求大",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习软件开发方法论和工程实践",
            "year1": "程序设计基础、数据结构、离散数学",
            "year2": "算法、数据库、软件工程概论、操作系统",
            "year3": "软件架构、Web开发、移动开发、测试",
            "year4": "企业实习、毕业项目"
        },
        "suitable_for": {
            "traits": ["喜欢编程", "逻辑思维好", "善于团队协作"],
            "skills": ["编程能力", "架构设计能力", "沟通能力"],
            "warning": "必须大量实践，只看书不够"
        },
        "prospects": {
            "trend": "互联网行业波动，但软件人才需求稳定",
            "hot": "互联网公司、外包公司、传统企业IT",
            "developing": "云计算、SaaS、企业数字化"
        },
        "career_advice": {
            "immediate": "做项目！做项目！做项目！",
            "certifications": "软考、阿里云认证",
            "timeline": "大二开始做完整项目"
        },
        "learning_path": {
            "freshman": "学编程，做小工具",
            "sophomore": "学主流框架，做完整项目",
            "junior": "实习+接私活积累经验",
            "senior": "秋招，简历突出项目经验"
        },
        "zhang_reviews": {
            "pros": ["就业好", "薪资高", "实践性强"],
            "cons": ["需要持续学习", "工作强度可能大"],
            "summary": "CS的亲兄弟，比CS更偏应用"
        }
    },
    
    {
        "code": "081001",
        "name": "土木工程",
        "category": "08 工学",
        "category_icon": "🏗️",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "施工方向起薪约5000-10000元，设计院更高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但行业下行压力增大",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习房屋建筑和基础设施的设计施工",
            "year1": "高等数学、理论力学、材料力学",
            "year2": "结构力学、混凝土结构设计原理、钢结构",
            "year3": "基础工程、土木工程施工、工程项目管理",
            "year4": "毕业设计、施工实习"
        },
        "suitable_for": {
            "traits": ["能吃苦", "空间想象能力", "身体素质好"],
            "skills": ["力学分析能力", "识图绘图能力", "现场协调能力"],
            "warning": "施工方向需要常驻工地，工作条件艰苦"
        },
        "prospects": {
            "trend": "2024年房地产行业低迷，新基建带来新机会",
            "hot": "施工企业、设计院、房地产公司",
            "developing": "装配式建筑、智能建造、城市更新"
        },
        "career_advice": {
            "immediate": "尽早去工地实习，了解行业",
            "certifications": "建造师（工作后考）、结构工程师",
            "timeline": "大三确定方向：施工/设计/甲方"
        },
        "learning_path": {
            "freshman": "力学基础，打好专业基础",
            "sophomore": "学专业核心课，去工地实习",
            "junior": "确定方向，考相关证书",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["就业稳定", "越老越值钱", "技术门槛高"],
            "cons": ["行业下行", "工地条件艰苦", "薪资增长慢"],
            "summary": "行业寒冬中，适合能吃苦、耐得住的人"
        }
    },
    
    {
        "code": "081301",
        "name": "建筑学",
        "category": "08 工学",
        "category_icon": "🏛️",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-12000元，需要熬资历",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，建筑行业整体承压",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习建筑设计理论和实践",
            "year1": "建筑素描、建筑水彩、建筑概论",
            "year2": "建筑设计原理、中外建筑史、建筑构造",
            "year3": "居住建筑设计、公共建筑设计、城市规划",
            "year4": "毕业设计、建筑事务所实习"
        },
        "suitable_for": {
            "traits": ["有审美", "有创造力", "能熬夜画图"],
            "skills": ["美术基础", "空间设计能力", "软件建模能力"],
            "warning": "需要美术基础，需要准备作品集"
        },
        "prospects": {
            "trend": "行业整体承压，但优秀建筑师仍然稀缺",
            "hot": "设计院、建筑事务所、房地产公司",
            "developing": "绿色建筑、智慧城市、历史建筑保护"
        },
        "career_advice": {
            "immediate": "做作品集！做作品集！做作品集！",
            "certifications": "注册建筑师（工作后考）",
            "timeline": "大三开始准备作品集"
        },
        "learning_path": {
            "freshman": "练手绘，打美术基础",
            "sophomore": "学建筑设计软件，做课程设计",
            "junior": "去设计院实习，完善作品集",
            "senior": "申请留学或秋招"
        },
        "zhang_reviews": {
            "pros": ["有成就感", "越老越值钱", "艺术与技术结合"],
            "cons": ["学习周期长", "前期收入低", "行业承压"],
            "summary": "真正热爱建筑的人适合，赚钱不是首要目标"
        }
    },
    
    {
        "code": "081801",
        "name": "车辆工程",
        "category": "08 工学",
        "category_icon": "🚗",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "新能源方向起薪高，约8000-18000元",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，新能源汽车带动需求",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习汽车设计、制造和新技术",
            "year1": "高等数学、机械制图、工程力学",
            "year2": "机械原理、汽车构造、发动机原理",
            "year3": "汽车理论、新能源汽车技术、智能网联汽车",
            "year4": "毕业设计、汽车企业实习"
        },
        "suitable_for": {
            "traits": ["热爱汽车", "动手能力强", "关注新技术"],
            "skills": ["机械设计能力", "汽车电子知识", "新能源技术"],
            "warning": "传统方向就业差，新能源方向前景好"
        },
        "prospects": {
            "trend": "2024年新能源汽车爆发，人才缺口大",
            "hot": "比亚迪、蔚来、小鹏等新能源车企",
            "developing": "自动驾驶、动力电池、智能座舱"
        },
        "career_advice": {
            "immediate": "往新能源和自动驾驶方向靠",
            "certifications": "汽车工程师认证",
            "timeline": "大三确定方向：传统/新能源/智能"
        },
        "learning_path": {
            "freshman": "机械基础，了解汽车结构",
            "sophomore": "学汽车构造，关注新能源技术",
            "junior": "去车企实习，学智能网联知识",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["新能源方向薪资高", "汽车行业稳定"],
            "cons": ["传统方向就业差", "地域限制（车企集中）"],
            "summary": "选对方向很重要，新能源和智能驾驶是未来"
        }
    },
    
    {
        "code": "082502",
        "name": "环境工程",
        "category": "08 工学",
        "category_icon": "🌿",
        "difficulty": 3,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，稳定型",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，环保政策带动需求",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习环境污染治理和环境管理",
            "year1": "普通化学、环境科学概论、环境监测",
            "year2": "水污染控制工程、大气污染控制工程",
            "year3": "固体废物处理、环境影响评价、环境管理",
            "year4": "毕业设计、环保企业实习"
        },
        "suitable_for": {
            "traits": ["关心环境", "有责任感", "动手能力"],
            "skills": ["化学实验能力", "工程设计能力", "政策理解能力"],
            "warning": "薪资相对不高，需要情怀"
        },
        "prospects": {
            "trend": "双碳目标带动，环保行业迎来发展机遇",
            "hot": "环保公司、环境监测、政府环保部门",
            "developing": "碳中和、污水处理、新能源环保"
        },
        "career_advice": {
            "immediate": "关注环保政策和双碳目标",
            "certifications": "环境影响评价工程师",
            "timeline": "大三确定方向"
        },
        "learning_path": {
            "freshman": "化学基础，了解环境问题",
            "sophomore": "学水气固处理技术",
            "junior": "去环保公司实习",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["行业前景好", "有社会意义", "政策支持"],
            "cons": ["薪资不高", "就业岗位有限"],
            "summary": "有环保情怀的人适合，赚钱不是首要目标"
        }
    },
    
    {
        "code": "083001",
        "name": "生物医学工程",
        "category": "08 工学",
        "category_icon": "🏥",
        "difficulty": 5,
        "popularity": 4,
        "salary": {
            "description": "起薪约6000-15000元，医疗器械方向高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，医疗器械行业发展迅速",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习医学与工程交叉的理论和应用",
            "year1": "高等数学、生物学基础、电路基础",
            "year2": "生理学、数字信号处理、医学影像学",
            "year3": "生物材料、医疗器械设计、嵌入式系统",
            "year4": "毕业设计、医疗器械企业实习"
        },
        "suitable_for": {
            "traits": ["对医学和工程都有兴趣", "学习能力强", "细心"],
            "skills": ["编程能力", "电子电路能力", "医学知识"],
            "warning": "交叉学科，需要学习多个领域知识"
        },
        "prospects": {
            "trend": "医疗器械国产替代加速，人才需求增加",
            "hot": "医疗器械公司、医院设备科、医疗AI",
            "developing": "手术机器人、AI诊断、可穿戴设备"
        },
        "career_advice": {
            "immediate": "学编程和嵌入式，确定细分方向",
            "certifications": "医疗器械工程师认证",
            "timeline": "大三确定方向"
        },
        "learning_path": {
            "freshman": "基础课程，确定医学还是工程方向",
            "sophomore": "学电子或编程，进实验室",
            "junior": "去医疗器械公司实习",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["交叉学科优势", "行业前景好", "不可替代性强"],
            "cons": ["学习难度大", "需要持续学习"],
            "summary": "真正热爱医工结合的人适合"
        }
    },
    
    {
        "code": "080703",
        "name": "通信工程",
        "category": "08 工学",
        "category_icon": "📱",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约6000-15000元，5G/6G带动需求",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，通信行业需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习通信原理、信号处理和通信系统",
            "year1": "电路分析、模拟电路、数字电路、信号与系统",
            "year2": "通信原理、数字信号处理、电磁场理论",
            "year3": "移动通信、光纤通信、卫星通信",
            "year4": "毕业设计、通信企业实习"
        },
        "suitable_for": {
            "traits": ["对通信技术感兴趣", "数学物理好", "逻辑思维强"],
            "skills": ["信号处理能力", "编程能力", "硬件设计能力"],
            "warning": "知识更新快，需要持续学习"
        },
        "prospects": {
            "trend": "5G商用推进，6G研发启动，通信人才需求稳定",
            "hot": "华为、中兴、移动运营商、通信设备商",
            "developing": "5G应用、卫星互联网、物联网"
        },
        "career_advice": {
            "immediate": "学FPGA和信号处理，确定细分方向",
            "certifications": "通信工程师认证",
            "timeline": "大三确定方向"
        },
        "learning_path": {
            "freshman": "电路基础+信号基础",
            "sophomore": "学通信原理，做通信项目",
            "junior": "去华为等企业实习",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["行业稳定", "技术门槛高", "不容易被替代"],
            "cons": ["学习难度大", "大公司集中"],
            "summary": "通信是基础设施，专业人才需求稳定"
        }
    },
    
    {
        "code": "080601",
        "name": "电气工程及其自动化",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-12000元，国家电网是主要去向",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，电网和电力设备需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习电力系统和电气控制技术",
            "year1": "高等数学、电路、电机学基础",
            "year2": "电磁场、电力系统分析、继电保护",
            "year3": "发电厂电气部分、电力电子技术、PLC",
            "year4": "毕业设计、电力企业实习"
        },
        "suitable_for": {
            "traits": ["对电气感兴趣", "动手能力强", "能适应倒班"],
            "skills": ["电气设计能力", "PLC编程", "电力系统分析"],
            "warning": "电网工作需要倒班或出差"
        },
        "prospects": {
            "trend": "新能源并网、新型电力系统带来新机遇",
            "hot": "国家电网、南方电网、电力设备商",
            "developing": "新能源发电、储能、智能电网"
        },
        "career_advice": {
            "immediate": "关注电网考试，大三开始准备",
            "certifications": "注册电气工程师（工作后考）",
            "timeline": "大三准备电网考试"
        },
        "learning_path": {
            "freshman": "电路电机基础",
            "sophomore": "电力系统分析，进电网实习",
            "junior": "准备电网考试",
            "senior": "电网考试/考研"
        },
        "zhang_reviews": {
            "pros": ["电网工作稳定", "福利好", "社会地位高"],
            "cons": ["考试竞争激烈", "晋升慢"],
            "summary": "想进体制内电网的人适合"
        }
    },
    
    {
        "code": "080202",
        "name": "机械设计制造及其自动化",
        "category": "08 工学",
        "category_icon": "🔧",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，需要经验积累",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但薪资增长慢",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习机械设计制造和自动化技术",
            "year1": "机械制图、工程力学、机械设计基础",
            "year2": "机械原理、材料力学、数控技术",
            "year3": "先进制造技术、机器人技术、液压传动",
            "year4": "毕业设计、机械企业实习"
        },
        "suitable_for": {
            "traits": ["喜欢机械", "动手能力强", "空间想象能力"],
            "skills": ["机械设计能力", "绘图能力", "数控编程"],
            "warning": "车间环境，需要从基层做起"
        },
        "prospects": {
            "trend": "智能制造带动，但传统机械薪资增长慢",
            "hot": "制造业企业、汽车厂、机械设备商",
            "developing": "智能制造、工业机器人、3D打印"
        },
        "career_advice": {
            "immediate": "学CAD/SolidWorks，做机械项目",
            "certifications": "机械工程师认证",
            "timeline": "大二开始做项目"
        },
        "learning_path": {
            "freshman": "机械制图基础",
            "sophomore": "学CAD/SolidWorks，做课程设计",
            "junior": "去机械企业实习",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["就业稳定", "越老越值钱", "技术积累价值高"],
            "cons": ["起薪不高", "工作环境一般"],
            "summary": "传统工科，适合能吃苦积累的人"
        }
    },
    
    # 10 医学类
    {
        "code": "100201",
        "name": "临床医学",
        "category": "10 医学",
        "category_icon": "🩺",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "规培期间低（3000-6000元），主治后显著提升",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但必须读研读博才有好发展",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习临床诊断治疗和医学实践",
            "year1": "人体解剖学、组织学与胚胎学、生物化学",
            "year2": "生理学、病理学、病理生理学、药理学",
            "year3": "诊断学、内科学、外科学、妇产科学",
            "year4": "内科学实习、外科学实习、毕业实习"
        },
        "suitable_for": {
            "traits": ["有爱心", "心理素质好", "学习能力强"],
            "skills": ["记忆能力（大量医学知识）", "动手能力（临床操作）", "沟通能力"],
            "warning": "培养周期极长：5年本科+3年硕士+3年博士+3年规培=14年"
        },
        "prospects": {
            "trend": "2024年医疗需求增加，医生社会地位和收入稳定",
            "hot": "三甲医院、医学科研、医学教育",
            "developing": "精准医疗、AI辅助诊断、远程医疗"
        },
        "career_advice": {
            "immediate": "必须读研读博，临床和科研要兼顾",
            "certifications": "执业医师资格证（必考）、规培证",
            "timeline": "本科5年+硕士3年+博士3年+规培3年=14年"
        },
        "learning_path": {
            "freshman": "医学基础课，打好基础",
            "sophomore": "基础医学课，开始接触临床",
            "junior": "临床实习，备考研究生",
            "senior": "实习+考研"
        },
        "zhang_reviews": {
            "pros": ["社会地位高", "越老越值钱", "帮助他人成就感强"],
            "cons": ["培养周期极长", "前期收入低", "工作强度大", "医患关系"],
            "summary": "真正热爱医学、能承受长期培养周期的人适合"
        }
    },
    
    {
        "code": "100301",
        "name": "口腔医学",
        "category": "10 医学",
        "category_icon": "🦷",
        "difficulty": 5,
        "popularity": 4,
        "salary": {
            "description": "独立执业后收入可观，牙医是金领职业",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，牙医需求大",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习口腔疾病诊断和治疗",
            "year1": "人体解剖学、生物化学、口腔解剖生理学",
            "year2": "口腔组织病理学、口腔颌面外科学",
            "year3": "口腔修复学、口腔内科学、口腔正畸学",
            "year4": "口腔科实习、毕业实习"
        },
        "suitable_for": {
            "traits": ["手巧", "有耐心", "审美能力"],
            "skills": ["动手操作能力", "空间想象能力", "沟通能力"],
            "warning": "需要持续学习新技术，种植牙等新技术收入高"
        },
        "prospects": {
            "trend": "口腔健康意识提升，牙医需求持续增长",
            "hot": "口腔医院、口腔诊所、综合医院口腔科",
            "developing": "种植牙、正畸、口腔美容"
        },
        "career_advice": {
            "immediate": "必须读研，动手能力要强",
            "certifications": "执业医师资格证、口腔专科医师证",
            "timeline": "本科5年+硕士/规培3年"
        },
        "learning_path": {
            "freshman": "医学基础课",
            "sophomore": "口腔基础课，练习操作",
            "junior": "口腔临床实习",
            "senior": "实习+考研"
        },
        "zhang_reviews": {
            "pros": ["收入高", "医患关系相对缓和", "可独立执业"],
            "cons": ["培养周期长", "需要动手能力"],
            "summary": "手巧、有耐心的人适合，是医学里收入较好的方向"
        }
    },
    
    {
        "code": "101101",
        "name": "护理学",
        "category": "10 医学",
        "category_icon": "💉",
        "difficulty": 3,
        "popularity": 4,
        "salary": {
            "description": "起薪约4000-8000元，编制内稳定",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率极高，护士缺口大",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习临床护理和护理管理",
            "year1": "人体解剖学、生理学、护理学基础",
            "year2": "内科护理学、外科护理学、儿科护理学",
            "year3": "妇产科护理学、急危重症护理学、精神科护理学",
            "year4": "护理实习、毕业实习"
        },
        "suitable_for": {
            "traits": ["有爱心", "耐心细心", "心理素质好"],
            "skills": ["护理操作能力", "沟通能力", "应急处理能力"],
            "warning": "夜班多，工作强度大"
        },
        "prospects": {
            "trend": "老龄化社会，护理需求持续增长",
            "hot": "医院护士、社区护士、养老机构",
            "developing": "老年护理、康复护理、家庭护士"
        },
        "career_advice": {
            "immediate": "必须考护士资格证",
            "certifications": "护士资格证（必考）、专科护士证",
            "timeline": "大三开始准备护士资格证考试"
        },
        "learning_path": {
            "freshman": "医学基础课+护理基础",
            "sophomore": "各科护理学",
            "junior": "临床实习",
            "senior": "考护士资格证，准备就业"
        },
        "zhang_reviews": {
            "pros": ["就业稳定", "需求量大", "白衣天使社会地位"],
            "cons": ["夜班多", "工作强度大", "医患关系"],
            "summary": "有爱心、能吃苦的人适合"
        }
    },
    
    {
        "code": "100701",
        "name": "药学",
        "category": "10 医学",
        "category_icon": "💊",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，研发方向需要高学历",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率较高，但研发需要硕博",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习药物研发、生产和使用",
            "year1": "无机化学、有机化学、分析化学",
            "year2": "生物化学、药物化学、药理学",
            "year3": "药剂学、药物分析、药事管理",
            "year4": "毕业实习、毕业论文"
        },
        "suitable_for": {
            "traits": ["化学好", "细心", "有耐心"],
            "skills": ["化学实验能力", "数据分析能力", "记忆力"],
            "warning": "研发需要读研读博，销售门槛低但压力大"
        },
        "prospects": {
            "trend": "创新药发展，药物研发人才需求增加",
            "hot": "药企、药店、医院药房、监管部门",
            "developing": "创新药、生物药、药物研发"
        },
        "career_advice": {
            "immediate": "确定方向：研发/生产/销售",
            "certifications": "执业药师证",
            "timeline": "大三确定方向"
        },
        "learning_path": {
            "freshman": "化学基础",
            "sophomore": "药学专业基础课",
            "junior": "去药企实习",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["医药行业稳定", "可做研发"],
            "cons": ["研发周期长", "薪资增长慢"],
            "summary": "研发需要高学历，销售门槛低"
        }
    },
    
    {
        "code": "101001",
        "name": "中医学",
        "category": "10 医学",
        "category_icon": "🏮",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约4000-8000元，名中医收入高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，需要经验积累",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习中医学理论和中医临床实践",
            "year1": "中医基础理论、中医诊断学、中药学",
            "year2": "方剂学、伤寒论、金匮要略",
            "year3": "中医内科学、针灸学、中医各家学说",
            "year4": "中医临床实习、毕业实习"
        },
        "suitable_for": {
            "traits": ["热爱中医", "古文基础", "有耐心"],
            "skills": ["记忆能力（大量经典）", "辨证论治能力", "沟通能力"],
            "warning": "成才周期长，需要跟师学习"
        },
        "prospects": {
            "trend": "国家支持中医发展，但竞争也增加",
            "hot": "中医院、中医诊所、养生机构",
            "developing": "中医现代化、中药研发、中医养生"
        },
        "career_advice": {
            "immediate": "拜师学艺，跟老中医抄方",
            "certifications": "中医执业医师证",
            "timeline": "大三开始跟师"
        },
        "learning_path": {
            "freshman": "中医基础+背诵经典",
            "sophomore": "中医经典+临床基础",
            "junior": "临床实习+跟师",
            "senior": "实习+考研"
        },
        "zhang_reviews": {
            "pros": ["越老越值钱", "国家政策支持", "可独立执业"],
            "cons": ["成才周期长", "现代医学竞争"],
            "summary": "真正热爱中医、愿意沉淀的人适合"
        }
    },
    
    # 11 管理学类
    {
        "code": "120201",
        "name": "工商管理",
        "category": "11 管理学",
        "category_icon": "📋",
        "difficulty": 3,
        "popularity": 5,
        "salary": {
            "description": "差距极大，起薪约5000-15000元",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但竞争激烈",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习企业运营管理的理论和实践",
            "year1": "管理学原理、经济学基础、会计学基础",
            "year2": "市场营销、人力资源管理、组织行为学",
            "year3": "战略管理、运营管理、财务管理",
            "year4": "毕业论文、企业实习"
        },
        "suitable_for": {
            "traits": ["善于交际", "有领导力", "综合能力强"],
            "skills": ["沟通协调能力", "商业思维", "数据分析能力"],
            "warning": "万金油专业，需要尽早确定方向"
        },
        "prospects": {
            "trend": "管理培训生竞争激烈，但管培生项目仍受欢迎",
            "hot": "管理培训生、管培生项目、企业管理岗位",
            "developing": "数字化管理、创业管理"
        },
        "career_advice": {
            "immediate": "尽早实习，确定方向：市场/HR/财务/运营",
            "certifications": "人力资源管理师、会计资格证",
            "timeline": "大二开始实习积累经验"
        },
        "learning_path": {
            "freshman": "了解商业世界，确定兴趣方向",
            "sophomore": "学专业基础课，开始实习",
            "junior": "深入方向，找管培生项目",
            "senior": "秋招，争取管培生offer"
        },
        "zhang_reviews": {
            "pros": ["就业面广", "综合能力培养"],
            "cons": ["不够专业", "竞争激烈"],
            "summary": "需要尽早确定方向，不能什么都学"
        }
    },
    
    {
        "code": "120203",
        "name": "会计学",
        "category": "11 管理学",
        "category_icon": "🧾",
        "difficulty": 4,
        "popularity": 5,
        "salary": {
            "description": "起薪约5000-10000元，注会持证后显著提升",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，会计人才需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习财务核算、审计和财务管理",
            "year1": "会计学原理、管理学、经济法",
            "year2": "财务会计、成本会计、管理会计",
            "year3": "审计学、财务管理、税法",
            "year4": "毕业论文、会计事务所/企业实习"
        },
        "suitable_for": {
            "traits": ["细心", "对数字敏感", "有原则性"],
            "skills": ["计算能力", "逻辑分析能力", "细心耐心"],
            "warning": "必须考CPA，否则很难有发展"
        },
        "prospects": {
            "trend": "会计电算化冲击基础岗位，高端会计仍稀缺",
            "hot": "企业财务、会计师事务所、金融机构",
            "developing": "管理会计、财务分析、CFO"
        },
        "career_advice": {
            "immediate": "必须考CPA，实习积累经验",
            "certifications": "CPA（必考）、ACCA（加分）",
            "timeline": "大三开始备考CPA"
        },
        "learning_path": {
            "freshman": "会计基础，打好专业基础",
            "sophomore": "学中级财务会计，开始备考CPA",
            "junior": "去会计事务所实习，备考CPA",
            "senior": "秋招，CPA过几门"
        },
        "zhang_reviews": {
            "pros": ["就业稳定", "越老越值钱", "可考CPA"],
            "cons": ["初级岗位竞争激烈", "AI冲击基础核算"],
            "summary": "CPA是硬道理，过了CPA前途光明"
        }
    },
    
    {
        "code": "120401",
        "name": "公共事业管理",
        "category": "11 管理学",
        "category_icon": "🏛️",
        "difficulty": 3,
        "popularity": 3,
        "salary": {
            "description": "体制内为主，起薪约5000-9000元",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率中等，考公是主要出路",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习公共部门管理和公共政策",
            "year1": "管理学原理、政治学基础、公共行政",
            "year2": "公共政策分析、公共部门人力资源管理",
            "year3": "公共事业管理、法律基础、公共关系",
            "year4": "毕业论文、公共部门实习"
        },
        "suitable_for": {
            "traits": ["关心公共事务", "有责任感", "善于沟通"],
            "skills": ["政策分析能力", "公文写作能力", "组织协调能力"],
            "warning": "就业不如想象中好，需要考公或考研"
        },
        "prospects": {
            "trend": "考公热门专业，但竞争激烈",
            "hot": "公务员、事业单位、公共部门",
            "developing": "公共政策、非营利组织管理"
        },
        "career_advice": {
            "immediate": "尽早准备考公或考研",
            "certifications": "人力资源管理师",
            "timeline": "大三开始备考"
        },
        "learning_path": {
            "freshman": "了解公共管理领域",
            "sophomore": "专业基础课，开始准备考公",
            "junior": "实习+备考",
            "senior": "考公/考研"
        },
        "zhang_reviews": {
            "pros": ["考公有优势", "稳定"],
            "cons": ["专业性不强", "就业面窄"],
            "summary": "适合想进体制内的人"
        }
    },
    
    {
        "code": "120202",
        "name": "市场营销",
        "category": "11 管理学",
        "category_icon": "📢",
        "difficulty": 3,
        "popularity": 4,
        "salary": {
            "description": "底薪低+提成，能力差异极大",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但淘汰率高",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习市场分析和营销策划",
            "year1": "管理学原理、经济学基础、市场营销学",
            "year2": "消费者行为学、市场调研、广告学",
            "year3": "营销策划、数字营销、品牌管理",
            "year4": "毕业论文、营销实战实习"
        },
        "suitable_for": {
            "traits": ["善于交际", "有创意", "抗压能力强"],
            "skills": ["沟通能力", "创意策划能力", "数据分析能力"],
            "warning": "销售岗位门槛低，但做好很难"
        },
        "prospects": {
            "trend": "数字营销兴起，短视频/直播带货成为新方向",
            "hot": "品牌策划、数字营销、销售管培生",
            "developing": "直播电商、私域运营、跨境营销"
        },
        "career_advice": {
            "immediate": "积累实战经验，有自己的案例",
            "certifications": "营销师认证",
            "timeline": "大二开始实习"
        },
        "learning_path": {
            "freshman": "营销基础课，开始做小生意/兼职",
            "sophomore": "学数字营销，运营自己的账号",
            "junior": "去营销公司实习",
            "senior": "秋招，有自己案例"
        },
        "zhang_reviews": {
            "pros": ["能者多得", "不看出身看能力"],
            "cons": ["不稳定", "淘汰率高"],
            "summary": "适合有冲劲、能承受压力的人"
        }
    },
    
    {
        "code": "120801",
        "name": "电子商务",
        "category": "11 管理学",
        "category_icon": "🛒",
        "difficulty": 3,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-12000元，运营岗位差异大",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，电商行业蓬勃发展",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习电子商务运营和技术",
            "year1": "管理学原理、经济学、电子商务概论",
            "year2": "网络经济学、网络营销、网页设计",
            "year3": "电商运营、数据分析、供应链管理",
            "year4": "毕业论文、电商企业实习"
        },
        "suitable_for": {
            "traits": ["对互联网感兴趣", "善于学习", "有商业思维"],
            "skills": ["运营能力", "数据分析能力", "沟通能力"],
            "warning": "行业变化快，需要持续学习"
        },
        "prospects": {
            "trend": "直播电商、短视频电商成为新趋势",
            "hot": "电商平台、直播电商、品牌电商",
            "developing": "跨境电商、私域电商、即时零售"
        },
        "career_advice": {
            "immediate": "运营自己的网店或账号，积累经验",
            "certifications": "电子商务师",
            "timeline": "大二开始做电商项目"
        },
        "learning_path": {
            "freshman": "电商基础，了解电商生态",
            "sophomore": "学运营技能，开始做项目",
            "junior": "去电商公司实习",
            "senior": "秋招，有成功案例"
        },
        "zhang_reviews": {
            "pros": ["行业前景好", "创业机会多"],
            "cons": ["变化快", "竞争激烈"],
            "summary": "适合有商业嗅觉、善于学习的人"
        }
    },
    
    {
        "code": "120601",
        "name": "物流管理",
        "category": "11 管理学",
        "category_icon": "📦",
        "difficulty": 3,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，供应链方向薪资高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，电商带动物流需求",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习物流运作和供应链管理",
            "year1": "管理学原理、经济学、物流学概论",
            "year2": "仓储管理、运输管理、供应链管理",
            "year3": "物流系统规划、国际物流、物流信息系统",
            "year4": "毕业论文、物流企业实习"
        },
        "suitable_for": {
            "traits": ["逻辑思维好", "细心", "能吃苦"],
            "skills": ["系统规划能力", "数据分析能力", "协调能力"],
            "warning": "物流基层工作条件艰苦"
        },
        "prospects": {
            "trend": "智慧物流、跨境物流发展迅速",
            "hot": "电商物流、快递公司、供应链公司",
            "developing": "智慧物流、跨境电商供应链"
        },
        "career_advice": {
            "immediate": "学供应链软件（SAP等）",
            "certifications": "供应链管理师",
            "timeline": "大三确定方向"
        },
        "learning_path": {
            "freshman": "物流基础课",
            "sophomore": "学供应链管理，进物流公司实习",
            "junior": "学物流信息系统",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["就业稳定", "行业需求大"],
            "cons": ["基层工作条件差", "薪资增长慢"],
            "summary": "供应链方向更有前景"
        }
    },
    
    {
        "code": "120901",
        "name": "旅游管理",
        "category": "11 管理学",
        "category_icon": "✈️",
        "difficulty": 3,
        "popularity": 3,
        "salary": {
            "description": "起薪约4000-8000元，服务行业特点",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但疫情后恢复中",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习旅游运营和管理",
            "year1": "旅游学概论、管理学、导游业务",
            "year2": "旅游经济学、酒店管理、景区管理",
            "year3": "旅游规划、会展管理、旅游市场营销",
            "year4": "毕业论文、旅游企业实习"
        },
        "suitable_for": {
            "traits": ["热爱旅游", "善于交际", "服务意识"],
            "skills": ["沟通能力", "组织协调能力", "外语能力"],
            "warning": "服务行业工作时间长，节假日不能休息"
        },
        "prospects": {
            "trend": "旅游复苏，但竞争激烈",
            "hot": "酒店、旅行社、景区、旅游电商",
            "developing": "文旅融合、定制旅游、旅游科技"
        },
        "career_advice": {
            "immediate": "考导游证，多实习积累经验",
            "certifications": "导游证（导游必考）",
            "timeline": "大二考导游证"
        },
        "learning_path": {
            "freshman": "旅游基础课，考导游证",
            "sophomore": "酒店/旅行社实习",
            "junior": "深入方向，准备就业",
            "senior": "秋招"
        },
        "zhang_reviews": {
            "pros": ["能到处玩", "行业复苏中"],
            "cons": ["薪资不高", "工作时间长"],
            "summary": "热爱旅游、能吃苦的人适合"
        }
    },
    
    {
        "code": "120204",
        "name": "财务管理",
        "category": "11 管理学",
        "category_icon": "💹",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-12000元， CFO路线薪资高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，企业财务需求稳定",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习企业财务和投融资管理",
            "year1": "会计学原理、管理学、财务学基础",
            "year2": "中级财务会计、财务管理、投资学",
            "year3": "公司金融、风险管理、财务报表分析",
            "year4": "毕业论文、财务实习"
        },
        "suitable_for": {
            "traits": ["对数字敏感", "细心", "有原则"],
            "skills": ["财务分析能力", "数据分析能力", "风险意识"],
            "warning": "需要考CPA或CFA才有好发展"
        },
        "prospects": {
            "trend": "企业合规要求提升，财务人才需求稳定",
            "hot": "企业财务、投资机构、金融机构",
            "developing": "财务数字化、CFO、风控"
        },
        "career_advice": {
            "immediate": "考CPA或CFA，积累实习经验",
            "certifications": "CPA、CFA",
            "timeline": "大三开始备考"
        },
        "learning_path": {
            "freshman": "财务基础，打好会计基础",
            "sophomore": "学财务分析，开始备考",
            "junior": "去金融或财务公司实习",
            "senior": "秋招"
        },
        "zhang_reviews": {
            "pros": ["企业必需", "越老越值钱", "可向CFO发展"],
            "cons": ["考证压力大", "AI冲击基础岗位"],
            "summary": "财务是企业的命脉，有真才实学的人有前途"
        }
    },
    
    {
        "code": "120103",
        "name": "工程管理",
        "category": "11 管理学",
        "category_icon": "🏗️",
        "difficulty": 4,
        "popularity": 4,
        "salary": {
            "description": "起薪约5000-12000元，甲方方向薪资高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，基建和房地产带动需求",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习工程项目的计划组织和管理",
            "year1": "管理学原理、工程制图、工程力学",
            "year2": "工程经济学、项目管理、工程合同管理",
            "year3": "工程造价、工程施工、工程监理",
            "year4": "毕业论文、工程项目实习"
        },
        "suitable_for": {
            "traits": ["综合能力强", "协调能力好", "能适应工地"],
            "skills": ["项目管理能力", "合同管理能力", "成本控制能力"],
            "warning": "需要去工地实践"
        },
        "prospects": {
            "trend": "基础设施建设稳定，但房地产下行",
            "hot": "房地产公司、施工企业、监理公司",
            "developing": "智慧工地、BIM、工程咨询"
        },
        "career_advice": {
            "immediate": "考建造师，学BIM",
            "certifications": "建造师（工作后考）",
            "timeline": "大三确定方向"
        },
        "learning_path": {
            "freshman": "工程基础+管理基础",
            "sophomore": "项目管理课，去工地实习",
            "junior": "学BIM，准备考证",
            "senior": "秋招或考研"
        },
        "zhang_reviews": {
            "pros": ["就业稳定", "越老越值钱"],
            "cons": ["工地条件艰苦", "房地产下行"],
            "summary": "甲方方向更有前景"
        }
    },
    
    # 12 艺术学类
    {
        "code": "130502",
        "name": "视觉传达设计",
        "category": "12 艺术学",
        "category_icon": "🎨",
        "difficulty": 3,
        "popularity": 4,
        "salary": {
            "description": "差距极大，5000-30000元不等",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但竞争激烈",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习视觉设计和创意表达",
            "year1": "素描、色彩、平面构成、设计概论",
            "year2": "字体设计、标志设计、包装设计",
            "year3": "品牌设计、UI设计、广告设计",
            "year4": "毕业设计、设计公司实习"
        },
        "suitable_for": {
            "traits": ["有审美", "有创意", "对设计感兴趣"],
            "skills": ["设计软件（PS/AI/AE）", "创意能力", "审美能力"],
            "warning": "作品集是就业的关键"
        },
        "prospects": {
            "trend": "UI设计、短视频设计需求增加",
            "hot": "设计公司、互联网公司、广告公司",
            "developing": "UI设计、品牌设计、插画"
        },
        "career_advice": {
            "immediate": "做作品集！做作品集！做作品集！",
            "certifications": "Adobe认证",
            "timeline": "大二开始做作品集"
        },
        "learning_path": {
            "freshman": "设计基础，练手绘",
            "sophomore": "学设计软件，做课程作品",
            "junior": "去设计公司实习，完善作品集",
            "senior": "秋招/春招"
        },
        "zhang_reviews": {
            "pros": ["能发挥创意", "可自己接单"],
            "cons": ["竞争激烈", "需要持续学习"],
            "summary": "作品集决定一切，没有好作品集找不到好工作"
        }
    },
    
    {
        "code": "130310",
        "name": "动画",
        "category": "12 艺术学",
        "category_icon": "🎬",
        "difficulty": 4,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-15000元，游戏动画高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率较高，游戏影视行业带动",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习动画制作和创意",
            "year1": "素描、色彩、动画概论、动画运动规律",
            "year2": "二维动画制作、三维动画基础、分镜头设计",
            "year3": "Maya/3ds Max深入、动画特效、后期合成",
            "year4": "毕业设计、动画公司实习"
        },
        "suitable_for": {
            "traits": ["热爱动画", "有想象力", "能熬夜"],
            "skills": ["动画制作能力", "软件操作能力", "艺术审美"],
            "warning": "需要作品集，身体要能熬夜"
        },
        "prospects": {
            "trend": "游戏动漫行业发展迅速，人才需求大",
            "hot": "游戏公司、动画公司、影视公司",
            "developing": "游戏动画、元宇宙内容、NFT"
        },
        "career_advice": {
            "immediate": "学Maya或Unity，做个人作品",
            "certifications": "软件认证",
            "timeline": "大二确定方向：2D/3D/游戏"
        },
        "learning_path": {
            "freshman": "动画基础，练手绘",
            "sophomore": "学动画软件，做短片",
            "junior": "确定方向，做作品",
            "senior": "秋招，有成熟作品"
        },
        "zhang_reviews": {
            "pros": ["能创作", "游戏行业薪资高"],
            "cons": ["加班多", "需要持续学习"],
            "summary": "热爱动画、能吃苦的人适合"
        }
    },
    
    {
        "code": "130201",
        "name": "音乐表演",
        "category": "12 艺术学",
        "category_icon": "🎵",
        "difficulty": 5,
        "popularity": 3,
        "salary": {
            "description": "不稳定，3000-30000元差距极大",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率一般，竞争激烈",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习音乐表演专业技能",
            "year1": "专业主课（钢琴/声乐/器乐）、乐理、视唱练耳",
            "year2": "专业主课、和声、作品分析",
            "year3": "专业主课、合唱/合奏、舞台表演",
            "year4": "毕业音乐会、艺术实践"
        },
        "suitable_for": {
            "traits": ["音乐天赋", "舞台表现力", "刻苦练习"],
            "skills": ["演奏/演唱能力", "音乐素养", "舞台经验"],
            "warning": "必须是真爱，否则坚持不下去"
        },
        "prospects": {
            "trend": "音乐教育、自媒体成为新出路",
            "hot": "乐团、音乐教育、音乐自媒体",
            "developing": "音乐教育、音乐治疗、音乐版权"
        },
        "career_advice": {
            "immediate": "多演出，积累舞台经验",
            "certifications": "教师资格证（想当老师）",
            "timeline": "大学期间多演出"
        },
        "learning_path": {
            "freshman": "专业主课，每天练习",
            "sophomore": "专业提升，参加比赛",
            "junior": "开始教学实践，尝试自媒体",
            "senior": "准备就业或考研"
        },
        "zhang_reviews": {
            "pros": ["能从事热爱的事业", "有艺术氛围"],
            "cons": ["竞争激烈", "收入不稳定"],
            "summary": "必须是真爱，否则尽早转行"
        }
    },
    
    # 金融类
    {
        "code": "020301",
        "name": "金融学",
        "category": "02 经济学",
        "category_icon": "💹",
        "difficulty": 5,
        "popularity": 5,
        "salary": {
            "description": "金融行业两极分化严重，头部机构应届30K+，基础岗位5K",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率高，但头部机构竞争极其激烈",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习金融机构、金融市场和金融工具",
            "year1": "微观经济学、宏观经济学、高等数学",
            "year2": "货币金融学、金融市场学、公司金融",
            "year3": "证券投资学、金融工程、风险管理",
            "year4": "毕业论文、金融机构实习"
        },
        "suitable_for": {
            "traits": ["数学好", "对金融感兴趣", "抗压能力强"],
            "skills": ["数学（必须精通）", "数据分析能力", "英语"],
            "warning": "头部机构竞争极其激烈，需要名校+证书+实习"
        },
        "prospects": {
            "trend": "2024年金融行业分化，头部机构难进",
            "hot": "投行、券商、基金、银行总行",
            "developing": "量化投资、金融科技、财富管理"
        },
        "career_advice": {
            "immediate": "必须考CFA/CPA，实习必须去头部机构",
            "certifications": "CFA、CPA、FRM",
            "timeline": "大二开始准备CFA，大三实习必须头部"
        },
        "learning_path": {
            "freshman": "金融基础课，学数学英语",
            "sophomore": "学CFA一级，找实习",
            "junior": "去头部机构实习，考证",
            "senior": "秋招，冲击头部"
        },
        "zhang_reviews": {
            "pros": ["顶尖机构薪资极高", "社会地位高"],
            "cons": ["竞争极其激烈", "头部难进", "工作强度大"],
            "summary": "名校+证书+实习三件套，缺一不可"
        }
    },
    
    {
        "code": "020303",
        "name": "保险学",
        "category": "02 经济学",
        "category_icon": "🛡️",
        "difficulty": 3,
        "popularity": 3,
        "salary": {
            "description": "起薪约5000-10000元，精算方向薪资高",
            "source": "暂无权威公开数据，仅供参考"
        },
        "employment_rate": {
            "description": "就业率较高，保险行业发展稳健",
            "source": "暂无权威公开数据"
        },
        "what_you_learn": {
            "summary": "学习保险理论和实务",
            "year1": "保险学概论、经济学基础、数学",
            "year2": "人身保险、财产保险、保险法",
            "year3": "精算基础、风险管理、保险营销",
            "year4": "毕业论文、保险企业实习"
        },
        "suitable_for": {
            "traits": ["数学好", "细心", "有耐心"],
            "skills": ["精算能力", "数据分析能力", "沟通能力"],
            "warning": "精算师是金领，但考试极难"
        },
        "prospects": {
            "trend": "保险行业转型，健康险、养老险发展",
            "hot": "保险公司、保险经纪、精算事务所",
            "developing": "健康险、养老险、保险科技"
        },
        "career_advice": {
            "immediate": "如果走精算方向，必须考精算师",
            "certifications": "精算师（SOA/CAA）",
            "timeline": "大三开始考精算"
        },
        "learning_path": {
            "freshman": "保险基础课+数学",
            "sophomore": "保险专业课，确定方向",
            "junior": "去保险公司实习",
            "senior": "秋招，精算方向继续考证"
        },
        "zhang_reviews": {
            "pros": ["精算师薪资高", "稳定"],
            "cons": ["精算考试难", "保险行业口碑一般"],
            "summary": "精算方向是金领，但需要通过极难的考试"
        }
    },
]


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
    
    skills_html = ''
    for skill in suitable.get('skills', []):
        skills_html += f'<span class="skill-tag">{skill}</span>'
    
    pros_list = ''.join([f'<li>{p}</li>' for p in reviews.get('pros', [])])
    cons_list = ''.join([f'<li>{c}</li>' for c in reviews.get('cons', [])])
    
    card = f'''
        <div class="major-card" id="card-{code}" data-category="{category}" onclick="toggleCard('{code}')">
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
            
            <p style="margin-top:10px;font-size:0.9em;color:rgba(255,255,255,0.7);">
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
                <div class="detail-content" style="color:#ffc107;">
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
                
                <div class="detail-title">⭐ 张雪峰点评</div>
                <div class="pros-cons">
                    <div class="pros-box">
                        <strong style="color:#38ef7d;">✅ 优点：</strong>
                        <ul style="padding-left:15px;margin-top:5px;">{pros_list}</ul>
                    </div>
                    <div class="cons-box">
                        <strong style="color:#f5576c;">❌ 缺点：</strong>
                        <ul style="padding-left:15px;margin-top:5px;">{cons_list}</ul>
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
    
    # 构建HTML，使用字符串替换避免CSS大括号冲突
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>专业星图 V2 - 真实、专业的大学生专业选择指南</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #fff;
            line-height: 1.8;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            text-align: center;
            padding: 60px 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
        }}
        
        header h1 {{
            font-size: 3em;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }}
        
        header p {{
            font-size: 1.2em;
            color: rgba(255,255,255,0.8);
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .stats-banner {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stat-label {{
            color: rgba(255,255,255,0.6);
            font-size: 0.9em;
        }}
        
        .filter-section {{
            background: rgba(255,255,255,0.05);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        
        .filter-title {{
            font-size: 1.2em;
            margin-bottom: 15px;
            color: rgba(255,255,255,0.9);
        }}
        
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .filter-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.1);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.95em;
        }}
        
        .filter-btn:hover {{
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }}
        
        .filter-btn.active {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }}
        
        .majors-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
        }}
        
        .major-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .major-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(102, 126, 234, 0.5);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .category-icon {{
            font-size: 2.5em;
        }}
        
        .major-name {{
            font-size: 1.4em;
            font-weight: bold;
        }}
        
        .major-code {{
            font-size: 0.85em;
            color: rgba(255,255,255,0.5);
        }}
        
        .difficulty-stars {{
            margin-top: 5px;
            color: #f5576c;
        }}
        
        .salary-tag {{
            display: inline-block;
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.85em;
            margin: 10px 0;
        }}
        
        .data-source-tag {{
            display: inline-block;
            background: rgba(255,193,7,0.2);
            color: #ffc107;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.75em;
            margin-left: 10px;
        }}
        
        .detail-section {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .detail-title {{
            font-size: 1em;
            color: #667eea;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .detail-content {{
            font-size: 0.9em;
            color: rgba(255,255,255,0.8);
            margin-bottom: 10px;
        }}
        
        .year-list {{
            list-style: none;
            padding-left: 15px;
        }}
        
        .year-list li {{
            margin: 5px 0;
            position: relative;
            padding-left: 15px;
        }}
        
        .year-list li::before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: #667eea;
        }}
        
        .pros-cons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        
        .pros-box, .cons-box {{
            padding: 10px;
            border-radius: 10px;
            font-size: 0.85em;
        }}
        
        .pros-box {{
            background: rgba(56, 239, 125, 0.1);
            border-left: 3px solid #38ef7d;
        }}
        
        .cons-box {{
            background: rgba(245, 87, 108, 0.1);
            border-left: 3px solid #f5576c;
        }}
        
        .summary-box {{
            background: rgba(102, 126, 234, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-style: italic;
            color: rgba(255,255,255,0.9);
        }}
        
        .skill-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 5px;
        }}
        
        .skill-tag {{
            background: rgba(255,255,255,0.1);
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.8em;
        }}
        
        .hidden {{
            display: none;
        }}
        
        .expanded .detail-section {{
            display: block;
        }}
        
        footer {{
            text-align: center;
            padding: 40px;
            color: rgba(255,255,255,0.5);
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .majors-grid {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 2em;
            }}
            
            .stats-banner {{
                gap: 30px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 专业星图 V2</h1>
            <p>真实、专业的大学生专业选择指南 - 基于2024年最新行业趋势<br>
            <span style="font-size:0.8em;color:#ffc107;">⚠️ 本网站薪资数据均为定性描述，不提供具体数字，数据仅供参考</span></p>
            
            <div class="stats-banner">
                <div class="stat-item">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">精选专业</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{categories}</div>
                    <div class="stat-label">学科门类</div>
                </div>
            </div>
        </header>
        
        <section class="filter-section">
            <div class="filter-title">📚 按学科筛选：</div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">全部专业</button>
                {filter_buttons}
            </div>
        </section>
        
        <div class="majors-grid" id="majorsGrid">
            {major_cards}
        </div>
        
        <footer>
            <p>专业星图 V2 | 数据来源：暂无权威公开数据，仅供参考</p>
            <p style="margin-top:10px;">⚠️ 本网站所有薪资、就业率等数据均为定性描述，不提供具体数字</p>
        </footer>
    </div>
    
    <script>
        let expandedCards = new Set();
        
        function toggleCard(code) {{
            const card = document.getElementById('card-' + code);
            if (expandedCards.has(code)) {{
                expandedCards.delete(code);
                card.classList.remove('expanded');
            }} else {{
                expandedCards.add(code);
                card.classList.add('expanded');
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
                if (category === 'all' || card.dataset.category === category) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}
        
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => filterMajors(btn.dataset.filter));
        }});
    </script>
</body>
</html>'''
    
    return html


def main():
    html = generate_html()
    
    output_path = '/workspace/major_starmap_v2.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 专业星图 V2 生成完成！")
    print(f"📊 共生成 {len(MAJORS_DATA)} 个专业")
    print(f"📁 输出文件：{output_path}")
    print(f"\n⚠️ 重要提示：")
    print(f"  - 所有薪资数据均为定性描述，不提供具体数字")
    print(f"  - 数据标记为'暂无权威公开数据，仅供参考'")
    print(f"  - 请打开 {output_path} 查看效果")


if __name__ == '__main__':
    main()
