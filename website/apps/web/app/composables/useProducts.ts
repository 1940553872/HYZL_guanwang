import type { ContentItem } from '~/utils/types'

/** 全部产品（42 条，一次读取后在各页面复用，用于相关产品互链）。 */
export async function useProducts() {
  const res = await useContentList('product', {}, 'list:product:all')
  const bySlug = computed(() => {
    const m = new Map<string, ContentItem>()
    for (const p of res.data.value.items) m.set(p.slug, p)
    return m
  })
  const pick = (slugs: string[] = []) => slugs.map((s) => bySlug.value.get(s)).filter(Boolean) as ContentItem[]
  return { data: res.data, bySlug, pick }
}
