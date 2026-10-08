<script setup lang="ts">
// P-23 工业智能体应用
const { data } = await useContentList('product', { category: 'agent' })
usePageSeo({ title: '工业智能体应用', description: '面向生产作业、质量识别、预测性维护、智能仓储、安全应急、数字员工与生产系统的 7 类工业智能体应用。' })
const icons = ['factory', 'quality', 'maintenance', 'layers', 'safety', 'chat', 'cpu']
</script>

<template>
  <div>
    <PageHero title="工业智能体应用" eyebrow="Industrial AI Agents" lead="以工业增强模型（SLM）+ 专家系统增强既有工业系统，让智能体在生产、质量、设备、仓储与应急场景中承担可度量的工作。"
              :crumbs="[{ name: '产品与技术', to: '/products' }, { name: '工业智能体应用' }]" />
    <section class="section bg-paper">
      <div class="container-site grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <NuxtLink v-for="(a, i) in data.items" :key="a.slug" :to="`/products/agents/${a.slug}`" class="card card-hover group flex flex-col p-7">
          <UiIcon :name="icons[i] || 'cpu'" :size="30" class="text-brand-blue-700" />
          <p class="eyebrow mt-6 !text-[11px]">{{ a.data.en }}</p>
          <h2 class="mt-2 text-xl">{{ a.title }}</h2>
          <p class="mt-3 flex-1 text-[15px] leading-7 text-ink-600">{{ a.summary }}</p>
          <span class="mt-5 inline-flex items-center gap-1 text-sm font-semibold text-brand-blue-700">了解详情<UiIcon name="arrow" :size="16" /></span>
        </NuxtLink>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
