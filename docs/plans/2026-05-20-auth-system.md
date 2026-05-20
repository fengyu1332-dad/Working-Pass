# 专业星图登录与后台管理系统实施计划（续）

---

## 阶段二：用户端核心功能（续）

### Task 6: 创建报告浏览与下载页面（续）

**Files:**
- Create: `/workspace/user/reports.html`
- Create: `/workspace/js/reports.js`

---

（接 Task 6 的报告浏览页面的完整内容：

```html
<!-- /workspace/user/reports.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>报告浏览 - 专业星图</title>
    <link rel="stylesheet" href="/css/common.css">
    <style>
        .search-bar {
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
        }

        .search-bar .form-input {
            flex: 1;
        }

        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .report-card {
            cursor: pointer;
            transition: all 0.3s;
        }

        .report-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px var(--shadow);
        }

        .report-code {
            display: inline-block;
            background: var(--secondary-container);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: var(--secondary);
            margin-bottom: 12px;
        }

        .report-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--secondary);
            margin-bottom: 8px;
        }

        .report-meta {
            display: flex;
            justify-content: space-between;
            color: var(--on-surface-variant);
            font-size: 14px;
            margin-top: 16px;
        }

        /* 报告详情模态框 */
        .report-detail {
            max-width: 700px;
        }

        .report-preview {
            background: var(--secondary-container);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            max-height: 300px;
            overflow-y: auto;
        }

        .report-locked {
            text-align: center;
            padding: 32px;
            background: var(--secondary-container);
            border-radius: 12px;
            margin: 20px 0;
        }

        .report-locked-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav">
            <a href="/" class="nav-logo">专业星图</a>
            <div class="nav-links">
                <a href="/user/dashboard.html" class="nav-link">个人中心</a>
                <a href="#" id="logoutBtn" class="nav-link">退出</a>
            </div>
        </nav>

        <h1 style="font-size: 32px; color: var(--secondary); margin-bottom: 24px;">专业深度报告</h1>

        <!-- 搜索栏 -->
        <div class="search-bar">
            <input type="text" id="searchInput" class="form-input" placeholder="搜索专业名称或代码...">
            <button class="btn btn-primary" onclick="searchReports()">搜索</button>
        </div>

        <!-- 报告列表 -->
        <div class="reports-grid" id="reportsGrid">
            <!-- 报告卡片将通过 JS 加载 -->
        </div>
    </div>

    <!-- 报告详情模态框 -->
    <div class="modal" id="reportModal">
        <div class="modal-content report-detail">
            <div class="modal-header">
                <h2 class="modal-title" id="modalTitle">报告详情</h2>
                <button class="modal-close" onclick="closeReportModal()">&times;</button>
            </div>

            <div id="modalContent">
                <!-- 报告内容将通过 JS 加载 -->
            </div>
        </div>
    </div>

    <script type="module">
        import { checkAuthAndRedirect, logout, getUserProfile, showToast } from '/js/auth.js'
        import { getReports, getReport, downloadReport } from '/js/reports.js'

        let currentReports = []
        let currentProfile = null

        // 检查登录状态
        await checkAuthAndRedirect()

        // 加载用户资料
        async function loadProfile() {
            currentProfile = await getUserProfile()
        }

        // 加载报告列表
        async function loadReports(search = null) {
            const reports = await getReports(null, search)
            currentReports = reports
            renderReports(reports)
        }

        // 渲染报告列表
        function renderReports(reports) {
            const grid = document.getElementById('reportsGrid')
            grid.innerHTML = ''

            if (reports.length === 0) {
                grid.innerHTML = `
                    <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--on-surface-variant);">
                        暂无报告数据
                    </div>
                `
                return
            }

            reports.forEach(report => {
                const card = document.createElement('div')
                card.className = 'card report-card'
                card.onclick = () => showReportDetail(report)
                card.innerHTML = `
                    <div class="report-code">${report.major_code}</div>
                    <div class="report-title">${report.major_name}</div>
                    <div style="color: var(--on-surface-variant); font-size: 14px;">${report.category}</div>
                    <div class="report-meta">
                        <span>下载 ${report.download_count} 次</span>
                        <span>消耗 1 点</span>
                    </div>
                `
                grid.appendChild(card)
            })
        }

        // 显示报告详情
        async function showReportDetail(report) {
            const modal = document.getElementById('reportModal')
            const title = document.getElementById('modalTitle')
            const content = document.getElementById('modalContent')

            title.textContent = report.major_name

            content.innerHTML = `
                <div class="report-code">${report.major_code}</div>
                <div style="color: var(--on-surface-variant); margin-bottom: 16px;">${report.category}</div>
                
                <!-- 预览内容 -->
                <div class="report-preview">
                    <div style="font-weight: 600; margin-bottom: 12px;">👁️ 免费预览</div>
                    <div style="white-space: pre-wrap;">${report.preview_content || '暂无预览内容'}</div>
                </div>
                
                <!-- 锁定内容 -->
                <div class="report-locked">
                    <div class="report-locked-icon">🔒</div>
                    <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">解锁完整报告</div>
                    <div style="color: var(--on-surface-variant); margin-bottom: 20px;">
                        您的点数: <span style="color: var(--primary); font-weight: 700;">${currentProfile?.points_balance || 0}</span>
                    </div>
                    <button class="btn btn-primary" onclick="downloadReportWrapper('${report.id}')">
                        消耗 1 点下载完整报告
                    </button>
                    ${(currentProfile?.points_balance || 0) < 1 ? `
                        <div style="margin-top: 12px;">
                            <a href="/user/purchase.html" style="color: var(--primary); text-decoration: none;">点数不足？去充值 &rarr;</a>
                        </div>
                    ` : ''}
                </div>
            `

            modal.classList.add('active')
        }

        // 下载报告包装器
        async function downloadReportWrapper(reportId) {
            try {
                const fullContent = await downloadReport(reportId)
                
                // 刷新用户资料
                await loadProfile()
                
                // 显示完整内容
                const content = document.getElementById('modalContent')
                const report = currentReports.find(r => r.id === reportId)
                
                content.innerHTML = `
                    <div class="report-code">${report.major_code}</div>
                    <div style="color: var(--on-surface-variant); margin-bottom: 20px;">${report.category}</div>
                    <div style="white-space: pre-wrap;">${fullContent}</div>
                    <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--outline); text-align: center;">
                        <button class="btn btn-primary" onclick="closeReportModal()">关闭</button>
                    </div>
                `
            } catch (error) {
                showToast(error.message || '下载失败', 'error')
            }
        }

        // 搜索报告
        function searchReports() {
            const search = document.getElementById('searchInput').value
            loadReports(search)
        }

        // 关闭模态框
        function closeReportModal() {
            document.getElementById('reportModal').classList.remove('active')
        }

        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', (e) => {
            e.preventDefault()
            logout()
        })

        // 初始化
        await loadProfile()
        await loadReports()
    </script>
</body>
</html>
```

---

### Task 7: 创建订单与下载历史页面

**Files:**
- Create: `/workspace/user/orders.html`

**Goal:** 实现订单和下载记录查看功能

- [ ] **Step 1: 创建历史记录页面**

```html
<!-- /workspace/user/orders.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>历史记录 - 专业星图</title>
    <link rel="stylesheet" href="/css/common.css">
    <style>
        .tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 2px solid var(--outline);
        }

        .tab-btn {
            padding: 12px 24px;
            background: none;
            border: none;
            font-size: 16px;
            font-weight: 600;
            color: var(--on-surface-variant);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
            transition: all 0.3s;
        }

        .tab-btn:hover {
            color: var(--secondary);
        }

        .tab-btn.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }

        .records-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .record-item {
            padding: 20px;
            border-bottom: 1px solid var(--outline);
        }

        .record-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .record-title {
            font-weight: 600;
            color: var(--secondary);
            margin-bottom: 4px;
        }

        .record-meta {
            color: var(--on-surface-variant);
            font-size: 14px;
        }

        .record-points {
            font-size: 18px;
            font-weight: 700;
        }

        .positive {
            color: var(--success);
        }

        .negative {
            color: var(--error);
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav">
            <a href="/" class="nav-logo">专业星图</a>
            <div class="nav-links">
                <a href="/user/dashboard.html" class="nav-link">个人中心</a>
                <a href="#" id="logoutBtn" class="nav-link">退出</a>
            </div>
        </nav>

        <h1 style="font-size: 32px; color: var(--secondary); margin-bottom: 8px;">历史记录</h1>
        <p style="color: var(--on-surface-variant); margin-bottom: 24px;">查看您的订单和下载记录</p>

        <!-- 标签页 -->
        <div class="tabs">
            <button class="tab-btn active" data-tab="orders" onclick="switchTab('orders')">订单记录</button>
            <button class="tab-btn" data-tab="downloads" onclick="switchTab('downloads')">下载记录</button>
        </div>

        <!-- 订单记录 -->
        <div id="ordersTab" class="card" style="padding: 0;">
            <div id="ordersList" class="records-list">
                <!-- 订单记录将通过 JS 加载 -->
            </div>
        </div>

        <!-- 下载记录 -->
        <div id="downloadsTab" class="card" style="padding: 0; display: none;">
            <div id="downloadsList" class="records-list">
                <!-- 下载记录将通过 JS 加载 -->
            </div>
        </div>
    </div>

    <script type="module">
        import { checkAuthAndRedirect, logout, showToast } from '/js/auth.js'
        import { getOrders, getDownloadRecords } from '/js/payments.js'

        let currentTab = 'orders'

        // 检查登录状态
        await checkAuthAndRedirect()

        // 切换标签页
        function switchTab(tab) {
            currentTab = tab
            
            // 更新按钮状态
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.tab === tab)
            })
            
            // 显示对应内容
            document.getElementById('ordersTab').style.display = tab === 'orders' ? 'block' : 'none'
            document.getElementById('downloadsTab').style.display = tab === 'downloads' ? 'block' : 'none'
            
            // 加载数据
            if (tab === 'orders') {
                loadOrders()
            } else {
                loadDownloads()
            }
        }

        // 加载订单
        async function loadOrders() {
            try {
                const orders = await getOrders()
                const list = document.getElementById('ordersList')
                
                if (orders.length === 0) {
                    list.innerHTML = `
                        <div style="padding: 48px; text-align: center; color: var(--on-surface-variant);">
                            暂无订单记录
                        </div>
                    `
                    return
                }

                list.innerHTML = orders.map(order => `
                    <div class="record-item">
                        <div class="record-header">
                            <div>
                                <div class="record-title">${order.point_packages?.name || '点数充值'}</div>
                                <div class="record-meta">
                                    ${new Date(order.created_at).toLocaleString('zh-CN')} • 
                                    ${order.status === 'paid' ? '✅ 已支付' : order.status === 'pending' ? '⏳ 待支付' : order.status === 'cancelled' ? '❌ 已取消' : order.status}
                                </div>
                            </div>
                            <div class="record-points positive">
                                +${order.points}
                            </div>
                        </div>
                    </div>
                `).join('')
            } catch (error) {
                showToast('加载订单失败', 'error')
            }
        }

        // 加载下载记录
        async function loadDownloads() {
            try {
                const downloads = await getDownloadRecords()
                const list = document.getElementById('downloadsList')
                
                if (downloads.length === 0) {
                    list.innerHTML = `
                        <div style="padding: 48px; text-align: center; color: var(--on-surface-variant);">
                            暂无下载记录
                        </div>
                    `
                    return
                }

                list.innerHTML = downloads.map(record => `
                    <div class="record-item">
                        <div class="record-header">
                            <div>
                                <div class="record-title">${record.reports?.major_name || '专业报告'}</div>
                                <div class="record-meta">
                                    ${record.reports?.major_code || ''} • 
                                    ${new Date(record.created_at).toLocaleString('zh-CN')}
                                </div>
                            </div>
                            <div class="record-points negative">
                                -${record.points_spent}
                            </div>
                        </div>
                    </div>
                `).join('')
            } catch (error) {
                showToast('加载下载记录失败', 'error')
            }
        }

        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', (e) => {
            e.preventDefault()
            logout()
        })

        // 初始化
        loadOrders()
    </script>
</body>
</html>
```

---

## 阶段三：管理后台（MVP）

### Task 8: 创建管理后台首页

**Files:**
- Create: `/workspace/admin/index.html`
- Create: `/workspace/css/admin.css`

**Goal:** 实现管理后台数据概览页面

- [ ] **Step 1: 创建管理后台样式文件

```css
/* /workspace/css/admin.css */
/* 管理后台通用样式 */
.admin-layout {
    display: grid;
    grid-template-columns: 240px 1fr;
    min-height: 100vh;
}

.admin-sidebar {
    background: var(--surface-container);
    border-right: 1px solid var(--outline);
    padding: 24px 0;
}

.admin-sidebar-nav {
    list-style: none;
}

.admin-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 24px;
    color: var(--on-surface);
    text-decoration: none;
    transition: all 0.3s;
}

.admin-nav-item:hover {
    background: var(--secondary-container);
}

.admin-nav-item.active {
    background: var(--primary-container);
    color: var(--primary);
    font-weight: 600;
}

.admin-content {
    padding: 24px 32px;
}

.admin-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 32px;
}

.admin-stat-card {
    background: var(--surface-container);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 24px var(--shadow);
}

.admin-stat-value {
    font-size: 36px;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 4px;
}

.admin-stat-label {
    font-size: 14px;
    color: var(--on-surface-variant);
}

.admin-section {
    background: var(--surface-container);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 24px var(--shadow);
}

.admin-section-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--secondary);
    margin-bottom: 20px;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
}

.admin-table th,
.admin-table td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--outline);
}

.admin-table th {
    font-weight: 600;
    color: var(--secondary);
    background: var(--secondary-container);
}

.admin-table tr:hover {
    background: var(--secondary-container);
}
```

- [ ] **Step 2: 创建管理后台首页

```html
<!-- /workspace/admin/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>管理后台 - 专业星图</title>
    <link rel="stylesheet" href="/css/common.css">
    <link rel="stylesheet" href="/css/admin.css">
</head>
<body>
    <div class="admin-layout">
        <!-- 侧边栏 -->
        <div class="admin-sidebar">
            <div style="padding: 0 24px; margin-bottom: 24px;">
                <div class="admin-logo" style="font-size: 20px; font-weight: 700; color: var(--secondary);">
                    专业星图
                </div>
                <div style="font-size: 14px; color: var(--on-surface-variant); margin-top: 4px;">
                    管理后台
                </div>
            </div>
            <nav class="admin-sidebar-nav">
                <a href="/admin/index.html" class="admin-nav-item active">
                    📊 数据概览
                </a>
                <a href="/admin/users.html" class="admin-nav-item">
                    👥 用户管理
                </a>
                <a href="/admin/reports.html" class="admin-nav-item">
                    📚 报告管理
                </a>
            </nav>
            <div style="margin-top: auto; padding: 0 24px; border-top: 1px solid var(--outline); margin-top: 24px; padding-top: 24px;">
                <a href="/user/dashboard.html" class="admin-nav-item">
                    ← 返回用户端
                </a>
                <a href="#" id="logoutBtn" class="admin-nav-item" style="color: var(--error);">
                    退出登录
                </a>
            </div>
        </div>

        <!-- 内容区域 -->
        <div class="admin-content">
            <h1 style="font-size: 28px; color: var(--secondary); margin-bottom: 24px;">
                数据概览
            </h1>

            <!-- 统计卡片 -->
            <div class="admin-stats-grid">
                <div class="admin-stat-card">
                    <div class="admin-stat-value" id="totalUsers">0</div>
                    <div class="admin-stat-label">总用户数</div>
                </div>
                <div class="admin-stat-card">
                    <div class="admin-stat-value" id="totalOrders">0</div>
                    <div class="admin-stat-label">总订单数</div>
                </div>
                <div class="admin-stat-card">
                    <div class="admin-stat-value" id="totalDownloads">0</div>
                    <div class="admin-stat-label">总下载次数</div>
                </div>
                <div class="admin-stat-card">
                    <div class="admin-stat-value" id="totalReports">0</div>
                    <div class="admin-stat-label">报告数量</div>
                </div>
            </div>

            <!-- 热门报告 -->
            <div class="admin-section">
                <h2 class="admin-section-title">热门报告 TOP 5</h2>
                <table class="admin-table" id="topReportsTable">
                    <thead>
                        <tr>
                            <th>专业代码</th>
                            <th>专业名称</th>
                            <th>下载次数</th>
                        </tr>
                    </thead>
                    <tbody id="topReportsBody">
                        <!-- 数据将通过 JS 加载 -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script type="module">
        import { checkAuthAndRedirect, logout, isAdmin, showToast } from '/js/auth.js'
        import { supabase } from '/js/supabase-client.js'

        // 检查登录和管理员状态
        const isLoggedIn = await checkAuthAndRedirect()
        if (!isLoggedIn) {
            // 已经被重定向
        }

        // 检查是否是管理员
        if (!await isAdmin()) {
            showToast('无权访问管理后台', 'error')
            window.location.href = '/user/dashboard.html'
        }

        // 加载统计数据
        async function loadStats() {
            // 这是模拟数据，实际项目中需要通过聚合查询
            // 这里为了简化直接获取所有数据
            
            try {
                // 用户数
                const { data: users } = await supabase.from('user_profiles').select('id', { count: 'exact' })
                document.getElementById('totalUsers').textContent = users.length
                
                // 报告数
                const { data: reports } = await supabase.from('reports').select('id', { count: 'exact' })
                document.getElementById('totalReports').textContent = reports.length
                
                // 订单数
                const { data: orders } = await supabase.from('orders').select('id', { count: 'exact' })
                document.getElementById('totalOrders').textContent = orders.length
                
                // 下载次数
                const { data: downloads } = await supabase.from('download_records').select('id', { count: 'exact' })
                document.getElementById('totalDownloads').textContent = downloads.length
                
                // 热门报告
                const { data: topReports } = await supabase
                    .from('reports')
                    .select('major_code, major_name, download_count')
                    .order('download_count', { ascending: false })
                    .limit(5)
                
                const tbody = document.getElementById('topReportsBody')
                tbody.innerHTML = topReports.map(r => `
                    <tr>
                        <td>${r.major_code}</td>
                        <td>${r.major_name}</td>
                        <td>${r.download_count}</td>
                    </tr>
                `).join('')
            } catch (error) {
                console.error('加载统计失败:', error)
                showToast('加载统计数据失败', 'error')
            }
        }

        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', (e) => {
            e.preventDefault()
            logout()
        })

        // 初始化
        loadStats()
    </script>
</body>
</html>
```

---

### Task 9: 创建用户管理页面

**Files:**
- Create: `/workspace/admin/users.html`

**Goal:** 实现用户列表查看和点数调整功能

- [ ] **Step 1: 创建用户管理页面

```html
<!-- /workspace/admin/users.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户管理 - 专业星图</title>
    <link rel="stylesheet" href="/css/common.css">
    <link rel="stylesheet" href="/css/admin.css">
    <style>
        .action-btns {
            display: flex;
            gap: 8px;
        }

        .btn-sm {
            padding: 8px 16px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="admin-layout">
        <!-- 侧边栏 -->
        <div class="admin-sidebar">
            <div style="padding: 0 24px; margin-bottom: 24px;">
                <div class="admin-logo" style="font-size: 20px; font-weight: 700; color: var(--secondary);">
                    专业星图
                </div>
            </div>
            <nav class="admin-sidebar-nav">
                <a href="/admin/index.html" class="admin-nav-item">
                    📊 数据概览
                </a>
                <a href="/admin/users.html" class="admin-nav-item active">
                    👥 用户管理
                </a>
                <a href="/admin/reports.html" class="admin-nav-item">
                    📚 报告管理
                </a>
            </nav>
            <div style="margin-top: auto; padding: 0 24px; border-top: 1px solid var(--outline); margin-top: 24px; padding-top: 24px;">
                <a href="#" id="logoutBtn" class="admin-nav-item" style="color: var(--error);">
                    退出登录
                </a>
            </div>
        </div>

        <!-- 内容区域 -->
        <div class="admin-content">
            <h1 style="font-size: 28px; color: var(--secondary); margin-bottom: 24px;">
                用户管理
            </h1>

            <div class="admin-section">
                <table class="admin-table" id="usersTable">
                    <thead>
                        <tr>
                            <th>用户ID</th>
                            <th>手机号</th>
                            <th>当前点数</th>
                            <th>角色</th>
                            <th>注册时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="usersTableBody">
                        <!-- 数据将通过 JS 加载 -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- 调整点数模态框 -->
    <div class="modal" id="pointsModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">调整用户点数</h2>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>

            <div id="modalContent">
                <form id="pointsForm">
                    <div class="form-group">
                        <label class="form-label">用户</label>
                        <div id="modalUserName" style="margin-bottom: 8px; color: var(--secondary); font-weight: 600;"></div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">调整方式</label>
                        <select id="adjustType" class="form-input">
                            <option value="add">增加点数</option>
                            <option value="set">设置点数</option>
                            <option value="deduct">扣减点数</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">数量</label>
                        <input type="number" id="adjustAmount" class="form-input" min="1" required>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">取消</button>
                        <button type="submit" class="btn btn-primary">确认</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script type="module">
        import { checkAuthAndRedirect, logout, isAdmin, showToast } from '/js/auth.js'
        import { supabase } from '/js/supabase-client.js'

        let currentUserId = null

        // 检查登录和管理员状态
        await checkAuthAndRedirect()
        if (!await isAdmin()) {
            showToast('无权访问管理后台', 'error')
            window.location.href = '/user/dashboard.html'
        }

        // 加载用户列表
        async function loadUsers() {
            try {
                const { data: users } = await supabase
                    .from('user_profiles')
                    .select('*')
                    .order('created_at', { ascending: false })

                const tbody = document.getElementById('usersTableBody')
                
                if (users.length === 0) {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" style="text-align: center; padding: 48px; color: var(--on-surface-variant);">
                                暂无用户
                            </td>
                        </tr>
                    `
                    return
                }

                tbody.innerHTML = users.map(user => `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.phone || '未设置'}</td>
                        <td>${user.points_balance}</td>
                        <td>${user.role === 'admin' ? '管理员' : '用户'}</td>
                        <td>${new Date(user.created_at).toLocaleString('zh-CN')}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" onclick="openPointsModal('${user.id}', '${user.phone || '未设置'}', ${user.points_balance})">
                                调整点数
                            </button>
                        </td>
                    </tr>
                `).join('')
            } catch (error) {
                console.error('加载用户列表失败:', error)
                showToast('加载用户列表失败', 'error')
            }
        }

        // 打开调整点数模态框
        function openPointsModal(userId, userPhone, currentPoints) {
            currentUserId = userId
            document.getElementById('modalUserName').textContent = 
                `${userPhone} (当前点数: ${currentPoints})
            document.getElementById('pointsModal').classList.add('active')
        }

        // 调整点数
        document.getElementById('pointsForm').addEventListener('submit', async (e) => {
            e.preventDefault()
            
            const adjustType = document.getElementById('adjustType').value
            const amount = parseInt(document.getElementById('adjustAmount').value)

            if (!currentUserId || !amount) {
                return
            }

            try {
                // 获取当前用户点数
                const { data: user } = await supabase
                    .from('user_profiles')
                    .select('points_balance')
                    .eq('id', currentUserId)
                    .single()

                let newPoints
                if (adjustType === 'add') {
                    newPoints = user.points_balance + amount
                } else if (adjustType === 'set') {
                    newPoints = amount
                } else if (adjustType === 'deduct') {
                    newPoints = user.points_balance - amount
                }

                // 更新点数
                await supabase
                    .from('user_profiles')
                    .update({ points_balance: newPoints })
                    .eq('id', currentUserId)

                showToast('点数调整成功', 'success')
                closeModal()
                loadUsers()
            } catch (error) {
                showToast('调整失败', 'error')
            }
        })

        // 关闭模态框
        function closeModal() {
            document.getElementById('pointsModal').classList.remove('active')
            document.getElementById('pointsForm').reset()
            currentUserId = null
        }

        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', (e) => {
            e.preventDefault()
            logout()
        })

        // 初始化
        loadUsers()
    </script>
</body>
</html>
```

---

### Task 10: 创建报告管理页面

**Files:**
- Create: `/workspace/admin/reports.html`

**Goal:** 实现报告列表和报告内容管理

- [ ] **Step 1: 创建报告管理页面

```html
<!-- /workspace/admin/reports.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>报告管理 - 专业星图</title>
    <link rel="stylesheet" href="/css/common.css">
    <link rel="stylesheet" href="/css/admin.css">
</head>
<body>
    <div class="admin-layout">
        <!-- 侧边栏 -->
        <div class="admin-sidebar">
            <div style="padding: 0 24px; margin-bottom: 24px;">
                <div class="admin-logo" style="font-size: 20px; font-weight: 700; color: var(--secondary);">
                    专业星图
                </div>
            </div>
            <nav class="admin-sidebar-nav">
                <a href="/admin/index.html" class="admin-nav-item">
                    📊 数据概览
                </a>
                <a href="/admin/users.html" class="admin-nav-item">
                    👥 用户管理
                </a>
                <a href="/admin/reports.html" class="admin-nav-item active">
                    📚 报告管理
                </a>
            </nav>
            <div style="margin-top: auto; padding: 0 24px; border-top: 1px solid var(--outline); margin-top: 24px; padding-top: 24px;">
                <a href="#" id="logoutBtn" class="admin-nav-item" style="color: var(--error);">
                    退出登录
                </a>
            </div>
        </div>

        <!-- 内容区域 -->
        <div class="admin-content">
            <h1 style="font-size: 28px; color: var(--secondary); margin-bottom: 24px;">
                报告管理
            </h1>

            <div class="admin-section">
                <table class="admin-table" id="reportsTable">
                    <thead>
                        <tr>
                            <th>专业代码</th>
                            <th>专业名称</th>
                            <th>学科门类</th>
                            <th>状态</th>
                            <th>下载次数</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="reportsTableBody">
                        <!-- 数据将通过 JS 加载 -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- 报告编辑模态框 -->
    <div class="modal" id="reportEditModal">
        <div class="modal-content" style="max-width: 800px;">
            <div class="modal-header">
                <h2 class="modal-title" id="editModalTitle">编辑报告</h2>
                <button class="modal-close" onclick="closeEditModal()">&times;</button>
            </div>

            <form id="reportEditForm">
                <div class="form-group">
                    <label class="form-label">专业代码</label>
                    <input type="text" id="editMajorCode" class="form-input" readonly>
                </div>
                <div class="form-group">
                    <label class="form-label">专业名称</label>
                    <input type="text" id="editMajorName" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">学科门类</label>
                    <input type="text" id="editCategory" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">预览内容（前20%）</label>
                    <textarea id="editPreviewContent" class="form-input" rows="4"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">完整报告内容</label>
                    <textarea id="editFullContent" class="form-input" rows="8"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">状态</label>
                    <select id="editStatus" class="form-input">
                        <option value="draft">草稿</option>
                        <option value="published">已发布</option>
                        <option value="archived">已归档</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeEditModal()">取消</button>
                    <button type="submit" class="btn btn-primary">保存</button>
                </div>
            </form>
        </div>
    </div>

    <script type="module">
        import { checkAuthAndRedirect, logout, isAdmin, showToast } from '/js/auth.js'
        import { supabase } from '/js/supabase-client.js'

        let currentReportId = null

        // 检查登录和管理员状态
        await checkAuthAndRedirect()
        if (!await isAdmin()) {
            showToast('无权访问管理后台', 'error')
            window.location.href = '/user/dashboard.html'
        }

        // 加载报告列表
        async function loadReports() {
            try {
                const { data: reports } = await supabase
                    .from('reports')
                    .select('*')
                    .order('created_at', { ascending: false })

                const tbody = document.getElementById('reportsTableBody')
                
                if (reports.length === 0) {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" style="text-align: center; padding: 48px; color: var(--on-surface-variant);">
                                暂无报告
                            </td>
                        </tr>
                    `
                    return
                }

                tbody.innerHTML = reports.map(report => `
                    <tr>
                        <td>${report.major_code}</td>
                        <td>${report.major_name}</td>
                        <td>${report.category}</td>
                        <td>
                            ${report.status === 'published' ? '✅ 已发布' : report.status === 'draft' ? '📝 草稿' : '📦 已归档'}</td>
                        <td>${report.download_count}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" onclick="openEditModal('${report.id}')">
                                编辑
                            </button>
                        </td>
                    </tr>
                `).join('')
            } catch (error) {
                console.error('加载报告列表失败:', error)
                showToast('加载报告列表失败', 'error')
            }
        }

        // 打开编辑模态框
        async function openEditModal(reportId) {
            currentReportId = reportId
            
            try {
                const { data: report } = await supabase
                    .from('reports')
                    .select('*')
                    .eq('id', reportId)
                    .single()

                if (report) {
                    document.getElementById('editMajorCode').value = report.major_code
                    document.getElementById('editMajorName').value = report.major_name
                    document.getElementById('editCategory').value = report.category
                    document.getElementById('editPreviewContent').value = report.preview_content || ''
                    document.getElementById('editFullContent').value = report.full_content || ''
                    document.getElementById('editStatus').value = report.status
                    document.getElementById('editModalTitle').textContent = '编辑报告'
                    document.getElementById('reportEditModal').classList.add('active')
                }
            } catch (error) {
                showToast('加载报告失败', 'error')
            }
        }

        // 保存报告
        document.getElementById('reportEditForm').addEventListener('submit', async (e) => {
            e.preventDefault()
            
            if (!currentReportId) return

            try {
                const updates = {
                    major_name: document.getElementById('editMajorName').value,
                    category: document.getElementById('editCategory').value,
                    preview_content: document.getElementById('editPreviewContent').value,
                    full_content: document.getElementById('editFullContent').value,
                    status: document.getElementById('editStatus').value,
                    updated_at: new Date().toISOString()
                }

                await supabase
                    .from('reports')
                    .update(updates)
                    .eq('id', currentReportId)

                showToast('保存成功', 'success')
                closeEditModal()
                loadReports()
            } catch (error) {
                showToast('保存失败', 'error')
            }
        })

        // 关闭模态框
        function closeEditModal() {
            document.getElementById('reportEditModal').classList.remove('active')
            document.getElementById('reportEditForm').reset()
            currentReportId = null
        }

        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', (e) => {
            e.preventDefault()
            logout()
        })

        // 初始化
        loadReports()
    </script>
</body>
</html>
```

---

## 阶段四：完善与测试

### Task 11: 生成所有页面链接与测试

**Files:**
- Modify: `/workspace/index.html` (添加登录入口)
- Modify: `/workspace/majors.html` (添加登录入口)

**Goal:** 完善现有页面与新系统的连接

- [ ] **Step 1: 更新首页添加登录按钮

在 [index.html](file:///workspace/index.html) 的 header 部分添加登录按钮：

```html
<!-- 在 header 部分添加 -->
<header>
    <h1>专业星图</h1>
    <p>温暖、专业的大学专业选择指南</p>
    <div style="margin-top: 20px;">
        <a href="/login.html" class="view-all-btn">登录/注册，获取深度报告</a>
    </div>
</header>
```

---

## 完成检查清单

- [ ] Supabase 项目配置
- [ ] 运行数据库初始化 SQL 脚本
- [ ] 配置 URL 项目 URL 和匿名密钥
- [ ] 注册一个普通用户并将其设为管理员
- [ ] 测试所有用户端页面（登录、个人中心、购买点数、报告浏览等）
- [ ] 测试管理后台功能
- [ ] 整体功能测试

---

计划保存并提交

这是完整的实施计划，分为四个阶段 11 个任务，预计 11-15 个工作日可完成 MVP 所有核心功能。