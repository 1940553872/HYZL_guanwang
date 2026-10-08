<script setup lang="ts">
import { INDUSTRY_LABEL } from '~/utils/links'
// P-40 案例列表：按行业筛选，筛选写入 URL；历史案例单独分组
const route = useRoute()
const router = useRouter()
const { data } = await useContentList('case')
const industry = computed(() => String(route.query.industry || ''))
const current = computed(() => data.value.items.filter((c) => !c.archived && (!industry.value || c.category === industry.value)))
const legacy = computed(() => data.value.items.filter((c) => c.archived && !industry.value))
const filters = computed(() => [...new Set(data.value.items.filter((c) => !c.archived).map((c) => c.category || ''))])
function setIndustry(v: string) { router.replace({ query: v ? { industry: v } : {} }) }
usePageSeo({ title: '客户案例', description: '华云智联在石油化工、矿山能源等行业的工业人工智能落地案例。' })
</script>

<template>
  <div>
    <PageHero title="客户案例" eyebrow="Customer Cases" lead="每个案例说明现场问题、方案与所用产品；客户名称与数据均经授权后公开。" :crumbs="[{ name: '客户案例' }]" />
    <section class="section bg-paper">
      <div class="container-site">
        <div role="group" aria-label="按行业筛选" class="mb-8 flex flex-wrap gap-2">
          <button type="button" :aria-pressed="!industry" :class="['h-9 rounded-sm border px-4 text-sm', !industry ? 'border-brand-blue-700 bg-brand-blue-700 text-white' : 'border-line-300 bg-white hover:border-brand-blue-700']"
                  @click="setIndustry('')">全部</button>
          <button v-for="f in filters" :key="f" type="button" :aria-pressed="industry === f"
                  :class="['h-9 rounded-sm border px-4 text-sm', industry === f ? 'border-brand-blue-700 bg-brand-blue-700 text-white' : 'border-line-300 bg-white hover:border-brand-blue-700']"
                  @click="setIndustry(f)">{{ INDUSTRY_LABEL[f] || f }}</button>
        </div>
        <div v-if="current.length" class="grid gap-6 md:grid-cols-2"><CaseCard v-for="c in current" :key="c.slug" :item="c" /></div>
        <EmptyState v-else title="该行业案例整理中" text="可查看其他行业案例，或直接预约现场演示。"><UiButton variant="secondary" @click="setIndustry('')">查看全部案例</UiButton></EmptyState>

        <div v-if="legacy.length" class="mt-20">
          <SectionHeader eyebrow="Archive" title="历史案例" lead="以下为公司早期工业云与智慧园区项目，保留供参考。" />
          <div class="grid gap-6 md:grid-cols-3"><CaseCard v-for="c in legacy" :key="c.slug" :item="c" /></div>
        </div>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
