# 专业星图 - 登录与后台管理系统设计文档

**版本**：v1.0
**创建日期**：2026-05-20
**状态**：待用户审查

---

## 一、项目概述

### 1.1 项目背景

专业星图网站是一个帮助学生了解大学专业选择的平台。现需要增加用户登录系统和后台管理功能，支持用户通过付费购买点数来下载深度分析报告。

### 1.2 项目目标

1. 实现用户注册和登录功能（手机号/邮箱）
2. 实现点数购买和消费系统
3. 实现深度分析报告的浏览和下载
4. 实现管理员后台系统

### 1.3 技术栈

- **前端**：HTML5 + CSS3 + JavaScript（原生）
- **后端服务**：Supabase（BaaS）
  - 用户认证（Auth）
  - PostgreSQL 数据库
  - 文件存储（Storage）
- **支付**：预留接口，当前版本为模拟支付

---

## 二、功能模块设计

### 2.1 用户系统

#### 2.1.1 用户注册

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 手机号 | string | 是 | 作为主要登录凭证 |
| 密码 | string | 是 | 至少8位，含数字和字母 |
| 邮箱 | string | 否 | 作为备用登录凭证 |

#### 2.1.2 用户登录

支持两种登录方式：
1. **手机号 + 密码**：主要登录方式
2. **邮箱 + 密码**：备用登录方式

#### 2.1.3 用户角色

| 角色 | 权限 |
|------|------|
| 普通用户 | 浏览报告、购买点数、下载报告、查看订单 |
| 管理员 | 所有普通用户权限 + 后台管理 |

### 2.2 点数系统

#### 2.2.1 点数套餐

| 套餐ID | 套餐名称 | 点数 | 价格（元） | 状态 |
|--------|----------|------|-----------|------|
| 1 | 体验档 | 1 | ¥1.00 | 上架 |
| 2 | 基础档 | 10 | ¥9.90 | 上架 |
| 3 | 推荐档 | 20 | ¥18.90 | 上架 |
| 4 | 畅享档 | 50 | ¥39.90 | 上架 |
| 5 | 尊享档 | 100 | ¥69.90 | 上架 |

#### 2.2.2 点数消费

- 每下载一份深度分析报告消耗 **1点**
- 点数不可提现
- 点数永久有效

### 2.3 报告系统

#### 2.3.1 报告结构

每份深度分析报告包含：
- 专业基本信息（代码、名称、学科门类）
- 深度分析内容（AI基于专属数据库实时生成）
- 发布时间
- 状态（草稿/已发布）

#### 2.3.2 报告下载流程

```
用户点击"下载报告" → 检查点数余额
    ├── 点数充足 → 扣减点数 → 生成报告 → 记录下载 → 返回报告文件
    └── 点数不足 → 提示充值
```

### 2.4 订单系统

#### 2.4.1 订单状态

| 状态码 | 状态名称 | 说明 |
|--------|----------|------|
| pending | 待支付 | 订单创建，等待用户支付 |
| paid | 已支付 | 支付成功，点数已到账 |
| cancelled | 已取消 | 订单超时或用户取消 |

#### 2.4.2 支付说明

在支付页面显著位置显示：
> ⚠️ **重要提示**：虚拟商品，一旦交付无法退货退款

---

## 三、数据库设计

### 3.1 数据表结构

#### 3.1.1 users（用户表）

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    points_balance INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 3.1.2 reports（报告表）

```sql
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    major_code VARCHAR(10) NOT NULL,
    major_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 3.1.3 point_packages（点数套餐表）

```sql
CREATE TABLE point_packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    points INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 3.1.4 orders（订单表）

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    package_id INTEGER REFERENCES point_packages(id),
    amount DECIMAL(10, 2) NOT NULL,
    points INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    paid_at TIMESTAMP WITH TIME ZONE
);
```

#### 3.1.5 download_records（下载记录表）

```sql
CREATE TABLE download_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    report_id UUID REFERENCES reports(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 四、页面设计

### 4.1 页面清单

#### 4.1.1 用户端页面

| 页面路径 | 页面名称 | 功能描述 |
|----------|----------|----------|
| /login.html | 登录页 | 手机号/邮箱登录 |
| /register.html | 注册页 | 用户注册 |
| /user/dashboard.html | 用户仪表板 | 查看点数余额、快捷入口 |
| /user/reports.html | 报告浏览 | 浏览和下载深度分析报告 |
| /user/orders.html | 我的订单 | 查看充值记录和下载历史 |

#### 4.1.2 管理端页面

| 页面路径 | 页面名称 | 功能描述 |
|----------|----------|----------|
| /admin/index.html | 管理后台首页 | 数据概览、热门报告 |
| /admin/users.html | 用户管理 | 用户列表、用户详情、调整点数 |
| /admin/reports.html | 报告管理 | 报告列表、新增/编辑报告 |
| /admin/orders.html | 订单管理 | 订单列表、订单统计 |
| /admin/packages.html | 套餐管理 | 点数套餐设置 |

### 4.2 页面设计规范

#### 4.2.1 视觉风格

- 与现有网站保持一致的设计语言
- 主色调：橙色（#E67E22）
- 辅助色：棕色（#705A49）
- 背景色：暖白色（#FFF8F5）

#### 4.2.2 响应式设计

- 移动端优先
- 断点：768px（平板）、1024px（桌面）

---

## 五、API 设计

### 5.1 认证 API

| 接口 | 方法 | 描述 |
|------|------|------|
| /auth/login | POST | 用户登录 |
| /auth/register | POST | 用户注册 |
| /auth/logout | POST | 用户登出 |
| /auth/me | GET | 获取当前用户信息 |

### 5.2 用户 API

| 接口 | 方法 | 描述 | 权限 |
|------|------|------|------|
| /users | GET | 获取用户列表 | 管理员 |
| /users/:id | GET | 获取用户详情 | 管理员 |
| /users/:id/points | PUT | 调整用户点数 | 管理员 |

### 5.3 报告 API

| 接口 | 方法 | 描述 | 权限 |
|------|------|------|------|
| /reports | GET | 获取报告列表 | 登录用户 |
| /reports/:id | GET | 获取报告详情 | 登录用户 |
| /reports | POST | 创建报告 | 管理员 |
| /reports/:id | PUT | 更新报告 | 管理员 |
| /reports/:id | DELETE | 删除报告 | 管理员 |
| /reports/:id/download | POST | 下载报告 | 登录用户 |

### 5.4 订单 API

| 接口 | 方法 | 描述 | 权限 |
|------|------|------|------|
| /orders | GET | 获取订单列表 | 管理员/本人 |
| /orders | POST | 创建订单 | 登录用户 |
| /orders/:id/pay | POST | 支付订单 | 登录用户 |
| /orders/:id/cancel | POST | 取消订单 | 登录用户 |

### 5.5 套餐 API

| 接口 | 方法 | 描述 | 权限 |
|------|------|------|------|
| /packages | GET | 获取套餐列表 | 公开 |
| /packages | POST | 创建套餐 | 管理员 |
| /packages/:id | PUT | 更新套餐 | 管理员 |
| /packages/:id | DELETE | 删除套餐 | 管理员 |

---

## 六、安全设计

### 6.1 认证安全

- 密码使用 bcrypt 加密存储
- 使用 JWT Token 进行身份验证
- Token 有效期：7天
- 登录失败限制：5次/小时

### 6.2 权限控制

- 管理员页面需要 role='admin' 权限
- 用户只能查看和操作自己的数据
- 敏感操作需要二次确认

### 6.3 数据安全

- 用户密码不可逆加密
- 敏感数据脱敏显示
- 操作日志记录

---

## 七、支付流程设计

### 7.1 支付流程

```
用户选择套餐 → 创建订单 → 选择支付方式 → 跳转支付页面
    ↓
支付成功 → 回调验证 → 更新订单状态 → 增加用户点数 → 发送通知
    ↓
支付失败 → 提示失败原因 → 返回订单页面
```

### 7.2 模拟支付

当前版本实现模拟支付：
1. 用户选择套餐，点击"立即购买"
2. 跳转模拟支付页面，显示订单信息
3. 点击"确认支付"（模拟）
4. 订单状态更新，点数增加

### 7.3 支付提示

支付页面必须包含：
```
⚠️ 重要提示：虚拟商品，一旦交付无法退货退款
```

---

## 八、实施计划

本设计文档确认后，将拆分为以下实施阶段：

1. **第一阶段：基础架构**
   - Supabase 项目配置
   - 数据库表创建
   - 基础页面框架

2. **第二阶段：用户系统**
   - 注册/登录功能
   - 用户认证
   - 密码重置

3. **第三阶段：点数与订单**
   - 点数套餐管理
   - 模拟支付流程
   - 订单管理

4. **第四阶段：报告系统**
   - 报告浏览页面
   - 报告下载功能
   - AI报告生成接口预留

5. **第五阶段：管理后台**
   - 用户管理
   - 报告管理
   - 订单管理
   - 套餐管理

---

## 九、待确认事项

1. ✅ 用户角色（管理员 + 普通用户）
2. ✅ 登录方式（手机号/邮箱）
3. ✅ 点数套餐（5档）
4. ✅ 消费规则（1点/份报告）
5. ✅ 支付提示（虚拟商品不可退款）
6. ⏳ AI报告生成接口（后续对接）
7. ⏳ 真实支付接口（支付宝/微信，后续对接）

---

**文档状态**：待用户审查确认
