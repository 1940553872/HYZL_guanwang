import { existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { FOOTER_COLUMNS, NAV } from '~/utils/nav'

const pages = fileURLToPath(new URL('../../app/pages', import.meta.url))

/** 判断路由是否有对应页面文件（支持 [param] 动态段）。 */
function routeExists(path: string): boolean {
  const clean = path.split(/[?#]/)[0]!.replace(/^\//, '')
  if (!clean) return existsSync(`${pages}/index.vue`)
  const segs = clean.split('/')
  const dir = segs.slice(0, -1).join('/')
  const last = segs[segs.length - 1]
  const candidates = [`${pages}/${clean}.vue`, `${pages}/${clean}/index.vue`, `${pages}/${dir}/[slug].vue`, `${pages}/${dir}/[sub].vue`]
  return candidates.some((c) => existsSync(c)) || (last !== undefined && existsSync(`${pages}/${dir}/[...slug].vue`))
}

describe('navigation', () => {
  it('has the 7 top-level items in order (K-02 §2.1)', () => {
    expect(NAV.map((n) => n.label)).toEqual(['产品与技术', '解决方案', '客户案例', '标准与研究', '服务支持', '新闻中心', '关于我们'])
  })
  it('points every link at an existing page', () => {
    const links = [
      ...NAV.flatMap((n) => [n.to, ...(n.columns ?? []).flatMap((c) => c.links.map((l) => l.to)), ...(n.promo ? [n.promo.to] : [])]),
      ...FOOTER_COLUMNS.flatMap((c) => c.links.map((l) => l.to)),
    ]
    const missing = links.filter((l) => !routeExists(l))
    expect(missing).toEqual([])
  })
})
