// ============================================================
// 专业星图 - E2E 测试：管理后台
// ============================================================
import { test, expect } from '@playwright/test';

/**
 * 通过 addInitScript 注入 mock Supabase 客户端，模拟已登录 admin
 */
async function mockAdminAuth(page) {
  await page.addInitScript(() => {
    const mockUser = { id: '00000000-0000-0000-0000-000000000001', email: 'admin@test.com' };
    const mockProfile = { id: '00000000-0000-0000-0000-000000000001', phone: '13800000000', points_balance: 999, role: 'admin', created_at: '2025-01-01T00:00:00Z' };

    // 查询构建器链式 API
    function createQueryChain(returnData) {
      const chain = {
        select: () => chain,
        insert: () => chain,
        update: () => chain,
        delete: () => chain,
        upsert: () => chain,
        eq: () => chain,
        neq: () => chain,
        gt: () => chain,
        gte: () => chain,
        lt: () => chain,
        lte: () => chain,
        ilike: () => chain,
        or: () => chain,
        order: () => chain,
        limit: () => chain,
        range: () => chain,
        single: () => Promise.resolve({ data: returnData, error: null }),
        maybeSingle: () => Promise.resolve({ data: returnData, error: null }),
        then: (resolve) => Promise.resolve({ data: returnData, error: null }).then(resolve),
      };
      return chain;
    }

    const mockClient = {
      auth: {
        getUser: () => Promise.resolve({ data: { user: mockUser }, error: null }),
        signOut: () => Promise.resolve({ error: null }),
        onAuthStateChange: () => ({ data: { subscription: { unsubscribe: () => {} } } }),
        signInWithPassword: () => Promise.resolve({ data: { user: mockUser }, error: null }),
        signUp: () => Promise.resolve({ data: { user: mockUser }, error: null }),
      },
      from: (table) => {
        if (table === 'user_profiles') {
          return createQueryChain(mockProfile);
        }
        return createQueryChain(null);
      },
    };

    // 拦截 supabase 全局变量的设置，替换为 mock
    let _supabaseSet = false;
    Object.defineProperty(window, 'supabase', {
      get() {
        return _supabaseSet ? { createClient: () => mockClient } : undefined;
      },
      set(val) {
        _supabaseSet = true;
      },
      configurable: true,
    });
  });
}

// ─── Auth Guard ────────────────────────────────────────────

test.describe('管理后台 - Auth Guard', () => {
  test('未登录访问 /admin/index.html 跳转到登录页', async ({ page }) => {
    await page.goto('/admin/index.html');
    await page.waitForURL(/login\.html/);
    expect(page.url()).toContain('login.html');
  });

  test('未登录访问 /admin/users.html 跳转到登录页', async ({ page }) => {
    await page.goto('/admin/users.html');
    await page.waitForURL(/login\.html/);
  });

  test('未登录访问 /admin/reports.html 跳转到登录页', async ({ page }) => {
    await page.goto('/admin/reports.html');
    await page.waitForURL(/login\.html/);
  });

  test('未登录访问 /admin/majors.html 跳转到登录页', async ({ page }) => {
    await page.goto('/admin/majors.html');
    await page.waitForURL(/login\.html/);
  });

  test('未登录访问 /admin/packages.html 跳转到登录页', async ({ page }) => {
    await page.goto('/admin/packages.html');
    await page.waitForURL(/login\.html/);
  });
});

// ─── 页面结构（已登录 admin） ──────────────────────────────

test.describe('管理后台 - 页面结构（已登录）', () => {
  test.beforeEach(async ({ page }) => {
    await mockAdminAuth(page);
  });

  test('admin/index.html 渲染侧边栏和统计卡片', async ({ page }) => {
    await page.goto('/admin/index.html');
    await expect(page.locator('#adminSidebar')).toBeAttached();
    await expect(page.locator('#totalUsers')).toBeAttached();
    await expect(page.locator('#totalMajors')).toBeAttached();
    await expect(page.locator('#totalReports')).toBeAttached();
    await expect(page.locator('#totalOrders')).toBeAttached();
    await expect(page.locator('#totalDownloads')).toBeAttached();
    await expect(page.locator('#totalRevenue')).toBeAttached();
  });

  test('admin/index.html 渲染今日统计和图表', async ({ page }) => {
    await page.goto('/admin/index.html');
    await expect(page.locator('#todayDownloads')).toBeAttached();
    await expect(page.locator('#todayRevenue')).toBeAttached();
    await expect(page.locator('#revenueBarChart')).toBeAttached();
    await expect(page.locator('#topReportsTable')).toBeAttached();
  });

  test('admin/index.html 快捷操作卡片存在', async ({ page }) => {
    await page.goto('/admin/index.html');
    const cards = page.locator('.quick-action-card');
    await expect(cards.first()).toBeAttached();
    expect(await cards.count()).toBe(4);
  });

  test('admin/users.html 渲染用户表格和搜索栏', async ({ page }) => {
    await page.goto('/admin/users.html');
    await expect(page.locator('#adminSidebar')).toBeAttached();
    await expect(page.locator('#usersTable')).toBeAttached();
    await expect(page.locator('#userSearch')).toBeAttached();
  });

  test('admin/reports.html 渲染报告表格和新增按钮', async ({ page }) => {
    await page.goto('/admin/reports.html');
    await expect(page.locator('#adminSidebar')).toBeAttached();
    await expect(page.locator('#reportsTable')).toBeAttached();
    await expect(page.locator('#addReportBtn')).toBeAttached();
  });

  test('admin/majors.html 渲染专业表格和筛选栏', async ({ page }) => {
    await page.goto('/admin/majors.html');
    await expect(page.locator('#adminSidebar')).toBeAttached();
    await expect(page.locator('#majorsTable')).toBeAttached();
    await expect(page.locator('#addMajorBtn')).toBeAttached();
    await expect(page.locator('#majorSearch')).toBeAttached();
    await expect(page.locator('#categoryFilterSelect')).toBeAttached();
  });

  test('admin/packages.html 渲染套餐表格和新增按钮', async ({ page }) => {
    await page.goto('/admin/packages.html');
    await expect(page.locator('#adminSidebar')).toBeAttached();
    await expect(page.locator('#packagesTable')).toBeAttached();
    await expect(page.locator('#addPackageBtn')).toBeAttached();
  });
});

// ─── 弹窗系统 ───────────────────────────────────────────────

test.describe('管理后台 - 弹窗系统', () => {
  test.beforeEach(async ({ page }) => {
    await mockAdminAuth(page);
  });

  test('modal 元素存在于 admin/users.html', async ({ page }) => {
    await page.goto('/admin/users.html');
    await expect(page.locator('#adminModal')).toBeAttached();
    await expect(page.locator('#adminModalTitle')).toBeAttached();
    await expect(page.locator('#adminModalBody')).toBeAttached();
    await expect(page.locator('#adminModalClose')).toBeAttached();
  });

  test('点击"新增报告"打开弹窗', async ({ page }) => {
    await page.goto('/admin/reports.html');
    await page.waitForSelector('#addReportBtn', { state: 'visible', timeout: 10000 });
    await page.locator('#addReportBtn').click();
    await expect(page.locator('#adminModal.active')).toBeAttached();

    // 通过 Escape 键关闭弹窗
    await page.keyboard.press('Escape');
    await expect(page.locator('#adminModal.active')).not.toBeAttached();
  });

  test('点击"新增套餐"打开弹窗', async ({ page }) => {
    await page.goto('/admin/packages.html');
    await page.waitForSelector('#addPackageBtn', { state: 'visible', timeout: 10000 });
    await page.locator('#addPackageBtn').click();
    await expect(page.locator('#adminModal.active')).toBeAttached();

    // 关闭弹窗
    await page.locator('#cancelPkgBtn').click();
    await expect(page.locator('#adminModal.active')).not.toBeAttached();
  });

  test('点击"新增专业"打开弹窗', async ({ page }) => {
    await page.goto('/admin/majors.html');
    await page.waitForSelector('#addMajorBtn', { state: 'visible', timeout: 10000 });
    await page.locator('#addMajorBtn').click();
    await expect(page.locator('#adminModal.active')).toBeAttached();

    // 关闭弹窗
    await page.locator('#cancelMajorBtn').click();
    await expect(page.locator('#adminModal.active')).not.toBeAttached();
  });
});

// ─── 侧边栏导航 ────────────────────────────────────────────

test.describe('管理后台 - 侧边栏', () => {
  test.beforeEach(async ({ page }) => {
    await mockAdminAuth(page);
  });

  test('侧边栏包含所有 5 个导航入口', async ({ page }) => {
    await page.goto('/admin/index.html');
    await page.waitForSelector('.admin-nav-item', { timeout: 10000 });

    const navItems = page.locator('.admin-nav-item');
    expect(await navItems.count()).toBeGreaterThanOrEqual(5);

    // 验证侧边栏关键链接
    await expect(page.locator('.admin-nav-item[href="/admin/index.html"]')).toBeAttached();
    await expect(page.locator('.admin-nav-item[href="/admin/users.html"]')).toBeAttached();
    await expect(page.locator('.admin-nav-item[href="/admin/reports.html"]')).toBeAttached();
    await expect(page.locator('.admin-nav-item[href="/admin/majors.html"]')).toBeAttached();
    await expect(page.locator('.admin-nav-item[href="/admin/packages.html"]')).toBeAttached();
  });

  test('当前页导航项高亮', async ({ page }) => {
    await page.goto('/admin/majors.html');
    await page.waitForSelector('.admin-nav-item.active', { timeout: 10000 });

    const activeItem = page.locator('.admin-nav-item.active');
    await expect(activeItem).toBeAttached();
    await expect(activeItem).toHaveAttribute('href', '/admin/majors.html');
  });

  test('退出登录按钮存在', async ({ page }) => {
    await page.goto('/admin/index.html');
    await page.waitForSelector('#adminLogoutBtn', { timeout: 10000 });
    await expect(page.locator('#adminLogoutBtn')).toBeAttached();
  });
});
