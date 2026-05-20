# 专业星图 - 登录与后台管理系统设计文档

**版本：** v1.0  
**创建日期：** 2026-05-20  
**状态：** 待实施  
**作者：** 专业星图团队

---

## 目录

1. [项目概述](#1-项目概述)
2. [技术架构](#2-技术架构)
3. [数据库设计](#3-数据库设计)
4. [页面设计](#4-页面设计)
5. [API设计](#5-api设计)
6. [业务流程](#6-业务流程)
7. [安全设计](#7-安全设计)
8. [实施计划](#8-实施计划)
9. [风险评估](#9-风险评估)

---

## 1. 项目概述

### 1.1 项目背景

专业星图是一个帮助学生了解大学专业选择的平台，目前已拥有611个完整的专业信息库。为了进一步提升用户体验，实现商业变现，需要增加用户登录系统和深度分析报告功能。

### 1.2 核心决策

| 决策项 | 选择 | 说明 |
|--------|------|------|
| **认证系统** | Supabase Auth | 企业级安全、开发效率高 |
| **支付方式** | 模拟支付 | 快速验证商业模式 |
| **第三方登录** | 微信登录 | 中国用户首选 |
| **报告生成** | 预先生成 | 用户体验最佳 |
| **点数有效期** | 永久有效 | 用户体验最好 |
| **预览功能** | 预览+付费 | 引导用户购买 |
| **功能范围** | MVP版本 | 聚焦核心功能 |

### 1.3 功能范围

#### 1.3.1 用户端（MVP）

| 功能模块 | 功能描述 | 优先级 |
|----------|----------|--------|
| 用户认证 | 手机号/微信注册登录 | P0 |
| 个人中心 | 查看点数余额、快捷入口 | P0 |
| 报告浏览 | 浏览611个专业报告列表 | P0 |
| 报告预览 | 免费查看报告前20%内容 | P0 |
| 报告下载 | 消耗1点下载完整报告 | P0 |
| 点数购买 | 模拟支付购买点数套餐 | P0 |
| 历史记录 | 查看订单和下载历史 | P0 |

#### 1.3.2 管理端（MVP）

| 功能模块 | 功能描述 | 优先级 |
|----------|----------|--------|
| 数据概览 | 查看用户数、订单数、下载数 | P1 |
| 用户管理 | 查看用户列表、调整点数 | P1 |
| 报告管理 | 查看报告列表、上传/更新报告 | P2 |

### 1.4 成功指标

- 用户注册率 > 30%
- 报告购买转化率 > 5%
- 月留存率 > 20%
- 日活跃用户 > 100（上线第一个月）

---

## 2. 技术架构

### 2.1 技术栈

```
┌─────────────────────────────────────────────────────────────┐
│                        前端层                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  HTML5 + CSS3 + JavaScript（原生）                     │  │
│  │  - 响应式设计（移动优先）                              │  │
│  │  - Supabase JS SDK（客户端）                            │  │
│  │  - Font Awesome（图标库）                               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        认证层                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase Auth                                         │  │
│  │  - 手机号+密码登录                                      │  │
│  │  - 微信登录（OAuth 2.0）                                 │  │
│  │  - JWT Token 自动管理                                    │  │
│  │  - 密码重置、邮箱验证（可选）                              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase PostgreSQL                                    │  │
│  │  - Row Level Security (RLS)                             │  │
│  │  - 用户扩展信息表                                       │  │
│  │  - 报告表、订单表、下载记录表                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        存储层                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase Storage（可选）                                │  │
│  │  - 报告文件存储                                          │  │
│  │  - CDN 加速                                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        支付层                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  模拟支付（第一阶段）                                    │  │
│  │  - 纯前端实现                                            │  │
│  │  - 立即成功，点数到账                                    │  │
│  │  - 后续可升级为真实支付                                    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 架构优势

1. **🔐 企业级安全** - Supabase 提供银行级安全认证，数据加密传输
2. **⚡ 高性能** - 全球 CDN 加速，平均响应时间 < 100ms
3. **💰 低成本** - 免费套餐支持 10 万月活用户
4. **📱 易于扩展** - 支持微信登录、真实支付等未来功能
5. **🧪 易于维护** - 统一的 Supabase 生态系统，减少技术债务

### 2.3 文件结构

```
/workspace/
├── index.html                    # 首页（现有）
├── majors.html                   # 专业列表页（现有）
├── login.html                    # 登录页
├── register.html                 # 注册页
├── user/
│   ├── dashboard.html            # 个人中心
│   ├── reports.html              # 报告浏览页
│   ├── orders.html               # 订单/下载历史
│   └── purchase.html             # 购买点数页
├── admin/
│   ├── index.html                # 管理后台首页
│   ├── users.html                # 用户管理
│   └── reports.html              # 报告管理
├── css/
│   ├── style.css                 # 全局样式
│   └── admin.css                 # 后台样式
├── js/
│   ├── app.js                    # 应用入口
│   ├── auth.js                   # 认证模块
│   ├── reports.js                # 报告模块
│   └── payments.js               # 支付模块
├── docs/
│   └── design.md                 # 设计文档（本文件）
└── package.json                  # 项目配置
```

---

## 3. 数据库设计

### 3.1 数据库表结构

#### 3.1.1 user_profiles（用户扩展信息表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY, REFERENCES auth.users(id) | 用户ID（关联Supabase Auth） |
| phone | VARCHAR(20) | UNIQUE | 手机号 |
| points_balance | INTEGER | DEFAULT 0, CHECK >= 0 | 点数余额 |
| role | VARCHAR(20) | DEFAULT 'user', CHECK IN ('user', 'admin') | 用户角色 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    phone VARCHAR(20) UNIQUE,
    points_balance INTEGER DEFAULT 0 CHECK (points_balance >= 0),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用 Row Level Security
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- 用户只能查看自己的信息
CREATE POLICY "用户只能查看自己的信息"
ON user_profiles FOR SELECT
USING (auth.uid() = id);

-- 用户可以更新自己的信息
CREATE POLICY "用户可以更新自己的信息"
ON user_profiles FOR UPDATE
USING (auth.uid() = id);

-- 管理员可以查看所有用户信息
CREATE POLICY "管理员可以查看所有用户"
ON user_profiles FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- 管理员可以更新所有用户信息
CREATE POLICY "管理员可以更新所有用户"
ON user_profiles FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- 触发器：自动更新 updated_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_profiles_modtime
BEFORE UPDATE ON user_profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();
```

---

#### 3.1.2 reports（报告表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | 报告ID |
| major_code | VARCHAR(10) | NOT NULL, UNIQUE | 专业代码 |
| major_name | VARCHAR(100) | NOT NULL | 专业名称 |
| category | VARCHAR(50) | NOT NULL | 学科门类 |
| preview_content | TEXT | NULL | 免费预览内容（前20%） |
| full_content | TEXT | NULL | 完整报告内容 |
| status | VARCHAR(20) | DEFAULT 'draft', CHECK IN ('draft', 'published', 'archived') | 报告状态 |
| download_count | INTEGER | DEFAULT 0 | 下载次数 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

```sql
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    major_code VARCHAR(10) NOT NULL UNIQUE,
    major_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    preview_content TEXT,
    full_content TEXT,
    status VARCHAR(20) DEFAULT 'draft' 
        CHECK (status IN ('draft', 'published', 'archived')),
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用 RLS
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

-- 所有登录用户可以查看已发布的报告列表
CREATE POLICY "登录用户可查看已发布报告"
ON reports FOR SELECT
USING (
    auth.role() = 'authenticated' AND status = 'published'
);

-- 管理员可以管理所有报告
CREATE POLICY "管理员可管理报告"
ON reports FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- 触发器：自动更新 updated_at
CREATE TRIGGER update_reports_modtime
BEFORE UPDATE ON reports
FOR EACH ROW EXECUTE FUNCTION update_modified_column();
```

---

#### 3.1.3 point_packages（点数套餐表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | SERIAL | PRIMARY KEY | 套餐ID |
| name | VARCHAR(50) | NOT NULL | 套餐名称 |
| description | TEXT | NULL | 套餐描述 |
| points | INTEGER | NOT NULL, CHECK > 0 | 点数数量 |
| price | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | 价格（元） |
| is_active | BOOLEAN | DEFAULT true | 是否上架 |
| sort_order | INTEGER | DEFAULT 0 | 排序顺序 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

```sql
CREATE TABLE point_packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    points INTEGER NOT NULL CHECK (points > 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    is_active BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用 RLS
ALTER TABLE point_packages ENABLE ROW LEVEL SECURITY;

-- 公开查看所有上架的套餐
CREATE POLICY "公开查看套餐"
ON point_packages FOR SELECT
USING (is_active = true);

-- 仅管理员可管理套餐
CREATE POLICY "管理员管理套餐"
ON point_packages FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- 触发器：自动更新 updated_at
CREATE TRIGGER update_packages_modtime
BEFORE UPDATE ON point_packages
FOR EACH ROW EXECUTE FUNCTION update_modified_column();
```

**默认套餐配置：**

| id | name | description | points | price | sort_order |
|----|------|-------------|--------|-------|------------|
| 1 | 体验套餐 | 尝试下载1份报告 | 1 | 1.00 | 1 |
| 2 | 基础套餐 | 适合普通需求 | 10 | 9.90 | 2 |
| 3 | 推荐套餐 | 性价比最高，购买最多 | 20 | 18.90 | 3 |
| 4 | 畅享套餐 | 满足深度调研需求 | 50 | 39.90 | 4 |
| 5 | 尊享套餐 | 专业调研，长期使用 | 100 | 69.90 | 5 |

---

#### 3.1.4 orders（订单表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | 订单ID |
| user_id | UUID | NOT NULL, REFERENCES user_profiles(id) | 用户ID |
| package_id | INTEGER | NOT NULL, REFERENCES point_packages(id) | 套餐ID |
| amount | DECIMAL(10,2) | NOT NULL | 订单金额 |
| points | INTEGER | NOT NULL | 获得点数 |
| status | VARCHAR(20) | DEFAULT 'pending', CHECK IN ('pending', 'paid', 'cancelled', 'refunded') | 订单状态 |
| payment_method | VARCHAR(20) | DEFAULT 'mock' | 支付方式 |
| paid_at | TIMESTAMPTZ | NULL | 支付时间 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| expires_at | TIMESTAMPTZ | NULL | 过期时间 |

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user_profiles(id),
    package_id INTEGER NOT NULL REFERENCES point_packages(id),
    amount DECIMAL(10, 2) NOT NULL,
    points INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' 
        CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded')),
    payment_method VARCHAR(20) DEFAULT 'mock',
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- 启用 RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 用户只能查看自己的订单
CREATE POLICY "用户只能查看自己的订单"
ON orders FOR SELECT
USING (auth.uid() = user_id);

-- 用户只能创建自己的订单
CREATE POLICY "用户只能创建订单"
ON orders FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- 用户可以更新自己的订单（取消等）
CREATE POLICY "用户可以更新自己的订单"
ON orders FOR UPDATE
USING (auth.uid() = user_id);

-- 管理员可以查看所有订单
CREATE POLICY "管理员查看所有订单"
ON orders FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);
```

---

#### 3.1.5 download_records（下载记录表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | 记录ID |
| user_id | UUID | NOT NULL, REFERENCES user_profiles(id) | 用户ID |
| report_id | UUID | NOT NULL, REFERENCES reports(id) | 报告ID |
| points_spent | INTEGER | NOT NULL, DEFAULT 1 | 消耗点数 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |

```sql
CREATE TABLE download_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user_profiles(id),
    report_id UUID NOT NULL REFERENCES reports(id),
    points_spent INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用 RLS
ALTER TABLE download_records ENABLE ROW LEVEL SECURITY;

-- 用户只能查看自己的下载记录
CREATE POLICY "用户只能查看自己的下载记录"
ON download_records FOR SELECT
USING (auth.uid() = user_id);

-- 用户可以插入自己的下载记录
CREATE POLICY "用户可以插入自己的下载记录"
ON download_records FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- 管理员可以查看所有下载记录
CREATE POLICY "管理员查看所有下载记录"
ON download_records FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);
```

---

### 3.2 Supabase 配置 checklist

- [ ] 创建新的 Supabase 项目
- [ ] 配置数据库表结构（5张表）
- [ ] 配置 Row Level Security 策略
- [ ] 创建触发器和函数
- [ ] 配置 Auth 提供商（手机号、微信）
- [ ] 配置项目 API Keys
- [ ] 初始化默认套餐数据
- [ ] 创建初始管理员账户
- [ ] 配置项目 URL 和域名
- [ ] 设置 CORS 和安全策略

---

## 4. 页面设计

### 4.1 设计规范

#### 4.1.1 视觉规范

**与现有网站保持一致：**

| 设计元素 | 值 |
|----------|-----|
| 主色调 | `#E67E22`（橙色） |
| 辅助色 | `#705A49`（棕色） |
| 背景色 | `#FFF8F5`（暖白色） |
| 卡片背景 | `#FFFFFF` |
| 文字颜色 | `#2C2621` |
| 次要文字 | `#8B7E74` |
| 圆角 | `16px`（大）、`12px`（中）、`8px`（小） |
| 阴影 | `0 4px 24px rgba(112, 90, 73, 0.05)` |

#### 4.1.2 响应式断点

| 断点 | 设备类型 |
|------|----------|
| < 768px | 手机 |
| 768px - 1024px | 平板 |
| > 1024px | 桌面 |

---

### 4.2 用户端页面

#### 4.2.1 登录页（`/login.html`）

**功能：**
- 手机号 + 密码登录
- 微信扫码登录
- 忘记密码（可选）
- 跳转注册页

**页面布局：**
```
┌─────────────────────────────────────┐
│  [Logo] 专业星图                     │
│                                     │
│  ┌───────────────────────────────┐  │
│  │                               │  │
│  │  [手机号输入框]                │  │
│  │                               │  │
│  │  [密码输入框]                  │  │
│  │                               │  │
│  │  [登录按钮]                    │  │
│  │                               │  │
│  │  ──────────────────────       │  │
│  │                               │  │
│  │  [微信登录按钮]                │  │
│  │                               │  │
│  │  还没有账号？[立即注册]        │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

#### 4.2.2 注册页（`/register.html`）

**功能：**
- 手机号输入
- 验证码发送/验证
- 密码设置
- 确认密码
- 用户协议勾选

**页面布局：**
```
┌─────────────────────────────────────┐
│  [Logo] 专业星图                     │
│                                     │
│  ┌───────────────────────────────┐  │
│  │                               │  │
│  │  [手机号输入框]                │  │
│  │                               │  │
│  │  [验证码输入框] [获取验证码]    │  │
│  │                               │  │
│  │  [密码输入框]                  │  │
│  │                               │  │
│  │  [确认密码输入框]              │  │
│  │                               │  │
│  │  [√] 我已阅读并同意[用户协议]  │  │
│  │                               │  │
│  │  [注册按钮]                    │  │
│  │                               │  │
│  │  已有账号？[立即登录]          │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

#### 4.2.3 个人中心（`/user/dashboard.html`）

**功能：**
- 显示用户信息（头像、昵称）
- 显示点数余额（大数字展示）
- 快捷入口按钮
  - 浏览报告
  - 购买点数
  - 我的订单
  - 退出登录

**页面布局：**
```
┌─────────────────────────────────────────┐
│  导航栏：[Logo] [个人中心] [退出]        │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  [头像]  用户昵称                  │  │
│  │                                   │  │
│  │  点数余额：                       │  │
│  │  ┌─────────────────────────────┐ │  │
│  │  │                             │ │  │
│  │  │        128                  │ │  │
│  │  │      (当前点数)             │ │  │
│  │  │                             │ │  │
│  │  └─────────────────────────────┘ │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  快捷操作                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  浏览   │  │  购买   │  │  订单   │ │
│  │  报告   │  │  点数   │  │  历史   │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

---

#### 4.2.4 报告浏览页（`/user/reports.html`）

**功能：**
- 报告列表展示
- 搜索/筛选（按学科、关键词）
- 点击报告查看详情/预览
- 已下载的报告标识

**页面布局：**
```
┌─────────────────────────────────────────┐
│  导航栏：[Logo] [个人中心] [退出]        │
├─────────────────────────────────────────┤
│                                         │
│  [搜索框]  [学科筛选]                    │
│                                         │
│  报告列表                               │
│  ┌───────────────────────────────────┐ │
│  │ [已下载] 计算机科学与技术          │ │
│  │      工学门类 · 下载 1283次        │ │
│  │  [查看详情]                        │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ 临床医学                          │ │
│  │      医学门类 · 下载 892次         │ │
│  │  [查看详情]                        │ │
│  └───────────────────────────────────┘ │
│  ...                                   │
│                                         │
└─────────────────────────────────────────┘
```

**报告详情弹窗：**
```
┌─────────────────────────────────────────┐
│  [关闭]  计算机科学与技术               │
├─────────────────────────────────────────┤
│                                         │
│  预览内容（免费，前20%）                 │
│  ┌───────────────────────────────────┐ │
│  │  专业基本信息...                  │ │
│  │  雪峰点评（部分）...               │ │
│  │  ...                              │ │
│  └───────────────────────────────────┘ │
│  ─────────────────────────────────────  │
│  🔒 剩余内容需要点数解锁                │
│                                         │
│  您的点数：128                          │
│  [消耗 1 点下载完整报告]                │
│                                         │
└─────────────────────────────────────────┘
```

---

#### 4.2.5 订单/下载历史（`/user/orders.html`）

**功能：**
- 订单记录（购买点数）
- 下载记录（消耗点数）
- 分页展示

**页面布局：**
```
┌─────────────────────────────────────────┐
│  导航栏：[Logo] [个人中心] [退出]        │
├─────────────────────────────────────────┤
│                                         │
│  [订单记录] [下载记录]  (标签切换)      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 2026-05-20  购买推荐套餐          │ │
│  │        +20点 · ¥18.90 · 已支付    │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │ 2026-05-19  下载计算机科学报告     │ │
│  │        -1点 · 已完成               │ │
│  └───────────────────────────────────┘ │
│  ...                                   │
│                                         │
└─────────────────────────────────────────┘
```

---

#### 4.2.6 购买点数页（`/user/purchase.html`）

**功能：**
- 显示点数套餐列表
- 套餐对比
- 点击选择套餐并购买
- 模拟支付流程

**页面布局：**
```
┌─────────────────────────────────────────┐
│  导航栏：[Logo] [个人中心] [退出]        │
├─────────────────────────────────────────┤
│                                         │
│  当前点数：128                          │
│                                         │
│  选择套餐                               │
│  ┌───────────────────────────────────┐ │
│  │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │ │
│  │ │  1  │ │ 10  │ │ 20  │ │ 50  │ │ │
│  │ │ 点  │ │ 点  │ │ 点  │ │ 点  │ │ │
│  │ │ ¥1  │ │¥9.9 │ │¥18.9│ │¥39.9│ │ │
│  │ └─────┘ └─────┘ └─────┘ └─────┘ │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

**模拟支付弹窗：**
```
┌─────────────────────────────────────────┐
│  [关闭]  确认购买                       │
├─────────────────────────────────────────┤
│                                         │
│  套餐：推荐套餐                          │
│  点数：+20                              │
│  金额：¥18.90                           │
│                                         │
│  ⚠️ 重要提示：虚拟商品，一旦交付无法退货退款│
│                                         │
│  [确认支付（模拟）]                      │
│                                         │
└─────────────────────────────────────────┘
```

---

### 4.3 管理端页面

#### 4.3.1 管理后台首页（`/admin/index.html`）

**功能：**
- 数据概览卡片
  - 总用户数
  - 今日新增用户
  - 总订单数
  - 今日订单数
  - 总下载数
  - 今日下载数
- 热门报告TOP5
- 最近订单列表

---

#### 4.3.2 用户管理（`/admin/users.html`）

**功能：**
- 用户列表（分页）
- 搜索/筛选
- 查看用户详情
- 调整用户点数
- 变更用户角色

---

#### 4.3.3 报告管理（`/admin/reports.html`）

**功能：**
- 报告列表
- 搜索/筛选（按学科、状态）
- 查看/编辑报告内容
- 上传/更新报告
- 修改报告状态

---

## 5. API 设计

### 5.1 认证 API（Supabase Auth 内置）

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| POST | `/auth/v1/token?grant_type=password` | 手机号+密码登录 | 公开 |
| POST | `/auth/v1/signup` | 用户注册 | 公开 |
| POST | `/auth/v1/token?grant_type=refresh_token` | 刷新Token | 认证用户 |
| POST | `/auth/v1/logout` | 登出 | 认证用户 |
| GET | `/auth/v1/user` | 获取当前用户 | 认证用户 |
| POST | `/auth/v1/signin?provider=wechat` | 微信登录 | 公开 |

**JavaScript 示例：**

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)

// 手机号+密码登录
const { data, error } = await supabase.auth.signInWithPassword({
  phone: '+8613800138000',
  password: 'password123'
})

// 用户注册
const { data, error } = await supabase.auth.signUp({
  phone: '+8613800138000',
  password: 'password123'
})

// 微信登录
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'wechat'
})

// 登出
await supabase.auth.signOut()

// 获取当前用户
const { data: { user } } = await supabase.auth.getUser()
```

---

### 5.2 业务 API（基于 Supabase JS SDK）

#### 5.2.1 用户相关

**获取用户扩展信息：**
```javascript
async function getUserProfile() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return null

  const { data, error } = await supabase
    .from('user_profiles')
    .select('*')
    .eq('id', user.id)
    .single()

  if (error) throw error
  return data
}
```

**更新用户信息：**
```javascript
async function updateUserProfile(updates) {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('未登录')

  const { data, error } = await supabase
    .from('user_profiles')
    .update(updates)
    .eq('id', user.id)
    .select()
    .single()

  if (error) throw error
  return data
}
```

**管理员：调整用户点数：**
```javascript
async function adjustUserPoints(userId, pointsDelta) {
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('points_balance')
    .eq('id', userId)
    .single()

  const { data, error } = await supabase
    .from('user_profiles')
    .update({
      points_balance: profile.points_balance + pointsDelta
    })
    .eq('id', userId)

  if (error) throw error
  return data
}
```

---

#### 5.2.2 报告相关

**获取报告列表：**
```javascript
async function getReports(filters = {}) {
  let query = supabase
    .from('reports')
    .select('*')
    .eq('status', 'published')

  if (filters.category) {
    query = query.eq('category', filters.category)
  }

  if (filters.search) {
    query = query.or(`major_name.ilike.%${filters.search}%,major_code.ilike.%${filters.search}%`)
  }

  const { data, error } = await query.order('download_count', { ascending: false })

  if (error) throw error
  return data
}
```

**获取报告详情：**
```javascript
async function getReport(reportId) {
  const { data, error } = await supabase
    .from('reports')
    .select('*')
    .eq('id', reportId)
    .single()

  if (error) throw error
  return data
}
```

**下载报告（扣点）：**
```javascript
async function downloadReport(reportId) {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('未登录')

  // 1. 获取报告信息
  const { data: report } = await supabase
    .from('reports')
    .select('*')
    .eq('id', reportId)
    .single()

  if (!report) throw new Error('报告不存在')

  // 2. 获取用户点数
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('points_balance')
    .eq('id', user.id)
    .single()

  if (profile.points_balance < 1) {
    throw new Error('点数不足，请先购买')
  }

  // 3. 扣减点数
  await supabase
    .from('user_profiles')
    .update({ points_balance: profile.points_balance - 1 })
    .eq('id', user.id)

  // 4. 记录下载
  await supabase
    .from('download_records')
    .insert({
      user_id: user.id,
      report_id: reportId,
      points_spent: 1
    })

  // 5. 更新报告下载次数
  await supabase
    .from('reports')
    .update({ download_count: report.download_count + 1 })
    .eq('id', reportId)

  return report.full_content
}
```

**管理员：创建/更新报告：**
```javascript
async function createReport(reportData) {
  const { data, error } = await supabase
    .from('reports')
    .insert(reportData)
    .select()
    .single()

  if (error) throw error
  return data
}

async function updateReport(reportId, updates) {
  const { data, error } = await supabase
    .from('reports')
    .update(updates)
    .eq('id', reportId)
    .select()
    .single()

  if (error) throw error
  return data
}
```

---

#### 5.2.3 套餐相关

**获取套餐列表：**
```javascript
async function getPackages() {
  const { data, error } = await supabase
    .from('point_packages')
    .select('*')
    .eq('is_active', true)
    .order('sort_order')

  if (error) throw error
  return data
}
```

---

#### 5.2.4 订单相关

**创建订单：**
```javascript
async function createOrder(packageId) {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('未登录')

  // 1. 获取套餐信息
  const { data: pkg } = await supabase
    .from('point_packages')
    .select('*')
    .eq('id', packageId)
    .single()

  if (!pkg) throw new Error('套餐不存在')

  // 2. 创建订单
  const expiresAt = new Date(Date.now() + 30 * 60 * 1000) // 30分钟后过期
  const { data: order, error } = await supabase
    .from('orders')
    .insert({
      user_id: user.id,
      package_id: packageId,
      amount: pkg.price,
      points: pkg.points,
      status: 'pending',
      expires_at: expiresAt.toISOString()
    })
    .select()
    .single()

  if (error) throw error
  return order
}
```

**模拟支付：**
```javascript
async function payOrder(orderId) {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('未登录')

  // 1. 获取订单信息
  const { data: order } = await supabase
    .from('orders')
    .select('*')
    .eq('id', orderId)
    .single()

  if (!order) throw new Error('订单不存在')
  if (order.status !== 'pending') throw new Error('订单状态不正确')
  if (new Date(order.expires_at) < new Date()) throw new Error('订单已过期')

  // 2. 模拟支付（立即成功）
  await supabase
    .from('orders')
    .update({
      status: 'paid',
      paid_at: new Date().toISOString()
    })
    .eq('id', orderId)

  // 3. 获取用户当前点数
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('points_balance')
    .eq('id', user.id)
    .single()

  // 4. 增加用户点数
  await supabase
    .from('user_profiles')
    .update({
      points_balance: profile.points_balance + order.points
    })
    .eq('id', user.id)

  return { success: true, points: order.points }
}
```

**获取订单列表：**
```javascript
async function getOrders() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('未登录')

  const { data, error } = await supabase
    .from('orders')
    .select('*, point_packages(*)')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false })

  if (error) throw error
  return data
}
```

---

#### 5.2.5 下载记录相关

**获取下载记录：**
```javascript
async function getDownloadRecords() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('未登录')

  const { data, error } = await supabase
    .from('download_records')
    .select('*, reports(*)')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false })

  if (error) throw error
  return data
}
```

---

## 6. 业务流程

### 6.1 用户注册/登录流程

```
开始
  ↓
选择登录方式
  ├─ 手机号登录
  │   ↓
  │ 输入手机号 + 密码
  │   ↓
  │ Supabase Auth 验证
  │   ↓
  │ 验证通过
  │   ↓
  │ 检查是否有 user_profiles 记录
  │   ├─ 有 → 获取记录
  │   └─ 无 → 自动创建（点数=0）
  │   ↓
  │ 跳转个人中心
  │
  └─ 微信登录
      ↓
  跳转微信授权页面
      ↓
  用户授权
      ↓
  回调获取微信 OpenID
      ↓
  关联/创建账户
      ↓
  检查是否有 user_profiles 记录
      ├─ 有 → 获取记录
      └─ 无 → 自动创建（点数=0）
      ↓
  跳转个人中心
```

---

### 6.2 报告浏览与下载流程

```
用户登录
  ↓
进入报告列表页
  ↓
浏览/搜索报告
  ↓
点击某个报告
  ↓
显示报告详情弹窗
  ↓
显示免费预览内容（前20%）
  ↓
用户决策：
  ├─ 继续预览 → 结束
  └─ 下载完整报告
       ↓
  检查点数是否 >= 1
       ├─ 否 → 提示"点数不足" → 跳转充值页
       └─ 是 → 扣减1点 → 返回完整报告
                  ↓
            记录下载历史
                  ↓
            增加报告下载计数
                  ↓
            显示完整报告内容
```

---

### 6.3 点数购买流程

```
用户登录
  ↓
进入购买点数页
  ↓
浏览套餐列表
  ↓
选择某个套餐
  ↓
创建待支付订单（30分钟有效期）
  ↓
跳转模拟支付页面
  ↓
显示订单信息：
  - 套餐名称
  - 获得点数
  - 金额
  - ⚠️ 重要提示：虚拟商品，一旦交付无法退货退款
  ↓
用户点击"确认支付"
  ↓
订单状态更新：pending → paid
  ↓
记录支付时间 paid_at
  ↓
自动增加用户点数
  ↓
显示"充值成功"提示
  ↓
返回个人中心或继续浏览
```

---

## 7. 安全设计

### 7.1 认证安全

| 措施 | 说明 |
|------|------|
| **密码存储** | Supabase Auth 使用 bcrypt 加密，不可逆 |
| **Token 机制** | JWT Token，有效期 7 天，自动刷新 |
| **HTTPS** | 所有传输加密 |
| **登录限制** | 建议限制失败次数（如5次/小时） |

### 7.2 数据安全

| 措施 | 说明 |
|------|------|
| **Row Level Security** | 用户只能访问自己的数据 |
| **输入验证** | 所有用户输入验证、防 SQL 注入 |
| **XSS 防护** | 输出内容转义 |
| **数据备份** | Supabase 自动备份 |

### 7.3 权限控制

| 资源 | user | admin |
|------|------|-------|
| 查看自己的 user_profiles | ✅ | ✅ |
| 查看所有 user_profiles | ❌ | ✅ |
| 查看已发布的 reports | ✅ | ✅ |
| 创建/编辑 reports | ❌ | ✅ |
| 创建自己的 orders | ✅ | ✅ |
| 查看所有 orders | ❌ | ✅ |

---

## 8. 实施计划

### 8.1 阶段划分

#### 阶段一：基础架构（3-4天）⭐

**目标：** 搭建项目基础框架

| 任务 | 描述 | 工期 |
|------|------|------|
| T1.1 | Supabase 项目配置 + 数据库表创建 | 0.5天 |
| T1.2 | RLS 策略配置 + 触发器创建 | 0.5天 |
| T1.3 | 基础页面模板（登录/注册/个人中心框架） | 1天 |
| T1.4 | Supabase Auth 集成（手机号登录） | 1天 |
| T1.5 | 单元测试 + 文档更新 | 0.5天 |

**交付物：**
- 可运行的 Supabase 项目
- 可登录的基础页面框架
- 数据库初始化脚本

---

#### 阶段二：核心功能（4-5天）⭐⭐

**目标：** 实现用户端核心功能

| 任务 | 描述 | 工期 |
|------|------|------|
| T2.1 | 用户注册/登录（手机号+微信） | 1.5天 |
| T2.2 | 个人中心（点数余额展示） | 0.5天 |
| T2.3 | 报告浏览/预览页面 | 1天 |
| T2.4 | 点数购买/模拟支付 | 1.5天 |
| T2.5 | 下载记录/订单历史页面 | 0.5天 |

**交付物：**
- 完整的用户端功能
- 可购买点数的模拟支付系统
- 报告浏览和下载功能

---

#### 阶段三：管理后台（2-3天）

**目标：** 实现管理端核心功能

| 任务 | 描述 | 工期 |
|------|------|------|
| T3.1 | 管理后台首页（数据概览） | 0.5天 |
| T3.2 | 用户管理（列表/调整点数） | 1天 |
| T3.3 | 报告管理（列表/上传） | 1天 |

**交付物：**
- 功能完善的管理后台
- 数据统计和可视化

---

#### 阶段四：测试与优化（2-3天）

**目标：** 确保系统稳定可用

| 任务 | 描述 | 工期 |
|------|------|------|
| T4.1 | 功能测试（用户端+管理端） | 1天 |
| T4.2 | 安全测试（RLS、权限验证） | 0.5天 |
| T4.3 | 性能优化（加载速度、响应） | 0.5天 |
| T4.4 | 用户体验优化（交互、提示） | 0.5天 |

**交付物：**
- 测试报告
- 优化后的最终版本

---

### 8.2 总工期

**总计：11-15个工作日**

**里程碑：**
- **Week 1-2**：完成阶段一 + 阶段二
- **Week 3**：完成阶段三 + 阶段四
- **Week 3末**：Beta测试 + 上线准备

---

## 9. 风险评估

### 9.1 风险列表

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| 微信登录配置复杂 | 中 | 高 | 预留手机号登录作为备选方案 |
| 611个报告生成耗时 | 高 | 中 | 分批生成，优先热门专业 |
| 用户不愿意付费 | 中 | 高 | 加强免费预览、优化转化漏斗 |
| Supabase 服务中断 | 低 | 高 | 定期备份，准备降级方案 |
| 点数计算并发问题 | 中 | 中 | 使用数据库事务、乐观锁 |
| 初期用户量不足 | 高 | 中 | 加强推广、优化运营活动 |

### 9.2 降级方案

如果 Supabase 服务暂时不可用，可以：
1. 显示维护提示
2. 允许用户继续浏览免费内容
3. 核心功能临时禁用

---

## 附录

### A. 相关链接

- [Supabase 官方文档](https://supabase.com/docs)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)
- [专业星图现有代码库](../index.html)

### B. 变更历史

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-05-20 | 初始版本 | 专业星图团队 |

---

**文档结束**
