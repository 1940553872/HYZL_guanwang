<script setup lang="ts">
import { DialogClose, DialogContent, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from 'reka-ui'
// 搜索浮层：支持按产品代号（iMES、SpatiGo）与关键词搜索，回车进入 P-90
const open = defineModel<boolean>('open', { default: false })
const q = ref('')
const hot = ['SpatiGo', 'iMES', '预测性维护', '数字孪生', '标准', '具身智能']
function go(term = q.value) {
  const t = term.trim()
  if (!t) return
  open.value = false
  navigateTo({ path: '/search', query: { q: t } })
}
</script>

<template>
  <DialogRoot v-model:open="open">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-[60] bg-navy-900/70" />
      <DialogContent class="fixed inset-x-4 top-20 z-[70] mx-auto max-w-2xl rounded-md bg-white p-6 text-ink-900 shadow-2 outline-none md:top-28"
                     :aria-describedby="undefined">
        <DialogTitle class="text-lg font-semibold">站内搜索</DialogTitle>
        <form role="search" class="mt-4 flex gap-2" @submit.prevent="go()">
          <label for="site-search" class="sr-only">搜索关键词</label>
          <input id="site-search" v-model="q" type="search" maxlength="50" autocomplete="off" placeholder="输入产品代号或关键词，如 iMES、预测性维护"
                 class="h-12 flex-1 rounded-sm border border-line-300 px-4 text-base outline-none focus:border-brand-blue-700">
          <UiButton type="submit" size="lg">搜索</UiButton>
        </form>
        <div class="mt-5 flex flex-wrap items-center gap-2 text-sm">
          <span class="text-ink-500">热门：</span>
          <button v-for="h in hot" :key="h" type="button" class="tag hover:border-brand-blue-700 hover:text-brand-blue-700" @click="go(h)">{{ h }}</button>
        </div>
        <DialogClose class="absolute top-4 right-4 inline-flex size-10 items-center justify-center" aria-label="关闭搜索"><UiIcon name="close" /></DialogClose>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
