#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 最终版 - 完整专业数据 + 新UI + 星空背景
"""

from typing import List, Dict, Any

MAJORS_DATA: List[Dict[str, Any]] = [
    {
        "code": "010101",
        "name": "哲学",
        "category": "01 哲学",
        "category_icon": "🎓",
        "difficulty": 4,
        "popularity": 2,
        "salary": {"description": "起薪约5000-8000元，学术路线前期收入较低", "source": "暂无权威公开数据，仅供参考"},
        "employment_rate": {"description": "就业率中等，对口就业率较低", "source": "暂无权威公开数据"},
        "what_you_learn": {"summary": "哲学专业学习如何思考、推理和论证", "year1": "中国哲学史、西方哲学史、逻辑学入门", "year2": "马克思主义哲学、伦理学、美学", "year3": "宗教学、科学技术哲学，专业原著选读", "year4": "毕业论文写作、哲学专题研讨"},
        "suitable_for": {"traits": ["喜欢深度思考", "对人生意义感兴趣", "耐得住寂寞"], "skills": ["阅读理解能力（大量原著）", "写作表达能力", "逻辑推理能力"], "warning": "需要长期积累，短期难以见成效"},
        "prospects": {"trend": "就业面较窄但稳定，哲学思维在管理咨询、公共政策等领域受重视", "hot": "公务员、编辑、教师", "developing": "智库研究员、文化产业"},
        "career_advice": {"immediate": "尽早确定方向：学术/教育/其他", "certifications": "教师资格证（想当老师必考）", "timeline": "大三开始准备考研或考公"},
        "learning_path": {"freshman": "读经典原著：论语、道德经、柏拉图对话录", "sophomore": "建立知识框架，写读书笔记", "junior": "参加读书会，尝试写学术论文", "senior": "确定方向：考研/考公/就业"},
        "zhang_reviews": {"pros": ["培养批判性思维：哲学训练逻辑推理能力，让人看问题更深刻", "考公优势明显：行测逻辑题和申论写作有天然优势", "能看透事物本质：哲学训练抽象思维能力", "学术地位独特：哲学家在学术界有崇高地位", "跨领域适应性强：思维方式迁移到各行各业"], "cons": ["对口工作稀少：纯哲学对口岗位非常有限", "起薪普遍较低：学术路线前期收入不高", "必须持续深造：本科就业竞争力弱，硕博是常态", "社会认可度有限：家长和雇主可能不理解哲学价值", "见效慢周期长：思维能力的提升需要长期积累"], "summary": "哲学专业适合真正热爱思考、对人生意义有追问的人。如果你想赚快钱、追求短期回报，哲学不适合你；但如果你愿意用四年时间培养批判性思维和深度思考能力，哲学是很好的通识教育。"}
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
        "what_you_learn": {"summary": "研究资源配置、经济发展和市场运行规律", "year1": "微积分、线性代数、政治经济学、微观经济学", "year2": "宏观经济学、统计学、概率论、计量经济学基础", "year3": "国际金融、货币银行学、财政学、计量经济学应用", "year4": "毕业论文，专业方向选修"},
        "suitable_for": {"traits": ["数学基础好", "对经济现象感兴趣", "逻辑思维强"], "skills": ["数学（微积分、概率统计必须精通）", "数据分析能力", "英语（看英文文献）"], "warning": "数学不好慎选，计量经济学需要较强数学基础"},
        "prospects": {"trend": "2024年经济形势复杂，但经济专业人才需求稳定", "hot": "银行、证券、咨询公司、四大", "developing": "数据分析、量化投资、公共政策"},
        "career_advice": {"immediate": "必须掌握Python或Stata进行数据分析", "certifications": "CFA（美国特许金融分析师）、CPA", "timeline": "大三暑假前拿到实习，大四准备秋招"},
        "learning_path": {"freshman": "学好数学和英语，了解经济学基本框架", "sophomore": "开始学计量经济学和数据分析工具", "junior": "参加数学建模竞赛，找第一份实习", "senior": "秋招/考研，简历突出实习和项目经验"},
        "zhang_reviews": {"pros": ["就业面极广：银行、证券、基金、咨询、四大都可以去", "金融行业认可度高：经济金融知识是入行必备", "培养商业思维：理解市场运行规律和经济现象", "考研/出国有优势：经济学是商科申请的基础学科", "考公热门专业：经济学考公岗位多，选择余地大"], "cons": ["数学要求极高：微积分、概率论、计量经济学都是难关", "竞争极其激烈：好岗位往往需要985/211背景", "顶尖岗位门槛高：投行、券商核心岗位需要研究生学历", "证书要求高：CFA、CPA等证书是加分项或必选项", "学习内容宽泛：什么都学但什么都不精"], "summary": "经济学是万金油专业，就业面广但竞争激烈。数学好是必要条件，数学不好的人学起来会很痛苦。选校很重要，985/211的经济学毕业生才有竞争力，普通院校的经济学就业一般。"}
    },
]

def add_university_recommendations():
    university_recs = {
        "哲学": {"chinese": ["北京大学", "复旦大学", "中国人民大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
        "经济学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Harvard", "LSE"]},
        "财政学": {"chinese": ["北京大学", "中国人民大学", "中央财经大学"], "foreign": ["Harvard", "LSE", "Columbia"]},
        "法学": {"chinese": ["中国人民大学", "北京大学", "中国政法大学"], "foreign": ["Harvard Law", "Yale Law", "Oxford"]},
        "教育学": {"chinese": ["北京师范大学", "华东师范大学", "南京师范大学"], "foreign": ["Harvard GSE", "Stanford GSE", "UCL"]},
        "汉语言文学": {"chinese": ["北京大学", "复旦大学", "南京大学"], "foreign": ["Harvard", "Oxford", "Yale"]},
        "英语": {"chinese": ["北京大学", "北京外国语大学", "上海外国语大学"], "foreign": ["Oxford", "Cambridge", "Harvard"]},
        "新闻学": {"chinese": ["中国人民大学", "复旦大学", "中国传媒大学"], "foreign": ["Columbia Journalism", "NYU", "USC"]},
        "数学与应用数学": {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["MIT", "Princeton", "Harvard"]},
        "物理学": {"chinese": ["北京大学", "清华大学", "南京大学"], "foreign": ["MIT", "Stanford", "Princeton"]},
        "计算机科学与技术": {"chinese": ["清华大学", "北京大学", "浙江大学"], "foreign": ["MIT", "Stanford", "CMU"]},
        "临床医学": {"chinese": ["北京协和医学院", "北京大学医学部", "复旦大学上海医学院"], "foreign": ["Johns Hopkins", "Harvard", "Mayo Clinic"]},
    }
    
    for major in MAJORS_DATA:
        name = major["name"]
        if name in university_recs:
            rec = university_recs[name]
        else:
            rec = {"chinese": ["北京大学", "清华大学", "复旦大学"], "foreign": ["Harvard", "MIT", "Oxford"]}
        major["chinese_top_universities"] = rec["chinese"]
        major["foreign_top_universities"] = rec["foreign"]


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
    chinese_unis = major.get("chinese_top_universities", [])
    foreign_unis = major.get("foreign_top_universities", [])
    
    skills_html = "".join(['<span class="skill-tag">' + s + '</span>' for s in suitable.get("skills", [])])
    pros_list = "".join(['<li>' + p + '</li>' for p in reviews.get("pros", [])])
    cons_list = "".join(['<li>' + c + '</li>' for c in reviews.get("cons", [])])
    chinese_unis_html = "".join(['<span class="uni-tag chinese">' + u + '</span>' for u in chinese_unis])
    foreign_unis_html = "".join(['<span class="uni-tag foreign">' + u + '</span>' for u in foreign_unis])
    traits_str = "、".join(suitable.get("traits", []))
    
    card = '''
        <div class="major-card" id="card-{code}" data-category="{category}" data-name="{name}" onclick="toggleCard(\'{code}\')">
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
                <div class="detail-content">{summary}</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{year1}</li>
                    <li><strong>大二：</strong>{year2}</li>
                    <li><strong>大三：</strong>{year3}</li>
                    <li><strong>大四：</strong>{year4}</li>
                </ul>
                
                <div class="detail-title">👤 适合人群</div>
                <div class="detail-content"><strong>特质：</strong>{traits}</div>
                <div class="detail-content"><strong>技能要求：</strong></div>
                <div class="skill-tags">{skills_html}</div>
                <div class="detail-content warning">⚠️ {warning}</div>
                
                <div class="detail-title">📈 前景展望</div>
                <div class="detail-content"><strong>趋势：</strong>{trend}</div>
                <div class="detail-content"><strong>热门去向：</strong>{hot}</div>
                <div class="detail-content"><strong>新兴方向：</strong>{developing}</div>
                
                <div class="detail-title">💼 就业建议</div>
                <div class="detail-content"><strong>立即行动：</strong>{immediate}</div>
                <div class="detail-content"><strong>证书建议：</strong>{certifications}</div>
                <div class="detail-content"><strong>时间线：</strong>{timeline}</div>
                
                <div class="detail-title">🛤️ 学习路径</div>
                <ul class="year-list">
                    <li><strong>大一：</strong>{l_freshman}</li>
                    <li><strong>大二：</strong>{l_sophomore}</li>
                    <li><strong>大三：</strong>{l_junior}</li>
                    <li><strong>大四：</strong>{l_senior}</li>
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
                    💬 总结：{review_summary}
                </div>
            </div>
        </div>
    '''.format(
        code=code, name=name, category=category, icon=icon, difficulty=difficulty,
        salary_desc=salary_desc, salary_source=salary_source, employment_desc=employment_desc,
        summary=what_learn.get("summary", ""),
        year1=what_learn.get("year1", ""), year2=what_learn.get("year2", ""),
        year3=what_learn.get("year3", ""), year4=what_learn.get("year4", ""),
        traits=traits_str,
        skills_html=skills_html,
        warning=suitable.get("warning", ""),
        trend=prospects.get("trend", ""), hot=prospects.get("hot", ""), developing=prospects.get("developing", ""),
        immediate=career.get("immediate", ""), certifications=career.get("certifications", ""), timeline=career.get("timeline", ""),
        l_freshman=learning.get("freshman", ""), l_sophomore=learning.get("sophomore", ""),
        l_junior=learning.get("junior", ""), l_senior=learning.get("senior", ""),
        chinese_unis_html=chinese_unis_html, foreign_unis_html=foreign_unis_html,
        pros_list=pros_list, cons_list=cons_list,
        review_summary=reviews.get("summary", "")
    )
    return card


def generate_filter_buttons(majors):
    categories = sorted(set([m["category"] for m in majors]))
    buttons = []
    for cat in categories:
        icon = next((m["category_icon"] for m in majors if m["category"] == cat), "📚")
        buttons.append('<button class="filter-btn" data-filter="' + cat + '">' + icon + ' ' + cat + '</button>')
    return "\n".join(buttons)


CSS = """
        :root {
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
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
            background: var(--surface);
            min-height: 100vh;
            color: var(--on-surface);
            line-height: 1.8;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        header {
            text-align: center;
            padding: 48px 40px;
            background: url("https://clipart-library.com/2023/39da0ff93cafedf4b04f229446c30978.jpg") center/cover no-repeat;
            border-radius: 24px;
            margin-bottom: 40px;
            box-shadow: 0 4px 24px var(--shadow);
            position: relative;
        }
        header::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 248, 245, 0.88);
            border-radius: 24px;
            z-index: 0;
        }
        header > * { position: relative; z-index: 1; }
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
        .search-section { background: var(--surface-container); padding: 24px 32px; border-radius: 20px; margin-bottom: 24px; box-shadow: 0 4px 24px var(--shadow); }
        .search-box { display: flex; gap: 12px; align-items: center; }
        .search-input { flex: 1; padding: 14px 20px; border: 2px solid var(--outline); border-radius: 16px; font-size: 16px; outline: none; transition: all 0.3s; background: #FFF1EA; }
        .search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.1); }
        .search-icon { font-size: 24px; color: var(--secondary); }
        .filter-section { background: var(--surface-container); padding: 28px 32px; border-radius: 20px; margin-bottom: 32px; box-shadow: 0 4px 24px var(--shadow); }
        .filter-title { font-family: "Literata", serif; font-size: 20px; font-weight: 600; margin-bottom: 16px; color: var(--secondary); }
        .filter-buttons { display: flex; flex-wrap: wrap; gap: 10px; }
        .filter-btn { padding: 10px 20px; border: 2px solid var(--outline); border-radius: 9999px; background: transparent; color: var(--secondary); cursor: pointer; transition: all 0.3s; font-size: 14px; font-weight: 500; }
        .filter-btn:hover { background: var(--secondary-container); transform: translateY(-2px); }
        .filter-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
        .majors-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }
        .major-card { background: var(--surface-container); border-radius: 20px; padding: 28px; transition: all 0.3s; cursor: pointer; border: 2px solid var(--outline); box-shadow: 0 4px 24px var(--shadow); }
        .major-card:hover { transform: translateY(-4px); box-shadow: 0 8px 40px var(--shadow); border-color: var(--primary); }
        .card-header { display: flex; align-items: center; gap: 16px; margin-bottom: 18px; }
        .category-icon { font-size: 32px; background: var(--primary-container); width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; border-radius: 16px; }
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
        .summary-box { background: var(--secondary-container); padding: 20px; border-radius: 16px; margin-top: 20px; color: var(--on-surface); font-size: 14px; line-height: 1.8; }
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
        @media (max-width: 768px) { .majors-grid { grid-template-columns: 1fr; } header { padding: 32px 24px; } header h1 { font-size: 28px; } .stats-banner { gap: 40px; } .container { padding: 20px; } .pros-cons { grid-template-columns: 1fr; } }
"""

JAVASCRIPT = """
        let expandedCards = new Set();
        function toggleCard(code) {
            const card = document.getElementById("card-" + code);
            if (expandedCards.has(code)) {
                expandedCards.delete(code);
                card.classList.remove("expanded");
                const detail = card.querySelector(".detail-section");
                if (detail) detail.classList.add("hidden");
            } else {
                expandedCards.add(code);
                card.classList.add("expanded");
                const detail = card.querySelector(".detail-section");
                if (detail) detail.classList.remove("hidden");
            }
        }
        function filterMajors(category) {
            document.querySelectorAll(".filter-btn").forEach(btn => {
                btn.classList.remove("active");
                if (btn.dataset.filter === category) btn.classList.add("active");
            });
            document.querySelectorAll(".major-card").forEach(card => {
                if (category === "all" || card.dataset.category === category) card.classList.remove("hidden");
                else card.classList.add("hidden");
            });
        }
        function searchMajors(query) {
            const searchTerm = query.toLowerCase().trim();
            document.querySelectorAll(".major-card").forEach(card => {
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                if (name.includes(searchTerm) || category.includes(searchTerm)) card.classList.remove("hidden");
                else card.classList.add("hidden");
            });
        }
        document.querySelectorAll(".filter-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                document.getElementById("searchInput").value = "";
                filterMajors(btn.dataset.filter);
            });
        });
        document.getElementById("searchInput").addEventListener("input", (e) => searchMajors(e.target.value));
"""


def main():
    add_university_recommendations()
    total = len(MAJORS_DATA)
    categories = len(set([m["category"] for m in MAJORS_DATA]))
    filter_buttons = generate_filter_buttons(MAJORS_DATA)
    major_cards = "".join([generate_major_card(m) for m in MAJORS_DATA])
    
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>专业星图 - 温暖、专业的大学专业选择指南</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
""" + CSS + """
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
                    <div class="stat-number">""" + str(total) + """</div>
                    <div class="stat-label">专业收录</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">""" + str(categories) + """</div>
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
                """ + filter_buttons + """
            </div>
        </section>
        
        <div class="majors-grid" id="majorsGrid">
            """ + major_cards + """
        </div>
        
        <footer>
            <p>专业星图 · 温暖的专业指南</p>
            <p style="margin-top:8px;font-size:13px;">数据仅供参考 · 请结合自身情况选择</p>
        </footer>
    </div>
    
    <script>
""" + JAVASCRIPT + """
    </script>
</body>
</html>"""
    
    output_path = "/workspace/major_starmap_with_stars.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 专业星图（带星空背景）生成完成！")
    print(f"📊 共生成 {total} 个专业")
    print(f"🖼️ Header已添加星空插画背景")
    print(f"📁 输出文件：{output_path}")
    print(f"\n图片信息：")
    print(f"  - 主题：星空插画")
    print(f"  - 尺寸：455×735 像素")
    print(f"  - 来源：clipart-library.com")


if __name__ == "__main__":
    main()
