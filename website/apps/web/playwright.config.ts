import { defineConfig, devices } from '@playwright/test'

// E2E 冒烟测试：需先启动站点（../../start.sh 或 npm run start + API），默认 http://localhost:3000
export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  retries: 0,
  reporter: [['list']],
  use: { baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } },
    { name: 'mobile', use: { ...devices['Pixel 7'] } },
  ],
})
