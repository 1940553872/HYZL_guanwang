<script setup lang="ts">
// P-23 智能体详情
const route = useRoute()
const slug = String(route.params.slug)
const [{ data: a }, { data: list }] = await Promise.all([
  useContentItem('product', slug),
  useContentList('product', { category: 'agent' }),
])
if (a.value.category !== 'agent') throw createError({ statusCode: 404, statusMessage: '页面不存在', fatal: true })
const others = computed(() => list.value.items.filter((x) => x.slug !== slug).slice(0, 3))
usePageSeo({ title: `${a.value.title} · 工业智能体应用`, description: a.value.summary })
</script>

<template>
  <div>
    <PageHero :title="a.title" :eyebrow="a.data.en" :lead="a.summary"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: '工业智能体应用', to: '/products/agents' }, { name: a.title }]">
      <UiButton :to="`/demo?product=agents`" variant="ondark" arrow>预约现场演示</UiButton>
    </PageHero>
    <section class="section bg-white">
      <div class="container-site"><PanelSection :panel="a.data" /></div>
    </section>
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="More Agents" title="其他智能体应用" />
        <div class="grid gap-4 md:grid-cols-3"><ProductCard v-for="o in others" :key="o.slug" :item="o" /></div>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
