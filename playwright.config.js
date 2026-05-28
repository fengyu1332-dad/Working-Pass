import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3456',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  webServer: {
    command: 'npm run build && npx vite preview --port 3456',
    url: 'http://localhost:3456',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },

  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 },
        launchOptions: {
          executablePath: 'C:/Users/fengy/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe',
        },
      },
    },
  ],
});
