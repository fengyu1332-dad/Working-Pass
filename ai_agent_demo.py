#!/usr/bin/env python3
"""
专业星图 - AI Agent深度报告生成系统
版本：v1.1 (简化演示版)
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ReportStatus(Enum):
    """报告状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


class QualityScore(Enum):
    """质量评分等级"""
    A = "A"  # 优秀
    B = "B"  # 良好
    C = "C"  # 合格
    D = "D"  # 不合格


class BaseAgent:
    """Agent基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def log(self, message: str):
        """记录日志"""
        print(f"[{self.name}] {message}")
    
    def run(self, input_data: Dict) -> Dict:
        """执行Agent任务（子类实现）"""
        raise NotImplementedError


class DataCollectionAgent(BaseAgent):
    """数据收集Agent"""
    
    def __init__(self):
        super().__init__("DataCollectionAgent")
    
    def run(self, input_data: Dict) -> Dict:
        """收集并完善专业数据"""
        self.log(f"开始收集专业数据: {input_data.get('major_name')}")
        
        # 模拟从数据库获取数据
        major_data = {
            "major_code": input_data['major_code'],
            "major_name": input_data['major_name'],
            "category": input_data['category'],
            "overview": "计算机科学与技术是研究计算机的设计、制造和应用的学科，培养计算机专业人才。",
            "suitable_for": "对编程、计算机技术感兴趣，逻辑思维强的学生。",
            "career_outlook": "信息技术快速发展，就业在互联网企业、软件开发、系统运维等领域。",
            "salary_range": "¥15k-40k",
            "yearly_courses": {
                "大一": ["高等数学", "线性代数", "C语言程序设计", "计算机导论"],
                "大二": ["数据结构", "计算机组成原理", "操作系统", "Java程序设计"],
                "大三": ["计算机网络", "数据库系统", "软件工程", "算法设计"],
                "大四": ["实习", "毕业设计"]
            },
            "top_universities": {
                "domestic": ["清华大学", "北京大学", "浙江大学", "上海交通大学", "复旦大学"],
                "international": ["MIT", "Stanford", "CMU", "UC Berkeley"]
            }
        }
        
        return major_data


class DeepAnalysisAgent(BaseAgent):
    """深度分析Agent"""
    
    def __init__(self):
        super().__init__("DeepAnalysisAgent")
    
    def run(self, input_data: Dict) -> Dict:
        """生成专业深度分析"""
        self.log(f"开始深度分析: {input_data.get('major_name')}")
        
        analysis_content = f"""## 七、深度分析

### 7.1 学科定位
{input_data['major_name']}是计算机科学与技术领域的核心专业，在信息技术产业中扮演着关键角色。

### 7.2 核心能力培养
该专业注重培养学生的编程能力、算法思维、系统设计能力以及解决实际问题的能力。

### 7.3 行业发展趋势
随着人工智能、大数据、云计算等技术的快速发展，该专业的发展前景非常广阔。

### 7.4 就业市场分析
就业需求持续旺盛，主要就业方向包括软件开发、数据分析、人工智能等。

### 7.5 职业发展路径
从初级工程师到技术专家，再到技术管理岗位，发展路径清晰。

### 7.6 技能要求
需要掌握扎实的编程基础、算法知识、系统设计能力，以及良好的团队协作能力。
"""
        
        return {"deep_analysis": analysis_content}


class XuefengCommentAgent(BaseAgent):
    """雪峰点评Agent"""
    
    def __init__(self):
        super().__init__("XuefengCommentAgent")
    
    def run(self, input_data: Dict) -> Dict:
        """生成雪峰风格点评"""
        self.log(f"开始雪峰点评: {input_data.get('major_name')}")
        
        comment_content = f"""## 八、雪峰点评

{input_data['major_name']}？这可是现在最火的专业之一！

【先说"痛点"】
1. **学习压力不小！** 课程难度大，编程作业多，需要持续学习新技术
2. **竞争也很激烈！** 学的人多，想要脱颖而出需要真本事

【但也有优势】
1. **就业真的好！** 需求旺盛，起薪高，发展机会多
2. **薪资待遇好！** 比很多传统行业起薪高不少
3. **发展空间大！** 从技术到管理，路径很多

【报考建议】
- 真的喜欢编程、喜欢计算机的，大胆报！
- 如果只是想跟风，要慎重考虑，因为学习并不轻松

【总结】
{input_data['major_name']}是一个有前途、有"钱"途的专业，但也需要付出努力！
"""
        
        return {"xuefeng_comment": comment_content}


class ComposerAgent(BaseAgent):
    """报告合成Agent"""
    
    def __init__(self):
        super().__init__("ComposerAgent")
    
    def run(self, input_data: Dict) -> Dict:
        """合成完整报告"""
        self.log("开始合成报告...")
        
        major_data = input_data['major_data']
        deep_analysis = input_data.get('deep_analysis', '')
        xuefeng_comment = input_data.get('xuefeng_comment', '')
        
        # 生成完整报告
        sections = []
        
        # 1. 专业概述
        if major_data.get('overview'):
            sections.append(f"## 一、专业概述\n{major_data['overview']}")
        
        # 2. 课程安排
        if major_data.get('yearly_courses'):
            sections.append("## 二、课程安排")
            for year, courses in major_data['yearly_courses'].items():
                sections.append(f"\n{year}: {', '.join(courses)}")
        
        # 3. 就业前景
        if major_data.get('career_outlook'):
            sections.append(f"\n## 三、就业前景\n{major_data['career_outlook']}")
        
        # 4. 薪资范畴
        if major_data.get('salary_range'):
            sections.append(f"\n## 四、薪资范畴\n{major_data['salary_range']}")
        
        # 5. 适合人群
        if major_data.get('suitable_for'):
            sections.append(f"\n## 五、适合人群\n{major_data['suitable_for']}")
        
        # 6. 顶级院校
        if major_data.get('top_universities'):
            sections.append("\n## 六、顶级院校推荐")
            univs = major_data['top_universities']
            if univs.get('domestic'):
                sections.append(f"\n国内: {', '.join(univs['domestic'])}")
            if univs.get('international'):
                sections.append(f"\n国际: {', '.join(univs['international'])}")
        
        # 7. 深度分析
        if deep_analysis:
            sections.append(f"\n{deep_analysis}")
        
        # 8. 雪峰点评
        if xuefeng_comment:
            sections.append(f"\n{xuefeng_comment}")
        
        full_content = "\n".join(sections)
        
        # 生成预览内容
        preview_length = int(len(full_content) * 0.2)
        preview_content = full_content[:preview_length]
        
        # 确保在完整的句子或段落结束
        if len(preview_content) < len(full_content):
            last_newline = preview_content.rfind('\n')
            if last_newline > 0:
                preview_content = preview_content[:last_newline]
        
        preview_content += "\n\n（完整内容请解锁报告）"
        
        return {
            "preview_content": preview_content,
            "full_content": full_content
        }


class QualityAssuranceAgent(BaseAgent):
    """质量审核Agent"""
    
    def __init__(self):
        super().__init__("QualityAssuranceAgent")
    
    def run(self, input_data: Dict) -> Dict:
        """审核报告质量"""
        self.log("开始质量审核...")
        
        report_content = input_data['full_content']
        
        # 1. 质量评分
        score, score_level = self._evaluate_quality(report_content)
        
        self.log(f"质量评分: {score_level} ({score}分)")
        
        return {
            "quality_score": score_level,
            "score_value": score,
            "corrected_content": report_content
        }
    
    def _evaluate_quality(self, content: str) -> Tuple[int, QualityScore]:
        """评估质量"""
        score = 0
        
        # 1. 内容完整性（30分）
        sections = ["专业概述", "课程安排", "就业前景", "雪峰点评"]
        complete_count = sum(1 for s in sections if s in content)
        score += int(30 * (complete_count / len(sections)))
        
        # 2. 内容长度（20分）
        if len(content) > 2000:
            score += 20
        elif len(content) > 1000:
            score += 15
        elif len(content) > 500:
            score += 10
        else:
            score += 5
        
        # 3. 结构规范性（20分）
        if "## " in content:
            score += 20
        else:
            score += 10
        
        # 4. 雪峰点评存在（30分）
        if "雪峰点评" in content:
            score += 30
        
        # 确定等级
        if score >= 90:
            level = QualityScore.A
        elif score >= 75:
            level = QualityScore.B
        elif score >= 60:
            level = QualityScore.C
        else:
            level = QualityScore.D
        
        return score, level


class CoordinatorAgent(BaseAgent):
    """任务协调Agent"""
    
    def __init__(self):
        super().__init__("CoordinatorAgent")
        self.data_collection_agent = DataCollectionAgent()
        self.deep_analysis_agent = DeepAnalysisAgent()
        self.xuefeng_comment_agent = XuefengCommentAgent()
        self.composer_agent = ComposerAgent()
        self.qa_agent = QualityAssuranceAgent()
    
    def run(self, input_data: Dict) -> Dict:
        """协调执行完整的报告生成流程"""
        task_id = f"task_{int(time.time())}"
        self.log(f"开始执行任务: {task_id}")
        self.log(f"专业: {input_data.get('major_name')}")
        
        try:
            # 阶段1: 数据收集
            self.log("\n=== 阶段1: 数据收集 ===")
            major_data = self.data_collection_agent.run(input_data)
            
            # 阶段2: 深度分析
            self.log("\n=== 阶段2: 深度分析 ===")
            analysis_result = self.deep_analysis_agent.run(major_data)
            
            # 阶段3: 雪峰点评
            self.log("\n=== 阶段3: 雪峰点评 ===")
            comment_result = self.xuefeng_comment_agent.run(major_data)
            
            # 阶段4: 报告合成
            self.log("\n=== 阶段4: 报告合成 ===")
            composer_input = {
                "major_data": major_data,
                "deep_analysis": analysis_result['deep_analysis'],
                "xuefeng_comment": comment_result['xuefeng_comment']
            }
            composer_result = self.composer_agent.run(composer_input)
            
            # 阶段5: 质量审核
            self.log("\n=== 阶段5: 质量审核 ===")
            qa_input = {
                "full_content": composer_result['full_content']
            }
            qa_result = self.qa_agent.run(qa_input)
            
            # 整理结果
            final_report = {
                "task_id": task_id,
                "status": ReportStatus.COMPLETED,
                "major_code": input_data['major_code'],
                "major_name": input_data['major_name'],
                "preview_content": composer_result['preview_content'],
                "full_content": qa_result['corrected_content'],
                "quality_score": qa_result['quality_score'],
                "score_value": qa_result['score_value']
            }
            
            self.log(f"\n✅ 任务完成! 质量等级: {qa_result['quality_score'].value}")
            
            return final_report
            
        except Exception as e:
            self.log(f"❌ 任务失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "task_id": task_id,
                "status": ReportStatus.FAILED,
                "error": str(e)
            }


def demo():
    """演示AI Agent报告生成系统"""
    print("=" * 60)
    print("专业星图 - AI Agent深度报告生成系统")
    print("=" * 60)
    
    # 创建协调Agent
    coordinator = CoordinatorAgent()
    
    # 模拟请求
    request = {
        "major_code": "080901",
        "major_name": "计算机科学与技术",
        "category": "08 工学",
        "priority": "high"
    }
    
    # 执行报告生成
    print(f"\n🚀 开始生成报告: {request['major_name']}")
    print("-" * 60)
    
    result = coordinator.run(request)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 生成结果")
    print("=" * 60)
    print(f"任务ID: {result['task_id']}")
    print(f"状态: {result['status'].value}")
    if result['status'] == ReportStatus.COMPLETED:
        print(f"质量等级: {result.get('quality_score', 'N/A').value}")
        print(f"评分: {result.get('score_value', 'N/A')}")
        
        print("\n📄 预览内容:")
        print("-" * 40)
        print(result['preview_content'][:600] + ("..." if len(result['preview_content']) > 600 else ""))
        
        print(f"\n📄 完整报告长度: {len(result['full_content'])} 字符")
        print("\n📄 完整报告开头:")
        print("-" * 40)
        print(result['full_content'][:800] + "...")


if __name__ == "__main__":
    demo()
