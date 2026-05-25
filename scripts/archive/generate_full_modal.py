#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成完整的模态框版本专业星图"""

# 读取文件
with open('generate_merged.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到MAJORS_DATA的开始
start_idx = None
for i, line in enumerate(lines):
    if 'MAJORS_DATA' in line and '=' in line:
        start_idx = i
        break

# 找到def generate_major_card的位置（结束标记）
end_idx = None
for i, line in enumerate(lines):
    if 'def generate_major_card' in line:
        end_idx = i
        break

if start_idx and end_idx:
    majors_lines = lines[start_idx:end_idx]
    majors_code = ''.join(majors_lines)
    
    # 执行提取的数据
    local_vars = {}
    exec(majors_code, {}, local_vars)
    MAJORS_DATA = local_vars.get('MAJORS_DATA', [])
    
    print(f"成功读取 {len(MAJORS_DATA)} 个专业")
    
    # 生成HTML
    html_parts = []
    
    # HTML头部
    html_parts.append(f'''<!DOCTYPE html>
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
        header p {{ font-size: 16px; color: var(--on-surface-variant); max-width: 800px; margin: 0 auto; }}
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
        .filter-btn {{ padding: 10px 20px; border: 2px solid var(--outline); border-radius: 9999px; background: transparent; color: var(--secondary); cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.3s; }}
        .filter-btn:hover {{ background: var(--secondary-container); transform: translateY(-2px); }}
        .filter-btn.active {{ background: var(--primary); color: var(--on-primary); border-color: var(--primary); }}
        .majors-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }}
        .major-card {{ background: var(--surface-container); border-radius: 20px; padding: 28px; cursor: pointer; border: 2px solid var(--outline); box-shadow: 0 4px 24px var(--shadow); transition: all 0.3s; }}
        .major-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 40px var(--shadow); border-color: var(--primary); }}
        .card-header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 18px; }}
        .category-icon {{ font-size: 32px; background: var(--primary-container); width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; border-radius: 16px; }}
        .major-name {{ font-family: "Literata", serif; font-size: 24px; font-weight: 600; color: var(--secondary); }}
        .major-code {{ font-size: 12px; color: var(--on-surface-variant); font-weight: 500; margin-top: 4px; }}
        .difficulty-stars {{ margin-top: 8px; color: var(--primary); font-size: 14px; }}
        .salary-tag {{ display: inline-block; background: var(--primary-container); color: var(--secondary); padding: 6px 16px; border-radius: 9999px; font-size: 13px; font-weight: 500; margin: 12px 0; }}
        .data-source-tag {{ display: inline-block; background: var(--secondary-container); color: var(--secondary); padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 500; margin-left: 10px; }}
        .employment-desc {{ margin-top: 10px; font-size: 0.9em; color: var(--on-surface-variant); }}
        
        /* 模态框样式 */
        .modal {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); display: none; align-items: center; justify-content: center; z-index: 9999; overflow-y: auto; padding: 20px; }}
        .modal.show {{ display: flex; }}
        .modal-content {{ background: var(--surface-container); max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto; border-radius: 24px; box-shadow: 0 8px 48px rgba(0, 0, 0, 0.1); }}
        .modal-header {{ display: flex; justify-content: space-between; align-items: center; padding: 24px; border-bottom: 1px solid var(--outline); position: sticky; top: 0; background: var(--surface-container); z-index: 10; }}
        .modal-title {{ display: flex; align-items: center; gap: 16px; }}
        .modal-title h2 {{ font-family: "Literata", serif; font-size: 28px; font-weight: 700; color: var(--secondary); margin: 0; }}
        .modal-close {{ background: var(--secondary-container); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 24px; cursor: pointer; color: var(--secondary); transition: all 0.3s; }}
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
        
        /* CTA按钮样式 */
        .cta-section { margin-top: 32px; text-align: center; }
        .cta-button { 
            background: linear-gradient(135deg, #E67E22 0%, #D35400 100%);
            color: white;
            border: none;
            padding: 16px 48px;
            border-radius: 9999px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 20px rgba(230, 126, 34, 0.4);
        }
        .cta-button:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 6px 30px rgba(230, 126, 34, 0.5);
        }
        
        /* 预热模态框 */
        .preheat-modal { 
            position: fixed; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            background: rgba(0, 0, 0, 0.6); 
            display: none; 
            align-items: center; 
            justify-content: center; 
            z-index: 10000; 
            overflow-y: auto; 
            padding: 20px; 
        }
        .preheat-modal.show { display: flex; }
        .preheat-content { 
            background: var(--surface-container); 
            max-width: 600px; 
            width: 100%; 
            border-radius: 24px; 
            padding: 48px; 
            text-align: center;
            position: relative;
        }
        .preheat-icon { font-size: 72px; margin-bottom: 24px; }
        .preheat-title { 
            font-family: "Literata", serif; 
            font-size: 28px; 
            font-weight: 700; 
            color: var(--secondary); 
            margin-bottom: 16px; 
        }
        .preheat-desc { 
            font-size: 16px; 
            color: var(--on-surface-variant); 
            margin-bottom: 32px; 
            line-height: 1.8;
        }
        .preheat-features { 
            text-align: left; 
            margin-bottom: 32px; 
            padding-left: 20px;
        }
        .preheat-features li { 
            margin: 12px 0; 
            font-size: 15px; 
            color: var(--on-surface);
        }
        .preheat-features li::before { 
            content: "✅"; 
            margin-right: 12px;
        }
        .preheat-email {
            margin-bottom: 32px;
        }
        .preheat-email input {
            padding: 14px 20px;
            width: 70%;
            border: 2px solid var(--outline);
            border-radius: 12px 0 0 12px;
            font-size: 16px;
            outline: none;
        }
        .preheat-email button {
            padding: 14px 24px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 0 12px 12px 0;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .preheat-email button:hover {
            background: #D35400;
        }
        .preheat-close { 
            position: absolute; 
            top: 16px; 
            right: 16px; 
            background: var(--secondary-container); 
            border: none; 
            width: 40px; 
            height: 40px; 
            border-radius: 50%; 
            font-size: 24px; 
            cursor: pointer; 
            color: var(--secondary); 
        }
        .preheat-close:hover { 
            background: var(--primary); 
            color: white; 
        }
        
        footer {{ text-align: center; padding: 48px 20px; color: var(--on-surface-variant); font-size: 14px; margin-top: 48px; border-top: 1px solid var(--outline); }}
        @media (max-width: 768px) {{ 
            .majors-grid {{ grid-template-columns: 1fr; }} 
            header {{ padding: 32px 24px; }} 
            header h1 {{ font-size: 28px; }} 
            .stats-banner {{ gap: 40px; }} 
            .container {{ padding: 20px; }} 
            .pros-cons {{ grid-template-columns: 1fr; }} 
            .modal {{ padding: 10px; }}
            .modal-content {{ max-height: 95vh; }}
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
                    <div class="stat-number">{len(MAJORS_DATA)}</div>
                    <div class="stat-label">专业收录</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(set([m['category'] for m in MAJORS_DATA]))}</div>
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
''')
    
    # 添加筛选按钮
    categories = sorted(set([m['category'] for m in MAJORS_DATA]))
    for cat in categories:
        icon = next((m['category_icon'] for m in MAJORS_DATA if m['category'] == cat), '📚')
        html_parts.append(f'                <button class="filter-btn" data-filter="{cat}">{icon} {cat}</button>\n')
    
    html_parts.append(f'''            </div>
        </section>
        
        <div class="majors-grid" id="majorsGrid">
        </div>
        
        <footer>
            <p>专业星图 · 温暖的专业指南</p>
            <p style="margin-top:8px;font-size:13px;">数据仅供参考 · 请结合自身情况选择</p>
        </footer>
    </div>
    
    <!-- 模态框容器 -->
    <div id="modal-container"></div>
    
    <!-- 预热模态框 -->
    <div id="preheat-modal" class="preheat-modal">
        <div class="preheat-content">
            <button class="preheat-close" onclick="closePreheatModal()">✕</button>
            <div class="preheat-icon">🔮</div>
            <h2 class="preheat-title">深度分析报告即将上线</h2>
            <p class="preheat-desc">
                我们正在全力打造专业的深度分析报告，为您提供更权威、更深度的专业选择指导。
            </p>
            <ul class="preheat-features">
                <li>📊 权威就业数据（教育部/人社部数据支持）</li>
                <li>🎯 个性化职业发展路径分析</li>
                <li>👔 HR视角的市场需求解读</li>
                <li>💡 张雪峰风格的硬核报考建议</li>
                <li>📈 行业趋势深度分析</li>
            </ul>
            <div class="preheat-email">
                <input type="email" id="notify-email" placeholder="输入邮箱，第一时间获取通知">
                <button onclick="subscribeNotify()">订阅通知</button>
            </div>
            <p style="font-size: 13px; color: var(--on-surface-variant);">
                预计上线时间：2026年6月 | 前1000名订阅用户享专属优惠
            </p>
        </div>
    </div>
    
    <script>
        // 专业数据
        const majorsData = [
''')
    
    # 添加专业数据
    for i, major in enumerate(MAJORS_DATA):
        skills = ''.join([f'<span class="skill-tag">{s}</span>' for s in major.get('suitable_for', {}).get('skills', [])])
        pros = ''.join([f'<li>{p}</li>' for p in major.get('zhang_reviews', {}).get('pros', [])])
        cons = ''.join([f'<li>{c}</li>' for c in major.get('zhang_reviews', {}).get('cons', [])])
        chinese_unis = ''.join([f'<span class="uni-tag chinese">{u}</span>' for u in major.get('chinese_top_universities', [])])
        foreign_unis = ''.join([f'<span class="uni-tag foreign">{u}</span>' for u in major.get('foreign_top_universities', [])])
        
        content = f'''
            {{
                code: "{major['code']}",
                name: "{major['name']}",
                category: "{major['category']}",
                categoryIcon: "{major['category_icon']}",
                difficulty: "{"★" * major['difficulty']}{"☆" * (5 - major['difficulty'])}",
                salary: "{major['salary']['description']}",
                salarySource: "{major['salary']['source']}",
                employment: "{major['employment_rate']['description']}",
                content: `
                    <div class="detail-title">📖 学什么</div>
                    <div class="detail-content">{major['what_you_learn'].get('summary', '')}</div>
                    <ul class="year-list">
                        <li><strong>大一：</strong>{major['what_you_learn'].get('year1', '')}</li>
                        <li><strong>大二：</strong>{major['what_you_learn'].get('year2', '')}</li>
                        <li><strong>大三：</strong>{major['what_you_learn'].get('year3', '')}</li>
                        <li><strong>大四：</strong>{major['what_you_learn'].get('year4', '')}</li>
                    </ul>
                    
                    <div class="detail-title">👤 适合人群</div>
                    <div class="detail-content"><strong>特质：</strong>{'、'.join(major['suitable_for'].get('traits', []))}</div>
                    <div class="detail-content"><strong>技能要求：</strong></div>
                    <div class="skill-tags">{skills}</div>
                    <div class="detail-content warning">⚠️ {major['suitable_for'].get('warning', '')}</div>
                    
                    <div class="detail-title">📈 前景展望</div>
                    <div class="detail-content"><strong>趋势：</strong>{major['prospects'].get('trend', '')}</div>
                    <div class="detail-content"><strong>热门去向：</strong>{major['prospects'].get('hot', '')}</div>
                    <div class="detail-content"><strong>新兴方向：</strong>{major['prospects'].get('developing', '')}</div>
                    
                    <div class="detail-title">💼 就业建议</div>
                    <div class="detail-content"><strong>立即行动：</strong>{major['career_advice'].get('immediate', '')}</div>
                    <div class="detail-content"><strong>证书建议：</strong>{major['career_advice'].get('certifications', '')}</div>
                    <div class="detail-content"><strong>时间线：</strong>{major['career_advice'].get('timeline', '')}</div>
                    
                    <div class="detail-title">🛤️ 学习路径</div>
                    <ul class="year-list">
                        <li><strong>大一：</strong>{major['learning_path'].get('freshman', '')}</li>
                        <li><strong>大二：</strong>{major['learning_path'].get('sophomore', '')}</li>
                        <li><strong>大三：</strong>{major['learning_path'].get('junior', '')}</li>
                        <li><strong>大四：</strong>{major['learning_path'].get('senior', '')}</li>
                    </ul>
                    
                    <div class="detail-title">🎓 名校推荐</div>
                    <div class="uni-section">
                        <strong class="uni-label">🇨🇳 国内TOP3：</strong>
                        <div class="uni-tags">{chinese_unis}</div>
                    </div>
                    <div class="uni-section">
                        <strong class="uni-label">🌍 国外TOP3：</strong>
                        <div class="uni-tags">{foreign_unis}</div>
                    </div>
                    
                    <div class="detail-title">⭐ 雪峰点评</div>
                    <div class="pros-cons">
                        <div class="pros-box">
                            <strong class="pros-title">✅ 优势分析：</strong>
                            <ul class="pros-cons-list">{pros}</ul>
                        </div>
                        <div class="cons-box">
                            <strong class="cons-title">❌ 劣势分析：</strong>
                            <ul class="pros-cons-list">{cons}</ul>
                        </div>
                    </div>
                    <div class="summary-box">
                        💬 总结：{major['zhang_reviews'].get('summary', '')}
                    </div>
                    
                    <div class="cta-section">
                        <button class="cta-button" onclick="showPreheatModal()">🔥 获取深度分析报告</button>
                    </div>
                `
            }}'''
        
        if i < len(MAJORS_DATA) - 1:
            content += ','
        
        html_parts.append(content)
    
    html_parts.append('''
        ];
        
        // 初始化页面
        function initPage() {
            renderMajors();
            bindEvents();
        }
        
        // 渲染专业卡片
        function renderMajors(filter = 'all', search = '') {
            const grid = document.getElementById('majorsGrid');
            grid.innerHTML = '';
            
            let filtered = majorsData;
            
            if (filter !== 'all') {
                filtered = filtered.filter(m => m.category === filter);
            }
            
            if (search) {
                const searchLower = search.toLowerCase();
                filtered = filtered.filter(m => 
                    m.name.toLowerCase().includes(searchLower) || 
                    m.category.toLowerCase().includes(searchLower)
                );
            }
            
            filtered.forEach(major => {
                const card = createCard(major);
                grid.appendChild(card);
            });
        }
        
        // 创建专业卡片
        function createCard(major) {
            const div = document.createElement('div');
            div.className = 'major-card';
            div.dataset.category = major.category;
            div.dataset.name = major.name;
            div.onclick = () => openModal(major.code);
            
            div.innerHTML = `
                <div class="card-header">
                    <span class="category-icon">${major.categoryIcon}</span>
                    <div>
                        <div class="major-name">${major.name}</div>
                        <div class="major-code">${major.code}</div>
                        <div class="difficulty-stars">难度：${major.difficulty}</div>
                    </div>
                </div>
                <div class="salary-tag">💰 ${major.salary}</div>
                <span class="data-source-tag">${major.salarySource}</span>
                <p class="employment-desc">就业形势：${major.employment}</p>
            `;
            
            return div;
        }
        
        // 打开模态框
        let currentModalCode = null;
        
        function openModal(code) {
            const major = majorsData.find(m => m.code === code);
            if (!major) return;
            
            const container = document.getElementById('modal-container');
            container.innerHTML = `
                <div class="modal show" id="modal-${major.code}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="modal-title">
                                <span class="category-icon">${major.categoryIcon}</span>
                                <div>
                                    <h2>${major.name}</h2>
                                    <div class="difficulty-stars">难度：${major.difficulty}</div>
                                </div>
                            </div>
                            <button class="modal-close" onclick="closeModal('${major.code}')">✕</button>
                        </div>
                        <div class="modal-body">
                            ${major.content}
                        </div>
                    </div>
                </div>
            `;
            
            document.body.style.overflow = 'hidden';
            currentModalCode = code;
            
            // 点击背景关闭
            document.querySelector('.modal').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeModal(currentModalCode);
                }
            });
        }
        
        // 关闭模态框
        function closeModal(code) {
            const modal = document.getElementById('modal-' + code);
            if (modal) {
                modal.classList.remove('show');
                setTimeout(() => {
                    document.getElementById('modal-container').innerHTML = '';
                }, 300);
            }
            document.body.style.overflow = '';
            currentModalCode = null;
        }
        
        // 显示预热模态框
        function showPreheatModal() {
            const modal = document.getElementById('preheat-modal');
            if (modal) {
                modal.classList.add('show');
                document.body.style.overflow = 'hidden';
            }
        }
        
        // 关闭预热模态框
        function closePreheatModal() {
            const modal = document.getElementById('preheat-modal');
            if (modal) {
                modal.classList.remove('show');
                document.body.style.overflow = '';
            }
        }
        
        // 订阅通知
        function subscribeNotify() {
            const email = document.getElementById('notify-email').value;
            if (email && email.includes('@')) {
                alert('✅ 订阅成功！我们会在深度分析报告上线时第一时间通知您！');
                document.getElementById('notify-email').value = '';
                closePreheatModal();
            } else {
                alert('请输入有效的邮箱地址');
            }
        }
        
        // 点击预热模态框背景关闭
        document.addEventListener('DOMContentLoaded', function() {
            const preheatModal = document.getElementById('preheat-modal');
            if (preheatModal) {
                preheatModal.addEventListener('click', function(e) {
                    if (e.target === preheatModal) {
                        closePreheatModal();
                    }
                });
            }
        });
        
        // 绑定事件
        function bindEvents() {
            // 筛选按钮
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    document.getElementById('searchInput').value = '';
                    renderMajors(this.dataset.filter, '');
                });
            });
            
            // 搜索输入
            document.getElementById('searchInput').addEventListener('input', function() {
                const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
                renderMajors(activeFilter, this.value);
            });
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', initPage);
    </script>
</body>
</html>
''')
    
    # 写入文件
    with open('major_starmap_complete.html', 'w', encoding='utf-8') as f:
        f.write(''.join(html_parts))
    
    print(f"✅ 成功生成完整版本！")
    print(f"📊 共 {len(MAJORS_DATA)} 个专业")
    print(f"📁 输出文件：major_starmap_complete.html")
    
else:
    print("❌ 未找到专业数据")
