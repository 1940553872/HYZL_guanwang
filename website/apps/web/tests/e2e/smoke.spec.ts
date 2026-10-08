import { expect, test } from '@playwright/test'

// 主要页面可访问、有唯一 H1、移动端无横向滚动（K-06 §3 冒烟用例）
const ROUTES = [
  '/', '/products', '/products/spatigo', '/products/spatigo/quality', '/products/imllm', '/products/agents',
  '/products/agents/maintenance-agent', '/products/engines', '/products/software', '/products/software/imes',
  '/products/security-integration', '/solutions', '/solutions/petrochemical', '/cases', '/cases/embodied-energy-safety',
  '/research', '/research/labs', '/support', '/news', '/news/2020/company-01', '/about', '/about/honors',
  '/about/partners', '/about/contact', '/about/careers', '/demo', '/legal/privacy',
]

for (const path of ROUTES) {
  test(`page ${path} renders`, async ({ page }) => {
    const errors: string[] = []
    page.on('pageerror', (e) => errors.push(String(e)))
    const res = await page.goto(path)
    expect(res?.status()).toBe(200)
    await expect(page.locator('h1')).toHaveCount(1)
    await expect(page).toHaveTitle(/华云智联/)
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)
    expect(overflow).toBeLessThanOrEqual(0)
    expect(errors).toEqual([])
  })
}

test('unknown page returns 404 with recovery links', async ({ page }) => {
  const res = await page.goto('/this-page-does-not-exist')
  expect(res?.status()).toBe(404)
  await expect(page.getByRole('heading', { level: 1 })).toContainText('页面不存在')
  await expect(page.getByRole('button', { name: '返回首页' })).toBeVisible()
})

test('legacy .html URLs redirect with 301', async ({ request }) => {
  const res = await request.get('/product.html', { maxRedirects: 0 })
  expect(res.status()).toBe(301)
  expect(res.headers().location).toBe('/products')
})

test('sitemap and robots are served', async ({ request }) => {
  const sm = await request.get('/sitemap.xml')
  expect(sm.ok()).toBeTruthy()
  expect(await sm.text()).toContain('/products/software/imes')
  expect(await (await request.get('/robots.txt')).text()).toContain('Sitemap:')
})
