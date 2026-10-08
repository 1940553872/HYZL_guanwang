<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
import { productPath } from '~/utils/links'
// P-20 平台总览：盘古华云智能工厂平台 7+10+2+N（iMoM 3.2）
const [{ data: imom }, { data: home }, products] = await Promise.all([
  useContentItem('product', 'imom'),
  useFetch<ContentItem>('/api/v1/content/page/home', { key: 'page:home' }),
  useProducts(),
])
const all = computed(() => products.data.value.items)
const byCat = (c: string) => all.value.filter((p) => p.category === c)
const groups = computed(() => [
  { id: 'spatigo', title: '旗舰产品 · 空间群弈™ SpatiGo™', lead: '工业监管—执行智能体集群，四个子产品。', items: [...byCat('flagship'), ...byCat('sub_product')], to: '/products/spatigo' },
  { id: 'imllm', title: '工业增强大模型 iMLLM', lead: '多模态应用大模型、LLM 交互与智能体群控。', items: byCat('model'), to: '/products/imllm' },
  { id: 'agents', title: '工业智能体应用', lead: '面向生产、质量、运维、仓储、应急等场景的 7 类智能体。', items: byCat('agent'), to: '/products/agents' },
  { id: 'engines', title: '智能引擎群', lead: '7 组工业智能引擎构成数据与算法底座。', items: byCat('engine'), to: '/products/engines' },
  { id: 'software', title: '工业软件', lead: '工业标准软件与工业高级软件。', items: byCat('software'), to: '/products/software' },
])
const brain = computed(() => imom.value.data.brain)
usePageSeo({ title: '产品与技术 · 盘古华云智能工厂平台', description: imom.value.summary })
</script>

<template>
  <div>
    <PageHero :title="imom.title" eyebrow="Pangoo Cloud · 7+10+2+N" :code="imom.data.code" :lead="imom.summary"
              :crumbs="[{ name: '产品与技术', to: '/products' }]">
      <UiButton to="/demo?product=imom" variant="ondark" arrow>预约现场演示</UiButton>
      <UiButton to="#architecture" variant="ghost">查看平台架构</UiButton>
    </PageHero>

    <section class="bg-white py-12">
      <div class="container-site grid gap-4 md:grid-cols-2">
        <div v-for="f in imom.data.facts" :key="f" class="flex gap-3 rounded-sm bg-brand-blue-50 p-5">
          <UiIcon name="check" class="shrink-0 text-brand-blue-700" /><p class="text-[15px] leading-7 text-ink-900">{{ f }}</p>
        </div>
      </div>
    </section>

    <section id="architecture" class="section on-dark bg-navy-900 text-on-dark">
      <div class="container-site">
        <SectionHeader eyebrow="Architecture" title="7+10+2+N 分层架构" dark lead="7 组智能引擎 + 10 组工业软件 + 2 类约束 + N 个智能体，底层为跨媒体数据底座。" />
        <ArchDiagram :layers="(home?.data as any)?.arch || []" />
      </div>
    </section>

    <section class="section bg-paper">
      <div class="container-site space-y-16">
        <div v-for="g in groups" :id="g.id" :key="g.id">
          <div class="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div>
              <h2 class="text-2xl">{{ g.title }}</h2>
              <p class="mt-2 text-ink-600">{{ g.lead }}</p>
            </div>
            <UiButton :to="g.to" variant="text" arrow>进入</UiButton>
          </div>
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <ProductCard v-for="p in g.items.slice(0, 8)" :key="p.slug" :item="p" :compact="g.items.length > 4" />
          </div>
        </div>
        <NuxtLink to="/products/security-integration" class="card card-hover flex items-center gap-5 p-6">
          <UiIcon name="shield" :size="32" class="shrink-0 text-brand-blue-700" />
          <span class="flex-1"><span class="block text-lg font-semibold">安全与集成</span><span class="text-ink-600">工业协议、数据安全和数据接口；等保 2.0 二级、TLS 1.3 + 国密 SM4。</span></span>
          <UiIcon name="arrow" class="text-brand-blue-700" />
        </NuxtLink>
      </div>
    </section>

    <section v-if="brain" class="section bg-white">
      <div class="container-site">
        <PanelSection :panel="brain" title="工业生产智慧大脑" />
      </div>
    </section>

    <CtaBand />
  </div>
</template>
