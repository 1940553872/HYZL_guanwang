// 内容 → 前端路由（与后端 SearchService.urlOf 保持一致，design_document/K-02 §2.1）
export function productPath(p: { slug: string; category?: string }): string {
  switch (p.category) {
    case 'platform': return '/products'
    case 'flagship': return '/products/spatigo'
    case 'sub_product': return `/products/spatigo/${p.slug.replace('spatigo-', '')}`
    case 'model': return '/products/imllm'
    case 'agent': return `/products/agents/${p.slug}`
    case 'engine_group': return '/products/engines'
    case 'engine': return `/products/engines#${p.slug}`
    case 'software': return `/products/software/${p.slug}`
    case 'software_group': return '/products/software'
    case 'security': return '/products/security-integration'
    default: return '/products'
  }
}

export function formatDate(d?: string): string {
  if (!d) return ''
  const [y, m, day] = d.split('-')
  return `${y}年${Number(m)}月${Number(day)}日`
}

export const INDUSTRY_LABEL: Record<string, string> = {
  'mining-power': '矿山与电力',
  petrochemical: '石油化工',
  'aerospace-equipment': '航空航天与装备制造',
  'steel-metallurgy': '钢铁冶金',
  'tobacco-food': '烟草与食药制造',
  'water-municipal': '水务与市政',
  legacy: '历史案例',
}
