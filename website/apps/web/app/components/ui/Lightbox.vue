<script setup lang="ts">
import { DialogClose, DialogContent, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from 'reka-ui'
// 图片灯箱：证书、标准、产品截图（K-01 §4 Lightbox），Esc 关闭、焦点锁定
const model = defineModel<{ src: string; alt?: string } | null>({ default: null })
const open = computed({ get: () => !!model.value, set: (v) => { if (!v) model.value = null } })
</script>

<template>
  <DialogRoot v-model:open="open">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-[80] bg-navy-900/85" />
      <DialogContent class="fixed inset-4 z-[90] flex flex-col items-center justify-center outline-none md:inset-10"
                     :aria-describedby="undefined">
        <DialogTitle class="sr-only">{{ model?.alt || '图片预览' }}</DialogTitle>
        <img v-if="model" :src="model.src" :alt="model.alt || ''" class="max-h-[85vh] w-auto rounded-md bg-white shadow-2">
        <p v-if="model?.alt" class="mt-3 text-center text-sm text-on-dark">{{ model.alt }}</p>
        <DialogClose class="absolute top-0 right-0 inline-flex size-11 items-center justify-center rounded-full bg-white text-ink-900"
                     aria-label="关闭预览">
          <UiIcon name="close" />
        </DialogClose>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
