<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
import { INDUSTRY_LABEL } from '~/utils/links'
// 案例卡：行业 / 场景标签 + 标题 + 摘要；历史案例加“历史案例”标签（K-02 §2.1）
defineProps<{ item: ContentItem; dark?: boolean }>()
</script>

<template>
  <NuxtLink :to="`/cases/${item.slug}`"
            :class="['group flex h-full flex-col overflow-hidden rounded-sm border transition-colors', dark ? 'border-white/15 bg-navy-800 hover:border-brand-orange-500' : 'card card-hover']">
    <div v-if="item.data.image" class="aspect-[16/9] overflow-hidden bg-paper">
      <img :src="item.data.image.src" :alt="item.title" :width="item.data.image.w" :height="item.data.image.h" loading="lazy"
           class="size-full object-cover transition-transform duration-300 group-hover:scale-[1.03]">
    </div>
    <div class="flex flex-1 flex-col p-6">
      <p class="flex flex-wrap gap-2 text-xs">
        <span :class="dark ? 'rounded-xs bg-white/10 px-2 py-0.5 text-on-dark' : 'tag'">{{ INDUSTRY_LABEL[item.category || ''] || item.category }}</span>
        <span v-if="item.data.scenario" :class="dark ? 'rounded-xs bg-white/10 px-2 py-0.5 text-on-dark' : 'tag'">{{ item.data.scenario }}</span>
      </p>
      <h3 :class="['mt-3 text-lg leading-7', dark && 'text-white']">{{ item.title }}</h3>
      <p :class="['mt-2 line-clamp-3 flex-1 text-[15px] leading-7', dark ? 'text-on-dark-muted' : 'text-ink-600']">{{ item.summary }}</p>
      <span :class="['mt-4 inline-flex items-center gap-1 text-sm font-semibold', dark ? 'text-brand-orange-500' : 'text-brand-blue-700']">
        查看案例<UiIcon name="arrow" :size="16" />
      </span>
    </div>
  </NuxtLink>
</template>
