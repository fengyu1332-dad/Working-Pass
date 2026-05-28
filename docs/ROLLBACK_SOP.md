# 专业星图 — 回滚标准操作流程 (SOP)

**版本**: v1.0 | **最后更新**: 2026-05-26

---

## 一、触发条件

以下任一情况发生时，应立即评估是否执行回滚：

| 级别 | 条件 | 响应时间 |
|------|------|:--------:|
| P0 紧急 | 首页无法访问、所有用户无法登录、数据完全不可见 | 立即执行 |
| P1 严重 | 核心功能断裂（专业搜索无结果、报告无法下载）、支付流程异常 | 15 分钟内 |
| P2 一般 | 非核心页面报错、UI 显示异常但不影响主流程 | 1 小时内 |

---

## 二、回滚步骤

### GitHub Pages 回滚（前端）

```bash
# 1. 查看最近的部署提交
git log --oneline origin/gh-pages -5

# 2. 确定要回滚到的提交 SHA（通常是上一个正常版本的 HEAD）
ROLLBACK_SHA=<上一个正常的提交SHA>

# 3. 切到 gh-pages 分支
git fetch origin gh-pages
git checkout gh-pages

# 4. 硬回滚到目标版本
git reset --hard $ROLLBACK_SHA

# 5. 强制推送（注意：这是少数允许 force push 的场景）
git push origin gh-pages --force

# 6. 切回主分支
git checkout main
```

### 如果 gh-pages 分支由 GitHub Actions 自动部署

```bash
# 方法 1：在 GitHub 仓库 Settings > Pages 中切换源分支为上一个 tag

# 方法 2：手动触发上一次成功的 workflow run
# GitHub Actions → Deploy to GitHub Pages → 上一次成功运行 → Re-run all jobs

# 方法 3：手动部署已知正常的提交
git checkout <known-good-commit>
git push origin HEAD:gh-pages --force
git checkout main
```

### Supabase 回滚（后端）

Supabase 不提供一键回滚。采用以下替代方案：

```sql
-- 1. 如果是数据问题，从备份恢复（见 docs/STORAGE_GUIDE.md）
-- 2. 如果是 RLS 策略问题，重新执行 sql/supabase-init.sql 中的原始策略
-- 3. 如果是表结构问题，在 Supabase Dashboard > SQL Editor 中手动修复
```

---

## 三、验证步骤

回滚完成后，**必须**逐项验证：

- [ ] 首页正常加载，专业数据可见
- [ ] 搜索功能返回正常结果
- [ ] 专业详情弹窗正常打开
- [ ] 用户可正常登录/注册
- [ ] 报告列表可正常加载
- [ ] 点数购买流程正常
- [ ] 移动端页面正常显示
- [ ] 浏览器控制台无红色错误

### 快速验证命令

```bash
# 检查首页 HTTP 状态
curl -s -o /dev/null -w "%{http_code}" https://<你的域名>/

# 检查 Supabase API
curl -s -H "apikey: <ANON_KEY>" "https://<PROJECT_ID>.supabase.co/rest/v1/majors?select=count"
```

---

## 四、通知模板

事故通知（通过飞书/Slack/微信群发送）：

```
【专业星图 - 回滚通知】

事故时间：YYYY-MM-DD HH:MM
回滚时间：YYYY-MM-DD HH:MM
影响范围：<简述哪些功能受影响>
回滚版本：<回滚到的提交 SHA>
当前状态：<已恢复 / 持续关注>

回滚人：<姓名>
验证人：<姓名>
```
```

---

## 五、预防措施

1. **每次部署前**：确保最近一次成功的 GitHub Pages workflow run 是可达的
2. **重大变更前**：在本地完整验证所有核心页面
3. **保留备份**：`sql/` 目录保留完整的初始化 SQL，可随时重建数据库结构
4. **分支保护**：main 分支开启 branch protection，要求 PR review 后方可合并

---

## 六、相关链接

- GitHub Actions 部署日志：`https://github.com/<owner>/<repo>/actions/workflows/deploy.yml`
- Uptime 监控日志：`https://github.com/<owner>/<repo>/actions/workflows/uptime.yml`
- Supabase Dashboard：`https://supabase.com/dashboard/project/<PROJECT_ID>`
