# 深度分析报告批量生成 — 经验总结与操作手册

> 基于 2026-05-29 日 883 份报告批量生成实战经验提炼
> 配套文档：CLAUDE.md（内容标准）| quality-verify.js（验证脚本）

---

## 一、核心教训

### 1.1 Python/JS 语法混淆

**问题：** 在 Python 中写了 JavaScript 语法 `text_only.length`

**教训：** 从 Edge Function (TypeScript) 移植 buildPreview 逻辑到 Python 时，必须逐行检查语法差异。

**检查清单：**
- `str.length` → `len(str)`
- `array.length` → `len(array)`
- `array.push(x)` → `array.append(x)`
- `array.includes(x)` → `x in array`
- `const { x } = obj` → `x = obj.get('x')` 或 `x = obj['x']`

### 1.2 异常被静默吞掉

**问题：** 原代码在 except 块中判断 `if "API" not in str(e): raise`，导致 API 错误（状态码非 200）被吞掉。后续代码访问未赋值的 `html` 变量崩溃。

```python
# ❌ 错误写法
except asyncio.TimeoutError:
    raise Exception("timeout")
except Exception as e:
    if "API" not in str(e) and "timeout" not in str(e):
        raise
    # 这里 API 错误会被静默吞掉！

# ✅ 正确写法
except asyncio.TimeoutError:
    raise Exception(f"timeout after {TIMEOUT}s")
except Exception:
    raise  # 无条件 re-raise
```

**教训：** except 块中永远不要有条件 re-raise。如果需要分类处理错误，在调用方 catch 并按类型分发。

### 1.3 断点续传进度文件不可靠

**问题：** 进度文件每 5 份保存一次，但如果脚本中途崩溃，最后一批未保存进度的报告会丢失。初次运行时进度文件为空（0 entries），导致 435 份已有的报告无法被跳过。

**解决方案：**
- 启动时**同时**检查：1）进度文件（`batch_progress.json`）2）Supabase 数据库已有报告
- `existing_codes = from_db | from_progress_file`（取并集）
- 进度文件只作为辅助加速，Supabase 查询才是权威来源

### 1.4 409 重复键应视为成功而非失败

**问题：** Supabase reports 表有 `major_code UNIQUE` 约束。如果同一专业被两次生成（如从进度文件恢复时），第二次 insert 会报 409。

**解决方案：**
```python
async def insert_report(session, report):
    ...
    if resp.status == 409:
        print(f"  [SKIP] duplicate: {report['major_code']}")
        return False  # 返回 False 但不抛异常
    ...
```

### 1.5 并发 + 串行日志导致输出交错

**问题：** 5 个并发请求同时完成时，`print()` 输出会交错，日志难以阅读。

**已接受的折中：** 不引入额外锁（会影响性能），交错输出可接受。

### 1.6 Windows GBK 编码导致 emoji/中文 乱码

**问题：** Windows 终端默认 GBK 编码，emoji 和 `¥` 符号无法正常显示。

**解决方案：**
```bash
# 设置环境变量
PYTHONIOENCODING=utf-8 python -u script.py > log.txt 2>&1

# 或在脚本头部
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

---

## 二、标准参数配置

### 2.1 API 调用参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `model` | `deepseek-chat` | 性价比最高 |
| `max_tokens` | **16000** | 10000 导致末尾章节截断 |
| `temperature` | **0.5** | 数据准确性 + 创造性的平衡点 |
| `timeout` | **180s** | 130s 不够（约 8% 超时）；180s 降至 0% |
| `concurrency` | **5** | 5 并发稳定；更高可能触发 429 |

### 2.2 验证阈值

| 指标 | 阈值 | 说明 |
|------|------|------|
| 最低字符数 | **7000** | 8000 过于严格（~3% 误杀）；7000 合理 |
| 最少 h2 章节 | 13 | 缺章直接拒绝 |
| h1 标题匹配 | 必须含专业名 | 防止张冠李戴 |
| HTML 表格 | 至少 1 个 | 确保数据可视化 |
| AI 身份暴露 | 禁止 | "作为AI""根据训练数据" 等 |

### 2.3 重试参数

| 场景 | 策略 |
|------|------|
| 字数不足 (<7000) | 重新生成（temperature 不变，max_tokens 不变） |
| 超时 | 重新生成（timeout 已增至 180s） |
| API 错误 (5xx) | 等待 30s 后重试 |
| 速率限制 (429) | 等待 60s 后重试 |

---

## 三、生成前检查清单

每次批量生成前，逐项确认：

- [ ] `DEEPSEEK_API_KEY` 已设置且有余额
- [ ] Supabase `reports` 表无 schema 变更
- [ ] `majors` 表数据完整（883 条，12 字段非空）
- [ ] `validate_report()` 阈值确认合理
- [ ] `build_preview()` 核对 Chapter 名称与 `CHAPTER_DESC` 一致
- [ ] 超时参数 >= 180s
- [ ] `insert_report()` 正确处理 409
- [ ] except 块无静默吞异常
- [ ] `PYTHONIOENCODING=utf-8` 已设置
- [ ] 进度文件路径正确
- [ ] `CONCURRENCY` 不超过 5

---

## 四、执行流程

```
Phase 0: 质量检查
  node scripts/quality-verify.js
    确认 883 majors 数据完整、12 字段非空、格式正确

Phase 1: 小规模测试
  python scripts/batch_test_5.py
    检查 5 份不同门类报告质量（13 章完整、字数达标、数据具体）
    人工审阅至少 2 份

Phase 2: 全量生成
  python scripts/batch_generate_reports.py
    5 并发、断点续传、自动入库 status=draft
    预期耗时：~2.5 小时 / 448 份

Phase 3: 重试失败
  查看 batch_failed.json 统计失败原因
  调整参数后重新运行（自动跳过已有）
  目标：0 失败

Phase 4: 发布
  管理后台一键全量发布：PATCH /rest/v1/reports?status=eq.draft → published
  或 SQL: UPDATE reports SET status='published' WHERE status='draft';
```

---

## 五、常见故障速查

| 症状 | 根因 | 解决 |
|------|------|------|
| 报告末尾章节不完整 | max_tokens 不足 | 增至 16000 |
| `'str' object has no attribute 'length'` | Python 中写了 JS 语法 | `len()` |
| `cannot access local variable 'html'` | API 错误被吞 + html 未赋值 | except 块改为无条件 raise |
| 大量 409 冲突 | UNIQUE 约束 + 断点恢复时重复生成 | insert 中 catch 409 返回 False |
| 日志全是乱码 | GBK 编码 | `PYTHONIOENCODING=utf-8` |
| 8% 超时 | DeepSeek 偶尔响应慢 | 超时 130s→180s |
| `'gbk' codec can't encode '\xa5'` | `¥` 字符 | 设置 UTF-8 输出 wrapper |
| 进度已保存但重启后重复生成 | 进度文件不包含 DB 已有数据 | 启动时取 `from_db | from_file` 并集 |

---

## 六、质量验证脚本使用

```bash
# 运行全量质量检查（12 项）
node scripts/quality-verify.js

# 快速检查特定问题
python scripts/scan_name_mismatches.py   # 张冠李戴扫描
python scripts/check_quality.py          # 字段维度统计
```

**已知可忽略的告警：**
- `yearly_courses` < 10 门课：军事/公安/小语种等特殊专业，宁缺毋假
- `top_universities` 国际院校不足 3 所：中国特有专业（公安/中医/党务），合理
- `name 与 MOE 不一致`：确认是终端编码问题（GBK 显示）还是真实差异后再决定

---

## 七、关键文件索引

| 文件 | 作用 |
|------|------|
| `scripts/batch_generate_reports.py` | **生产级批量生成脚本**（5 并发/断点续传/自动入库） |
| `scripts/batch_test_5.py` | 5 份测试报告（质量验证用） |
| `scripts/quality-verify.js` | 12 项全字段质量验证（CI 门禁） |
| `scripts/scan_name_mismatches.py` | 张冠李戴扫描 |
| `scripts/fix-all-content-fields.js` | 内容字段批量修复 |
| `scripts/fix-all-name-mismatches.js` | overview 张冠李戴修复 |
| `scripts/check_quality.py` | 快速字段维度统计 |
| `scripts/data/knowledge-base.js` | 14 门类 KB 模板函数 |
| `supabase/functions/generate-report/index.ts` | Edge Function（单份生成） |
| `data/batch_progress.json` | 断点续传进度 |
| `data/batch_failed.json` | 失败记录 |
| `.claude/CLAUDE.md` | 内容生成标准与字段规范 |
| `.claude/REPORT_GENERATION_GUIDE.md` | 本文档 |

---

## 八、版本历史

| 日期 | 事件 |
|------|------|
| 2026-05-29 | 初始批量测试：5 份通过 |
| 2026-05-29 | 首次生产运行：214 成功 / 661 失败（API 吞异常 bug） |
| 2026-05-29 | 修复后二次运行：416 成功 / 32 失败（超时+字数不足） |
| 2026-05-29 | 最终重试：32 全部成功 |
| 2026-05-29 | 总计 883/883 (100%) 报告入库并发布 |
