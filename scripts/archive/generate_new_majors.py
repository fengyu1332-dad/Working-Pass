#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业星图 - 批量生成新专业报告
生成5个新的深度分析报告
作者：专业星图团队
日期：2026-05-23
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv()
from utils.api_client import DeepSeekClient


NEW_MAJORS = [
    {
        "code": "120203K",
        "name": "会计学",
        "category": "12 管理学",
        "description": "培养具备管理、经济、法律和会计学等方面的知识和能力，能在企、事业单位及政府部门从事会计实务以及教学、科研方面工作的工商管理学科高级专门人才",
        "courses": "基础会计、财务会计、成本会计、管理会计、财务管理、审计学、会计信息系统、税法、经济法、统计学",
        "employment": "会计师、审计师、财务经理、CFO、税务专员、金融分析师、公务员"
    },
    {
        "code": "080202",
        "name": "机械设计制造及其自动化",
        "category": "08 工学",
        "description": "培养具备机械设计制造基础知识与应用能力，能在工业生产第一线从事机械制造领域内的设计制造、科技开发、应用研究、运行管理和经营销售等方面工作的高级工程技术人才",
        "courses": "机械制图、理论力学、材料力学、机械原理、机械设计、电工电子技术、机电传动控制、数控技术、模具设计、先进制造技术",
        "employment": "机械工程师、结构工程师、工艺工程师、机电工程师、设备管理、质量工程师、销售工程师"
    },
    {
        "code": "080701",
        "name": "电子信息工程",
        "category": "08 工学",
        "description": "培养具备电子技术和信息系统的基础知识，能从事各类电子设备和信息系统的研究、设计、制造、应用和开发的高等工程技术人才",
        "courses": "电路理论、信号与系统、数字信号处理、通信原理、电子线路、数字系统设计、微机原理、嵌入式系统、电磁场理论、天线与微波技术",
        "employment": "电子工程师、通信工程师、嵌入式开发、硬件工程师、算法工程师、IT技术支持、项目经理"
    },
    {
        "code": "050201",
        "name": "英语",
        "category": "05 文学",
        "description": "培养具有扎实的英语语言基础和广博的文化知识，能在外事、经贸、文化、新闻出版、教育、科研、旅游等部门从事翻译、研究、教学、管理工作的英语高级专门人才",
        "courses": "基础英语、高级英语、英语听力、英语口语、英语写作、翻译理论与实践、英美文学、语言学概论、跨文化交际、二外法语/日语",
        "employment": "翻译、外贸业务员、英语教师、外企白领、跨境电商运营、国际导游、媒体编辑、外交官"
    },
    {
        "code": "070101",
        "name": "数学与应用数学",
        "category": "07 理学",
        "description": "培养掌握数学科学的基本理论与基本方法，具备运用数学知识、使用计算机解决实际问题的能力，受到科学研究的初步训练，能在科技、教育和经济部门从事研究、教学工作或在生产经营及管理部门从事实际应用、开发研究和管理工作的高级专门人才",
        "courses": "数学分析、高等代数、解析几何、概率论与数理统计、常微分方程、实变函数、复变函数、抽象代数、数值分析、数学建模、运筹学",
        "employment": "数据分析师、量化交易员、算法工程师、精算师、统计学家、金融工程师、IT研发、教育科研"
    }
]


def generate_single_report(major, llm_client, index, total):
    major_name = major.get("name")
    major_code = major.get("code")
    print(f"\n{'='*80}")
    print(f"[{index}/{total}] 正在生成报告：{major_name} ({major_code})")
    print(f"{'='*80}")
    
    prompt = f"""你是一位资深的高考志愿填报专家和职业规划顾问。请为"{major_name}"（专业代码：{major_code}）生成一份专业、详细、周到的深度分析报告。

报告要求：
1. 数据来源必须明确标注（麦可思研究院、智联招聘、BOSS直聘、教育部、国家统计局等）
2. 语言表达要专业、详细、周到，不要过于口语化，但要保持清晰易懂
3. 结构完整，逻辑清晰，涵盖学生和家长关心的所有核心问题
4. 雪峰点评部分保持幽默、接地气、实用的风格

专业信息：
- 专业名称：{major_name}
- 专业代码：{major_code}
- 所属学科门类：{major.get('category')}
- 专业简介：{major.get('description')}
- 核心课程：{major.get('courses')}
- 主要就业方向：{major.get('employment')}

请按照以下结构生成报告：

## 一、专业概述
1.1 专业定义与学科定位
1.2 培养目标
1.3 学科特点与核心价值

## 二、课程安排与学习内容
2.1 主干课程体系（分年级说明）
2.2 核心课程详解
2.3 实践教学环节
2.4 知识体系与能力培养要求

## 三、就业前景分析
3.1 就业率数据（标注来源：麦可思研究院2024年中国本科生就业报告）
   - 毕业半年后总体就业率
   - 对口就业率（从事专业相关工作的比例）
   - 就业满意度
   - 毕业去向分布（就业/考研/出国/其他比例）
3.2 主要就业方向与岗位
3.3 行业分布（标注来源：智联招聘2024年大学生就业白皮书）
3.4 绿牌/红牌专业标识（标注来源：麦可思2025年绿牌/红牌专业榜）

## 四、薪资水平与职业发展
4.1 薪资数据（标注来源：BOSS直聘研究院2024年薪资报告）
   - 毕业半年后平均起薪
   - 工作3年后平均薪资
   - 工作5年后平均薪资
   - 高薪比例（月薪过万、过2万比例）
   - 城市薪资差异（一线/新一线/二线城市对比）
4.2 职业发展路径
4.3 职业天花板评估
4.4 长期发展潜力

## 五、考研与深造分析
5.1 考研必要性评估（本科就业是否够用？考研价值几何？）
5.2 考研数据（录取率、名校录取率）（标注来源：教育部2024年考研数据）
5.3 推荐深造方向
5.4 优秀院校推荐（分层次：A+/A/A-）
5.5 读博建议（是否值得读博？读博后的出路）

## 六、考公考编分析
6.1 考公对口度评估（标注来源：2025年国考/省考职位表）
   - 可报考岗位数量
   - 平均竞争比
   - 上岸难度评估（1-5星）
6.2 适合的编制岗位
6.3 体制内薪资待遇
6.4 考公优势与劣势

## 七、行业发展与人才需求
7.1 行业生命周期评估（朝阳期/成熟期/夕阳期）
7.2 行业规模与增长率（标注来源：国家统计局、行业协会）
7.3 国家政策支持力度
7.4 人才缺口数据（标注来源：人社部、行业报告）
7.5 未来5年趋势预测

## 八、适合人群与适配度
8.1 适合特质画像（什么样的人适合学这个专业）
8.2 核心能力要求（数学/英语/逻辑等，1-5星评估）
8.3 不适合人群（哪些人不建议报考）
8.4 性别分析（男女比例、性别偏见、适合性别）

## 九、学业难度与学习建议
9.1 课程难度评估（1-5星）
9.2 专业挂科率数据
9.3 "杀手课"预警（挂科率高的课程）
9.4 每周学习强度建议
9.5 学习方法与策略建议

## 十、家庭背景与投入回报
10.1 教育投入成本（4年学费+生活费）
10.2 投入回报周期（几年能回本）
10.3 长期回报预期（10年后总收益）
10.4 普通家庭适合度（1-5星）
10.5 "三无家庭"（无背景无资本无人脉）的机会分析
10.6 风险提示（哪些情况可能导致投入打水漂）

## 十一、城市与地区适配
11.1 首选城市TOP5（发展机会多的城市）
11.2 产业重镇分布
11.3 不同城市的薪资水平对比
11.4 生活成本与压力评估

## 十二、AI影响与未来趋势
12.1 AI替代风险评估（1-5星，越高越容易被替代）
12.2 AI带来的转型机遇
12.3 AI加持价值（会用AI的人薪资溢价多少）
12.4 核心不可替代能力（AI无法替代的是什么）
12.5 未来5-10年趋势预测

## 十三、雪峰点评（张雪峰老师风格）
13.1 核心优势分析
13.2 真实弊端与痛点
13.3 报考建议（什么样的学生适合，什么样的学生慎报）
13.4 大学期间如何规划（实习、考证、竞赛等）
13.5 一句话总结

## 十四、综合评价与最终建议
14.1 多维度评分（就业/薪资/学习难度/考研/考公/稳定性）
14.2 综合推荐指数（1-5星）
14.3 风险总结
14.4 最终报考建议

注意事项：
- 所有数据都要标注来源（例如：数据来源：麦可思研究院《2024年中国本科生就业报告》）
- 内容要专业、详细、周到，不要简短概括
- 雪峰点评要保持张雪峰老师的风格：幽默、接地气、实用、敢说真话
- 用词要专业但易懂，避免过于晦涩
- 要有具体的数字支撑，不要泛泛而谈

现在，请开始生成完整的专业分析报告："""
    
    try:
        report_content = llm_client.generate(prompt, temperature=0.7, max_tokens=8000)
        return report_content
    except Exception as e:
        print(f"生成失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None


def save_report(report_content, major_name, major_code):
    os.makedirs("data/reports", exist_ok=True)
    filename = f"report_{major_code}_{major_name}.txt"
    filepath = os.path.join("data/reports", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"✅ 报告已保存：{filepath}")
    return filepath


def main():
    print(f"{'='*80}")
    print("专业星图 - 批量生成新专业报告")
    print(f"{'='*80}")
    print(f"\n需要生成的新专业：")
    for i, major in enumerate(NEW_MAJORS, 1):
        print(f"  {i}. {major['name']} ({major['code']})")
    
    llm_client = DeepSeekClient(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    )
    
    success_count = 0
    for i, major in enumerate(NEW_MAJORS, 1):
        print(f"\n{'='*80}")
        print(f"开始生成第 {i}/5 份报告...")
        print(f"{'='*80}")
        
        report_content = generate_single_report(major, llm_client, i, len(NEW_MAJORS))
        
        if report_content:
            save_report(report_content, major['name'], major['code'])
            success_count += 1
        else:
            print(f"❌ 报告生成失败：{major['name']}")
        
        if i < len(NEW_MAJORS):
            print(f"\n等待5秒后继续...")
            time.sleep(5)
    
    print(f"\n{'='*80}")
    print(f"🎉 批量生成完成！成功：{success_count}/{len(NEW_MAJORS)}")
    print(f"{'='*80}")
    print("\n下一步：运行以下命令清理并生成PDF：")
    print("  python batch_generate_all.py")


if __name__ == "__main__":
    main()
