<script setup lang="ts">
// P-90 搜索结果：按类型筛选，关键词高亮
const route = useRoute()
const router = useRouter()
const q = computed(() => String(route.query.q || '').trim().slice(0, 50))
const type = computed(() => String(route.query.type || ''))
const staticDemo = !!useRuntimeConfig().public.staticDemo
const input = ref(q.value)
watch(q, (v) => { input.value = v })
const { data, pending } = await useFetch<{ total: number; hits: { type: string; slug: string; title: string; snippet: string; url: string; code?: string }[] }>('/api/v1/search', {
  query: computed(() => ({ q: q.value, type: type.value || undefined, size: 50 })),
  immediate: !!q.value && !staticDemo,
  watch: staticDemo ? false : undefined,
  default: () => ({ total: 0, hits: [] }),
})
const TYPE_LABEL: Record<string, string> = { product: '产品', solution: '解决方案', case: '案例', news: '新闻', standard: '标准', patent: '专利', copyright: '软著', lab: '实验室' }
function submit() { if (input.value.trim()) router.push({ query: { q: input.value.trim() } }) }
function esc(s: string) { return s.replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]!) }
function hl(s: string) {
  const safe = esc(s || '')
  if (!q.value) return safe
  const re = new RegExp(esc(q.value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
  return safe.replace(re, (m) => `<mark class="bg-brand-orange-50 text-ink-900">${m}</mark>`)
}
useSeoMeta({ title: q.value ? `“${q.value}”的搜索结果` : '站内搜索', robots: 'noindex' })
</script>

<template>
  <div>
    <PageHero title="站内搜索" eyebrow="Search" :crumbs="[{ name: '搜索' }]">
      <form role="search" class="flex w-full max-w-2xl gap-2" @submit.prevent="submit">
        <label for="search-q" class="sr-only">搜索关键词</label>
        <input id="search-q" v-model="input" type="search" maxlength="50" placeholder="输入产品代号或关键词" class="h-12 flex-1 rounded-sm border-0 bg-white px-4 text-ink-900 outline-none">
        <UiButton type="submit" variant="ondark" size="lg">搜索</UiButton>
      </form>
    </PageHero>
    <section class="section bg-paper">
      <div class="container-site max-w-4xl">
        <EmptyState v-if="staticDemo" title="演示版暂不支持站内搜索" text="搜索需要内容服务在线运行。可以通过顶部导航浏览产品、方案与案例。">
          <UiButton to="/products" variant="secondary">浏览产品</UiButton>
          <UiButton to="/solutions" variant="secondary">解决方案</UiButton>
        </EmptyState>
        <template v-else>
        <p v-if="q" class="mb-6 text-ink-600" aria-live="polite">{{ pending ? '搜索中…' : `“${q}” 共找到 ${data.total} 条结果` }}</p>
        <ul v-if="data.hits.length" class="space-y-3">
          <li v-for="r in data.hits" :key="r.type + r.slug">
            <NuxtLink :to="r.url" class="card card-hover block p-5">
              <span class="flex items-center gap-2 text-xs"><span class="tag">{{ TYPE_LABEL[r.type] || r.type }}</span><span v-if="r.code" class="code text-brand-blue-500">{{ r.code }}</span></span>
              <!-- eslint-disable-next-line vue/no-v-html -->
              <span class="mt-2 block text-lg font-semibold" v-html="hl(r.title)" />
              <!-- eslint-disable-next-line vue/no-v-html -->
              <span class="mt-1 line-clamp-2 block text-sm leading-6 text-ink-600" v-html="hl(r.snippet)" />
            </NuxtLink>
          </li>
        </ul>
        <EmptyState v-else-if="q && !pending" title="没有找到相关内容" text="试试产品代号（如 iMES、SpatiGo）或更通用的关键词，也可以直接联系我们。">
          <UiButton to="/products" variant="secondary">浏览产品</UiButton>
          <UiButton to="/demo">预约现场演示</UiButton>
        </EmptyState>
        </template>
      </div>
    </section>
  </div>
</template>
