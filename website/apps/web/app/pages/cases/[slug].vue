<script setup lang="ts">
import { INDUSTRY_LABEL, formatDate } from '~/utils/links'
// P-41 案例详情：背景挑战 → 方案 → 时间线 → 所用产品
const route = useRoute()
const { data: c } = await useContentItem('case', String(route.params.slug))
const lightbox = ref<{ src: string; alt?: string } | null>(null)
const images = computed(() => (c.value.data.images || (c.value.data.image ? [c.value.data.image] : [])) as any[])
usePageSeo({ title: `${c.value.title} · 客户案例`, description: c.value.summary, image: c.value.data.image?.src })
</script>

<template>
  <div>
    <PageHero :title="c.title" :eyebrow="c.archived ? '历史案例' : 'Customer Case'" :lead="c.summary"
              :crumbs="[{ name: '客户案例', to: '/cases' }, { name: c.title }]" />
    <section class="section bg-white">
      <div class="container-site grid gap-12 lg:grid-cols-[1fr_320px]">
        <div class="space-y-10">
          <div v-if="c.data.challenge">
            <h2 class="text-2xl">现场问题</h2>
            <p class="mt-4 leading-8 text-ink-600">{{ c.data.challenge }}</p>
          </div>
          <div v-if="c.data.solution">
            <h2 class="text-2xl">方案</h2>
            <p class="mt-4 leading-8 text-ink-600">{{ c.data.solution }}</p>
          </div>
          <div v-if="c.data.timeline?.length">
            <h2 class="text-2xl">进展</h2>
            <ol class="mt-4 border-l-2 border-line-200 pl-6">
              <li v-for="t in c.data.timeline" :key="t.date" class="relative pb-4">
                <span class="absolute top-2 -left-[31px] size-3 rounded-full bg-brand-orange-500" />
                <time class="font-latin text-sm text-ink-500">{{ formatDate(t.date) }}</time>
                <p class="mt-1 leading-7 text-ink-600">{{ t.text }}</p>
              </li>
            </ol>
          </div>
          <div class="grid gap-4 sm:grid-cols-2">
            <button v-for="(im, i) in images" :key="i" type="button" class="card cursor-zoom-in overflow-hidden" :aria-label="`放大查看案例图片 ${i + 1}`"
                    @click="lightbox = { src: im.src, alt: c.title }">
              <img :src="im.src" :alt="`${c.title} 图片 ${i + 1}`" :width="im.w" :height="im.h" loading="lazy" class="w-full">
            </button>
          </div>
        </div>
        <aside class="h-fit space-y-4 lg:sticky lg:top-24">
          <dl class="card divide-y divide-line-200 text-sm">
            <div class="p-4"><dt class="text-ink-500">客户 / 项目</dt><dd class="mt-1 font-medium">{{ c.data.customer }}</dd></div>
            <div class="p-4"><dt class="text-ink-500">行业</dt><dd class="mt-1 font-medium">{{ INDUSTRY_LABEL[c.category || ''] }}</dd></div>
            <div v-if="c.data.scenario" class="p-4"><dt class="text-ink-500">场景</dt><dd class="mt-1 font-medium">{{ c.data.scenario }}</dd></div>
          </dl>
          <UiButton to="/demo" class="w-full">预约类似场景演示</UiButton>
        </aside>
      </div>
    </section>
    <RelatedProducts :slugs="c.data.products || []" title="案例所用产品" />
    <CtaBand />
    <Lightbox v-model="lightbox" />
  </div>
</template>
