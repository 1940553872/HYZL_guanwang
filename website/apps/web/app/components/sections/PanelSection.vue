<script setup lang="ts">
// 产品面板正文：定位 / 概述 / 核心能力（能力条目网格）/ 参数表
defineProps<{
  panel: { en?: string; positioning?: string; overview?: string[]; sectionTitle?: string; blocks?: any[]; tables?: { title: string; rows: string[][] }[] }
  title?: string
  id?: string
}>()
</script>

<template>
  <div>
    <div class="grid gap-8 lg:grid-cols-[1fr_1.6fr]">
      <div>
        <p v-if="panel.en" class="eyebrow">{{ panel.en }}</p>
        <h2 v-if="title" class="mt-3 text-2xl md:text-[30px] md:leading-[40px]">{{ title }}</h2>
        <p v-if="panel.positioning" class="mt-4 border-l-2 border-brand-orange-500 pl-4 text-lg leading-8 font-medium text-ink-900">{{ panel.positioning }}</p>
      </div>
      <div class="space-y-4">
        <p v-for="(o, i) in panel.overview" :key="i" class="text-[15px] leading-8 text-ink-600 md:text-base">{{ o }}</p>
      </div>
    </div>
    <div v-if="panel.blocks?.length" class="mt-12">
      <h3 class="mb-6 text-xl">{{ panel.sectionTitle || '核心能力' }}</h3>
      <ContentBlocks :blocks="panel.blocks" />
    </div>
    <div v-for="t in panel.tables || []" :key="t.title" class="mt-10">
      <h3 class="mb-4 text-xl">{{ t.title }}</h3>
      <div class="relative overflow-x-auto rounded-sm border border-line-200 bg-white">
        <table class="w-full min-w-[480px] text-left text-sm">
          <tbody>
            <tr v-for="(r, i) in t.rows" :key="i" class="border-b border-line-200 last:border-0">
              <td v-for="(c, j) in r" :key="j" :class="['px-4 py-3', j === 0 ? 'font-medium whitespace-nowrap text-ink-900' : 'text-ink-600']">{{ c }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
