// ============================================================
// 专业星图 - E2E 测试：适配测评
// ============================================================
import { test, expect } from '@playwright/test';

// ---- 辅助函数 ----

/** 等待测评页面数据加载完毕、问卷渲染 */
async function waitForQuizReady(page) {
  // 等待 loading 消失 + quiz card 填充内容
  await page.waitForSelector('#quizCard .quiz-question-group', { timeout: 15000 });
  await page.waitForTimeout(300);
}

async function answerStep1(page) {
  await waitForQuizReady(page);

  // 1a. 学科 multi-select
  const subjectBtns = page.locator('#quizCard .option-btn');
  const count = await subjectBtns.count();
  for (let i = 0; i < Math.min(3, count); i++) {
    await subjectBtns.nth(i).click();
    await page.waitForTimeout(80);
  }

  // 1b. 学习风格 single-card
  const styleCards = page.locator('#quizCard .option-card');
  if (await styleCards.count() > 0) {
    await styleCards.first().click();
    await page.waitForTimeout(80);
  }

  // 1c. 兴趣程度 likert（每个 likert-row 里选第4档）
  const rows = page.locator('#quizCard .likert-row');
  for (let i = 0; i < await rows.count(); i++) {
    await rows.nth(i).locator('.likert-btn[data-v="4"]').click();
    await page.waitForTimeout(50);
  }
}

async function answerCurrentPage(page) {
  // Handle whatever question types are currently visible
  const rankOpts = page.locator('#quizCard .rank-option');
  for (let i = 0; i < Math.min(3, await rankOpts.count()); i++) {
    await rankOpts.nth(i).click();
    await page.waitForTimeout(60);
  }
  const cards = page.locator('#quizCard .option-card');
  if (await cards.count() > 0) {
    await cards.first().click();
    await page.waitForTimeout(60);
  }
  const rows = page.locator('#quizCard .likert-row');
  for (let i = 0; i < await rows.count(); i++) {
    await rows.nth(i).locator('.likert-btn[data-v="3"]').click();
    await page.waitForTimeout(40);
  }
}

async function completeFullQuiz(page) {
  // Step 1
  await answerStep1(page);
  await page.locator('#btnNext').click();
  await page.waitForTimeout(500);

  // Step 2/3: navigate through remaining pages
  for (let sub = 0; sub < 5; sub++) {
    await answerCurrentPage(page);

    // Stop if submit button is visible
    if (await page.locator('#btnSubmit').isVisible()) break;
    // Stop if next button not visible (shouldn't happen)
    if (!(await page.locator('#btnNext').isVisible())) break;

    await page.locator('#btnNext').click();
    await page.waitForTimeout(500);
  }

  // Submit
  await page.waitForSelector('#btnSubmit', { state: 'visible', timeout: 5000 });
  await page.locator('#btnSubmit').click();
  await page.waitForTimeout(4000);
}

// ---- 测试 ----
test.describe('适配测评页面', () => {
  test('页面正常加载，显示问卷', async ({ page }) => {
    await page.goto('/assessment.html');
    // 等待数据加载完成后 quiz 出现
    await waitForQuizReady(page);
    await expect(page.locator('#quizSection')).toBeVisible();
    await expect(page.locator('#errorState')).not.toBeVisible();
  });

  test('进度条显示正确的步骤', async ({ page }) => {
    await page.goto('/assessment.html');
    await waitForQuizReady(page);
    const steps = page.locator('.progress-step');
    await expect(steps).toHaveCount(3);
    await expect(steps.first()).toContainText('学科兴趣');
  });

  test('第一步显示学科选项', async ({ page }) => {
    await page.goto('/assessment.html');
    await waitForQuizReady(page);
    const options = page.locator('#quizCard .option-btn');
    expect(await options.count()).toBeGreaterThanOrEqual(10);
  });

  test('选择学科后选项高亮', async ({ page }) => {
    await page.goto('/assessment.html');
    await waitForQuizReady(page);
    await page.locator('#quizCard .option-btn').first().click();
    await expect(page.locator('#quizCard .option-btn').first()).toHaveClass(/selected/);
  });

  test('未完成必答题无法进入下一步', async ({ page }) => {
    await page.goto('/assessment.html');
    await waitForQuizReady(page);
    // 不回答直接点下一步
    await page.locator('#btnNext').click();
    await page.waitForTimeout(600);
    // 应仍在第一步
    await expect(page.locator('.progress-step.active')).toContainText('学科兴趣');
  });

  test('完成第一步后可进入下一步', async ({ page }) => {
    await page.goto('/assessment.html');
    await answerStep1(page);
    await page.locator('#btnNext').click();
    await page.waitForTimeout(800);
    // 检查不在第一步（进度条已更新）
    await expect(page.locator('.progress-step.active')).not.toContainText('学科兴趣');
  });

  test('完整完成测评并查看结果', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('/assessment.html');
    await completeFullQuiz(page);
    await expect(page.locator('#resultsSection')).toBeVisible({ timeout: 15000 });
    const cards = page.locator('#resultsList .result-card');
    expect(await cards.count()).toBeGreaterThanOrEqual(1);
  });

  test('结果卡片显示百分比', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('/assessment.html');
    await completeFullQuiz(page);
    await expect(page.locator('#resultsList .result-card').first()).toBeVisible({ timeout: 15000 });
    await expect(page.locator('#resultsList').first()).toContainText('%');
  });
});

test.describe('首页决策入口', () => {
  test('决策工具区块存在', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.decision-tools-section')).toBeVisible();
  });

  test('三张决策卡片', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.decision-card')).toHaveCount(3);
  });

  test('卡片链接正确', async ({ page }) => {
    await page.goto('/');
    const hrefs = await page.locator('.decision-card').evaluateAll(
      els => els.map(el => el.getAttribute('href'))
    );
    expect(hrefs).toContain('majors.html');
    expect(hrefs).toContain('compare.html');
    expect(hrefs).toContain('assessment.html');
  });

  test('测评卡片有高亮样式', async ({ page }) => {
    await page.goto('/');
    const featured = page.locator('.decision-card-featured');
    await expect(featured).toBeVisible();
    await expect(featured).toHaveAttribute('href', 'assessment.html');
  });

  test('移动端卡片宽度适配', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');
    const box = await page.locator('.decision-card').first().boundingBox();
    expect(box.width).toBeGreaterThan(280);
  });
});

test.describe('分享功能', () => {
  test('测评完成后结果页有操作按钮', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('/assessment.html');
    await completeFullQuiz(page);
    await expect(page.locator('#resultsFooterArea')).toBeVisible({ timeout: 15000 });
    // 页脚应该包含操作按钮（保存/分享/重新测评/浏览）
    const footerText = await page.locator('#resultsFooterArea').textContent();
    expect(footerText.length).toBeGreaterThan(5);
  });
});
