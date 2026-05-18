#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 - 模态框版本（简化版）
"""
import json
import re

# 读取数据
with open('generate_merged.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 UNIVERSITY_RECOMMENDATIONS
uni_start = content.find('UNIVERSITY_RECOMMENDATIONS')
uni_end = content.find('}', content.find('}', uni_start + 20) + 1)
uni_data = content[uni_start:uni_end + 1]

# 提取 get_default_recommendations
func_start = content.find('def get_default_recommendations')
func_end = content.find('def add_university_recommendations', func_start)
func_data = content[func_start:func_end]

# 提取 add_university_recommendations
add_start = content.find('def add_university_recommendations')
add_end = content.find('def generate_major_card', add_start)
add_func = content[add_start:add_end]

# 找到 MAJORS_DATA 的开始和结束
majors_start = content.find('MAJORS_DATA')
majors_end = content.find('def generate_major_card', majors_start)
majors_content = content[majors_start:majors_end]

# 确保变量正确定义
exec(majors_content)
exec(uni_data)
exec(func_data)
exec(add_func)

def generate_major_card_simple(major):
    code = major["code"]
    name = major["name"]
    category = major["category"]
    icon = major["category_icon"]
    difficulty = "★" * major["difficulty"] + "☆" * (5 - major["difficulty"])
    salary_desc = major["salary"]["description"]
    salary_source = major["salary"]["source"]
    employment_desc = major["employment_rate"]["description"]
    
    return f'''
        <div class="major-card" data-category="{category}" data-name="{name}" onclick="openModal('{code}')">
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
        </div>
    '''

def generate_modal_html(major):
    code = major["code"]
    name = major["name"]
    icon = major["category_icon"]
    difficulty = "★" * major["difficulty"] + "☆" * (5 - major["difficulty"])
    what_learn = major["what_you_learn"]
    suitable = major["suitable_for"]
    prospects = major["prospects"]
    career = major["career_advice"]
    learning = major["learning_path"]
    reviews = major["zhang_reviews"]
    chinese_unis = major.get("chinese_top_universities", [])
    foreign_unis = major.get("foreign_top_universities", [])
    
    skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in suitable.get("skills", [])])
    pros_list = "".join([f'<li>{p}</li>' for p in reviews.get("pros", [])])
    cons_list = "".join([f'<li>{c}</li>' for c in reviews.get("cons", [])])
    chinese_unis_html = "".join([f'<span class="uni-tag chinese">{u}</span>' for u in chinese_unis])
    foreign_unis_html = "".join([f'<span class="uni-tag foreign">{u}</span>' for u in foreign_unis])
    
    return f'''
        <div id="modal-{code}" class="modal" style="display: none;">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title">
                        <span class="category-icon">{icon}</span>
                        <div>
                            <h2>{name}</h2>
                            <div class="difficulty-stars">难度：{difficulty}</div>
                        </div>
                    </div>
                    <button class="modal-close" onclick="closeModal('{code}')">✕</button>
                </div>
                <div class="modal-body">
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
                    <div class="summary-box">💬 总结：{reviews.get("summary", "")}</div>
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
    add_university_recommendations()
    total = len(MAJORS_DATA)
    categories = len(set([m["category"] for m in MAJORS_DATA]))
    filter_buttons = generate_filter_buttons(MAJORS_DATA)
    major_cards = "".join([generate_major_card_simple(m) for m in MAJORS_DATA])
    modals = "".join([generate_modal_html(m) for m in MAJORS_DATA])
    
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
            --on-primary: #FFFFFF;
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
        .stats-banner {{ display: flex; justify-content: center; gap: 64px; margin: 40px 0 24px; flex-wrap: wrap; }}
        .stat-item {{ text-align: center; }}
        .stat-number {{ font-family: "Literata", serif; font-size: 40px; font-weight: 700; color: var(--primary); line-height: 1.2; }}
        .stat-label {{ color: var(--on-surface-variant); font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}
        .search-section {{ background: var(--surface-container); padding: 24px 32px; border-radius: 20px; margin-bottom: 24px; box-shadow: 0 4px 24px var(--shadow); }}
        .search-box {{ display: flex; gap: 12px; align-items: center; }}
        .search-input {{ flex: 1; padding: 14px 20px; border: 2px solid var(--outline); border-radius: 16px; font-size: 16px; outline: none; background: #FFF1EA; }}
        .search-input:focus {{ border-color: var(--primary); box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.1); }}
        .search-icon {{ font-size: 24px; color: var(--secondary); }}
        .filter-section {{ background: var(--surface-container); padding: 28px 32px; border-radius: 20px; margin-bottom: 32px; box-shadow: 0 4px 24px var(--shadow); }}
        .filter-title {{ font-family: "Literata", serif; font-size: 20px; font-weight: 600; margin-bottom: 16px; color: var(--secondary); }}
        .filter-buttons {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .filter-btn {{ padding: 10px 20px; border: 2px solid var(--outline); border-radius: 9999px; background: transparent; color: var(--secondary); cursor: pointer; font-size: 14px; font-weight: 500; }}
        .filter-btn:hover {{ background: var(--secondary-container); transform: translateY(-2px); }}
        .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        .majors-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }}
        .major-card {{ background: var(--surface-container); border-radius: 20px; padding: 28px; cursor: pointer; border: 2px solid var(--outline); box-shadow: 0 4px 24px var(--shadow); }}
        .major-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 40px var(--shadow); border-color: var(--primary); }}
        .card-header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 18px; }}
        .category-icon {{ font-size: 32px; background: var(--primary-container); width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; border-radius: 16px; }}
        .major-name {{ font-family: "Literata", serif; font-size: 24px; font-weight: 600; color: var(--secondary); }}
        .major-code {{ font-size: 12px; color: var(--on-surface-variant); font-weight: 500; margin-top: 4px; }}
        .difficulty-stars {{ margin-top: 8px; color: var(--primary); font-size: 14px; }}
        .salary-tag {{ display: inline-block; background: var(--primary-container); color: var(--secondary); padding: 6px 16px; border-radius: 9999px; font-size: 13px; font-weight: 500; margin: 12px 0; }}
        .data-source-tag {{ display: inline-block; background: var(--secondary-container); color: var(--secondary); padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 500; margin-left: 10px; }}
        .employment-desc {{ margin-top: 10px; font-size: 0.9em; color: var(--on-surface-variant); }}
        .modal {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 9999; overflow-y: auto; padding: 20px; }}
        .modal-content {{ background: var(--surface-container); max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto; border-radius: 24px; box-shadow: 0 8px 48px rgba(0, 0, 0, 0.1); }}
        .modal-header {{ display: flex; justify-content: space-between; align-items: center; padding: 24px; border-bottom: 1px solid var(--outline); position: sticky; top: 0; background: var(--surface-container); z-index: 10; }}
        .modal-title {{ display: flex; align-items: center; gap: 16px; }}
        .modal-title h2 {{ font-family: "Literata", serif; font-size: 28px; font-weight: 700; color: var(--secondary); margin: 0; }}
        .modal-close {{ background: var(--secondary-container); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 24px; cursor: pointer; color: var(--secondary); }}
        .modal-close:hover {{ background: var(--primary); color: white; }}
        .modal-body {{ padding: 32px; }}
        .detail-title {{ font-family: "Literata", serif; font-size: 18px; font-weight: 600; color: var(--secondary); margin-bottom: 12px; margin-top: 24px; display: flex; align-items: center; gap: 8px; }}
        .detail-title:first-child {{ margin-top: 0; }}
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
        .skill-tags, .uni-tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
        .skill-tag, .uni-tag {{ padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 500; }}
        .skill-tag {{ background: var(--secondary-container); color: var(--secondary); }}
        .uni-tag.chinese {{ background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }}
        .uni-tag.foreign {{ background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }}
        .uni-section {{ margin-bottom: 12px; }}
        .uni-label {{ color: var(--secondary); }}
        .warning {{ color: #c05621 !important; }}
        footer {{ text-align: center; padding: 48px 20px; color: var(--on-surface-variant); font-size: 14px; margin-top: 48px; border-top: 1px solid var(--outline); }}
        @media (max-width: 768px) {{ 
            .majors-grid {{ grid-template-columns: 1fr; }} 
            .modal {{ padding: 10px; }}
            .modal-content {{ max-height: 95vh; }}
            .pros-cons {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>专业星图</h1>
            <p>温暖、专业的大学专业选择指南 · 帮助你找到最适合的专业</p>
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
        </footer>
    </div>
    
    {modals}
    
    <script>
        let currentModal = null;
        
        function openModal(code) {{
            document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
            const modal = document.getElementById('modal-' + code);
            if (modal) {{
                modal.style.display = 'flex';
                currentModal = code;
                document.body.style.overflow = 'hidden';
            }}
        }}
        
        function closeModal(code) {{
            const modal = document.getElementById('modal-' + code);
            if (modal) {{
                modal.style.display = 'none';
                currentModal = null;
                document.body.style.overflow = '';
            }}
        }}
        
        document.querySelectorAll('.modal').forEach(modal => {{
            modal.addEventListener('click', function(e) {{
                if (e.target === modal && currentModal) {{
                    closeModal(currentModal);
                }}
            }});
        }});
        
        function filterMajors(category) {{
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.dataset.filter === category) btn.classList.add('active');
            }});
            document.querySelectorAll('.major-card').forEach(card => {{
                if (category === 'all' || card.dataset.category === category) card.classList.remove('hidden');
                else card.classList.add('hidden');
            }});
        }}
        
        function searchMajors(query) {{
            const searchTerm = query.toLowerCase().trim();
            document.querySelectorAll('.major-card').forEach(card => {{
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                if (name.includes(searchTerm) || category.includes(searchTerm)) card.classList.remove('hidden');
                else card.classList.add('hidden');
            }});
        }}
        
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.getElementById('searchInput').value = '';
                filterMajors(btn.dataset.filter);
            }});
        }});
        
        document.getElementById('searchInput').addEventListener('input', (e) => searchMajors(e.target.value));
    </script>
</body>
</html>'''
    
    output_path = "/workspace/major_starmap_modal.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 专业星图 模态框版 生成完成！")
    print(f"📊 共生成 {total} 个专业")
    print(f"🎓 每个专业都包含国内外TOP3名校推荐")
    print(f"🔍 搜索功能正常")
    print(f"💬 使用模态框显示详情")
    print(f"📁 输出文件：{output_path}")

if __name__ == "__main__":
    main()
