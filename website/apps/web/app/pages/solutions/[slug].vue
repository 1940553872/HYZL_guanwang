<script setup lang="ts">
// P-31 行业方案
const route = useRoute()
const slug = String(route.params.slug)
const [{ data: s }, { data: cases }] = await Promise.all([
  useContentItem('solution', slug),
  useContentList('case', { category: slug, archived: false }),
])
usePageSeo({ title: `${s.value.title}解决方案`, description: s.value.summary })
</script>

<template>
  <div>
    <PageHero :title="`${s.title}解决方案`" eyebrow="Industry Solution" :lead="s.summary" :crumbs="[{ name: '解决方案', to: '/solutions' }, { name: s.title }]">
      <UiButton :to="`/demo?product=other`" variant="ondark" arrow>咨询{{ s.title }}方案</UiButton>
    </PageHero>
    <section class="section bg-white">
      <div class="container-site grid gap-10 lg:grid-cols-[1.4fr_1fr]">
        <div>
          <SectionHeader eyebrow="Practice" title="项目实践与能力沉淀" class="!mb-6" />
          <p v-for="(p, i) in s.data.paras" :key="i" class="mb-4 leading-8 text-ink-600">{{ p }}</p>
        </div>
        <aside class="h-fit rounded-sm bg-brand-blue-50 p-6">
          <p class="font-semibold">覆盖场景</p>
          <ul class="mt-4 space-y-3">
            <li v-for="sc in s.data.scenarios" :key="sc" class="flex items-center gap-2"><UiIcon name="check" :size="18" class="text-brand-blue-700" />{{ sc }}</li>
          </ul>
        </aside>
      </div>
    </section>
    <RelatedProducts :slugs="s.data.products || []" title="推荐产品组合" />
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Cases" title="行业案例" />
        <div v-if="cases.items.length" class="grid gap-6 md:grid-cols-2"><CaseCard v-for="c in cases.items" :key="c.slug" :item="c" /></div>
        <EmptyState v-else title="该行业案例整理中" text="可先浏览其他行业案例，或预约工程师交流您的现场问题。">
          <UiButton to="/cases" variant="secondary">浏览全部案例</UiButton>
          <UiButton to="/demo">预约现场演示</UiButton>
        </EmptyState>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
