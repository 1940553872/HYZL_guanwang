<script setup lang="ts">
import { DialogClose, DialogContent, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from 'reka-ui'
import { NAV } from '~/utils/nav'
// 移动端抽屉导航：一级项可展开二级（K-02 §2.2，移动端）
const open = defineModel<boolean>('open', { default: false })
const { public: pub } = useRuntimeConfig()
const expanded = ref<number | null>(null)
</script>

<template>
  <DialogRoot v-model:open="open">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-[60] bg-navy-900/60 lg:hidden" />
      <DialogContent class="fixed inset-y-0 right-0 z-[70] flex w-full max-w-sm flex-col bg-white text-ink-900 shadow-2 outline-none lg:hidden"
                     :aria-describedby="undefined">
        <div class="flex h-[60px] items-center justify-between border-b border-line-200 px-4">
          <DialogTitle class="text-base font-semibold">网站导航</DialogTitle>
          <DialogClose class="inline-flex size-10 items-center justify-center" aria-label="关闭菜单"><UiIcon name="close" /></DialogClose>
        </div>
        <nav aria-label="移动端导航" class="flex-1 overflow-y-auto px-4 py-2">
          <ul>
            <li v-for="(item, i) in NAV" :key="item.to" class="border-b border-line-200">
              <NuxtLink v-if="!item.columns" :to="item.to" class="flex h-14 items-center text-base font-medium">{{ item.label }}</NuxtLink>
              <template v-else>
                <button type="button" class="flex h-14 w-full items-center justify-between text-base font-medium"
                        :aria-expanded="expanded === i" @click="expanded = expanded === i ? null : i">
                  {{ item.label }}<UiIcon name="chevron" :size="18" :class="['transition-transform', expanded === i && 'rotate-180']" />
                </button>
                <div v-show="expanded === i" class="pb-4">
                  <div v-for="col in item.columns" :key="col.title" class="mt-2">
                    <p class="px-2 text-xs font-semibold text-ink-500">{{ col.title }}</p>
                    <NuxtLink v-for="l in col.links" :key="l.to + l.label" :to="l.to" class="block rounded-sm px-2 py-2 text-[15px] text-ink-600 hover:bg-paper">
                      {{ l.label }}
                    </NuxtLink>
                  </div>
                </div>
              </template>
            </li>
          </ul>
        </nav>
        <div class="space-y-3 border-t border-line-200 p-4">
          <UiButton to="/demo" class="w-full">预约现场演示</UiButton>
          <a :href="`tel:${pub.hotline}`" class="flex items-center justify-center gap-2 text-sm text-ink-600">
            <UiIcon name="phone" :size="16" />7×24 热线 <span class="font-latin font-semibold text-ink-900">{{ pub.hotline }}</span>
          </a>
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
