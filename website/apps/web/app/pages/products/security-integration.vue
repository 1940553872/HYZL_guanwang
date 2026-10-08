<script setup lang="ts">
// P-26 安全与集成
const { data: p } = await useContentItem('product', 'security-integration')
const sections = computed(() => (p.value.data.sections || []) as any[])
usePageSeo({ title: '安全与集成', description: '工业协议、数据安全和数据接口；满足等保2.0二级安全规范要求的平台安全与高可靠保障体系。' })
</script>

<template>
  <div>
    <PageHero title="安全与集成" eyebrow="Security & Integration" lead="全协议接入、全链路加密、全方位接口：满足等保 2.0 二级安全规范要求，传输采用 TLS 1.3 + 国密 SM4。"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: '安全与集成' }]" />
    <AnchorNav :items="sections.map((s) => ({ id: s.id, label: s.title }))" />
    <section v-for="(s, i) in sections" :id="s.id" :key="s.id" data-anchor :class="['section scroll-mt-28', i % 2 ? 'bg-paper' : 'bg-white']">
      <div class="container-site"><PanelSection :panel="s" :title="s.title" /></div>
    </section>
    <RelatedProducts :slugs="['imllm', 'engines', 'imom']" />
    <CtaBand />
  </div>
</template>
