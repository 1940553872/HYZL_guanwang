<script setup lang="ts">
// P-30 解决方案总览：行业 × 场景矩阵
const { data } = await useContentList('solution')
const scenarios = computed(() => [...new Set(data.value.items.flatMap((s) => s.data.scenarios || []))])
usePageSeo({ title: '解决方案', description: '面向矿山与电力、石油化工、航空航天与装备制造、钢铁冶金、烟草与食药制造、水务与市政六大行业的工业人工智能解决方案。' })
</script>

<template>
  <div>
    <PageHero title="解决方案" eyebrow="Solutions" lead="以行业现场问题为起点，组合空间群弈™ 智能体、工业增强大模型、引擎与工业软件，给出可落地、可验证的方案。"
              :crumbs="[{ name: '解决方案' }]" />
    <section class="section bg-white">
      <div class="container-site grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <NuxtLink v-for="(s, i) in data.items" :key="s.slug" :to="`/solutions/${s.slug}`" class="card card-hover group flex flex-col p-7">
          <span class="stat-num text-sm text-brand-orange-600">0{{ i + 1 }}</span>
          <h2 class="mt-3 text-xl">{{ s.title }}</h2>
          <p class="mt-3 flex-1 text-[15px] leading-7 text-ink-600">{{ s.summary }}</p>
          <p class="mt-5 flex flex-wrap gap-2"><span v-for="sc in s.data.scenarios" :key="sc" class="tag">{{ sc }}</span></p>
        </NuxtLink>
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container-site">
        <SectionHeader eyebrow="Industry × Scenario" title="行业 × 场景矩阵" lead="圆点表示该行业已有对应场景的项目实践或产品方案。" />
        <div class="relative overflow-x-auto rounded-sm border border-line-200 bg-white">
          <table class="w-full min-w-[720px] text-sm">
            <caption class="sr-only">行业与场景对应关系</caption>
            <thead>
              <tr class="border-b border-line-200 bg-paper text-left">
                <th scope="col" class="px-4 py-3 font-semibold">行业</th>
                <th v-for="sc in scenarios" :key="sc" scope="col" class="px-4 py-3 text-center font-semibold">{{ sc }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in data.items" :key="s.slug" class="border-b border-line-200 last:border-0">
                <th scope="row" class="px-4 py-3 text-left font-medium"><NuxtLink :to="`/solutions/${s.slug}`" class="link">{{ s.title }}</NuxtLink></th>
                <td v-for="sc in scenarios" :key="sc" class="px-4 py-3 text-center">
                  <span v-if="(s.data.scenarios || []).includes(sc)" class="inline-block size-2.5 rounded-full bg-brand-orange-500" aria-label="有" />
                  <span v-else class="sr-only">无</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <CtaBand />
  </div>
</template>
