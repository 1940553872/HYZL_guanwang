import type { ContentItem, ListResponse } from '~/utils/types'

/** 读取内容列表（经 Nitro 代理到 K-05 内容接口）。 */
export function useContentList<T = Record<string, any>>(
  type: string,
  query: Record<string, string | number | boolean | undefined> = {},
  key?: string,
) {
  return useFetch<ListResponse<T>>(`/api/v1/content/${type}`, {
    key: key ?? `list:${type}:${JSON.stringify(query)}`,
    query,
    default: () => ({ total: 0, items: [] }),
  })
}

/** 读取单条内容；不存在时显示 404 页面。 */
export async function useContentItem<T = Record<string, any>>(type: string, slug: string) {
  const res = await useFetch<ContentItem<T>>(`/api/v1/content/${type}/${slug}`, { key: `item:${type}:${slug}` })
  if (res.error.value || !res.data.value) {
    throw createError({ statusCode: res.error.value?.statusCode === 404 ? 404 : 500, statusMessage: '页面不存在', fatal: true })
  }
  return res as typeof res & { data: Ref<ContentItem<T>> }
}

export interface CommonInfo {
  company: string
  companyEn: string
  phone: string
  email: string
  postcode: string
  address: string
  icp: string
  website: string
  logo: { color: string; white: string; png: string }
  wechat: { src: string; w?: number; h?: number }
  foundedYear: number
}

/** 全站公共信息（联系方式、备案号、Logo）。 */
export function useCommon() {
  return useFetch<ContentItem<CommonInfo>>('/api/v1/content/page/common', { key: 'page:common' })
}
