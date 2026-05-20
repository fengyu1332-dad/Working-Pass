
# 专业星图

让人轻松了解专业选择背后的深层意义

## 项目概述

专业星图是一个帮助学生了解大学专业选择的平台，提供丰富的专业信息和深度分析报告。

## 项目结构

```
/workspace/
├── index.html                    # 首页
├── majors.html                   # 专业列表页
├── login.html                    # 登录页
├── register.html                 # 注册页
├── user/                         # 用户端页面
│   ├── dashboard.html            # 个人中心
│   ├── reports.html              # 报告浏览页
│   ├── orders.html               # 订单/下载历史
│   └── purchase.html             # 购买点数页
├── admin/                        # 管理端页面
│   ├── index.html                # 管理后台首页
│   ├── users.html                # 用户管理
│   └── reports.html              # 报告管理
├── css/                          # 样式文件
│   └── common.css                # 通用样式
├── js/                           # JavaScript 文件
│   └── supabase-client.js        # Supabase 客户端配置
├── docs/                         # 文档
│   └── design.md                 # 设计文档
├── supabase-init.sql             # 数据库初始化脚本
└── README.md                     # 项目说明
```

## 技术栈

- 前端：HTML5 + CSS3 + JavaScript (原生)
- 后端：Supabase (Auth + Database)
- 数据库：PostgreSQL
- 设计：响应式设计，移动优先

## 快速开始

### 1. 配置 Supabase

首先，你需要创建一个 Supabase 项目：

1. 访问 [supabase.com](https://supabase.com) 并创建账户
2. 创建新项目
3. 在项目设置中找到 API URL 和 anon key

### 2. 初始化数据库

在 Supabase 的 SQL Editor 中运行 `supabase-init.sql` 文件，这将创建所有必要的表、RLS 策略和触发器。

### 3. 配置客户端

编辑 `js/supabase-client.js` 文件，将 `YOUR_SUPABASE_URL` 和 `YOUR_SUPABASE_ANON_KEY` 替换为你自己的 Supabase 项目信息：

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';
```

### 4. 在 HTML 中引入

在你的 HTML 文件中引入必要的文件：

```html
&lt;link rel="stylesheet" href="css/common.css"&gt;
&lt;script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"&gt;&lt;/script&gt;
&lt;script src="js/supabase-client.js"&gt;&lt;/script&gt;
```

## 设计规范

### 颜色

- 主色调：#E67E22 (橙色)
- 辅助色：#705A49 (棕色)
- 背景色：#FFF8F5 (暖白色)
- 卡片背景：#FFFFFF
- 文字颜色：#2C2621

### 响应式断点

- 手机：&lt; 768px
- 平板：768px - 1024px
- 桌面：&gt; 1024px

## 主要功能

### 用户端

- 用户注册/登录（手机号 + 微信）
- 个人中心（查看点数余额）
- 浏览专业报告
- 免费预览报告内容
- 消耗点数下载完整报告
- 购买点数套餐
- 查看订单和下载历史

### 管理端

- 数据概览
- 用户管理
- 报告管理

## 数据库结构

### 主要表

- `user_profiles` - 用户扩展信息
- `reports` - 专业报告
- `point_packages` - 点数套餐
- `orders` - 订单记录
- `download_records` - 下载记录

详细的数据库结构和 RLS 策略请参考 `supabase-init.sql` 文件。

## 文档

- [设计文档](docs/design.md) - 详细的项目设计文档

## 开发

项目采用模块化设计，便于维护和扩展。所有页面都遵循相同的设计规范，确保用户体验的一致性。

## 许可证

本项目版权所有 © 2026 专业星图团队。
