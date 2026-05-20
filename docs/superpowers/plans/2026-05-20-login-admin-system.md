# 专业星图登录与后台管理系统实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为专业星图网站实现完整的用户登录系统和后台管理功能，支持用户购买点数下载深度分析报告。

**Architecture:** 采用纯前端 + Supabase BaaS 架构。前端使用原生 HTML/CSS/JavaScript，Supabase 提供用户认证、PostgreSQL 数据库和文件存储服务。所有页面与现有网站保持一致的视觉风格。

**Tech Stack:** HTML5, CSS3, JavaScript (ES6+), Supabase (Auth, Database, Storage)

---

## 文件结构

### 新建文件

```
/workspace/
├── login.html                    # 登录页面
├── register.html                 # 注册页面
├── user/
│   ├── dashboard.html            # 用户仪表板
│   ├── reports.html              # 报告浏览与下载
│   └── orders.html               # 我的订单
├── admin/
│   ├── index.html                # 管理后台首页
│   ├── users.html                # 用户管理
│   ├── reports.html              # 报告管理
│   ├── orders.html               # 订单管理
│   └── packages.html             # 套餐管理
├── js/
│   ├── supabase-config.js        # Supabase 配置
│   ├── auth.js                   # 认证模块
│   ├── api.js                    # API 封装
│   └── utils.js                  # 工具函数
└── css/
    └── auth.css                  # 认证相关样式
```

### 修改文件

```
/workspace/
└── index.html                    # 添加登录入口和点数显示
```

---

## Task 1: 基础配置和工具函数

**Files:**
- Create: `/workspace/js/supabase-config.js`
- Create: `/workspace/js/utils.js`

- [ ] **Step 1: 创建 Supabase 配置文件**

```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

window.supabaseClient = supabaseClient;
```

- [ ] **Step 2: 创建工具函数文件**

```javascript
const Utils = {
    formatPrice(price) {
        return '¥' + price.toFixed(2);
    },
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background: ${type === 'error' ? '#e53935' : type === 'success' ? '#43a047' : '#E67E22'};
            color: white;
            border-radius: 8px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    },
    
    validatePhone(phone) {
        return /^1[3-9]\d{9}$/.test(phone);
    },
    
    validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
    
    validatePassword(password) {
        return password.length >= 8 && /\d/.test(password) && /[a-zA-Z]/.test(password);
    },
    
    async checkAuth() {
        const { data: { user } } = await supabaseClient.auth.getUser();
        return user;
    },
    
    async requireAuth() {
        const user = await this.checkAuth();
        if (!user) {
            window.location.href = '/login.html';
            return null;
        }
        return user;
    },
    
    async requireAdmin() {
        const user = await this.requireAuth();
        if (!user) return null;
        
        const { data: profile } = await supabaseClient
            .from('users')
            .select('role')
            .eq('id', user.id)
            .single();
        
        if (!profile || profile.role !== 'admin') {
            Utils.showToast('无权访问管理后台', 'error');
            window.location.href = '/';
            return null;
        }
        return user;
    },
    
    getRedirectUrl() {
        const params = new URLSearchParams(window.location.search);
        return params.get('redirect') || '/';
    }
};

window.Utils = Utils;
```

- [ ] **Step 3: 提交基础配置**

```bash
git add js/supabase-config.js js/utils.js
git commit -m "feat: add supabase config and utility functions"
```

---

## Task 2: 认证模块

**Files:**
- Create: `/workspace/js/auth.js`

- [ ] **Step 1: 创建认证模块**

```javascript
const Auth = {
    async register(phone, password, email = null) {
        if (!Utils.validatePhone(phone)) {
            return { error: '请输入正确的手机号' };
        }
        
        if (!Utils.validatePassword(password)) {
            return { error: '密码至少8位，需包含数字和字母' };
        }
        
        if (email && !Utils.validateEmail(email)) {
            return { error: '请输入正确的邮箱地址' };
        }
        
        const { data, error } = await supabaseClient.auth.signUp({
            phone: phone,
            password: password,
            options: {
                data: {
                    phone: phone,
                    email: email || null
                }
            }
        });
        
        if (error) {
            return { error: error.message };
        }
        
        await supabaseClient.from('users').insert({
            id: data.user.id,
            phone: phone,
            email: email || null,
            role: 'user',
            points_balance: 0
        });
        
        return { data };
    },
    
    async loginWithPhone(phone, password) {
        if (!Utils.validatePhone(phone)) {
            return { error: '请输入正确的手机号' };
        }
        
        const { data, error } = await supabaseClient.auth.signInWithPassword({
            phone: phone,
            password: password
        });
        
        if (error) {
            return { error: error.message };
        }
        
        return { data };
    },
    
    async loginWithEmail(email, password) {
        if (!Utils.validateEmail(email)) {
            return { error: '请输入正确的邮箱地址' };
        }
        
        const { data, error } = await supabaseClient.auth.signInWithPassword({
            email: email,
            password: password
        });
        
        if (error) {
            return { error: error.message };
        }
        
        return { data };
    },
    
    async logout() {
        const { error } = await supabaseClient.auth.signOut();
        if (error) {
            return { error: error.message };
        }
        window.location.href = '/login.html';
        return { success: true };
    },
    
    async getCurrentUser() {
        const { data: { user } } = await supabaseClient.auth.getUser();
        if (!user) return null;
        
        const { data: profile } = await supabaseClient
            .from('users')
            .select('*')
            .eq('id', user.id)
            .single();
        
        return { ...user, ...profile };
    },
    
    async updateProfile(updates) {
        const user = await this.getCurrentUser();
        if (!user) return { error: '未登录' };
        
        const { data, error } = await supabaseClient
            .from('users')
            .update(updates)
            .eq('id', user.id);
        
        if (error) return { error: error.message };
        return { data };
    }
};

window.Auth = Auth;
```

- [ ] **Step 2: 提交认证模块**

```bash
git add js/auth.js
git commit -m "feat: add authentication module"
```

---

## Task 3: API 封装模块

**Files:**
- Create: `/workspace/js/api.js`

- [ ] **Step 1: 创建 API 封装模块**

```javascript
const API = {
    packages: {
        async list() {
            const { data, error } = await supabaseClient
                .from('point_packages')
                .select('*')
                .eq('status', 'active')
                .order('points', { ascending: true });
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async create(pkg) {
            const { data, error } = await supabaseClient
                .from('point_packages')
                .insert(pkg);
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async update(id, updates) {
            const { data, error } = await supabaseClient
                .from('point_packages')
                .update(updates)
                .eq('id', id);
            
            if (error) return { error: error.message };
            return { data };
        }
    },
    
    orders: {
        async list(userId = null, isAdmin = false) {
            let query = supabaseClient
                .from('orders')
                .select('*, point_packages(*)')
                .order('created_at', { ascending: false });
            
            if (!isAdmin && userId) {
                query = query.eq('user_id', userId);
            }
            
            const { data, error } = await query;
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async create(order) {
            const { data, error } = await supabaseClient
                .from('orders')
                .insert(order)
                .select()
                .single();
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async pay(orderId) {
            const { data: order } = await supabaseClient
                .from('orders')
                .select('*, users(*)')
                .eq('id', orderId)
                .single();
            
            if (!order) return { error: '订单不存在' };
            
            const { error: orderError } = await supabaseClient
                .from('orders')
                .update({ status: 'paid', paid_at: new Date().toISOString() })
                .eq('id', orderId);
            
            if (orderError) return { error: orderError.message };
            
            const newBalance = (order.users.points_balance || 0) + order.points;
            const { error: balanceError } = await supabaseClient
                .from('users')
                .update({ points_balance: newBalance })
                .eq('id', order.user_id);
            
            if (balanceError) return { error: balanceError.message };
            
            return { success: true };
        },
        
        async cancel(orderId) {
            const { error } = await supabaseClient
                .from('orders')
                .update({ status: 'cancelled' })
                .eq('id', orderId);
            
            if (error) return { error: error.message };
            return { success: true };
        }
    },
    
    reports: {
        async list(isAdmin = false) {
            let query = supabaseClient
                .from('reports')
                .select('*')
                .order('created_at', { ascending: false });
            
            if (!isAdmin) {
                query = query.eq('status', 'published');
            }
            
            const { data, error } = await query;
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async get(id) {
            const { data, error } = await supabaseClient
                .from('reports')
                .select('*')
                .eq('id', id)
                .single();
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async create(report) {
            const { data, error } = await supabaseClient
                .from('reports')
                .insert(report)
                .select()
                .single();
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async update(id, updates) {
            const { data, error } = await supabaseClient
                .from('reports')
                .update(updates)
                .eq('id', id);
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async delete(id) {
            const { error } = await supabaseClient
                .from('reports')
                .delete()
                .eq('id', id);
            
            if (error) return { error: error.message };
            return { success: true };
        }
    },
    
    downloads: {
        async list(userId) {
            const { data, error } = await supabaseClient
                .from('download_records')
                .select('*, reports(*)')
                .eq('user_id', userId)
                .order('created_at', { ascending: false });
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async create(userId, reportId) {
            const { data: user } = await supabaseClient
                .from('users')
                .select('points_balance')
                .eq('id', userId)
                .single();
            
            if (!user || user.points_balance < 1) {
                return { error: '点数不足，请先充值' };
            }
            
            const { error: balanceError } = await supabaseClient
                .from('users')
                .update({ points_balance: user.points_balance - 1 })
                .eq('id', userId);
            
            if (balanceError) return { error: balanceError.message };
            
            const { data, error: recordError } = await supabaseClient
                .from('download_records')
                .insert({ user_id: userId, report_id: reportId })
                .select()
                .single();
            
            if (recordError) return { error: recordError.message };
            
            await supabaseClient.rpc('increment_download_count', { report_id: reportId });
            
            return { data };
        }
    },
    
    users: {
        async list() {
            const { data, error } = await supabaseClient
                .from('users')
                .select('*')
                .order('created_at', { ascending: false });
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async get(id) {
            const { data, error } = await supabaseClient
                .from('users')
                .select('*')
                .eq('id', id)
                .single();
            
            if (error) return { error: error.message };
            return { data };
        },
        
        async updatePoints(userId, pointsDelta) {
            const { data: user } = await supabaseClient
                .from('users')
                .select('points_balance')
                .eq('id', userId)
                .single();
            
            if (!user) return { error: '用户不存在' };
            
            const newBalance = user.points_balance + pointsDelta;
            if (newBalance < 0) return { error: '点数不能为负' };
            
            const { error } = await supabaseClient
                .from('users')
                .update({ points_balance: newBalance })
                .eq('id', userId);
            
            if (error) return { error: error.message };
            return { success: true, newBalance };
        }
    }
};

window.API = API;
```

- [ ] **Step 2: 提交 API 模块**

```bash
git add js/api.js
git commit -m "feat: add API wrapper module"
```

---

## Task 4: 认证相关样式

**Files:**
- Create: `/workspace/css/auth.css`

- [ ] **Step 1: 创建认证样式文件**

```css
:root {
    --surface: #FFF8F5;
    --surface-container: #FFFFFF;
    --primary: #E67E22;
    --primary-hover: #D35400;
    --secondary: #705A49;
    --secondary-container: #EBE0D6;
    --on-surface: #2C2621;
    --on-surface-variant: #8B7E74;
    --outline: #DED0C6;
    --error: #e53935;
    --success: #43a047;
    --shadow: rgba(112, 90, 73, 0.05);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
    background: var(--surface);
    min-height: 100vh;
    color: var(--on-surface);
    line-height: 1.8;
}

.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.auth-card {
    background: var(--surface-container);
    border-radius: 24px;
    padding: 48px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 8px 48px var(--shadow);
}

.auth-logo {
    text-align: center;
    margin-bottom: 32px;
}

.auth-logo h1 {
    font-family: "Literata", serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--secondary);
    margin-bottom: 8px;
}

.auth-logo p {
    color: var(--on-surface-variant);
    font-size: 14px;
}

.auth-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
    border-bottom: 2px solid var(--outline);
    padding-bottom: 16px;
}

.auth-tab {
    flex: 1;
    padding: 12px;
    border: none;
    background: transparent;
    color: var(--on-surface-variant);
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    border-radius: 8px;
}

.auth-tab.active {
    color: var(--primary);
    background: var(--secondary-container);
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 14px;
    font-weight: 500;
    color: var(--secondary);
}

.form-group input {
    padding: 14px 16px;
    border: 2px solid var(--outline);
    border-radius: 12px;
    font-size: 16px;
    outline: none;
    transition: all 0.3s;
    background: #FFF1EA;
}

.form-group input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.1);
}

.form-group input.error {
    border-color: var(--error);
}

.form-error {
    color: var(--error);
    font-size: 12px;
}

.form-hint {
    color: var(--on-surface-variant);
    font-size: 12px;
}

.auth-button {
    padding: 16px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 20px rgba(230, 126, 34, 0.3);
}

.auth-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 30px rgba(230, 126, 34, 0.4);
}

.auth-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.auth-footer {
    text-align: center;
    margin-top: 24px;
    color: var(--on-surface-variant);
    font-size: 14px;
}

.auth-footer a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
}

.auth-footer a:hover {
    text-decoration: underline;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@media (max-width: 480px) {
    .auth-card {
        padding: 32px 24px;
    }
    
    .auth-logo h1 {
        font-size: 24px;
    }
}
```

- [ ] **Step 2: 提交样式文件**

```bash
git add css/auth.css
git commit -m "feat: add authentication styles"
```

---

## Task 5: 登录页面

**Files:**
- Create: `/workspace/login.html`

- [ ] **Step 1: 创建登录页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-logo">
                <h1>🌟 专业星图</h1>
                <p>温暖、专业的大学专业选择指南</p>
            </div>
            
            <div class="auth-tabs">
                <button class="auth-tab active" data-type="phone">📱 手机号登录</button>
                <button class="auth-tab" data-type="email">📧 邮箱登录</button>
            </div>
            
            <form class="auth-form" id="loginForm">
                <div class="form-group" id="phoneGroup">
                    <label for="phone">手机号</label>
                    <input type="tel" id="phone" name="phone" placeholder="请输入手机号" maxlength="11">
                    <span class="form-error" id="phoneError"></span>
                </div>
                
                <div class="form-group" id="emailGroup" style="display: none;">
                    <label for="email">邮箱</label>
                    <input type="email" id="email" name="email" placeholder="请输入邮箱地址">
                    <span class="form-error" id="emailError"></span>
                </div>
                
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" name="password" placeholder="请输入密码">
                    <span class="form-error" id="passwordError"></span>
                </div>
                
                <button type="submit" class="auth-button" id="submitBtn">登录</button>
            </form>
            
            <div class="auth-footer">
                还没有账号？<a href="/register.html">立即注册</a>
            </div>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        let loginType = 'phone';
        
        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                loginType = tab.dataset.type;
                
                document.getElementById('phoneGroup').style.display = loginType === 'phone' ? 'flex' : 'none';
                document.getElementById('emailGroup').style.display = loginType === 'email' ? 'flex' : 'none';
            });
        });
        
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = '登录中...';
            
            const password = document.getElementById('password').value;
            
            let result;
            if (loginType === 'phone') {
                const phone = document.getElementById('phone').value;
                result = await Auth.loginWithPhone(phone, password);
            } else {
                const email = document.getElementById('email').value;
                result = await Auth.loginWithEmail(email, password);
            }
            
            if (result.error) {
                Utils.showToast(result.error, 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = '登录';
                return;
            }
            
            Utils.showToast('登录成功', 'success');
            
            setTimeout(() => {
                const redirect = Utils.getRedirectUrl();
                window.location.href = redirect;
            }, 1000);
        });
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交登录页面**

```bash
git add login.html
git commit -m "feat: add login page"
```

---

## Task 6: 注册页面

**Files:**
- Create: `/workspace/register.html`

- [ ] **Step 1: 创建注册页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>注册 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-logo">
                <h1>🌟 专业星图</h1>
                <p>温暖、专业的大学专业选择指南</p>
            </div>
            
            <form class="auth-form" id="registerForm">
                <div class="form-group">
                    <label for="phone">手机号 *</label>
                    <input type="tel" id="phone" name="phone" placeholder="请输入手机号" maxlength="11" required>
                    <span class="form-error" id="phoneError"></span>
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱（选填）</label>
                    <input type="email" id="email" name="email" placeholder="可用于找回密码">
                    <span class="form-error" id="emailError"></span>
                </div>
                
                <div class="form-group">
                    <label for="password">密码 *</label>
                    <input type="password" id="password" name="password" placeholder="至少8位，包含数字和字母" required>
                    <span class="form-hint">密码至少8位，需包含数字和字母</span>
                    <span class="form-error" id="passwordError"></span>
                </div>
                
                <div class="form-group">
                    <label for="confirmPassword">确认密码 *</label>
                    <input type="password" id="confirmPassword" name="confirmPassword" placeholder="请再次输入密码" required>
                    <span class="form-error" id="confirmError"></span>
                </div>
                
                <button type="submit" class="auth-button" id="submitBtn">注册</button>
            </form>
            
            <div class="auth-footer">
                已有账号？<a href="/login.html">立即登录</a>
            </div>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script>
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const phone = document.getElementById('phone').value;
            const email = document.getElementById('email').value || null;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            document.querySelectorAll('.form-error').forEach(el => el.textContent = '');
            document.querySelectorAll('input').forEach(el => el.classList.remove('error'));
            
            let hasError = false;
            
            if (!Utils.validatePhone(phone)) {
                document.getElementById('phoneError').textContent = '请输入正确的手机号';
                document.getElementById('phone').classList.add('error');
                hasError = true;
            }
            
            if (email && !Utils.validateEmail(email)) {
                document.getElementById('emailError').textContent = '请输入正确的邮箱地址';
                document.getElementById('email').classList.add('error');
                hasError = true;
            }
            
            if (!Utils.validatePassword(password)) {
                document.getElementById('passwordError').textContent = '密码至少8位，需包含数字和字母';
                document.getElementById('password').classList.add('error');
                hasError = true;
            }
            
            if (password !== confirmPassword) {
                document.getElementById('confirmError').textContent = '两次密码输入不一致';
                document.getElementById('confirmPassword').classList.add('error');
                hasError = true;
            }
            
            if (hasError) return;
            
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = '注册中...';
            
            const result = await Auth.register(phone, password, email);
            
            if (result.error) {
                Utils.showToast(result.error, 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = '注册';
                return;
            }
            
            Utils.showToast('注册成功，请登录', 'success');
            
            setTimeout(() => {
                window.location.href = '/login.html';
            }, 1500);
        });
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交注册页面**

```bash
git add register.html
git commit -m "feat: add register page"
```

---

## Task 7: 用户仪表板页面

**Files:**
- Create: `/workspace/user/dashboard.html`

- [ ] **Step 1: 创建用户仪表板页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的仪表板 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .dashboard-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        
        .dashboard-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
        }
        
        .logout-btn {
            padding: 10px 20px;
            background: var(--secondary-container);
            border: none;
            border-radius: 8px;
            color: var(--secondary);
            cursor: pointer;
            font-size: 14px;
        }
        
        .points-card {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
            border-radius: 20px;
            padding: 32px;
            color: white;
            margin-bottom: 32px;
        }
        
        .points-card h2 {
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 8px;
        }
        
        .points-card .points-value {
            font-family: "Literata", serif;
            font-size: 48px;
            font-weight: 700;
        }
        
        .points-card .points-unit {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .action-card {
            background: var(--surface-container);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid var(--outline);
        }
        
        .action-card:hover {
            transform: translateY(-4px);
            border-color: var(--primary);
        }
        
        .action-card .icon {
            font-size: 32px;
            margin-bottom: 12px;
        }
        
        .action-card .title {
            font-weight: 600;
            color: var(--secondary);
        }
        
        .packages-section {
            background: var(--surface-container);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 32px;
        }
        
        .packages-section h2 {
            font-family: "Literata", serif;
            font-size: 20px;
            color: var(--secondary);
            margin-bottom: 24px;
        }
        
        .packages-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
        }
        
        .package-card {
            border: 2px solid var(--outline);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .package-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }
        
        .package-card .points {
            font-family: "Literata", serif;
            font-size: 28px;
            font-weight: 700;
            color: var(--primary);
        }
        
        .package-card .price {
            font-size: 18px;
            color: var(--secondary);
            margin-top: 8px;
        }
        
        .package-card .name {
            font-size: 12px;
            color: var(--on-surface-variant);
            margin-top: 4px;
        }
        
        .nav-links {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .nav-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            border-color: var(--primary);
        }
        
        .nav-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .payment-notice {
            background: #FFF3E0;
            border: 1px solid #FFCC80;
            border-radius: 12px;
            padding: 16px;
            margin-top: 16px;
            color: #E65100;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h1>🌟 我的仪表板</h1>
            <button class="logout-btn" onclick="Auth.logout()">退出登录</button>
        </div>
        
        <div class="nav-links">
            <a href="/user/dashboard.html" class="nav-link active">仪表板</a>
            <a href="/user/reports.html" class="nav-link">深度报告</a>
            <a href="/user/orders.html" class="nav-link">我的订单</a>
        </div>
        
        <div class="points-card">
            <h2>我的点数</h2>
            <div>
                <span class="points-value" id="pointsBalance">0</span>
                <span class="points-unit">点</span>
            </div>
        </div>
        
        <div class="quick-actions">
            <div class="action-card" onclick="window.location.href='/user/reports.html'">
                <div class="icon">📊</div>
                <div class="title">浏览深度报告</div>
            </div>
            <div class="action-card" onclick="window.location.href='/user/orders.html'">
                <div class="icon">📋</div>
                <div class="title">我的订单</div>
            </div>
            <div class="action-card" onclick="window.location.href='/'">
                <div class="icon">🏠</div>
                <div class="title">返回首页</div>
            </div>
        </div>
        
        <div class="packages-section">
            <h2>💎 充值点数</h2>
            <div class="packages-grid" id="packagesGrid"></div>
            <div class="payment-notice">
                ⚠️ <strong>重要提示：</strong>虚拟商品，一旦交付无法退货退款
            </div>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        async function init() {
            const user = await Utils.requireAuth();
            if (!user) return;
            
            const profile = await Auth.getCurrentUser();
            if (profile) {
                document.getElementById('pointsBalance').textContent = profile.points_balance || 0;
            }
            
            const { data: packages } = await API.packages.list();
            if (packages) {
                const grid = document.getElementById('packagesGrid');
                grid.innerHTML = packages.map(pkg => `
                    <div class="package-card" onclick="buyPackage('${pkg.id}', ${pkg.points}, ${pkg.price})">
                        <div class="points">${pkg.points}点</div>
                        <div class="price">¥${pkg.price.toFixed(2)}</div>
                        <div class="name">${pkg.name}</div>
                    </div>
                `).join('');
            }
        }
        
        async function buyPackage(packageId, points, price) {
            if (!confirm(`确认购买 ${points} 点，支付 ¥${price.toFixed(2)}？\n\n⚠️ 虚拟商品，一旦交付无法退货退款`)) {
                return;
            }
            
            const user = await Auth.getCurrentUser();
            if (!user) return;
            
            const { data: order, error } = await API.orders.create({
                user_id: user.id,
                package_id: packageId,
                amount: price,
                points: points,
                status: 'pending'
            });
            
            if (error) {
                Utils.showToast(error, 'error');
                return;
            }
            
            const { error: payError } = await API.orders.pay(order.id);
            if (payError) {
                Utils.showToast(payError, 'error');
                return;
            }
            
            Utils.showToast(`充值成功！获得 ${points} 点`, 'success');
            init();
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交用户仪表板页面**

```bash
git add user/dashboard.html
git commit -m "feat: add user dashboard page"
```

---

## Task 8: 用户报告浏览页面

**Files:**
- Create: `/workspace/user/reports.html`

- [ ] **Step 1: 创建用户报告浏览页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>深度分析报告 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .reports-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .reports-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        
        .reports-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
        }
        
        .points-display {
            background: var(--primary);
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .nav-links {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .nav-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            border-color: var(--primary);
        }
        
        .nav-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 24px;
        }
        
        .report-card {
            background: var(--surface-container);
            border-radius: 20px;
            padding: 28px;
            border: 2px solid var(--outline);
            transition: all 0.3s;
        }
        
        .report-card:hover {
            transform: translateY(-4px);
            border-color: var(--primary);
        }
        
        .report-card h3 {
            font-family: "Literata", serif;
            font-size: 20px;
            color: var(--secondary);
            margin-bottom: 12px;
        }
        
        .report-card .category {
            display: inline-block;
            background: var(--secondary-container);
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            color: var(--secondary);
            margin-bottom: 16px;
        }
        
        .report-card .downloads {
            color: var(--on-surface-variant);
            font-size: 14px;
            margin-bottom: 16px;
        }
        
        .download-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .download-btn:hover {
            transform: translateY(-2px);
        }
        
        .download-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .cost-info {
            text-align: center;
            color: var(--on-surface-variant);
            font-size: 12px;
            margin-top: 8px;
        }
    </style>
</head>
<body>
    <div class="reports-container">
        <div class="reports-header">
            <h1>📊 深度分析报告</h1>
            <div class="points-display">
                点数余额：<span id="pointsBalance">0</span> 点
            </div>
        </div>
        
        <div class="nav-links">
            <a href="/user/dashboard.html" class="nav-link">仪表板</a>
            <a href="/user/reports.html" class="nav-link active">深度报告</a>
            <a href="/user/orders.html" class="nav-link">我的订单</a>
        </div>
        
        <div class="reports-grid" id="reportsGrid"></div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        let currentUser = null;
        
        async function init() {
            currentUser = await Utils.requireAuth();
            if (!currentUser) return;
            
            const profile = await Auth.getCurrentUser();
            if (profile) {
                document.getElementById('pointsBalance').textContent = profile.points_balance || 0;
            }
            
            const { data: reports } = await API.reports.list(false);
            if (reports) {
                renderReports(reports);
            }
        }
        
        function renderReports(reports) {
            const grid = document.getElementById('reportsGrid');
            grid.innerHTML = reports.map(report => `
                <div class="report-card">
                    <h3>${report.major_name}</h3>
                    <div class="category">${report.category} | ${report.major_code}</div>
                    <div class="downloads">📥 已下载 ${report.download_count || 0} 次</div>
                    <button class="download-btn" onclick="downloadReport('${report.id}')">
                        下载深度分析报告
                    </button>
                    <div class="cost-info">消耗 1 点</div>
                </div>
            `).join('');
        }
        
        async function downloadReport(reportId) {
            const profile = await Auth.getCurrentUser();
            if (!profile) return;
            
            if (profile.points_balance < 1) {
                Utils.showToast('点数不足，请先充值', 'error');
                setTimeout(() => {
                    window.location.href = '/user/dashboard.html';
                }, 1500);
                return;
            }
            
            if (!confirm('确认下载此报告？将消耗 1 点')) {
                return;
            }
            
            const { error } = await API.downloads.create(profile.id, reportId);
            if (error) {
                Utils.showToast(error, 'error');
                return;
            }
            
            const { data: report } = await API.reports.get(reportId);
            if (report && report.content) {
                const blob = new Blob([report.content], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${report.major_name}_深度分析报告.html`;
                a.click();
                URL.revokeObjectURL(url);
            }
            
            Utils.showToast('下载成功！', 'success');
            init();
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交用户报告浏览页面**

```bash
git add user/reports.html
git commit -m "feat: add user reports page"
```

---

## Task 9: 用户订单页面

**Files:**
- Create: `/workspace/user/orders.html`

- [ ] **Step 1: 创建用户订单页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的订单 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .orders-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .orders-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
            margin-bottom: 32px;
        }
        
        .nav-links {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .nav-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            border-color: var(--primary);
        }
        
        .nav-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .section-title {
            font-family: "Literata", serif;
            font-size: 20px;
            color: var(--secondary);
            margin: 32px 0 16px;
        }
        
        .orders-table {
            width: 100%;
            background: var(--surface-container);
            border-radius: 16px;
            overflow: hidden;
        }
        
        .orders-table table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .orders-table th,
        .orders-table td {
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid var(--outline);
        }
        
        .orders-table th {
            background: var(--secondary-container);
            font-weight: 600;
            color: var(--secondary);
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-paid {
            background: #E8F5E9;
            color: #2E7D32;
        }
        
        .status-pending {
            background: #FFF3E0;
            color: #E65100;
        }
        
        .status-cancelled {
            background: #FFEBEE;
            color: #C62828;
        }
        
        .empty-state {
            text-align: center;
            padding: 48px;
            color: var(--on-surface-variant);
        }
    </style>
</head>
<body>
    <div class="orders-container">
        <div class="orders-header">
            <h1>📋 我的订单</h1>
        </div>
        
        <div class="nav-links">
            <a href="/user/dashboard.html" class="nav-link">仪表板</a>
            <a href="/user/reports.html" class="nav-link">深度报告</a>
            <a href="/user/orders.html" class="nav-link active">我的订单</a>
        </div>
        
        <h2 class="section-title">充值记录</h2>
        <div class="orders-table" id="ordersTable"></div>
        
        <h2 class="section-title">下载记录</h2>
        <div class="orders-table" id="downloadsTable"></div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        async function init() {
            const user = await Utils.requireAuth();
            if (!user) return;
            
            const profile = await Auth.getCurrentUser();
            if (!profile) return;
            
            const { data: orders } = await API.orders.list(profile.id, false);
            renderOrders(orders || []);
            
            const { data: downloads } = await API.downloads.list(profile.id);
            renderDownloads(downloads || []);
        }
        
        function renderOrders(orders) {
            const container = document.getElementById('ordersTable');
            
            if (orders.length === 0) {
                container.innerHTML = '<div class="empty-state">暂无充值记录</div>';
                return;
            }
            
            container.innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>订单时间</th>
                            <th>套餐</th>
                            <th>金额</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${orders.map(order => `
                            <tr>
                                <td>${Utils.formatDate(order.created_at)}</td>
                                <td>${order.points}点</td>
                                <td>¥${order.amount.toFixed(2)}</td>
                                <td>
                                    <span class="status-badge status-${order.status}">
                                        ${order.status === 'paid' ? '已支付' : order.status === 'pending' ? '待支付' : '已取消'}
                                    </span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }
        
        function renderDownloads(downloads) {
            const container = document.getElementById('downloadsTable');
            
            if (downloads.length === 0) {
                container.innerHTML = '<div class="empty-state">暂无下载记录</div>';
                return;
            }
            
            container.innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>下载时间</th>
                            <th>报告名称</th>
                            <th>消耗点数</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${downloads.map(dl => `
                            <tr>
                                <td>${Utils.formatDate(dl.created_at)}</td>
                                <td>${dl.reports?.major_name || '未知报告'}</td>
                                <td>1点</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交用户订单页面**

```bash
git add user/orders.html
git commit -m "feat: add user orders page"
```

---

## Task 10: 管理后台首页

**Files:**
- Create: `/workspace/admin/index.html`

- [ ] **Step 1: 创建管理后台首页**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>管理后台 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .admin-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .admin-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        
        .admin-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
        }
        
        .admin-nav {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        
        .admin-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .admin-link:hover {
            border-color: var(--primary);
        }
        
        .admin-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }
        
        .stat-card {
            background: var(--surface-container);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            border: 2px solid var(--outline);
        }
        
        .stat-card .value {
            font-family: "Literata", serif;
            font-size: 36px;
            font-weight: 700;
            color: var(--primary);
        }
        
        .stat-card .label {
            color: var(--on-surface-variant);
            font-size: 14px;
            margin-top: 8px;
        }
        
        .recent-section {
            background: var(--surface-container);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 32px;
        }
        
        .recent-section h2 {
            font-family: "Literata", serif;
            font-size: 20px;
            color: var(--secondary);
            margin-bottom: 24px;
        }
        
        .recent-list {
            list-style: none;
        }
        
        .recent-list li {
            padding: 16px 0;
            border-bottom: 1px solid var(--outline);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .recent-list li:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="admin-header">
            <h1>⚙️ 管理后台</h1>
            <button class="logout-btn" onclick="Auth.logout()">退出登录</button>
        </div>
        
        <div class="admin-nav">
            <a href="/admin/index.html" class="admin-link active">仪表板</a>
            <a href="/admin/users.html" class="admin-link">用户管理</a>
            <a href="/admin/reports.html" class="admin-link">报告管理</a>
            <a href="/admin/orders.html" class="admin-link">订单管理</a>
            <a href="/admin/packages.html" class="admin-link">套餐管理</a>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value" id="totalUsers">0</div>
                <div class="label">总用户数</div>
            </div>
            <div class="stat-card">
                <div class="value" id="totalOrders">0</div>
                <div class="label">总订单数</div>
            </div>
            <div class="stat-card">
                <div class="value" id="totalRevenue">¥0</div>
                <div class="label">总收入</div>
            </div>
            <div class="stat-card">
                <div class="value" id="totalReports">0</div>
                <div class="label">报告数量</div>
            </div>
        </div>
        
        <div class="recent-section">
            <h2>📋 最近订单</h2>
            <ul class="recent-list" id="recentOrders"></ul>
        </div>
        
        <div class="recent-section">
            <h2>🔥 热门报告</h2>
            <ul class="recent-list" id="hotReports"></ul>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        async function init() {
            const user = await Utils.requireAdmin();
            if (!user) return;
            
            const { data: users } = await API.users.list();
            document.getElementById('totalUsers').textContent = users ? users.length : 0;
            
            const { data: orders } = await API.orders.list(null, true);
            document.getElementById('totalOrders').textContent = orders ? orders.length : 0;
            
            if (orders) {
                const totalRevenue = orders
                    .filter(o => o.status === 'paid')
                    .reduce((sum, o) => sum + o.amount, 0);
                document.getElementById('totalRevenue').textContent = '¥' + totalRevenue.toFixed(2);
                
                const recentOrders = orders.slice(0, 5);
                document.getElementById('recentOrders').innerHTML = recentOrders.length > 0
                    ? recentOrders.map(o => `
                        <li>
                            <span>${o.points}点 - ¥${o.amount.toFixed(2)}</span>
                            <span style="color: var(--on-surface-variant)">${Utils.formatDate(o.created_at)}</span>
                        </li>
                    `).join('')
                    : '<li style="text-align: center; color: var(--on-surface-variant)">暂无订单</li>';
            }
            
            const { data: reports } = await API.reports.list(true);
            document.getElementById('totalReports').textContent = reports ? reports.length : 0;
            
            if (reports) {
                const hotReports = [...reports]
                    .sort((a, b) => (b.download_count || 0) - (a.download_count || 0))
                    .slice(0, 5);
                document.getElementById('hotReports').innerHTML = hotReports.length > 0
                    ? hotReports.map(r => `
                        <li>
                            <span>${r.major_name}</span>
                            <span style="color: var(--on-surface-variant)">📥 ${r.download_count || 0}</span>
                        </li>
                    `).join('')
                    : '<li style="text-align: center; color: var(--on-surface-variant)">暂无报告</li>';
            }
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交管理后台首页**

```bash
git add admin/index.html
git commit -m "feat: add admin dashboard page"
```

---

## Task 11: 管理后台用户管理页面

**Files:**
- Create: `/workspace/admin/users.html`

- [ ] **Step 1: 创建用户管理页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户管理 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .admin-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .admin-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
            margin-bottom: 32px;
        }
        
        .admin-nav {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        
        .admin-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .admin-link:hover {
            border-color: var(--primary);
        }
        
        .admin-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .users-table {
            width: 100%;
            background: var(--surface-container);
            border-radius: 16px;
            overflow: hidden;
        }
        
        .users-table table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .users-table th,
        .users-table td {
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid var(--outline);
        }
        
        .users-table th {
            background: var(--secondary-container);
            font-weight: 600;
            color: var(--secondary);
        }
        
        .role-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .role-admin {
            background: #E3F2FD;
            color: #1565C0;
        }
        
        .role-user {
            background: var(--secondary-container);
            color: var(--secondary);
        }
        
        .action-btn {
            padding: 8px 16px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            margin-right: 8px;
        }
        
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .modal.show {
            display: flex;
        }
        
        .modal-content {
            background: var(--surface-container);
            border-radius: 20px;
            padding: 32px;
            width: 100%;
            max-width: 400px;
        }
        
        .modal-content h2 {
            font-family: "Literata", serif;
            font-size: 20px;
            color: var(--secondary);
            margin-bottom: 24px;
        }
        
        .modal-content .form-group {
            margin-bottom: 20px;
        }
        
        .modal-content label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--secondary);
        }
        
        .modal-content input {
            width: 100%;
            padding: 12px;
            border: 2px solid var(--outline);
            border-radius: 8px;
            font-size: 16px;
        }
        
        .modal-buttons {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }
        
        .modal-buttons button {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
        }
        
        .btn-cancel {
            background: var(--secondary-container);
            border: none;
            color: var(--secondary);
        }
        
        .btn-save {
            background: var(--primary);
            border: none;
            color: white;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="admin-header">
            <h1>👥 用户管理</h1>
        </div>
        
        <div class="admin-nav">
            <a href="/admin/index.html" class="admin-link">仪表板</a>
            <a href="/admin/users.html" class="admin-link active">用户管理</a>
            <a href="/admin/reports.html" class="admin-link">报告管理</a>
            <a href="/admin/orders.html" class="admin-link">订单管理</a>
            <a href="/admin/packages.html" class="admin-link">套餐管理</a>
        </div>
        
        <div class="users-table">
            <table>
                <thead>
                    <tr>
                        <th>手机号</th>
                        <th>邮箱</th>
                        <th>角色</th>
                        <th>点数余额</th>
                        <th>注册时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="usersList"></tbody>
            </table>
        </div>
    </div>
    
    <div class="modal" id="pointsModal">
        <div class="modal-content">
            <h2>调整用户点数</h2>
            <p id="modalUserInfo"></p>
            <div class="form-group">
                <label>当前点数：<span id="currentPoints">0</span></label>
            </div>
            <div class="form-group">
                <label for="pointsDelta">调整数量（正数增加，负数减少）</label>
                <input type="number" id="pointsDelta" placeholder="输入调整数量">
            </div>
            <div class="modal-buttons">
                <button class="btn-cancel" onclick="closeModal()">取消</button>
                <button class="btn-save" onclick="savePoints()">保存</button>
            </div>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        let currentEditUserId = null;
        
        async function init() {
            const user = await Utils.requireAdmin();
            if (!user) return;
            
            const { data: users } = await API.users.list();
            renderUsers(users || []);
        }
        
        function renderUsers(users) {
            const tbody = document.getElementById('usersList');
            tbody.innerHTML = users.map(u => `
                <tr>
                    <td>${u.phone || '-'}</td>
                    <td>${u.email || '-'}</td>
                    <td>
                        <span class="role-badge role-${u.role}">${u.role === 'admin' ? '管理员' : '用户'}</span>
                    </td>
                    <td>${u.points_balance || 0}</td>
                    <td>${Utils.formatDate(u.created_at)}</td>
                    <td>
                        <button class="action-btn" onclick="openPointsModal('${u.id}', '${u.phone || u.email}', ${u.points_balance || 0})">
                            调整点数
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
        function openPointsModal(userId, userInfo, currentPoints) {
            currentEditUserId = userId;
            document.getElementById('modalUserInfo').textContent = `用户：${userInfo}`;
            document.getElementById('currentPoints').textContent = currentPoints;
            document.getElementById('pointsDelta').value = '';
            document.getElementById('pointsModal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('pointsModal').classList.remove('show');
            currentEditUserId = null;
        }
        
        async function savePoints() {
            const delta = parseInt(document.getElementById('pointsDelta').value);
            if (isNaN(delta)) {
                Utils.showToast('请输入有效数字', 'error');
                return;
            }
            
            const { error } = await API.users.updatePoints(currentEditUserId, delta);
            if (error) {
                Utils.showToast(error, 'error');
                return;
            }
            
            Utils.showToast('点数调整成功', 'success');
            closeModal();
            init();
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交用户管理页面**

```bash
git add admin/users.html
git commit -m "feat: add admin users management page"
```

---

## Task 12: 管理后台报告管理页面

**Files:**
- Create: `/workspace/admin/reports.html`

- [ ] **Step 1: 创建报告管理页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>报告管理 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .admin-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .admin-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        
        .admin-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
        }
        
        .admin-nav {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        
        .admin-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .admin-link:hover {
            border-color: var(--primary);
        }
        
        .admin-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .add-btn {
            padding: 12px 24px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 500;
        }
        
        .reports-table {
            width: 100%;
            background: var(--surface-container);
            border-radius: 16px;
            overflow: hidden;
        }
        
        .reports-table table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .reports-table th,
        .reports-table td {
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid var(--outline);
        }
        
        .reports-table th {
            background: var(--secondary-container);
            font-weight: 600;
            color: var(--secondary);
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-published {
            background: #E8F5E9;
            color: #2E7D32;
        }
        
        .status-draft {
            background: #FFF3E0;
            color: #E65100;
        }
        
        .action-btn {
            padding: 8px 16px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            margin-right: 8px;
        }
        
        .action-btn.delete {
            background: var(--error);
        }
        
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            overflow-y: auto;
            padding: 20px;
        }
        
        .modal.show {
            display: flex;
        }
        
        .modal-content {
            background: var(--surface-container);
            border-radius: 20px;
            padding: 32px;
            width: 100%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .modal-content h2 {
            font-family: "Literata", serif;
            font-size: 20px;
            color: var(--secondary);
            margin-bottom: 24px;
        }
        
        .modal-content .form-group {
            margin-bottom: 20px;
        }
        
        .modal-content label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--secondary);
        }
        
        .modal-content input,
        .modal-content textarea,
        .modal-content select {
            width: 100%;
            padding: 12px;
            border: 2px solid var(--outline);
            border-radius: 8px;
            font-size: 14px;
        }
        
        .modal-content textarea {
            min-height: 200px;
            resize: vertical;
        }
        
        .modal-buttons {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }
        
        .modal-buttons button {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
        }
        
        .btn-cancel {
            background: var(--secondary-container);
            border: none;
            color: var(--secondary);
        }
        
        .btn-save {
            background: var(--primary);
            border: none;
            color: white;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="admin-header">
            <h1>📊 报告管理</h1>
            <button class="add-btn" onclick="openAddModal()">+ 新增报告</button>
        </div>
        
        <div class="admin-nav">
            <a href="/admin/index.html" class="admin-link">仪表板</a>
            <a href="/admin/users.html" class="admin-link">用户管理</a>
            <a href="/admin/reports.html" class="admin-link active">报告管理</a>
            <a href="/admin/orders.html" class="admin-link">订单管理</a>
            <a href="/admin/packages.html" class="admin-link">套餐管理</a>
        </div>
        
        <div class="reports-table">
            <table>
                <thead>
                    <tr>
                        <th>专业名称</th>
                        <th>专业代码</th>
                        <th>学科门类</th>
                        <th>状态</th>
                        <th>下载次数</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="reportsList"></tbody>
            </table>
        </div>
    </div>
    
    <div class="modal" id="reportModal">
        <div class="modal-content">
            <h2 id="modalTitle">新增报告</h2>
            <div class="form-group">
                <label>专业代码</label>
                <input type="text" id="majorCode" placeholder="如：010101">
            </div>
            <div class="form-group">
                <label>专业名称</label>
                <input type="text" id="majorName" placeholder="如：哲学">
            </div>
            <div class="form-group">
                <label>学科门类</label>
                <input type="text" id="category" placeholder="如：01 哲学">
            </div>
            <div class="form-group">
                <label>报告内容</label>
                <textarea id="reportContent" placeholder="输入深度分析报告内容（支持HTML格式）"></textarea>
            </div>
            <div class="form-group">
                <label>状态</label>
                <select id="reportStatus">
                    <option value="draft">草稿</option>
                    <option value="published">已发布</option>
                </select>
            </div>
            <div class="modal-buttons">
                <button class="btn-cancel" onclick="closeModal()">取消</button>
                <button class="btn-save" onclick="saveReport()">保存</button>
            </div>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        let currentEditReportId = null;
        
        async function init() {
            const user = await Utils.requireAdmin();
            if (!user) return;
            
            const { data: reports } = await API.reports.list(true);
            renderReports(reports || []);
        }
        
        function renderReports(reports) {
            const tbody = document.getElementById('reportsList');
            tbody.innerHTML = reports.map(r => `
                <tr>
                    <td>${r.major_name}</td>
                    <td>${r.major_code}</td>
                    <td>${r.category}</td>
                    <td>
                        <span class="status-badge status-${r.status}">${r.status === 'published' ? '已发布' : '草稿'}</span>
                    </td>
                    <td>${r.download_count || 0}</td>
                    <td>
                        <button class="action-btn" onclick="openEditModal('${r.id}')">编辑</button>
                        <button class="action-btn delete" onclick="deleteReport('${r.id}')">删除</button>
                    </td>
                </tr>
            `).join('');
        }
        
        function openAddModal() {
            currentEditReportId = null;
            document.getElementById('modalTitle').textContent = '新增报告';
            document.getElementById('majorCode').value = '';
            document.getElementById('majorName').value = '';
            document.getElementById('category').value = '';
            document.getElementById('reportContent').value = '';
            document.getElementById('reportStatus').value = 'draft';
            document.getElementById('reportModal').classList.add('show');
        }
        
        async function openEditModal(reportId) {
            currentEditReportId = reportId;
            document.getElementById('modalTitle').textContent = '编辑报告';
            
            const { data: report } = await API.reports.get(reportId);
            if (report) {
                document.getElementById('majorCode').value = report.major_code;
                document.getElementById('majorName').value = report.major_name;
                document.getElementById('category').value = report.category;
                document.getElementById('reportContent').value = report.content || '';
                document.getElementById('reportStatus').value = report.status;
            }
            
            document.getElementById('reportModal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('reportModal').classList.remove('show');
            currentEditReportId = null;
        }
        
        async function saveReport() {
            const report = {
                major_code: document.getElementById('majorCode').value,
                major_name: document.getElementById('majorName').value,
                category: document.getElementById('category').value,
                content: document.getElementById('reportContent').value,
                status: document.getElementById('reportStatus').value
            };
            
            if (!report.major_code || !report.major_name || !report.category) {
                Utils.showToast('请填写完整信息', 'error');
                return;
            }
            
            let result;
            if (currentEditReportId) {
                result = await API.reports.update(currentEditReportId, report);
            } else {
                result = await API.reports.create(report);
            }
            
            if (result.error) {
                Utils.showToast(result.error, 'error');
                return;
            }
            
            Utils.showToast('保存成功', 'success');
            closeModal();
            init();
        }
        
        async function deleteReport(reportId) {
            if (!confirm('确认删除此报告？')) return;
            
            const { error } = await API.reports.delete(reportId);
            if (error) {
                Utils.showToast(error, 'error');
                return;
            }
            
            Utils.showToast('删除成功', 'success');
            init();
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交报告管理页面**

```bash
git add admin/reports.html
git commit -m "feat: add admin reports management page"
```

---

## Task 13: 管理后台订单管理页面

**Files:**
- Create: `/workspace/admin/orders.html`

- [ ] **Step 1: 创建订单管理页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>订单管理 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .admin-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .admin-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
            margin-bottom: 32px;
        }
        
        .admin-nav {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        
        .admin-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .admin-link:hover {
            border-color: var(--primary);
        }
        
        .admin-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .stats-row {
            display: flex;
            gap: 24px;
            margin-bottom: 32px;
        }
        
        .stat-item {
            background: var(--surface-container);
            padding: 20px 32px;
            border-radius: 16px;
            border: 2px solid var(--outline);
        }
        
        .stat-item .value {
            font-family: "Literata", serif;
            font-size: 24px;
            font-weight: 700;
            color: var(--primary);
        }
        
        .stat-item .label {
            color: var(--on-surface-variant);
            font-size: 14px;
        }
        
        .orders-table {
            width: 100%;
            background: var(--surface-container);
            border-radius: 16px;
            overflow: hidden;
        }
        
        .orders-table table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .orders-table th,
        .orders-table td {
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid var(--outline);
        }
        
        .orders-table th {
            background: var(--secondary-container);
            font-weight: 600;
            color: var(--secondary);
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-paid {
            background: #E8F5E9;
            color: #2E7D32;
        }
        
        .status-pending {
            background: #FFF3E0;
            color: #E65100;
        }
        
        .status-cancelled {
            background: #FFEBEE;
            color: #C62828;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="admin-header">
            <h1>📋 订单管理</h1>
        </div>
        
        <div class="admin-nav">
            <a href="/admin/index.html" class="admin-link">仪表板</a>
            <a href="/admin/users.html" class="admin-link">用户管理</a>
            <a href="/admin/reports.html" class="admin-link">报告管理</a>
            <a href="/admin/orders.html" class="admin-link active">订单管理</a>
            <a href="/admin/packages.html" class="admin-link">套餐管理</a>
        </div>
        
        <div class="stats-row">
            <div class="stat-item">
                <div class="value" id="totalOrders">0</div>
                <div class="label">总订单数</div>
            </div>
            <div class="stat-item">
                <div class="value" id="paidOrders">0</div>
                <div class="label">已支付</div>
            </div>
            <div class="stat-item">
                <div class="value" id="totalRevenue">¥0</div>
                <div class="label">总收入</div>
            </div>
        </div>
        
        <div class="orders-table">
            <table>
                <thead>
                    <tr>
                        <th>订单ID</th>
                        <th>用户ID</th>
                        <th>套餐</th>
                        <th>金额</th>
                        <th>状态</th>
                        <th>创建时间</th>
                        <th>支付时间</th>
                    </tr>
                </thead>
                <tbody id="ordersList"></tbody>
            </table>
        </div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        async function init() {
            const user = await Utils.requireAdmin();
            if (!user) return;
            
            const { data: orders } = await API.orders.list(null, true);
            
            if (orders) {
                document.getElementById('totalOrders').textContent = orders.length;
                
                const paidOrders = orders.filter(o => o.status === 'paid');
                document.getElementById('paidOrders').textContent = paidOrders.length;
                
                const totalRevenue = paidOrders.reduce((sum, o) => sum + o.amount, 0);
                document.getElementById('totalRevenue').textContent = '¥' + totalRevenue.toFixed(2);
                
                renderOrders(orders);
            }
        }
        
        function renderOrders(orders) {
            const tbody = document.getElementById('ordersList');
            tbody.innerHTML = orders.map(o => `
                <tr>
                    <td style="font-size: 12px; font-family: monospace;">${o.id.slice(0, 8)}...</td>
                    <td style="font-size: 12px; font-family: monospace;">${o.user_id.slice(0, 8)}...</td>
                    <td>${o.points}点</td>
                    <td>¥${o.amount.toFixed(2)}</td>
                    <td>
                        <span class="status-badge status-${o.status}">
                            ${o.status === 'paid' ? '已支付' : o.status === 'pending' ? '待支付' : '已取消'}
                        </span>
                    </td>
                    <td>${Utils.formatDate(o.created_at)}</td>
                    <td>${o.paid_at ? Utils.formatDate(o.paid_at) : '-'}</td>
                </tr>
            `).join('');
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交订单管理页面**

```bash
git add admin/orders.html
git commit -m "feat: add admin orders management page"
```

---

## Task 14: 管理后台套餐管理页面

**Files:**
- Create: `/workspace/admin/packages.html`

- [ ] **Step 1: 创建套餐管理页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>套餐管理 - 专业星图</title>
    <link href="https://fonts.googleapis.com/css2?family=Literata:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="/css/auth.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        .admin-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .admin-header h1 {
            font-family: "Literata", serif;
            font-size: 28px;
            color: var(--secondary);
            margin-bottom: 32px;
        }
        
        .admin-nav {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        
        .admin-link {
            padding: 12px 24px;
            background: var(--surface-container);
            border: 2px solid var(--outline);
            border-radius: 12px;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .admin-link:hover {
            border-color: var(--primary);
        }
        
        .admin-link.active {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        .packages-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
        }
        
        .package-card {
            background: var(--surface-container);
            border-radius: 20px;
            padding: 32px;
            text-align: center;
            border: 2px solid var(--outline);
            transition: all 0.3s;
        }
        
        .package-card.inactive {
            opacity: 0.6;
        }
        
        .package-card .points {
            font-family: "Literata", serif;
            font-size: 36px;
            font-weight: 700;
            color: var(--primary);
        }
        
        .package-card .price {
            font-size: 24px;
            color: var(--secondary);
            margin: 8px 0 16px;
        }
        
        .package-card .name {
            color: var(--on-surface-variant);
            font-size: 14px;
            margin-bottom: 16px;
        }
        
        .status-toggle {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 16px;
        }
        
        .toggle-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .toggle-btn.active {
            background: #E8F5E9;
            color: #2E7D32;
        }
        
        .toggle-btn.inactive {
            background: #FFEBEE;
            color: #C62828;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <div class="admin-header">
            <h1>💎 套餐管理</h1>
        </div>
        
        <div class="admin-nav">
            <a href="/admin/index.html" class="admin-link">仪表板</a>
            <a href="/admin/users.html" class="admin-link">用户管理</a>
            <a href="/admin/reports.html" class="admin-link">报告管理</a>
            <a href="/admin/orders.html" class="admin-link">订单管理</a>
            <a href="/admin/packages.html" class="admin-link active">套餐管理</a>
        </div>
        
        <div class="packages-grid" id="packagesGrid"></div>
    </div>
    
    <script src="/js/supabase-config.js"></script>
    <script src="/js/utils.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/api.js"></script>
    <script>
        async function init() {
            const user = await Utils.requireAdmin();
            if (!user) return;
            
            const { data: packages } = await supabaseClient
                .from('point_packages')
                .select('*')
                .order('points', { ascending: true });
            
            renderPackages(packages || []);
        }
        
        function renderPackages(packages) {
            const grid = document.getElementById('packagesGrid');
            grid.innerHTML = packages.map(pkg => `
                <div class="package-card ${pkg.status === 'inactive' ? 'inactive' : ''}">
                    <div class="points">${pkg.points}点</div>
                    <div class="price">¥${pkg.price.toFixed(2)}</div>
                    <div class="name">${pkg.name}</div>
                    <div class="status-toggle">
                        <button 
                            class="toggle-btn ${pkg.status === 'active' ? 'active' : 'inactive'}"
                            onclick="toggleStatus(${pkg.id}, '${pkg.status}')"
                        >
                            ${pkg.status === 'active' ? '✓ 已上架' : '✗ 已下架'}
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        async function toggleStatus(packageId, currentStatus) {
            const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
            
            const { error } = await API.packages.update(packageId, { status: newStatus });
            
            if (error) {
                Utils.showToast(error, 'error');
                return;
            }
            
            Utils.showToast(newStatus === 'active' ? '已上架' : '已下架', 'success');
            init();
        }
        
        init();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交套餐管理页面**

```bash
git add admin/packages.html
git commit -m "feat: add admin packages management page"
```

---

## Task 15: 更新首页添加登录入口

**Files:**
- Modify: `/workspace/index.html`

- [ ] **Step 1: 在首页头部添加登录入口**

在 `<header>` 标签内的 `</header>` 之前添加：

```html
<div style="margin-top: 24px;">
    <a href="/login.html" style="display: inline-block; padding: 12px 32px; background: linear-gradient(135deg, #E67E22 0%, #D35400 100%); color: white; text-decoration: none; border-radius: 9999px; font-weight: 600; box-shadow: 0 4px 20px rgba(230, 126, 34, 0.3);">登录 / 注册</a>
</div>
```

- [ ] **Step 2: 提交首页更新**

```bash
git add index.html
git commit -m "feat: add login entry on homepage"
```

---

## Task 16: 创建 Supabase 数据库初始化 SQL

**Files:**
- Create: `/workspace/supabase/init.sql`

- [ ] **Step 1: 创建数据库初始化脚本**

```sql
-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    role VARCHAR(20) DEFAULT 'user',
    points_balance INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 报告表
CREATE TABLE IF NOT EXISTS reports (
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

-- 点数套餐表
CREATE TABLE IF NOT EXISTS point_packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    points INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    package_id INTEGER REFERENCES point_packages(id),
    amount DECIMAL(10, 2) NOT NULL,
    points INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    paid_at TIMESTAMP WITH TIME ZONE
);

-- 下载记录表
CREATE TABLE IF NOT EXISTS download_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    report_id UUID REFERENCES reports(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 插入默认点数套餐
INSERT INTO point_packages (name, points, price, status) VALUES
    ('体验档', 1, 1.00, 'active'),
    ('基础档', 10, 9.90, 'active'),
    ('推荐档', 20, 18.90, 'active'),
    ('畅享档', 50, 39.90, 'active'),
    ('尊享档', 100, 69.90, 'active');

-- 创建下载计数函数
CREATE OR REPLACE FUNCTION increment_download_count(report_id UUID)
RETURNS void AS $$
BEGIN
    UPDATE reports SET download_count = download_count + 1 WHERE id = report_id;
END;
$$ LANGUAGE plpgsql;

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_reports_updated_at
    BEFORE UPDATE ON reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

- [ ] **Step 2: 提交数据库初始化脚本**

```bash
git add supabase/init.sql
git commit -m "feat: add supabase database initialization script"
```

---

## Task 17: 最终提交和总结

- [ ] **Step 1: 创建项目说明文档更新**

在 README.md 中添加登录系统说明：

```markdown
## 用户系统

### 功能特性
- 用户注册/登录（支持手机号和邮箱）
- 点数充值系统（5档套餐）
- 深度分析报告下载（1点/份）
- 管理员后台

### 快速开始

1. 在 Supabase 创建项目
2. 执行 `supabase/init.sql` 初始化数据库
3. 更新 `js/supabase-config.js` 中的配置
4. 访问 `/login.html` 开始使用

### 页面说明

| 页面 | 路径 | 说明 |
|------|------|------|
| 登录 | /login.html | 用户登录 |
| 注册 | /register.html | 用户注册 |
| 用户仪表板 | /user/dashboard.html | 查看点数、充值 |
| 深度报告 | /user/reports.html | 浏览下载报告 |
| 我的订单 | /user/orders.html | 订单历史 |
| 管理后台 | /admin/index.html | 管理员仪表板 |
```

- [ ] **Step 2: 最终提交**

```bash
git add README.md
git commit -m "docs: update README with user system documentation"
git log --oneline -10
```

---

## 自我审查

### 1. Spec 覆盖检查

| 需求 | 任务 | 状态 |
|------|------|------|
| 手机号+密码登录 | Task 5 | ✅ |
| 邮箱+密码登录 | Task 5 | ✅ |
| 用户注册 | Task 6 | ✅ |
| 5档点数套餐 | Task 16 | ✅ |
| 每份报告消耗1点 | Task 8 | ✅ |
| 虚拟商品不可退款提示 | Task 7 | ✅ |
| 用户仪表板 | Task 7 | ✅ |
| 报告浏览下载 | Task 8 | ✅ |
| 用户订单历史 | Task 9 | ✅ |
| 管理后台首页 | Task 10 | ✅ |
| 用户管理 | Task 11 | ✅ |
| 报告管理 | Task 12 | ✅ |
| 订单管理 | Task 13 | ✅ |
| 套餐管理 | Task 14 | ✅ |
| Supabase 数据库 | Task 16 | ✅ |

### 2. 占位符检查

✅ 无 "TODO"、"TBD"、"implement later" 等占位符

### 3. 类型一致性检查

✅ 所有函数名、变量名、API 方法名在各任务中保持一致

---

**计划完成，保存至：** `docs/superpowers/plans/2026-05-20-login-admin-system.md`
