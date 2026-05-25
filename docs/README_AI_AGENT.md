# 专业星图 AI Agent 系统

> 专业深度报告智能生成平台

## 项目简介

本项目是一个基于多Agent协作的智能报告生成系统，用于为高考考生提供专业深度分析报告。

## 核心功能

- 🤖 多Agent协作报告生成
- 📊 深度专业分析
- ⭐ 雪峰风格点评
- ✅ 质量审核与评分
- 💾 批量数据处理

## 系统架构

```
┌─────────────────────────────────────────┐
│           用户请求层                     │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          任务协调Agent                   │
│        (Coordinator Agent)              │
└──────────────────┬──────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│ 数据   │   │ 深度   │   │ 雪峰   │
│ 收集   │   │ 分析   │   │ 点评   │
│ Agent  │   │ Agent  │   │ Agent  │
└───┬────┘   └────┬───┘   └───┬────┘
    └──────────────┼────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          报告合成Agent                   │
│        (Composer Agent)                │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          质量审核Agent                   │
│      (Quality Assurance Agent)          │
└─────────────────────────────────────────┘
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/fengyu1332-dad/Working-Pass.git
cd Working-Pass
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
# LLM API配置
OPENAI_API_KEY=your_openai_api_key_here
# 或
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Supabase配置
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# 其他配置
LOG_LEVEL=INFO
MAX_WORKERS=5
```

### 5. 运行演示

```bash
python ai_agent_demo.py
```

## 项目结构

```
.
├── ai_agent_demo.py              # AI Agent演示程序
├── ai_agent_report_system.py     # AI Agent系统主文件
├── migrate_majors_to_reports.py  # 数据迁移脚本
├── config.py                      # 配置文件
├── utils/
│   ├── __init__.py
│   ├── api_client.py            # LLM API客户端
│   ├── database.py              # 数据库操作
│   └── logger.py                # 日志工具
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # Agent基类
│   ├── data_collection.py      # 数据收集Agent
│   ├── deep_analysis.py         # 深度分析Agent
│   ├── xuefeng_comment.py       # 雪峰点评Agent
│   ├── composer.py              # 报告合成Agent
│   └── quality_assurance.py     # 质量审核Agent
├── scripts/
│   ├── generate_report.py       # 单独生成报告
│   ├── batch_generate.py        # 批量生成报告
│   └── test_system.py           # 系统测试
├── docs/
│   ├── AI_AGENT_REPORT_SYSTEM.md    # 系统设计文档
│   ├── SETUP_GUIDE.md               # 设置指南
│   └── API_DOCUMENTATION.md         # API文档
└── tests/
    ├── test_agents.py
    ├── test_integration.py
    └── test_quality.py
```

## 使用指南

### 生成单个报告

```python
from agents.coordinator import CoordinatorAgent

coordinator = CoordinatorAgent()
result = coordinator.run({
    "major_code": "080901",
    "major_name": "计算机科学与技术",
    "category": "08 工学"
})

print(result)
```

### 批量生成报告

```bash
python scripts/batch_generate.py --start 1 --end 100
```

### 查看质量报告

```bash
python scripts/test_system.py --mode quality
```

## API接口

### REST API

#### 生成报告
```
POST /api/v1/reports/generate

{
  "major_code": "080901",
  "major_name": "计算机科学与技术",
  "category": "08 工学"
}
```

#### 批量生成
```
POST /api/v1/reports/batch

{
  "majors": [
    {"major_code": "080901", "major_name": "计算机科学与技术"},
    {"major_code": "080902", "major_name": "软件工程"}
  ]
}
```

#### 查询状态
```
GET /api/v1/reports/{task_id}
```

## 配置说明

### LLM配置

编辑 `config.py`:

```python
LLM_CONFIG = {
    "provider": "openai",  # openai, anthropic, baidu, alibaba
    "model": "gpt-4",      # gpt-4, gpt-3.5-turbo, claude-3-opus, etc.
    "temperature": 0.7,
    "max_tokens": 2000
}
```

### Agent配置

```python
AGENT_CONFIG = {
    "enable_cache": True,
    "retry_times": 3,
    "timeout": 60
}
```

## 质量保证

### 质量评分标准

- **A级（90-100分）**：优秀，直接发布
- **B级（75-89分）**：良好，小幅修正后发布
- **C级（60-74分）**：合格，需重新生成部分内容
- **D级（60分以下）**：不合格，重新生成

### 评分维度

- 内容完整性：20分
- 信息准确性：20分
- 深度分析：20分
- 实用性：20分
- 语言表达：10分
- 格式规范：10分

## 性能优化

### 1. 缓存策略

启用响应缓存避免重复生成：

```python
config.enable_cache = True
config.cache_ttl = 86400  # 24小时
```

### 2. 并发处理

批量生成时使用并发：

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(generate_report, majors)
```

### 3. 速率限制

遵守API速率限制：

```python
config.rate_limit = {
    "requests_per_minute": 60,
    "tokens_per_minute": 100000
}
```

## 监控与日志

### 日志配置

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_agent.log'),
        logging.StreamHandler()
    ]
)
```

### 性能监控

```bash
# 启动监控
python scripts/monitor.py --port 8080

# 查看日志
tail -f ai_agent.log
```

## 部署指南

### Docker部署

```bash
# 构建镜像
docker build -t professional-starmap-ai-agent .

# 运行容器
docker run -d -p 5000:5000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  professional-starmap-ai-agent
```

### 云函数部署

参考 `docs/DEPLOYMENT.md` 了解如何部署到：
- AWS Lambda
-阿里云函数计算
- 腾讯云SCF

## 常见问题

### Q: 报告生成失败怎么办？

A: 检查以下几点：
1. API密钥是否正确配置
2. API额度是否充足
3. 网络连接是否正常
4. 查看日志获取详细错误信息

### Q: 如何提高生成速度？

A: 优化策略：
1. 启用缓存避免重复生成
2. 使用更快的模型（如GPT-3.5）
3. 减少并发量避免API限流
4. 优化网络连接

### Q: 如何保证报告质量？

A: 质量保证措施：
1. 启用质量审核Agent
2. 设置最低质量阈值
3. 定期人工抽检
4. 收集用户反馈持续优化

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目主页：https://fengyu1332-dad.github.io/Working-Pass
- 问题反馈：https://github.com/fengyu1332-dad/Working-Pass/issues

## 致谢

- 张雪峰老师 - 专业的点评风格启发
- OpenAI - GPT-4模型支持
- Supabase - 数据库支持
- 所有贡献者
