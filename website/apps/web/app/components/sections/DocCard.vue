<script setup lang="ts">
import type { Media } from '~/utils/types'
// 证书 / 专利 / 软著 / 奖项缩略卡（竖版文档比例 3:4），点击放大
defineProps<{ title: string; image?: Media; meta?: string; badge?: string; badgeTone?: 'ok' | 'warn' | 'muted' }>()
const emit = defineEmits<{ open: [Media & { alt: string }] }>()
</script>

<template>
  <figure class="card flex h-full flex-col overflow-hidden">
    <button v-if="image" type="button" class="block aspect-[3/4] cursor-zoom-in overflow-hidden bg-paper" :aria-label="`放大查看：${title}`"
            @click="emit('open', { ...image, alt: title })">
      <img :src="image.thumb || image.src" :alt="title" loading="lazy" class="size-full object-contain p-2">
    </button>
    <div v-else class="flex aspect-[3/4] items-center justify-center bg-paper text-line-300"><UiIcon name="doc" :size="40" /></div>
    <figcaption class="flex flex-1 flex-col gap-1 border-t border-line-200 p-4">
      <span v-if="badge" :class="['self-start rounded-xs px-2 py-0.5 text-xs font-medium',
        badgeTone === 'warn' ? 'bg-[#FFF4E0] text-warning' : badgeTone === 'muted' ? 'bg-paper text-ink-500' : 'bg-[#E6F4EC] text-success']">{{ badge }}</span>
      <span class="text-sm leading-6 font-medium">{{ title }}</span>
      <span v-if="meta" class="code text-xs text-ink-500">{{ meta }}</span>
    </figcaption>
  </figure>
</template>
