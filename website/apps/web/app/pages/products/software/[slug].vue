<script setup lang="ts">
// P-25 软件详情
const route = useRoute()
const slug = String(route.params.slug)
const [{ data: s }, { data: list }, { data: solutions }] = await Promise.all([
  useContentItem('product', slug),
  useContentList('product', { category: 'software' }),
  useContentList('solution'),
])
if (s.value.category !== 'software') throw createError({ statusCode: 404, statusMessage: '页面不存在', fatal: true })
const siblings = computed(() => list.value.items.filter((x) => x.slug !== slug && x.data.group === s.value.data.group).slice(0, 4))
const usedIn = computed(() => solutions.value.items.filter((x) => (x.data.products || []).includes(slug)))
const groupName = computed(() => (s.value.data.group === 'standard' ? '工业标准软件' : '工业高级软件'))
usePageSeo({ title: `${s.value.data.fullName || s.value.title} · 工业软件`, description: s.value.summary })
</script>

<template>
  <div>
    <PageHero :title="s.data.name || s.title" :eyebrow="groupName" :code="s.data.code" :lead="s.summary"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: '工业软件', to: '/products/software' }, { name: s.data.code || s.title }]">
      <UiButton :to="`/demo?product=software`" variant="ondark" arrow>预约现场演示</UiButton>
    </PageHero>
    <section class="section bg-white">
      <div class="container-site grid gap-10 lg:grid-cols-[1fr_300px]">
        <ContentBlocks :blocks="s.data.blocks || []" />
        <aside class="h-fit space-y-6 lg:sticky lg:top-24">
          <div v-if="usedIn.length" class="rounded-sm bg-brand-blue-50 p-5">
            <p class="font-semibold">应用行业</p>
            <ul class="mt-3 space-y-2"><li v-for="u in usedIn" :key="u.slug"><NuxtLink :to="`/solutions/${u.slug}`" class="link text-sm">{{ u.title }}</NuxtLink></li></ul>
          </div>
          <div class="card p-5">
            <p class="font-semibold">需要演示或方案？</p>
            <p class="mt-2 text-sm leading-6 text-ink-600">工程师 1 个工作日内联系您。</p>
            <UiButton to="/demo?product=software" class="mt-4 w-full">预约现场演示</UiButton>
          </div>
        </aside>
      </div>
    </section>
    <section v-if="siblings.length" class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Related" :title="`更多${groupName}`" />
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"><ProductCard v-for="o in siblings" :key="o.slug" :item="o" /></div>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
