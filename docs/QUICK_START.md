# 专业星图 AI Agent 系统 - 快速开始指南

**版本**: v1.0  
**更新时间**: 2026-05-22

---

## 📋 目录

1. [环境准备](#1-环境准备)
2. [获取API密钥](#2-获取api密钥)
3. [配置项目](#3-配置项目)
4. [运行测试](#4-运行测试)
5. [生成第一批报告](#5-生成第一批报告)
6. [部署到生产环境](#6-部署到生产环境)

---

## 1. 环境准备

### 方式一：使用自动设置脚本（推荐）

```bash
# 克隆项目（如果还没有）
git clone https://github.com/fengyu1332-dad/Working-Pass.git
cd Working-Pass

# 运行自动设置脚本
python setup_env.py
```

脚本会自动完成：
- ✅ 检查Python版本
- ✅ 创建虚拟环境
- ✅ 安装所有依赖
- ✅ 创建配置文件

### 方式二：手动设置

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
```

---

## 2. 获取API密钥

### 选项1：OpenAI API（推荐）

1. 访问 https://platform.openai.com/
2. 注册账号并登录
3. 进入 API Keys 页面
4. 点击 "Create new secret key"
5. 复制生成的密钥

**注意**：
- GPT-4质量最好，但成本较高
- 可以先用GPT-3.5测试，降低成本

### 选项2：Anthropic Claude API

1. 访问 https://www.anthropic.com/
2. 注册账号并登录
3. 获取API密钥
4. Claude 3在长文本处理方面表现优异

### 选项3：国内API（百度/阿里）

如果主要面向国内用户，可以考虑：
- 百度文心一言：https://cloud.baidu.com/
- 阿里通义千问：https://dashscope.console.aliyun.com/

**优点**：访问速度快，无需翻墙  
**缺点**：质量略逊于GPT-4

---

## 3. 配置项目

### 3.1 编辑 .env 文件

```bash
# 打开 .env 文件
nano .env  # Linux/Mac
# 或使用记事本
notepad .env  # Windows
```

填入您的API密钥：

```env
# OpenAI 配置
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4

# Supabase 配置（已预先配置）
SUPABASE_URL=https://djteatwxjlnbjylynvjh.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# 系统配置
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 3.2 验证配置

```bash
# 测试数据库连接
python -c "from utils.database import get_supabase_client; client = get_supabase_client(); print('✅ 数据库连接成功')"

# 测试LLM客户端
python -c "from utils.api_client import get_default_client; print('✅ LLM客户端配置成功')"
```

---

## 4. 运行测试

### 4.1 运行演示程序

```bash
python ai_agent_demo.py
```

**预期输出**：
```
============================================================
专业星图 - AI Agent深度报告生成系统
============================================================

🚀 开始生成报告: 计算机科学与技术
------------------------------------------------------------
[CoordinatorAgent] 开始执行任务: task_xxx
...
✅ 任务完成! 质量等级: A

📊 生成结果
============================================================
任务ID: task_xxx
状态: completed
质量等级: A
评分: 90
```

### 4.2 测试质量评分系统

```bash
python scripts/test_system.py --mode quality
```

### 4.3 查看日志

```bash
# 实时查看日志
tail -f ai_agent.log

# 或查看最近100行
tail -100 ai_agent.log
```

---

## 5. 生成第一批报告

### 5.1 生成单个报告测试

```bash
python scripts/generate_report.py --major-code 080901 --major-name "计算机科学与技术"
```

### 5.2 批量生成前10个专业

```bash
python scripts/batch_generate.py --start 1 --end 10 --quality-threshold 60
```

**参数说明**：
- `--start`: 起始序号
- `--end`: 结束序号
- `--quality-threshold`: 质量分数阈值（低于此分数会重新生成）

### 5.3 查看生成进度

```bash
python scripts/batch_generate.py --start 1 --end 100 --verbose
```

批量生成100个专业报告，预计需要：
- **使用GPT-4**：约30-60分钟，成本约$5-10
- **使用GPT-3.5**：约15-30分钟，成本约$1-2

### 5.4 检查生成结果

```bash
# 查看已生成的报告数量
python -c "from utils.database import get_supabase_client; client = get_supabase_client(); print(f'已生成报告数: {client.get_reports_count()}')"

# 随机查看一个报告
python scripts/test_system.py --mode sample
```

---

## 6. 部署到生产环境

### 方案A：Docker部署（推荐）

#### 构建Docker镜像

```bash
# 构建镜像
docker build -t professional-starmap-ai-agent .

# 运行容器
docker run -d -p 5000:5000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e SUPABASE_URL=$SUPABASE_URL \
  -e SUPABASE_KEY=$SUPABASE_KEY \
  professional-starmap-ai-agent
```

#### 使用Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ai-agent:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

启动服务：

```bash
docker-compose up -d
```

### 方案B：云函数部署

#### AWS Lambda

```bash
# 安装AWS CLI和SAM CLI
pip install aws-sam-cli

# 初始化SAM项目
sam init --runtime python3.9

# 部署
sam deploy --guided
```

#### 阿里云函数计算

1. 安装函数计算CLI
2. 创建函数
3. 配置触发器（API网关）
4. 部署函数

详细步骤请参考：`docs/DEPLOYMENT.md`

### 方案C：传统服务器部署

```bash
# 1. 安装Nginx
sudo apt install nginx

# 2. 配置Gunicorn
pip install gunicorn

# 3. 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 4. 配置Nginx反向代理
sudo nano /etc/nginx/sites-available/default
```

---

## 🚀 快速开始清单

在继续之前，请确认以下步骤已完成：

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已创建
- [ ] 所有依赖已安装
- [ ] .env 文件已配置（包含API密钥）
- [ ] 运行 `python ai_agent_demo.py` 成功
- [ ] 测试生成1-2个报告成功

---

## 💡 常见问题

### Q1: 报 "No module named 'xxx'" 错误

**解决**：
```bash
pip install xxx
```

### Q2: 报 "API key not found" 错误

**解决**：
1. 检查 .env 文件是否正确配置
2. 确保没有多余的空格或引号
3. 重新加载环境变量：
```bash
export $(cat .env | xargs)  # Linux/Mac
```

### Q3: API调用失败或超时

**解决**：
1. 检查网络连接
2. 查看API配额是否用完
3. 降低并发数量

### Q4: 报告质量不高

**解决**：
1. 使用GPT-4而非GPT-3.5
2. 调整temperature参数（建议0.7）
3. 优化Prompt模板

---

## 📚 下一步

完成环境设置后，您可以：

1. **深入学习系统架构**：[AI_AGENT_REPORT_SYSTEM.md](docs/AI_AGENT_REPORT_SYSTEM.md)

2. **优化Prompt设计**：调整 `config.py` 中的AGENT_PROMPTS

3. **添加新功能**：扩展Agent能力，添加新的分析维度

4. **性能优化**：启用缓存、调整并发参数

5. **监控与日志**：配置生产环境的监控告警

---

## 🎯 成功指标

恭喜您！如果完成了以下内容，说明系统已正常运行：

- ✅ 成功运行 `python ai_agent_demo.py`
- ✅ 成功生成第一个专业报告
- ✅ 报告质量评分达到A级（90+分）
- ✅ 报告已保存到数据库

---

**有问题？**
- 查看详细文档：[docs/](docs/)
- 提交Issue：https://github.com/fengyu1332-dad/Working-Pass/issues
- 联系支持：fengyu1332@example.com

---

*祝您使用愉快！🚀*
