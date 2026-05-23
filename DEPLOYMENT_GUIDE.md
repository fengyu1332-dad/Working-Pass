# 深度报告系统 - 部署指南

## 系统架构

本系统采用混合方案提供深度报告服务：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户浏览报告   │ -> │   点数验证      │ -> │   返回报告内容   │
│   (user/reports)│    │   (1点/报告)    │    │   + PDF签名URL   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                        ┌───────────────────────────────┘
                        ▼
              ┌─────────────────────┐
              │  Supabase Storage   │
              │  (PDF文件存储)       │
              │  签名URL(1小时有效)  │
              └─────────────────────┘
```

## 部署步骤

### 1. 创建Supabase Storage存储桶

1. 登录Supabase Dashboard
2. 进入项目 -> Storage
3. 创建新存储桶：`reports-pdf`
4. 设置为 Public（或者配置适当的RLS策略）

### 2. 上传PDF文件到Storage

运行上传脚本：

```bash
cd /workspace
npm install @supabase/supabase-js
node upload_reports_to_storage.js
```

### 3. 导入报告数据到数据库

运行导入脚本：

```bash
node import_reports_to_db.js
```

### 4. 配置数据库表结构

确保以下表存在并配置了适当的RLS策略：

- `user_profiles`: 用户信息表
- `reports`: 报告数据表
- `download_records`: 下载记录表

### 5. 配置RLS策略

在Supabase Dashboard中，为相关表配置RLS策略，确保：
- 用户只能查看自己的profile
- 用户只能下载自己已付费的报告
- 下载记录只能由用户自己创建

## 用户获取报告的完整流程

1. **用户浏览**: 访问 `/user/reports.html`
2. **登录检查**: 系统检查用户是否已登录
3. **查看预览**: 用户可以看到报告的免费预览
4. **解锁报告**: 点击"解锁完整报告"按钮
5. **点数扣费**: 系统验证用户点数余额 >= 1
6. **返回内容**: 返回报告文本内容 + PDF签名URL
7. **下载PDF**: 用户可点击"下载PDF版"获取PDF文件

## 文件说明

- `upload_reports_to_storage.js`: 上传PDF到Storage
- `import_reports_to_db.js`: 导入报告数据到数据库
- `js/reports.js`: 前端报告下载模块（已更新）
- `user/reports.html`: 报告浏览页面（已更新）
- `index.html`: 首页（已更新下载入口）
- `data/reports/`: 报告源文件目录

## 注意事项

1. Storage中的PDF文件使用签名URL，有效期为1小时
2. 报告文本内容存储在数据库的`reports`表中
3. 已下载过的报告再次查看不需要额外扣点
4. 签名URL过期后需要重新生成
