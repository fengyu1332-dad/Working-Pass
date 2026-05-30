"""
批量生成测试 — 5份不同门类的深度分析报告
输出到 test_reports/ 目录供人工审核
"""
import asyncio, aiohttp, json, os, re, sys, time
from datetime import datetime
from pathlib import Path

# ============================================================
# 配置
# ============================================================
SUPABASE_URL = "https://djteatwxjlnbjylynvjh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4"

# 已有报告的专业代码（跳过这些）
EXISTING_REPORTS = {"050226","050206","050233","050234","080901","100201K","120106TK","120110T"}

# 测试：从不同门类各选1个
TEST_CODES = [
    "040106",   # 学前教育 (教育学)
    "050101",   # 汉语言文学 (文学)
    "060101",   # 历史学 (历史学)
    "080902",   # 软件工程 (工学/IT)
    "100301K",  # 口腔医学 (医学)
]

CONCURRENCY = 1       # 串行，便于观察
MAX_TOKENS = 16000
TEMPERATURE = 0.5
TIMEOUT = 120         # 秒
OUTPUT_DIR = Path(__file__).parent.parent / "test_reports"

# ============================================================
# Prompt（与 Edge Function 完全一致）
# ============================================================
SYSTEM_PROMPT = """你是"专业星图"平台的资深教育数据分析师，拥有20年中国高等教育和就业市场研究经验。你的分析风格兼具学术严谨性和张雪峰式的犀利接地气。

你的核心能力：
1. 精准引用数据——所有判断都有具体数字支撑（就业率、薪资中位数、录取率、增长率等）
2. 多维度分析——从学业、就业、薪资、地域、家庭背景、AI影响等角度全面剖析一个专业
3. 敢说真话——不回避专业的痛点、陷阱和残酷现实
4. 给可操作建议——不空谈，每条建议都是学生和家长能直接用的

输出格式要求：
- 纯HTML内容（不含<html>/<head>/<body>标签）
- 以<h1>标题开头
- 严格按13个章节结构组织
- 数据标注来源
- 语言：中文，专业知识扎实，点评风格犀利接地气"""


def safe_str(v, fallback="暂无数据"):
    if not v:
        return fallback
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, indent=2)
    return str(v)


def build_user_prompt(m):
    return f"""请为以下专业生成完整的13章节深度分析报告。

======= 专业基础信息 =======
专业名称：{m.get('name', '')}
专业代码：{m.get('code', '')}
学科门类：{m.get('category', '')}
学位：{m.get('degree', '未标注')}
学制：{m.get('duration', 4)}年
难度评级：{m.get('difficulty', '未标注')}

======= 专业概况 =======
{safe_str(m.get('overview'))}

======= 核心课程与技能 =======
{safe_str(m.get('what_you_learn'))}

======= 课程安排（JSON） =======
{safe_str(m.get('yearly_courses'))}

======= 就业前景描述 =======
{safe_str(m.get('career_outlook'))}

======= 薪资范围 =======
{safe_str(m.get('salary_range'))}

======= 适合人群分析 =======
{safe_str(m.get('suitable_for'))}

======= 就业方向（JSON） =======
{safe_str(m.get('career_directions'))}

======= 雪峰点评参考 =======
{safe_str(m.get('xuefeng_comment'))}

======= 推荐院校（JSON） =======
{safe_str(m.get('top_universities'))}

======= 报告结构要求 =======
严格按以下13章生成（每章<h2>标题须完全一致），总字数10000汉字左右，用具体数字而非模糊描述：

<h2>一、专业概述</h2>
- 1.1 专业定义与学科定位（150-200字）
- 1.2 培养目标（3-5条）
- 1.3 学科特点与核心价值（3-4个特点）

<h2>二、课程安排与学习内容</h2>
- 2.1 分年级课程体系（HTML表格：大一~大四）
- 2.2 核心课程详解（3-5门，每门50-80字）
- 2.3 实践教学环节（5-6项）
- 2.4 核心能力培养（4-5项）

<h2>三、就业前景分析</h2>
- 3.1 就业率数据（总体、对口、满意度，引用来源）
- 3.2 主要就业方向与岗位（7-10个，分"核心技术岗"和"拓展方向"）
- 3.3 行业分布（6个以上行业+大致百分比）
- 3.4 绿牌/红牌标识及解读

<h2>四、薪资水平与职业发展</h2>
- 4.1 薪资数据（应届/3年/5年/10年平均薪资）
- 4.2 高薪比例
- 4.3 城市薪资差异（一线/新一线/二线对比）
- 4.4 职业发展路径（技术线+管理线，入门→资深→专家/管理）
- 4.5 职业天花板评估
- 4.6 长期发展潜力（10年以上）

<h2>五、考研与深造分析</h2>
- 5.1 考研必要性评估
- 5.2 考研数据（报名趋势、录取率）
- 5.3 推荐深造方向（5个细分方向）
- 5.4 院校推荐（A+/A/A-三级）
- 5.5 读博建议

<h2>六、考公考编分析</h2>
- 6.1 对口度评估（可报岗位数、竞争比、上岸难度1-5星）
- 6.2 适合的编制岗位（公务员/事业编/国企）
- 6.3 体制内薪资待遇
- 6.4 考公优劣势对比

<h2>七、行业发展与人才需求</h2>
- 7.1 行业生命周期评估（成长期/成熟期/衰退期，说明理由）
- 7.2 行业规模与增长率（具体数字）
- 7.3 国家政策支持力度
- 7.4 人才缺口数据
- 7.5 未来5年趋势（5个具体判断）

<h2>八、适合人群与适配度</h2>
- 8.1 适合特质画像（5条）
- 8.2 核心能力星级表（HTML表格：数学/英语/逻辑/空间/记忆/动手/抗压等，1-5星）
- 8.3 不适合人群（4类）
- 8.4 性别分析（男女比例、性别偏见、适适合性结论）

<h2>九、学业难度与学习建议</h2>
- 9.1 课程难度评估（1-5星，各年级分开）
- 9.2 挂科率数据（列出百分比）
- 9.3 "杀手课"预警（3门，含原因）
- 9.4 每周学习强度建议
- 9.5 学习方法与策略（6条）

<h2>十、家庭背景与投入回报</h2>
- 10.1 教育投入成本（公办/民办4-5年总费用）
- 10.2 投入回报周期（几年"回本"）
- 10.3 长期回报预期（10年后年收入、终身总收入预估）
- 10.4 普通家庭适合度（1-5星）
- 10.5 "三无家庭"机会分析（无背景/资本/人脉）
- 10.6 风险提示

<h2>十一、城市与地区适配</h2>
- 11.1 首选城市Top5（含原因）
- 11.2 产业重镇分布
- 11.3 不同城市薪资对比表（HTML表格）
- 11.4 生活成本与压力评估

<h2>十二、AI影响与未来趋势</h2>
- 12.1 AI替代风险评估（1-5星）
- 12.2 AI带来的新机遇（3-5个新岗位/转型方向）
- 12.3 会用AI的薪资溢价
- 12.4 核心不可替代能力（5项）
- 12.5 未来5-10年趋势预测

<h2>十三、雪峰点评</h2>
- 13.1 核心优势分析（200-300字，口语化，有数据）
- 13.2 真实弊端与痛点（200-300字，直击痛点）
- 13.3 报考建议（150-200字）
- 13.4 一句话总结
- 风格：张雪峰式口语化、接地气、敢说真话、适当幽默。用"我跟你说""我给你分析分析""你自己掂量掂量"等表达。

======= 重要提醒 =======
1. 必须输出全部13个章节
2. 数据必须具体（数字、百分比、金额、排名），不用"较高""较多"
3. 总字数10000汉字左右
4. 用HTML标签排版（h2/h3/p/ul/li/table/thead/tbody/tr/th/td/strong/em/blockquote）
5. 数据来源标注：*数据来源：XXX*
6. 表格用 <table style="width:100%;border-collapse:collapse;margin:12px 0;">，th/td加 border="1" style="padding:8px;text-align:left;"
7. 禁止"根据我的训练数据""作为AI语言模型"等AI身份表达
8. 以<h1>专业名称 — 深度分析报告</h1>开头"""


# ============================================================
# 验证函数
# ============================================================
def validate_report(html, major_name):
    text_only = re.sub(r'<[^>]+>', '', html).replace('\n', '').replace(' ', '')
    char_count = len(text_only)

    h2_count = len(re.findall(r'<h2>', html))
    has_h1 = '<h1>' in html
    has_table = '<table' in html
    has_source = '数据来源' in text_only or '数据来源' in html
    has_ai_banned = any(x in text_only for x in ['根据我的训练数据', '作为AI语言模型', '作为人工智能'])

    # Check if h1 title contains the actual major name
    h1_match = re.findall(r'<h1>([^<]+)</h1>', html)
    name_in_h1 = major_name in (h1_match[0] if h1_match else '')
    has_wrong_name = not name_in_h1 and h1_match

    issues = []
    if char_count < 8000:
        issues.append(f"字数不足: {char_count}")
    if h2_count < 13:
        issues.append(f"章节不足: {h2_count}/13")
    if not has_h1:
        issues.append("缺少h1标题")
    if has_wrong_name:
        issues.append(f"专业名不匹配: h1={h1_match[0]} != {major_name}")
    if not has_table:
        issues.append("无HTML表格")
    if has_ai_banned:
        issues.append("含AI身份暴露")

    return {
        "char_count": char_count,
        "h2_chapters": h2_count,
        "has_h1": has_h1,
        "name_in_h1": name_in_h1,
        "has_table": has_table,
        "has_source": has_source,
        "has_ai_banned": has_ai_banned,
        "issues": issues,
        "pass": len(issues) == 0,
    }


# ============================================================
# 主逻辑
# ============================================================
async def fetch_major(session, code):
    url = f"{SUPABASE_URL}/rest/v1/majors?select=*&code=eq.{code}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    async with session.get(url, headers=headers) as resp:
        data = await resp.json()
        return data[0] if data else None


async def generate_report(session, major, api_key, sem):
    async with sem:
        name = major["name"]
        code = major["code"]
        print(f"\n{'='*60}")
        print(f"[{code}] {name} — 开始生成...")
        t0 = time.time()

        payload = {
            "model": "deepseek-chat",
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(major)},
            ],
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        try:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=TIMEOUT),
            ) as resp:
                if resp.status != 200:
                    err = await resp.text()
                    print(f"  [ERR] API错误 {resp.status}: {err[:300]}")
                    return None

                data = await resp.json()
                html = data["choices"][0]["message"]["content"]

        except asyncio.TimeoutError:
            print(f"  [ERR] 超时 ({TIMEOUT}s)")
            return None
        except Exception as e:
            print(f"  [ERR] 异常: {e}")
            return None

        elapsed = time.time() - t0

        # 验证
        validation = validate_report(html, name)
        status = "[PASS]" if validation["pass"] else "[WARN]"
        print(f"  {status} | {validation['char_count']}字 | {validation['h2_chapters']}章 | {elapsed:.0f}s")
        if validation["issues"]:
            for issue in validation["issues"]:
                print(f"     → {issue}")

        # 保存
        safe_name = re.sub(r'[\\/*?:"<>|]', '', name)
        filepath = OUTPUT_DIR / f"{code}_{safe_name}.html"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        meta = f"""<!--
  专业代码: {code}
  专业名称: {name}
  门类: {major.get('category', '')}
  生成时间: {datetime.now().isoformat()}
  字数: {validation['char_count']}
  章节数: {validation['h2_chapters']}
  验证: {status}
  耗时: {elapsed:.0f}s
-->
"""
        filepath.write_text(meta + html, encoding="utf-8")
        print(f"  已保存: {filepath}")

        return {
            "code": code,
            "name": name,
            "elapsed": elapsed,
            "validation": validation,
            "filepath": str(filepath),
        }


async def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        # 尝试从 .env 文件读取
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("DEEPSEEK_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        print("[ERR] 未找到 DEEPSEEK_API_KEY，请在 .env 文件中设置或设置环境变量")
        sys.exit(1)

    print("=" * 60)
    print("批量生成测试 — 5份不同门类深度分析报告")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)

    sem = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:
        # 1. 拉取5个测试专业
        majors = []
        for code in TEST_CODES:
            m = await fetch_major(session, code)
            if m:
                majors.append(m)
                cat = m.get('category', '?')
                print(f"  [OK] [{code}] {m['name']} ({cat})")
            else:
                print(f"  [ERR] [{code}] 未找到")

        if not majors:
            print("未找到任何测试专业，退出")
            return

        print(f"\n共 {len(majors)} 个专业，开始生成...")
        print("(每个报告预计 30-90 秒)\n")

        # 2. 逐个生成
        tasks = [generate_report(session, m, api_key, sem) for m in majors]
        results = await asyncio.gather(*tasks)

    # 3. 汇总
    passed = sum(1 for r in results if r and r["validation"]["pass"])
    failed = sum(1 for r in results if r is None)
    warned = len(results) - passed - failed

    print(f"\n{'='*60}")
    print(f"完成: {len(results)} 份")
    print(f"  [PASS]: {passed}")
    print(f"  [WARN]: {warned}")
    print(f"  [FAIL]: {failed}")
    print(f"\n报告保存在: {OUTPUT_DIR}")
    print("请检查输出质量后再决定是否大规模执行。")


if __name__ == "__main__":
    asyncio.run(main())
