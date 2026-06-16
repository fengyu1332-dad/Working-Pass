// ============================================================
// 专业星图 - E2E 测试：登录和注册
// ============================================================
import { test, expect } from '@playwright/test';

test.describe('登录页', () => {
  test('页面能正常加载', async ({ page }) => {
    const response = await page.goto('/login.html');
    expect(response.status()).toBeLessThan(400);

    await expect(page.locator('.logo-title')).toHaveText('专业星图');
    await expect(page.locator('#loginForm')).toBeVisible();
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('#loginBtn')).toBeVisible();
  });

  test('返回首页链接有效', async ({ page }) => {
    await page.goto('/login.html');

    const backLink = page.locator('.back-link');
    await expect(backLink).toBeVisible();
    await backLink.click();
    await page.waitForURL(/index\.html/);
  });

  test('空表单提交显示错误', async ({ page }) => {
    await page.goto('/login.html');

    // 移除浏览器原生 required 验证，测试 JS 层验证
    await page.evaluate(() => {
      document.getElementById('email').removeAttribute('required');
      document.getElementById('password').removeAttribute('required');
    });

    await page.locator('#loginBtn').click();

    const errorMsg = page.locator('#errorMessage');
    await expect(errorMsg).toHaveClass(/show/);
  });

  test('导航到注册页', async ({ page }) => {
    await page.goto('/login.html');

    const registerLink = page.locator('a[href="register.html"]');
    await expect(registerLink).toBeVisible();
    await registerLink.click();
    await page.waitForURL(/register\.html/);
  });

  test('注册链接指向注册页', async ({ page }) => {
    await page.goto('/login.html');

    const registerLink = page.locator('a[href="register.html"]');
    await expect(registerLink).toBeVisible();
    await expect(registerLink).toHaveText('去注册');
  });
});

test.describe('注册页', () => {
  test('页面能正常加载', async ({ page }) => {
    const response = await page.goto('/register.html');
    expect(response.status()).toBeLessThan(400);

    await expect(page.locator('.logo-title')).toHaveText('专业星图');
    await expect(page.locator('#registerForm')).toBeVisible();
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#phone')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('#confirmPassword')).toBeVisible();
    await expect(page.locator('#registerBtn')).toBeVisible();
  });

  test('空表单提交显示错误', async ({ page }) => {
    await page.goto('/register.html');

    // 移除浏览器原生 required 验证，测试 JS 层验证
    await page.evaluate(() => {
      document.getElementById('email').removeAttribute('required');
      document.getElementById('password').removeAttribute('required');
      document.getElementById('confirmPassword').removeAttribute('required');
      document.getElementById('terms').removeAttribute('required');
    });

    await page.locator('#registerBtn').click();

    const errorMsg = page.locator('#errorMessage');
    await expect(errorMsg).toHaveClass(/show/);
  });

  test('密码不匹配显示错误', async ({ page }) => {
    await page.goto('/register.html');

    // 移除浏览器原生 required/minlength 验证，测试 JS 层
    await page.evaluate(() => {
      document.getElementById('password').removeAttribute('required');
      document.getElementById('password').removeAttribute('minlength');
      document.getElementById('confirmPassword').removeAttribute('required');
    });

    await page.locator('#email').fill('test@example.com');
    await page.locator('#password').fill('pass123');
    await page.locator('#confirmPassword').fill('pass456');
    await page.locator('#terms').check();
    await page.locator('#registerBtn').click();

    const errorMsg = page.locator('#errorMessage');
    await expect(errorMsg).toHaveClass(/show/);
  });

  test('无效邮箱显示错误', async ({ page }) => {
    await page.goto('/register.html');

    await page.evaluate(() => {
      const el = document.getElementById('email');
      el.removeAttribute('required');
      el.type = 'text';
      document.getElementById('password').removeAttribute('required');
      document.getElementById('confirmPassword').removeAttribute('required');
      document.getElementById('terms').removeAttribute('required');
    });

    await page.locator('#email').fill('not-an-email');
    await page.locator('#password').fill('pass123');
    await page.locator('#confirmPassword').fill('pass123');
    await page.locator('#terms').check();
    await page.locator('#registerBtn').click();

    const errorMsg = page.locator('#errorMessage');
    await expect(errorMsg).toHaveClass(/show/);
  });

  test('导航到登录页', async ({ page }) => {
    await page.goto('/register.html');

    const loginLink = page.locator('a[href="login.html"]');
    await expect(loginLink).toBeVisible();
    await loginLink.click();
    await page.waitForURL(/login\.html/);
  });
});
