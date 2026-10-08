import { expect, test } from '@playwright/test'

// 关键任务流程（K-02 §3）：预约演示、搜索、核实资质、导航
test('T3 book a demo: validation then success', async ({ page }) => {
  await page.goto('/demo?product=spatigo-safety')
  await expect(page.getByLabel('关注产品 / 场景')).toHaveValue('spatigo-safety')
  await page.getByRole('button', { name: '提交预约' }).click()
  await expect(page.getByText('请填写姓名')).toBeVisible()
  await expect(page.getByText('手机号或邮箱至少填写一项')).toBeVisible()
  await expect(page.getByLabel('姓名 *')).toBeFocused()

  await page.getByLabel('姓名 *').fill('E2E 测试')
  await page.getByLabel('公司名称 *').fill('华云智联自动化测试')
  await page.getByLabel('邮箱').fill(`e2e-${test.info().project.name}@example.com`)
  await page.getByRole('checkbox').check()
  await page.getByRole('button', { name: '提交预约' }).click()
  await expect(page.getByRole('heading', { name: '提交成功' })).toBeVisible()
})

test('T1 search by product code ranks the exact product first', async ({ page }) => {
  await page.goto('/search?q=iMES')
  const first = page.locator('main ul li').first()
  await expect(first).toContainText('iMES 生产执行系统')
  await first.click()
  await expect(page).toHaveURL(/\/products\/software\/imes$/)
})

test('T4 verify certificates: status badge and lightbox', async ({ page }) => {
  await page.goto('/about/honors')
  await expect(page.getByText('高新技术企业证书')).toBeVisible()
  await page.getByRole('button', { name: /放大查看：ISO 9001/ }).click()
  await expect(page.getByRole('dialog')).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(page.getByRole('dialog')).toBeHidden()
})

test('standards table filters by scope', async ({ page }) => {
  await page.goto('/research')
  await page.getByRole('button', { name: '国际', exact: true }).click()
  await expect(page.getByText('共 12 条')).toBeVisible()
  await page.getByRole('button', { name: '2026 在编' }).click()
  await expect(page.getByText('IEEE P3701.1')).toBeVisible()
})

test('desktop mega menu and mobile drawer navigate to SpatiGo sub-product', async ({ page, isMobile }) => {
  await page.goto('/')
  if (isMobile) {
    await page.getByRole('button', { name: '打开菜单' }).click()
    await page.getByRole('dialog').getByRole('button', { name: '产品与技术' }).click()
    await page.getByRole('dialog').getByRole('link', { name: '安全之弈' }).click()
  } else {
    await page.getByRole('navigation', { name: '主导航' }).getByRole('button', { name: '产品与技术' }).click()
    await page.getByRole('link', { name: /安全之弈/ }).first().click()
  }
  await expect(page).toHaveURL(/\/products\/spatigo\/safety$/)
  await expect(page.locator('h1')).toContainText('安全之弈')
})
