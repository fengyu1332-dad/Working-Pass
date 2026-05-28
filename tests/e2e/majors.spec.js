// ============================================================
// 专业星图 - E2E 测试：专业列表页（双模式）
// ============================================================
import { test, expect } from '@playwright/test';

// 等待浏览模式加载完成的辅助函数
async function waitForBrowseView(page) {
  await page.waitForFunction(() => {
    const el = document.getElementById('browseTotalCount');
    return el && el.textContent !== '--';
  }, { timeout: 15000 });
}

// 进入列表模式的辅助函数
async function enterListView(page) {
  await waitForBrowseView(page);
  const viewAllBtn = page.locator('#viewAllMajorsBtn');
  await viewAllBtn.click();
  await page.waitForSelector('#listView', { state: 'visible', timeout: 10000 });
}

test.describe('专业列表页 - 浏览模式（默认）', () => {
  test('页面能正常加载浏览模式', async ({ page }) => {
    const response = await page.goto('/majors.html');
    expect(response.status()).toBeLessThan(400);

    await waitForBrowseView(page);

    await expect(page.locator('.browse-hero h1')).toBeVisible();
    await expect(page.locator('#browseSearchInput')).toBeVisible();
    await expect(page.locator('#categoryGrid')).toBeVisible();
  });

  test('分类卡片渲染', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    const cards = page.locator('.category-card');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
  });

  test('快速标签存在', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    const tags = page.locator('.quick-tag');
    const count = await tags.count();
    expect(count).toBeGreaterThanOrEqual(6);
  });

  test('热门精选卡片渲染', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    const picks = page.locator('.hot-pick-card');
    const count = await picks.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test('点击分类卡片进入列表模式', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    const firstCard = page.locator('.category-card').first();
    await firstCard.click();

    // 应该显示列表模式
    await expect(page.locator('#listView')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#breadcrumbTitle')).toBeVisible();
    await expect(page.locator('#resultsCount')).toBeVisible();
  });

  test('点击查看全部进入列表模式', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    await page.locator('#viewAllMajorsBtn').click();
    await expect(page.locator('#listView')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#breadcrumbTitle')).toHaveText('全部专业');
  });

  test('面包屑返回浏览模式', async ({ page }) => {
    await page.goto('/majors.html');
    await enterListView(page);

    await page.locator('#backToBrowse').click();

    // 应该回到浏览模式
    await expect(page.locator('#browseView')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#categoryGrid')).toBeVisible();
  });

  test('浏览模式搜索进入列表模式', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    await page.locator('#browseSearchInput').fill('计算机');
    await page.locator('#browseSearchBtn').click();

    await expect(page.locator('#listView')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('#breadcrumbTitle')).toContainText('计算机');
  });

  test('返回首页链接有效', async ({ page }) => {
    await page.goto('/majors.html');

    const navLogo = page.locator('.nav-logo');
    await expect(navLogo).toBeVisible();
    await navLogo.click();
    await page.waitForURL(/index\.html/);
  });
});

test.describe('专业列表页 - 列表模式', () => {
  test('筛选器选项存在', async ({ page }) => {
    await page.goto('/majors.html');
    await enterListView(page);

    await expect(page.locator('#categoryFilters')).toBeVisible();
    await expect(page.locator('#categoryFilters .category-option').first()).toBeVisible();
    await expect(page.locator('#difficultyFilters')).toBeVisible();
    const diffBtns = page.locator('#difficultyFilters .difficulty-btn');
    await expect(diffBtns.first()).toBeVisible();
    await expect(page.locator('#salaryFilters')).toBeVisible();
  });

  test('视图切换', async ({ page }) => {
    await page.goto('/majors.html');
    await enterListView(page);

    // 切换到列表视图
    const listBtn = page.locator('.view-btn[data-view="list"]');
    if (await listBtn.isVisible()) {
      await listBtn.click();
      await expect(listBtn).toHaveClass(/active/);
    }

    // 切回网格视图
    const gridBtn = page.locator('.view-btn[data-view="grid"]');
    if (await gridBtn.isVisible()) {
      await gridBtn.click();
      await expect(gridBtn).toHaveClass(/active/);
    }
  });

  test('排序下拉框存在', async ({ page }) => {
    await page.goto('/majors.html');
    await enterListView(page);

    const sortSelect = page.locator('#sortSelect');
    await expect(sortSelect).toBeVisible();

    const options = sortSelect.locator('option');
    await expect(options).toHaveCount(3);
  });

  test('搜索输入过滤', async ({ page }) => {
    await page.goto('/majors.html');
    await enterListView(page);

    const searchInput = page.locator('#searchInput');
    await searchInput.fill('计算机');

    const resultsCount = page.locator('#resultsCount');
    await expect(resultsCount).toBeVisible();
  });

  test('重置筛选按钮有效', async ({ page }) => {
    await page.goto('/majors.html');
    await enterListView(page);

    const resetBtn = page.locator('#resetFilters');
    await expect(resetBtn).toBeVisible();

    // 先选一个难度
    const diffBtn = page.locator('.difficulty-btn[data-difficulty="3"]');
    if (await diffBtn.isVisible()) {
      await diffBtn.click();
      await expect(diffBtn).toHaveClass(/active/);
    }

    // 重置
    await resetBtn.click();

    // "全部"难度应该恢复 active
    const allDiffBtn = page.locator('.difficulty-btn[data-difficulty="all"]');
    await expect(allDiffBtn).toHaveClass(/active/);
  });

  test('快速标签进入列表模式', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForBrowseView(page);

    const tag = page.locator('.quick-tag').first();
    await tag.click();

    await expect(page.locator('#listView')).toBeVisible({ timeout: 5000 });
  });
});
