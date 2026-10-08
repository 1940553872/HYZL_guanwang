/** 页面 SEO：title / description / canonical / OG（K-04 §5）。 */
export function usePageSeo(opts: { title: string; description?: string; image?: string }) {
  const route = useRoute()
  const { public: pub } = useRuntimeConfig()
  const url = `${pub.siteUrl}${route.path}`
  const desc = opts.description?.slice(0, 120)
  useSeoMeta({
    title: opts.title,
    description: desc,
    ogTitle: `${opts.title}｜华云智联`,
    ogDescription: desc,
    ogType: 'website',
    ogUrl: url,
    ogImage: `${pub.siteUrl}${opts.image ?? '/media/brand/logo.png'}`,
  })
  useHead({ link: [{ rel: 'canonical', href: url }] })
}

/** 面包屑结构化数据。 */
export function useBreadcrumbLd(items: { name: string; to: string }[]) {
  const { public: pub } = useRuntimeConfig()
  useHead({
    script: [{
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: items.map((it, i) => ({ '@type': 'ListItem', position: i + 1, name: it.name, item: `${pub.siteUrl}${it.to}` })),
      }),
    }],
  })
}
