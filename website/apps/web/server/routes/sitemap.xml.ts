// 动态 sitemap：静态页面 + 产品 / 方案 / 案例 / 新闻详情（K-04 §5）
import { productPath } from '../../app/utils/links'

interface Item { slug: string; category?: string; publishedAt?: string }

export default defineEventHandler(async (event) => {
  const { apiBase, public: pub } = useRuntimeConfig(event)
  const list = async (type: string) => {
    try {
      const r = await $fetch<{ items: Item[] }>(`${apiBase}/api/v1/content/${type}`)
      return r.items
    } catch {
      return []
    }
  }
  const statics = ['/', '/products', '/products/spatigo', '/products/imllm', '/products/agents', '/products/engines',
    '/products/software', '/products/security-integration', '/solutions', '/cases', '/research', '/research/labs',
    '/support', '/news', '/about', '/about/honors', '/about/partners', '/about/contact', '/about/careers', '/demo',
    '/legal/privacy']
  const [products, solutions, cases, news] = await Promise.all([list('product'), list('solution'), list('case'), list('news')])
  const urls = new Set<string>(statics)
  products.forEach((p) => {
    const path = productPath(p)
    if (!path.includes('#')) urls.add(path)
  })
  solutions.forEach((s) => urls.add(`/solutions/${s.slug}`))
  cases.forEach((c) => urls.add(`/cases/${c.slug}`))
  news.forEach((n) => urls.add(`/news/${n.slug}`))
  const body = [...urls].map((u) => `  <url><loc>${pub.siteUrl}${u}</loc></url>`).join('\n')
  setHeader(event, 'content-type', 'application/xml; charset=utf-8')
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`
})
