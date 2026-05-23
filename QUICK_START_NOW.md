# 🚀 快速操作指南 - 立即开始

## 已准备好的工具

我们已经为您准备好了所有需要的脚本！

---

## 📋 第一步：测试配置（5分钟）

### 1.1 运行系统测试
```bash
cd /workspace
python scripts/test_system.py
```

**预期结果**：所有测试通过 ✓

---

## 🧪 第二步：测试生成单个报告（10分钟）

### 2.1 试运行单个报告
```bash
python scripts/batch_generate.py --test
```

**这个命令会**：
- 获取数据库中的第一个专业
- 调用DeepSeek API生成报告
- 显示生成结果（不保存到数据库）

**预期结果**：
- 看到生成的报告预览
- 质量评分显示
- 雪峰点评示例

---

## 📦 第三步：开始批量生成

### 3.1 生成前5个专业（测试批量）
```bash
python scripts/batch_generate.py --start 1 --end 5
```

### 3.2 生成热门专业（前50个）
```bash
python scripts/batch_generate.py --start 1 --end 50
```

### 3.3 生成所有专业
```bash
python scripts/batch_generate.py --start 1
```

---

## ✅ 第四步：质量检查

### 4.1 运行完整质量检查
```bash
python scripts/quality_monitor.py --full
```

**这个命令会**：
- 检查所有已生成的报告
- 计算质量评分
- 找出需要审核的报告
- 生成统计报告

### 4.2 只查看统计
```bash
python scripts/quality_monitor.py --stats
```

### 4.3 导出低质量报告
```bash
python scripts/quality_monitor.py --export-low 70
```
（导出评分低于70分的报告）

---

## 📊 进度监控

### 查看生成进度
生成过程中会自动记录进度到 `data/generation_progress.json`

### 查看日志
所有操作日志保存在 `logs/batch_generate.log`

---

## 🎯 推荐执行流程

### 第1小时：测试阶段
```bash
# 1. 测试单个报告
python scripts/batch_generate.py --test

# 2. 如果满意，生成前5个
python scripts/batch_generate.py --start 1 --end 5

# 3. 检查质量
python scripts/quality_monitor.py --full
```

### 第2-4小时：第一波（50个）
```bash
python scripts/batch_generate.py --start 1 --end 50
python scripts/quality_monitor.py --full
```

### 第5-24小时：完整生成（611个）
```bash
python scripts/batch_generate.py --start 1
python scripts/quality_monitor.py --full
```

---

## 💰 成本监控

### DeepSeek API成本预估
| 操作 | 预计成本 |
|------|---------|
| 单个报告 | ¥0.1-0.2 |
| 前5个测试 | ¥0.5-1 |
| 前50个 | ¥5-10 |
| 全部611个 | ¥60-120 |

### 查看实际使用量
登录DeepSeek控制台查看API用量和费用：
https://platform.deepseek.com/

---

## ⚠️ 常见问题

### Q: 生成过程中报错怎么办？
A: 
- 检查 `logs/batch_generate.log` 查看详细错误
- 确认API Key配置正确
- 检查网络连接

### Q: 如何继续被中断的生成？
A: 直接重新运行相同的命令，系统会自动跳过已生成的报告。

### Q: 报告质量不满意怎么办？
A:
- 使用质量检查工具找出问题
- 可以重新生成低质量报告
- 根据反馈优化提示词

### Q: 如何查看已生成的报告？
A:
- 质量检查：`python scripts/quality_monitor.py --stats`
- 管理后台：https://fengyu1332-dad.github.io/Working-Pass/admin/index.html

---

## 📞 需要帮助？

查看详细文档：
- [实施路线图](docs/IMPLEMENTATION_PLAN.md)
- [AI Agent系统设计](docs/AI_AGENT_REPORT_SYSTEM.md)
- [开发指南](docs/DEVELOPMENT_GUIDE.md)

---

## 🎉 现在就开始！

**立即执行第一个命令：**
```bash
python scripts/batch_generate.py --test
```

看看效果如何！🚀
