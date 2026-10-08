<script setup lang="ts">
import { formatDate } from '~/utils/links'
// P-80 新闻列表：分类筛选 + 分页（写入 URL）；2020 年及以前的动态标注“历史动态”
const route = useRoute()
const router = useRouter()
const { data } = await useContentList('news')
const PAGE = 9
const cat = computed(() => String(route.query.category || ''))
const page = computed(() => Math.max(1, Number(route.query.page) || 1))
const filtered = computed(() => data.value.items.filter((n) => !cat.value || n.category === cat.value))
const pages = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE)))
const rows = computed(() => filtered.value.slice((page.value - 1) * PAGE, page.value * PAGE))
const featured = computed(() => data.value.items.find((n) => n.featured))
function go(q: Record<string, string | number | undefined>) { router.push({ query: { ...route.query, ...q } }) }
usePageSeo({ title: '新闻中心', description: '华云智联公司动态与行业资讯。' })
</script>

<template>
  <div>
    <PageHero title="新闻中心" eyebrow="Newsroom" lead="公司动态与行业资讯。" :crumbs="[{ name: '新闻中心' }]" />
    <section class="section bg-paper">
      <div class="container-site">
        <NuxtLink v-if="featured && !cat && page === 1" :to="`/news/${featured.slug}`" class="card card-hover mb-10 grid gap-6 p-6 md:grid-cols-[1fr_2fr] md:p-8">
          <div class="flex aspect-[16/9] items-center justify-center rounded-sm bg-navy-900 md:aspect-auto">
            <img src="/media/brand/logo-white.webp" alt="" class="h-10 opacity-80">
          </div>
          <div>
            <p class="flex items-center gap-2 text-sm text-ink-500"><span class="rounded-xs bg-brand-orange-500 px-2 py-0.5 text-xs font-semibold text-navy-900">最新</span><time class="font-latin">{{ formatDate(featured.publishedAt) }}</time></p>
            <h2 class="mt-3 text-2xl leading-9">{{ featured.title }}</h2>
            <p class="mt-3 leading-7 text-ink-600">{{ featured.summary }}</p>
          </div>
        </NuxtLink>
        <div role="group" aria-label="新闻分类" class="mb-8 flex gap-2">
          <button v-for="[k, l] in [['', '全部'], ['company', '公司动态'], ['industry', '行业资讯']]" :key="k" type="button" :aria-pressed="cat === k"
                  :class="['h-9 rounded-sm border px-4 text-sm', cat === k ? 'border-brand-blue-700 bg-brand-blue-700 text-white' : 'border-line-300 bg-white']"
                  @click="go({ category: k || undefined, page: undefined })">{{ l }}</button>
        </div>
        <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3"><NewsCard v-for="n in rows" :key="n.slug" :item="n" /></div>
        <nav v-if="pages > 1" aria-label="分页" class="mt-10 flex justify-center gap-2">
          <NuxtLink v-for="p in pages" :key="p" :to="{ query: { ...route.query, page: p > 1 ? p : undefined } }" :aria-current="p === page ? 'page' : undefined"
                    :class="['font-latin inline-flex size-10 items-center justify-center rounded-sm border text-sm', p === page ? 'border-brand-blue-700 bg-brand-blue-700 text-white' : 'border-line-300 bg-white hover:border-brand-blue-700']">{{ p }}</NuxtLink>
        </nav>
      </div>
    </section>
  </div>
</template>
