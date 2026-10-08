<script setup lang="ts">
import type { ContentItem } from '~/utils/types'
// 痛点问题卡（Bento）：以“现场问题”引出 SpatiGo™ 四个子产品
defineProps<{ items: ContentItem[] }>()
</script>

<template>
  <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
    <NuxtLink v-for="(p, i) in items" :key="p.slug" :to="`/products/spatigo/${p.slug.replace('spatigo-', '')}`"
              :class="['card card-hover group relative flex flex-col overflow-hidden p-6 md:p-7', i === 0 && 'xl:row-span-1']">
      <span class="inline-flex size-12 items-center justify-center rounded-sm bg-brand-blue-50 text-brand-blue-700">
        <UiIcon :name="p.data.icon || 'layers'" :size="26" />
      </span>
      <p class="mt-6 text-xl leading-8 font-bold md:text-[22px]">{{ p.data.question }}</p>
      <p class="mt-3 flex-1 text-[15px] leading-7 text-ink-600">{{ p.data.tagline }}</p>
      <p class="mt-6 flex items-center justify-between border-t border-line-200 pt-4">
        <span><span class="font-semibold">{{ p.title }}</span> <span class="code ml-1 text-xs text-ink-500">{{ p.data.code }}</span></span>
        <UiIcon name="arrow" :size="18" class="text-brand-blue-700 transition-transform group-hover:translate-x-1" />
      </p>
    </NuxtLink>
  </div>
</template>
