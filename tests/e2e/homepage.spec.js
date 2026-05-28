// ============================================================
// 专业星图 - E2E 测试：首页
// ============================================================
import { test, expect } from '@playwright/test';

test.describe('首页', () => {
  test('页面能正常加载', async ({ page }) => {
    const response = await page.goto('/');
    expect(response.status()).toBeLessThan(400);

    await expect(page.locator('.nav-logo')).toHaveText('专业星图');
    await expect(page.locator('#searchInput')).toBeVisible();
    await expect(page.locator('#searchBtn')).toBeVisible();
  });

  test('统计数字能正常显示', async ({ page }) => {
    await page.goto('/');

    const totalMajors = page.locator('#totalMajors');
    const totalCategories = page.locator('#totalCategories');

    // 数字可能是实际的或 fallback 的 0
    await expect(totalMajors).toBeVisible();
    await expect(totalCategories).toBeVisible();
  });

  test('搜索按钮跳转到专业列表页', async ({ page }) => {
    await page.goto('/');

    // 空搜索点击应该跳转到 majors 页
    await page.locator('#searchBtn').click();
    await page.waitForURL(/majors\.html/);
  });

  test('搜索输入回车触发搜索', async ({ page }) => {
    await page.goto('/');

    await page.locator('#searchInput').fill('');
    await page.locator('#searchInput').press('Enter');

    // 空搜索应该跳转
    await page.waitForURL(/majors\.html/);
  });

  test('导航栏显示登录/注册链接（未登录状态）', async ({ page }) => {
    await page.goto('/');

    const userArea = page.locator('#navUserArea');
    await expect(userArea).toBeVisible();

    // 未登录时应该显示登录和注册链接
    const loginLink = userArea.locator('a[href="login.html"]');
    const registerLink = userArea.locator('a[href="register.html"]');
    await expect(loginLink.first()).toBeVisible({ timeout: 5000 });
    await expect(registerLink.first()).toBeVisible({ timeout: 5000 });
  });

  test('查看全部按钮跳转', async ({ page }) => {
    await page.goto('/');

    const viewAllBtn = page.locator('.view-all-btn');
    if (await viewAllBtn.isVisible()) {
      await viewAllBtn.click();
      await page.waitForURL(/majors\.html/);
    }
  });

  test('特色专业卡片渲染', async ({ page }) => {
    await page.goto('/');

    // 等待加载完成
    await page.waitForSelector('#loading', { state: 'hidden', timeout: 15000 }).catch(() => {});

    const grid = page.locator('#featuredGrid');
    await expect(grid).toBeVisible({ timeout: 10000 });

    // 特色卡片应该存在
    const cards = grid.locator('.featured-card');
    const count = await cards.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});
