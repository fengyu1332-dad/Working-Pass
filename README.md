# 专业星图 🎓

> 温暖、专业的大学专业选择指南

## 项目介绍

专业星图是一个帮助高中生和家长了解大学专业的Web应用，提供：

- ✨ **611个专业**的详细介绍
- 📊 **深度分析报告**（15个热门专业）
- 💡 **张雪峰风格**的专业点评
- 🎯 **智能搜索**和分类浏览
- 📱 **响应式设计**，完美支持移动端

## 在线预览

🚀 **访问地址**（部署后更新）

## 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone <repository-url>
cd professional-starmap

# 2. 启动本地服务器
python3 -m http.server 3456

# 3. 浏览器访问
open http://localhost:3456
```

### Supabase配置

本项目使用Supabase作为后端服务：

1. 创建Supabase项目
2. 运行 `sql/supabase-init.sql` 初始化数据库
3. 更新 `js/supabase-client.js` 中的配置

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';
```

## 项目结构

```
professional-starmap/
├── index.html              # 首页
├── majors.html             # 专业列表页
├── login.html              # 登录页
├── register.html           # 注册页
├── test-tool.html          # 测试工具
│
├── user/                   # 用户中心
│   ├── dashboard.html      # 个人中心
│   ├── reports.html        # 深度报告
│   ├── orders.html         # 订单历史
│   └── purchase.html       # 点数购买
│
├── admin/                  # 管理后台
│   ├── index.html          # 管理首页
│   ├── users.html          # 用户管理
│   └── reports.html        # 报告管理
│
├── js/                     # JavaScript模块
│   ├── supabase-client.js  # Supabase客户端
│   ├── auth.js             # 认证模块
│   ├── payments.js         # 支付模块
│   └── reports.js          # 报告模块
│
├── css/                    # 样式文件
│   ├── common.css          # 通用样式
│   └── admin.css           # 管理后台样式
│
├── data/                   # 数据文件
│   └── reports/            # 深度报告
│       ├── index.html      # 报告索引
│       └── *.html/*.pdf    # 专业报告
│
├── docs/                   # 项目文档
│   ├── design.md           # 设计文档
│   ├── DEPLOYMENT_GUIDE.md # 部署指南
│   └── ...
│
├── scripts/                # 工具脚本
│   ├── archive/            # 归档脚本
│   └── ...
│
├── sql/                    # 数据库脚本
│   └── supabase-init.sql   # 初始化脚本
│
└── archive/                # 归档文件
```

## 技术栈

- **前端**: HTML5 + CSS3 + 原生JavaScript
- **后端**: Supabase (Auth + Database + Storage)
- **数据库**: PostgreSQL
- **设计**: 响应式设计，移动优先

## 核心功能

### 🏠 首页
- 精选专业推荐
- 专业搜索
- 统计数据展示

### 📚 专业列表
- 按学科分类浏览
- 搜索和筛选
- 专业详情弹窗

### 👤 用户系统
- 注册/登录
- 个人中心
- 点数管理
- 订单历史

### 📖 深度报告
- 15个热门专业的HTML报告
- PDF版本下载
- 完美的中文支持

## 部署指南

### GitHub Pages（推荐）

1. 将代码推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 配置自定义域名（可选）

详细部署步骤请参考 [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

## 项目进展

- ✅ 核心功能完成
- ✅ 611个专业数据导入
- ✅ 15个深度报告生成
- ✅ 项目清理完成
- 🔄 准备部署上线

**计划上线时间**: 2026年5月26日

详细进展请查看 [docs/项目进展分析与上线规划.md](docs/项目进展分析与上线规划.md)

## 开发团队

专业星图团队

## 许可证

© 2026 专业星图. All rights reserved.

---

**祝您好运！找到最适合的专业！** 🎉
