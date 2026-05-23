# 🚀 快速测试指南 - 3步搞定

## 📌 第一步：启动测试环境

### 方式一：使用自动脚本（推荐）
```bash
cd /workspace
./start-test.sh
# 然后选择 2 - 启动本地服务器
```

### 方式二：手动启动
```bash
cd /workspace
python3 -m http.server 8000
```

---

## 📌 第二步：打开测试工具

在浏览器中打开：

```
http://localhost:8000/test-tool.html
```

这个页面会帮你自动测试：
- ✅ Supabase连接
- ✅ 用户认证
- ✅ 报告系统
- ✅ 点数支付
- ✅ Storage存储

---

## 📌 第三步：进行完整功能测试

打开以下页面进行手动测试：

### 1️⃣ 用户注册
```
http://localhost:8000/register.html
```

### 2️⃣ 用户登录
```
http://localhost:8000/login.html
```

### 3️⃣ 购买点数
```
http://localhost:8000/user/purchase.html
```

### 4️⃣ 获取深度报告（最重要！）
```
http://localhost:8000/user/reports.html
```

---

## 📊 测试内容清单

### ✅ 用户注册管理
- [ ] 新用户注册功能
- [ ] 手机号验证
- [ ] 密码确认
- [ ] 注册成功后自动创建profile

### ✅ 用户购买点数管理
- [ ] 点数套餐列表显示
- [ ] 创建订单
- [ ] 模拟支付流程
- [ ] 点数自动增加
- [ ] 订单历史查询

### ✅ 用户获取深度报告
- [ ] 报告列表加载
- [ ] 免费预览查看
- [ ] 点数验证与扣减
- [ ] 完整报告内容显示
- [ ] PDF文件下载
- [ ] 已下载标识显示

---

## 🔧 如果遇到问题

### 问题：报告列表为空
```bash
cd /workspace
./start-test.sh
# 选择 3 - 导入报告数据
```

### 问题：PDF无法下载
```bash
cd /workspace
./start-test.sh
# 选择 4 - 上传PDF文件
```

### 问题：想先检查系统状态
```bash
cd /workspace
./start-test.sh
# 选择 1 - 运行系统验证
```

---

## 📚 相关文档

- 详细测试指南：[TEST_GUIDE.md](file:///workspace/TEST_GUIDE.md)
- 部署配置指南：[DEPLOYMENT_GUIDE.md](file:///workspace/DEPLOYMENT_GUIDE.md)
- 项目README：[README.md](file:///workspace/README.md)

---

## 🎯 快速命令汇总

| 命令 | 说明 |
|------|------|
| `./start-test.sh` | 启动测试菜单 |
| `node verify_system.js` | 运行系统验证 |
| `python3 -m http.server 8000` | 启动本地服务器 |
| `node import_reports_to_db.js` | 导入报告数据 |
| `node upload_reports_to_storage.js` | 上传PDF文件 |

---

## 💡 提示

1. **测试前确保**：在 [Supabase Dashboard](https://supabase.com) 中创建了 `reports-pdf` Storage桶
2. **建议使用**：Chrome或Firefox浏览器进行测试
3. **调试时**：按 F12 打开开发者工具查看控制台错误
4. **完整测试**：从注册开始，完整走一遍购买→获取报告流程

---

**准备好了吗？开始测试吧！** 🎉
