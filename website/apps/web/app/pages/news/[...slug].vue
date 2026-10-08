<script setup lang="ts">
import { formatDate } from '~/utils/links'
// P-81 新闻详情（URL：/news/<yyyy>/<slug>）
const route = useRoute()
const slug = ([] as string[]).concat(route.params.slug as any).join('/')
const [{ data: n }, { data: list }] = await Promise.all([useContentItem('news', slug), useContentList('news')])
const idx = computed(() => list.value.items.findIndex((x) => x.slug === slug))
const prev = computed(() => list.value.items[idx.value - 1])
const next = computed(() => list.value.items[idx.value + 1])
usePageSeo({ title: n.value.title, description: n.value.summary })
useHead({
  script: [{
    type: 'application/ld+json',
    innerHTML: JSON.stringify({ '@context': 'https://schema.org', '@type': 'NewsArticle', headline: n.value.title, datePublished: n.value.publishedAt, publisher: { '@type': 'Organization', name: '西安华云智联信息科技有限公司' } }),
  }],
})
</script>

<template>
  <div>
    <PageHero :title="n.title" :eyebrow="n.category === 'industry' ? '行业资讯' : '公司动态'" :crumbs="[{ name: '新闻中心', to: '/news' }, { name: '正文' }]" />
    <article class="section bg-white">
      <div class="container-site max-w-3xl">
        <p class="flex flex-wrap items-center gap-3 border-b border-line-200 pb-6 text-sm text-ink-500">
          <time :datetime="n.publishedAt" class="font-latin">{{ formatDate(n.publishedAt) }}</time>
          <span v-if="n.data.source">来源：{{ n.data.source }}</span>
          <span v-if="n.archived" class="tag">历史动态</span>
        </p>
        <div class="mt-8"><ContentBlocks :blocks="n.data.blocks || []" /></div>
        <nav aria-label="上一篇与下一篇" class="mt-14 grid gap-4 border-t border-line-200 pt-8 sm:grid-cols-2">
          <NuxtLink v-if="prev" :to="`/news/${prev.slug}`" class="card card-hover p-4 text-sm"><span class="text-ink-500">较新</span><span class="mt-1 line-clamp-2 block font-medium">{{ prev.title }}</span></NuxtLink>
          <span v-else />
          <NuxtLink v-if="next" :to="`/news/${next.slug}`" class="card card-hover p-4 text-right text-sm"><span class="text-ink-500">较早</span><span class="mt-1 line-clamp-2 block font-medium">{{ next.title }}</span></NuxtLink>
        </nav>
      </div>
    </article>
  </div>
</template>
