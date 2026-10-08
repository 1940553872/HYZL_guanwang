<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
import { productPath } from '~/utils/links'
// 产品卡：代号（等宽字体）+ 名称 + 一句话
const props = defineProps<{ item: ContentItem; compact?: boolean }>()
const code = computed(() => (props.item.data.code as string) || '')
</script>

<template>
  <NuxtLink :to="productPath(item)" class="card card-hover group flex h-full flex-col p-6">
    <p v-if="code" class="code text-sm text-brand-blue-500">{{ code }}</p>
    <h3 :class="['mt-1', compact ? 'text-base' : 'text-lg']">{{ item.data.name || item.title }}</h3>
    <p v-if="!compact && item.summary" class="mt-3 line-clamp-3 flex-1 text-[15px] leading-7 text-ink-600">{{ item.summary }}</p>
    <span class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-brand-blue-700">
      了解详情<UiIcon name="arrow" :size="16" class="transition-transform group-hover:translate-x-1" />
    </span>
  </NuxtLink>
</template>
