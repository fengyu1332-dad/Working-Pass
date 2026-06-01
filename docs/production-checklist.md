# 生产环境切换清单

## 一、支付宝密钥切换

### 1.1 获取生产环境凭证

- [ ] 登录 [支付宝开放平台](https://open.alipay.com/) 商户账号
- [ ] 在"控制台 → 我的应用"中找到已上线的应用，获取 **APPID**（替换沙箱 `2021xxx`）
- [ ] 在"接口加签方式"中上传应用公钥，获取 **支付宝公钥**
  - 模式选：**公钥模式** (非证书模式)
  - 语言选：**非 JAVA**
- [ ] 安全保存 **应用私钥**（即 `ALIPAY_PRIVATE_KEY`）

### 1.2 更新 Supabase Secrets

```bash
supabase secrets set ALIPAY_APP_ID=<生产APPID>
supabase secrets set ALIPAY_PRIVATE_KEY="<生产应用私钥>"
supabase secrets set ALIPAY_PUBLIC_KEY="<生产支付宝公钥>"
supabase secrets set ALIPAY_GATEWAY=https://openapi.alipay.com/gateway.do
```

> 注意：`ALIPAY_PRIVATE_KEY` 含换行，用引号包裹。

### 1.3 密钥格式验证

```bash
# 私钥应以 BEGIN/END 包裹
echo "$ALIPAY_PRIVATE_KEY" | head -1
# → -----BEGIN PRIVATE KEY-----
#    （不是 BEGIN RSA PRIVATE KEY）
```

---

## 二、前端 URL

- [ ] 确认生产域名（如 `https://your-domain.com`）

```bash
supabase secrets set FRONTEND_URL=https://your-domain.com
```

> `create-alipay-order` 函数用此 URL 构建 `return_url`（支付完成后跳回页面）。

---

## 三、代码检查

### 3.1 `supabase/functions/create-alipay-order/index.ts`

- [ ] 第 114 行：确认 `ALIPAY_GATEWAY` secret 已设置（代码有 fallback 到沙箱，生产必须覆盖）
- [ ] 第 115 行：确认 `FRONTEND_URL` secret 已设置

### 3.2 `supabase/functions/alipay-notify/index.ts`

- [ ] 确认 SHA256 验签逻辑使用 `ALIPAY_PUBLIC_KEY` secret
- [ ] 确认 `complete_alipay_order` RPC 已在数据库中创建

### 3.3 `js/pages/payment.js`

- [ ] 确认页面域名与 `FRONTEND_URL` 一致（支付宝要求 `return_url` 在白名单内）
- [ ] 确认 `payment-callback.html` 中的成功/超时/失败跳转路径使用相对路径

---

## 四、数据库检查

- [ ] `majors` 表 RLS 已启用（`sql/enable-majors-rls.sql`）
- [ ] `web_vitals` 表已创建（`sql/web-vitals-table.sql`）
- [ ] `admin_audit_logs` 表已创建（`sql/audit-logs.sql`）
- [ ] `expire_pending_orders` 函数 + pg_cron 定时任务已部署
- [ ] `complete_alipay_order` 函数存在（原子化支付完成）
- [ ] `spend_points` 函数存在（原子化积分消费）
- [ ] `log_admin_action` 函数存在（审计日志）

---

## 五、Edge Functions 部署

```bash
# 全部重新部署（生产配置就绪后）
supabase functions deploy create-alipay-order
supabase functions deploy alipay-notify --no-verify-jwt
supabase functions deploy expire-orders
supabase functions deploy collect-vitals --no-verify-jwt
supabase functions deploy generate-report
supabase functions deploy admin-create-user
supabase functions deploy admin-delete-user
```

---

## 六、测试验证

### 6.1 支付宝支付全链路

- [ ] 创建订单 → 跳转支付宝收银台（确认是生产收银台，非沙箱）
- [ ] 扫码支付 → 确认回调跳回 `payment-callback.html?out_trade_no=xxx`
- [ ] 验证订单状态从 `pending` → `paid`
- [ ] 验证用户点数余额增加
- [ ] 验证支付宝后台能看到交易记录

### 6.2 支付宝异步通知

- [ ] 确认 `alipay-notify` 函数路由可公开访问（无 401）
- [ ] 支付宝后台配置通知 URL：`https://<project>.supabase.co/functions/v1/alipay-notify`
- [ ] 手动创建订单 → 支付 → 确认通知被接收（查看 Edge Function 日志）

### 6.3 订单过期（备用）

- [ ] 创建订单后不支付，等待 `expires_at` 过期
- [ ] 确认 pg_cron 自动将状态改为 `expired`
- [ ] 确认 `expire-orders` Edge Function 可手动触发

### 6.4 Web Vitals

- [ ] 打开生产站点 → 浏览器 F12 → Network 搜索 `collect-vitals`
- [ ] 确认 `sendBeacon` POST 成功（200）
- [ ] 确认 `web_vitals` 表有新记录

### 6.5 审计日志

- [ ] 管理后台执行任意操作（改用户角色等）
- [ ] 确认 `admin_audit_logs` 表有新记录
- [ ] 确认记录包含 `admin_id`、`action`、`resource`、`detail`

---

## 七、回滚方案

如生产支付出现问题：

1. 支付宝密钥回滚：
   ```bash
   supabase secrets set ALIPAY_GATEWAY=https://openapi-sandbox.dl.alipaydev.com/gateway.do
   supabase secrets set ALIPAY_APP_ID=<沙箱APPID>
   # 恢复沙箱公私钥
   ```

2. 代码无 Git 变更（所有切换仅涉及 Supabase secrets），无需回滚代码

3. 数据库 RLS/函数不需要回滚（与支付无直接耦合）
