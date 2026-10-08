<script setup lang="ts">
// P-22 工业增强大模型 iMLLM：三个面板，页内锚点
const { data: p } = await useContentItem('product', 'imllm')
const sections = computed(() => (p.value.data.sections || []) as any[])
usePageSeo({ title: '工业增强大模型 iMLLM', description: p.value.summary })
</script>

<template>
  <div>
    <PageHero :title="`工业增强大模型 ${p.data.code}`" eyebrow="Industrial Multimodal LLM" :lead="p.summary"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: 'iMLLM' }]">
      <UiButton to="/demo?product=imllm" variant="ondark" arrow>预约现场演示</UiButton>
    </PageHero>
    <AnchorNav :items="sections.map((s) => ({ id: s.id, label: s.title }))" />
    <section v-for="(s, i) in sections" :id="s.id" :key="s.id" data-anchor :class="['section scroll-mt-28', i % 2 ? 'bg-paper' : 'bg-white']">
      <div class="container-site"><PanelSection :panel="s" :title="s.title" /></div>
    </section>
    <RelatedProducts :slugs="['spatigo', 'spatigo-safety', 'engines', 'security-integration']" />
    <CtaBand :to="`/demo?product=imllm`" />
  </div>
</template>
