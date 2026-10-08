// 与 K-05 内容接口一致的类型
export interface Media { src: string; w?: number; h?: number; thumb?: string; alt?: string }

export type Block =
  | { t: 'p'; text: string }
  | { t: 'h'; text: string }
  | { t: 'cap'; label: string; text: string }
  | ({ t: 'img' } & Media)

export interface ContentItem<T = Record<string, any>> {
  type: string
  slug: string
  title: string
  summary?: string
  category?: string
  sort: number
  featured: boolean
  publishedAt?: string
  expiresAt?: string
  authorized: boolean
  archived: boolean
  status?: 'valid' | 'expiring'
  data: T
}

export interface ListResponse<T = Record<string, any>> { total: number; items: ContentItem<T>[] }
