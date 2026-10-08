<script setup lang="ts">
// P-21 空间群弈™ SpatiGo™
const [{ data: p }, { data: subs }, { data: cases }] = await Promise.all([
  useContentItem('product', 'spatigo'),
  useContentList('product', { category: 'sub_product' }),
  useContentList('case', { archived: false }),
])
usePageSeo({ title: '空间群弈™ SpatiGo™ 工业监管—执行智能体集群', description: p.value.summary })
const principles = [
  { icon: 'layers', title: '监管—执行分层', text: '监管智能体负责感知、判断与规划，执行智能体负责动作；能力边界清晰，软硬约束明确。' },
  { icon: 'shield', title: '人在回路', text: '默认“人在环上”，关键动作由人确认；全过程审计追溯，异常时可核查动作与结果。' },
  { icon: 'cpu', title: 'LLM—WM 双模型', text: '语言模型理解意图与知识，世界模型约束物理与工艺边界，支撑可信执行。' },
]
</script>

<template>
  <div>
    <PageHero :title="p.data.name" eyebrow="Flagship" :code="p.data.code" :lead="p.summary" :crumbs="[{ name: '产品与技术', to: '/products' }, { name: 'SpatiGo™' }]">
      <UiButton to="/demo?product=spatigo" variant="ondark" arrow>预约现场演示</UiButton>
    </PageHero>

    <section class="section bg-white">
      <div class="container-site grid gap-10 lg:grid-cols-[1fr_1.2fr] lg:items-start">
        <div class="space-y-4">
          <p v-for="(t, i) in p.data.intro" :key="i" class="leading-8 text-ink-600">{{ t }}</p>
        </div>
        <div class="grid gap-4">
          <div v-for="x in principles" :key="x.title" class="card flex gap-4 p-6">
            <UiIcon :name="x.icon" :size="28" class="shrink-0 text-brand-blue-700" />
            <div><h3 class="text-lg">{{ x.title }}</h3><p class="mt-1 text-[15px] leading-7 text-ink-600">{{ x.text }}</p></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="4 Sub-products" title="四个子产品，回答四类现场问题" />
        <PainCards :items="subs.items" />
      </div>
    </section>

    <section v-if="cases.items.length" class="section bg-white">
      <div class="container-site">
        <SectionHeader eyebrow="Evidence" title="相关案例" />
        <div class="grid gap-6 md:grid-cols-2"><CaseCard v-for="c in cases.items" :key="c.slug" :item="c" /></div>
      </div>
    </section>
    <CtaBand title="预约 SpatiGo™ 现场演示" to="/demo?product=spatigo" />
  </div>
</template>
