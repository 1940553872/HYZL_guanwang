<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
// P-60 服务支持：7×24 服务、实施方法、服务内容；资料下载（P-61）待白皮书 / 手册就绪后上线
const { data: page } = await useFetch<ContentItem>('/api/v1/content/page/support', { key: 'page:support' })
const s = computed(() => page.value?.data as any)
usePageSeo({ title: '服务支持', description: '7×24 小时服务中心，分析咨询、方案论证、项目实施、交付验证与运维服务的全流程支持。' })
</script>

<template>
  <div v-if="s">
    <PageHero title="服务支持" eyebrow="Service & Support" :lead="s.intro[0]" :crumbs="[{ name: '服务支持' }]">
      <UiButton :href="`tel:${s.hotline}`" variant="ondark"><UiIcon name="phone" :size="18" />7×24 热线 {{ s.hotline }}</UiButton>
      <UiButton to="/about/contact" variant="ghost">联系我们</UiButton>
    </PageHero>
    <section class="section bg-white">
      <div class="container-site">
        <SectionHeader eyebrow="Methodology" title="实施方法" lead="从现场调研到持续运维，每一步都有明确的交付物与验收口径。" />
        <ol class="grid gap-4 md:grid-cols-5">
          <li v-for="(st, i) in s.steps" :key="st.title" class="card relative p-6">
            <span class="stat-num text-3xl text-brand-orange-600">0{{ i + 1 }}</span>
            <h3 class="mt-3 text-lg">{{ st.title }}</h3>
            <p class="font-latin text-xs text-ink-500">{{ st.en }}</p>
            <p class="mt-3 text-sm leading-6 text-ink-600">{{ st.text }}</p>
          </li>
        </ol>
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Services" title="服务内容" />
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="sv in s.services" :key="sv.title" class="card p-6">
            <h3 class="text-lg">{{ sv.title }}</h3>
            <p class="font-latin text-xs text-ink-500">{{ sv.en }}</p>
            <ul class="mt-4 space-y-2 text-[15px] text-ink-600">
              <li v-for="it in sv.items" :key="it" class="flex items-center gap-2"><span class="size-1.5 bg-brand-orange-500" />{{ it }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
    <section class="section bg-white">
      <div class="container-site">
        <SectionHeader eyebrow="Downloads" title="资料下载" />
        <EmptyState title="产品手册与白皮书整理中" text="如需产品资料，请留下联系方式，工程师将发送对应资料并为您讲解。">
          <UiButton to="/demo?product=other">索取产品资料</UiButton>
        </EmptyState>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
