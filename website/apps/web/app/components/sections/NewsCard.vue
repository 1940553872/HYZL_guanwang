<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
import { formatDate } from '~/utils/links'
defineProps<{ item: ContentItem }>()
const firstImg = (it: ContentItem) => (it.data.blocks || []).find((b: any) => b.t === 'img')
</script>

<template>
  <NuxtLink :to="`/news/${item.slug}`" class="card card-hover group flex h-full flex-col overflow-hidden">
    <div class="aspect-[16/9] overflow-hidden bg-brand-blue-50">
      <img v-if="firstImg(item)" :src="firstImg(item).src" :alt="item.title" loading="lazy" :width="firstImg(item).w" :height="firstImg(item).h"
           class="size-full object-cover">
      <div v-else class="flex size-full items-center justify-center"><img src="/media/brand/logo.webp" alt="" class="h-10 opacity-30"></div>
    </div>
    <div class="flex flex-1 flex-col p-5">
      <p class="flex items-center gap-2 text-xs text-ink-500">
        <time :datetime="item.publishedAt" class="font-latin">{{ formatDate(item.publishedAt) }}</time>
        <span class="tag">{{ item.category === 'industry' ? '行业资讯' : '公司动态' }}</span>
        <span v-if="item.archived" class="tag">历史动态</span>
      </p>
      <h3 class="mt-3 line-clamp-2 text-base leading-7 group-hover:text-brand-blue-700">{{ item.title }}</h3>
      <p class="mt-2 line-clamp-2 text-sm leading-6 text-ink-600">{{ item.summary }}</p>
    </div>
  </NuxtLink>
</template>
