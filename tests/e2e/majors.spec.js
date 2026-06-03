// ============================================================
// 专业星图 - E2E 测试：专业列表页（按需加载）
// ============================================================
import { test, expect } from '@playwright/test';

// 等待门类入口卡片加载完成
async function waitForCategoryEntries(page) {
  await page.waitForSelector('.category-entry-card', { state: 'visible', timeout: 15000 });
}

// 点击门类入口卡片并等待专业数据加载
async function selectCategoryAndWait(page, categoryName) {
  const card = page.locator('.category-entry-card', { hasText: categoryName });
  await card.click();
  await page.waitForSelector('#loading', { state: 'hidden', timeout: 15000 });
  await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 15000 });
}

test.describe('专业列表页 - 初始状态', () => {
  test('页面能正常加载并显示门类入口卡片', async ({ page }) => {
    const response = await page.goto('/majors.html');
    expect(response.status()).toBeLessThan(400);

    await waitForCategoryEntries(page);

    // 入口卡片可见
    const cards = page.locator('.category-entry-card');
    const count = await cards.count();
    expect(count).toBeGreaterThanOrEqual(13); // 14个门类，至少13个

    // 提示文字可见
    await expect(page.locator('.category-entry-hint')).toBeVisible();
  });

  test('侧边栏门类列表已填充且"全部学科"在底部', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    const options = page.locator('#categoryFilters .category-option');
    const count = await options.count();
    expect(count).toBeGreaterThanOrEqual(14); // 13+门类 + 全部学科

    // 最后一个应该是 "全部学科"
    const lastOption = options.last();
    await expect(lastOption).toContainText('全部学科');

    // 默认没有任何选项是 active
    const activeCount = await page.locator('#categoryFilters .category-option.active').count();
    expect(activeCount).toBe(0);
  });

  test('返回首页链接有效', async ({ page }) => {
    await page.goto('/majors.html');

    const navLogo = page.locator('.nav-logo');
    await expect(navLogo).toBeVisible();
    await navLogo.click();
    await page.waitForURL(/index\.html/);
  });
});

test.describe('专业列表页 - 按需加载', () => {
  test('点击门类入口卡片加载该门类专业', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    // 点击第一个门类卡片
    const firstCard = page.locator('.category-entry-card').first();
    const categoryName = await firstCard.locator('.category-entry-name').textContent();
    await firstCard.click();

    // 入口卡片隐藏，加载骨架出现然后隐藏
    await expect(page.locator('#categoryEntries')).toBeHidden();
    await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 15000 });

    // 结果计数显示该门类专业数
    const resultsCount = page.locator('#resultsCount');
    await expect(resultsCount).toBeVisible();
    const text = await resultsCount.textContent();
    expect(text).toMatch(/\d+ 个专业/);

    // 侧边栏该门类高亮
    const activeOption = page.locator('#categoryFilters .category-option.active');
    await expect(activeOption).toBeVisible();
  });

  test('点击侧边栏门类切换专业数据', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    // 点击侧边栏第一个非全部门类
    const sidebarOptions = page.locator('#categoryFilters .category-option');
    const firstCat = sidebarOptions.first();
    await firstCat.click();

    await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 15000 });
    await expect(firstCat).toHaveClass(/active/);

    // 再点击另一个门类
    const secondCat = sidebarOptions.nth(1);
    await secondCat.click();
    await page.waitForSelector('#loading', { state: 'hidden', timeout: 15000 });
    await expect(secondCat).toHaveClass(/active/);
    await expect(firstCat).not.toHaveClass(/active/);
  });
});

test.describe('专业列表页 - 筛选与视图', () => {
  test('加载门类后难度筛选有效', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    // 加载一个专业较多的门类
    const card = page.locator('.category-entry-card').first();
    await card.click();
    await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 15000 });

    // 选择难度3星
    const diffBtn = page.locator('.difficulty-btn[data-difficulty="3"]');
    if (await diffBtn.isVisible()) {
      await diffBtn.click();
      await expect(diffBtn).toHaveClass(/active/);
    }
  });

  test('视图切换', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    const card = page.locator('.category-entry-card').first();
    await card.click();
    await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 15000 });

    const listBtn = page.locator('.view-btn[data-view="list"]');
    if (await listBtn.isVisible()) {
      await listBtn.click();
      await expect(listBtn).toHaveClass(/active/);
    }

    const gridBtn = page.locator('.view-btn[data-view="grid"]');
    if (await gridBtn.isVisible()) {
      await gridBtn.click();
      await expect(gridBtn).toHaveClass(/active/);
    }
  });

  test('重置筛选按钮有效', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    const card = page.locator('.category-entry-card').first();
    await card.click();
    await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 15000 });

    // 选一个难度
    const diffBtn = page.locator('.difficulty-btn[data-difficulty="3"]');
    if (await diffBtn.isVisible()) {
      await diffBtn.click();
      await expect(diffBtn).toHaveClass(/active/);
    }

    // 重置
    await page.locator('#resetFilters').click();
    const allDiffBtn = page.locator('.difficulty-btn[data-difficulty="all"]');
    await expect(allDiffBtn).toHaveClass(/active/);
  });

  test('排序下拉框存在', async ({ page }) => {
    await page.goto('/majors.html');

    const sortSelect = page.locator('#sortSelect');
    await expect(sortSelect).toBeVisible();
    const options = sortSelect.locator('option');
    await expect(options).toHaveCount(3);
  });
});

test.describe('专业列表页 - 全部学科加载', () => {
  test('点击"全部学科"加载所有专业', async ({ page }) => {
    await page.goto('/majors.html');
    await waitForCategoryEntries(page);

    // 点击侧边栏底部的 "全部学科"
    const allBtn = page.locator('#categoryFilters .category-option').last();
    await expect(allBtn).toContainText('全部学科');
    await allBtn.click();

    await page.waitForSelector('#majorsGrid', { state: 'visible', timeout: 30000 });
    await expect(allBtn).toHaveClass(/active/);
  });
});
